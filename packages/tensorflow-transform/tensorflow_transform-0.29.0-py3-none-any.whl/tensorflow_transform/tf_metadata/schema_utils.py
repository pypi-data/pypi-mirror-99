# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utilities for using the tf.Metadata Schema within TensorFlow."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Dict, Mapping, Optional

# GOOGLE-INITIALIZATION

import tensorflow as tf

from tensorflow_transform import common_types
from tensorflow_transform.tf_metadata import schema_utils_legacy
# TODO(https://issues.apache.org/jira/browse/SPARK-22674): Switch to
# `collections.namedtuple` or `typing.NamedTuple` once the Spark issue is
# resolved.
from tfx_bsl.types import tfx_namedtuple

from tensorflow_metadata.proto.v0 import schema_pb2


def schema_from_feature_spec(
    feature_spec: Mapping[str, common_types.FeatureSpecType],
    domains: Optional[Mapping[str, common_types.DomainType]] = None
) -> schema_pb2.Schema:
  """Convert a feature spec to a Schema proto.

  Args:
    feature_spec: A TensorFlow feature spec
    domains: (optional) a dict whose keys are feature names and values are one
        of schema_pb2.IntDomain, schema_pb2.StringDomain or
        schema_pb2.FloatDomain.

  Returns:
    A Schema proto

  Raises:
    ValueError: If the feature spec cannot be converted to a Schema proto.
  """
  if domains is None:
    domains = {}

  result = schema_pb2.Schema()

  # Some feature specs can only be represented with the legacy schema, in
  # particular feature specs where any FixedLenFeature has default_value set.
  # We represent these (and only these) using a schema with
  # generate_legacy_feature_spec=True.  Note the generate_legacy_feature_spec
  # field is not part of the open source codebase.
  if schema_utils_legacy.should_set_generate_legacy_feature_spec(feature_spec):
    return _legacy_schema_from_feature_spec(feature_spec, domains)

  schema_utils_legacy.set_generate_legacy_feature_spec(result, False)

  # Add the features to the schema.
  for name, spec in sorted(feature_spec.items()):
    if isinstance(spec, tf.io.SparseFeature):
      (index_feature, value_feature, sparse_feature) = (
          _sparse_feature_from_feature_spec(spec, name, domains))
      for f in index_feature:
        result.feature.add().CopyFrom(f)
      result.feature.add().CopyFrom(value_feature)
      result.sparse_feature.add().CopyFrom(sparse_feature)
    else:
      result.feature.add().CopyFrom(
          _feature_from_feature_spec(spec, name, domains))
  return result


def _sparse_feature_from_feature_spec(spec, name, domains):
  """Returns a representation of a SparseFeature from a feature spec."""
  if isinstance(spec.index_key, list):
    assert isinstance(spec.size, (list, tuple, tf.TensorShape)), type(spec.size)
    assert len(spec.index_key) == len(spec.size), (spec.index_key, spec.size)
    spec_size = [
        s.value if isinstance(s, tf.compat.v1.Dimension) else s
        for s in spec.size
    ]
    int_domains = [
        schema_pb2.IntDomain(min=0, max=size - 1) if size is not None else None
        for size in spec_size
    ]
    index_feature = [
        schema_pb2.Feature(
            name=key, type=schema_pb2.INT, int_domain=int_domain)
        for (key, int_domain) in zip(spec.index_key, int_domains)
    ]
    index_feature_ref = [
        schema_pb2.SparseFeature.IndexFeature(name=key)
        for key in spec.index_key
    ]
  else:
    # Create a index feature.
    index_feature = [
        schema_pb2.Feature(
            name=spec.index_key,
            type=schema_pb2.INT,
            int_domain=schema_pb2.IntDomain(min=0, max=spec.size - 1))
    ]
    index_feature_ref = [
        schema_pb2.SparseFeature.IndexFeature(name=spec.index_key)
    ]

  # Create a value feature.
  value_feature = schema_pb2.Feature(name=spec.value_key)
  _set_type(name, value_feature, spec.dtype)
  _set_domain(name, value_feature, domains.get(name))

  # Create a sparse feature which refers to the index and value features.
  value_feature_ref = schema_pb2.SparseFeature.ValueFeature(
      name=spec.value_key)
  sparse_feature = schema_pb2.SparseFeature(
      name=name,
      is_sorted=True if spec.already_sorted else None,
      index_feature=index_feature_ref,
      value_feature=value_feature_ref)

  return (index_feature, value_feature, sparse_feature)


def _feature_from_feature_spec(spec, name, domains):
  """Returns a representation of a Feature from a feature spec."""
  if isinstance(spec, tf.io.FixedLenFeature):
    if spec.default_value is not None:
      raise ValueError(
          'feature "{}" had default_value {}, but FixedLenFeature must have '
          'default_value=None'.format(name, spec.default_value))
    dims = [schema_pb2.FixedShape.Dim(size=size) for size in spec.shape]
    feature = schema_pb2.Feature(
        name=name,
        presence=schema_pb2.FeaturePresence(min_fraction=1.0),
        shape=schema_pb2.FixedShape(dim=dims))
  elif isinstance(spec, tf.io.VarLenFeature):
    feature = schema_pb2.Feature(name=name)
  else:
    raise TypeError(
        'Spec for feature "{}" was {} of type {}, expected a '
        'FixedLenFeature, VarLenFeature or SparseFeature'.format(
            name, spec, type(spec)))

  _set_type(name, feature, spec.dtype)
  _set_domain(name, feature, domains.get(name))
  return feature


def _set_type(name, feature, dtype):
  """Set the type of a Feature proto."""
  if dtype == tf.int64:
    feature.type = schema_pb2.INT
  elif dtype == tf.float32:
    feature.type = schema_pb2.FLOAT
  elif dtype == tf.string:
    feature.type = schema_pb2.BYTES
  else:
    raise ValueError(
        'Feature "{}" has invalid dtype {}'.format(name, dtype))


def _set_domain(name, feature, domain):
  """Set the domain of a Feature proto."""
  if domain is None:
    return

  if isinstance(domain, schema_pb2.IntDomain):
    feature.int_domain.CopyFrom(domain)
  elif isinstance(domain, schema_pb2.StringDomain):
    feature.string_domain.CopyFrom(domain)
  elif isinstance(domain, schema_pb2.FloatDomain):
    feature.float_domain.CopyFrom(domain)
  else:
    raise ValueError(
        'Feature "{}" has invalid domain {}'.format(name, domain))


SchemaAsFeatureSpecResult = tfx_namedtuple.TypedNamedTuple(
    'SchemaAsFeatureSpecResult',
    [('feature_spec', Dict[str, common_types.FeatureSpecType]),
     ('domains', Dict[str, common_types.DomainType])])


# A tag used to indicate that a feature was inferred from a RaggedTensor.  A
# Schema containing such a feature cannot be conerted to a feature spec,
# because there is no feature spec for a RaggedTensor.
RAGGED_TENSOR_TAG = 'ragged_tensor'


def schema_as_feature_spec(
    schema_proto: schema_pb2.Schema) -> SchemaAsFeatureSpecResult:
  """Generates a feature spec from a Schema proto.

  For a Feature with a FixedShape we generate a FixedLenFeature with no default.
  For a Feature without a FixedShape we generate a VarLenFeature.  For a
  SparseFeature we generate a SparseFeature.

  Args:
    schema_proto: A Schema proto.

  Returns:
    A pair (feature spec, domains) where feature spec is a dict whose keys are
        feature names and values are instances of FixedLenFeature, VarLenFeature
        or SparseFeature, and `domains` is a dict whose keys are feature names
        and values are one of the `domain_info` oneof, e.g. IntDomain.

  Raises:
    ValueError: If the schema proto is invalid.
  """
  for feature in schema_proto.feature:
    if RAGGED_TENSOR_TAG in feature.annotation.tag:
      raise ValueError(
          'Feature "{}" had tag "{}".  Features represented by a '
          'RaggedTensor cannot be serialized/deserialized to Example proto or '
          'other formats, and cannot have a feature spec generated for '
          'them.'.format(feature.name, RAGGED_TENSOR_TAG))

  if schema_utils_legacy.get_generate_legacy_feature_spec(schema_proto):
    return _legacy_schema_as_feature_spec(schema_proto)
  feature_spec = {}
  # Will hold the domain_info (IntDomain, FloatDomain etc.) of the feature.  For
  # sparse features, will hold the domain_info of the values feature.  Features
  # that do not have a domain set will not be present in `domains`.
  domains = {}
  feature_by_name = {feature.name: feature for feature in schema_proto.feature}
  string_domains = _get_string_domains(schema_proto)

  # Generate a `tf.SparseFeature` for each element of
  # `schema_proto.sparse_feature`.  This also removed the features from
  # feature_by_name.
  # TODO(KesterTong): Allow sparse features to share index features.
  for feature in schema_proto.sparse_feature:
    if _include_in_parsing_spec(feature):
      feature_spec[feature.name], domains[feature.name] = (
          _sparse_feature_as_feature_spec(
              feature, feature_by_name, string_domains))

  # Generate a `tf.FixedLenFeature` or `tf.VarLenFeature` for each element of
  # `schema_proto.feature` that was not referenced by a `SparseFeature`.
  for name, feature in feature_by_name.items():
    if _include_in_parsing_spec(feature):
      feature_spec[name], domains[name] = _feature_as_feature_spec(
          feature, string_domains)

  schema_utils_legacy.check_for_unsupported_features(schema_proto)

  domains = {name: domain for name, domain in domains.items()
             if domain is not None}
  return SchemaAsFeatureSpecResult(feature_spec, domains)


def _get_string_domains(schema):
  return {domain.name: domain for domain in schema.string_domain}


def _get_domain(feature, string_domains):
  """Get the domain of a feature, possibly looking up a schema-level domain."""
  domain_info = feature.WhichOneof('domain_info')
  if domain_info is None:
    return None
  if domain_info == 'domain':
    try:
      return string_domains[feature.domain]
    except KeyError:
      tf.compat.v1.logging.warn(
          'Feature "%s" referred to string domain "%s" which did not exist',
          feature.name, feature.domain)
      return None
  return getattr(feature, domain_info)


def _sparse_feature_as_feature_spec(feature, feature_by_name, string_domains):
  """Returns a representation of a SparseFeature as a feature spec."""
  index_keys = [index_feature.name for index_feature in feature.index_feature]
  index_features = []
  for index_key in index_keys:
    try:
      index_features.append(feature_by_name.pop(index_key))
    except KeyError:
      raise ValueError(
          'sparse_feature "{}" referred to index feature "{}" which did not '
          'exist in the schema'.format(feature.name, index_key))

  value_key = feature.value_feature.name
  try:
    value_feature = feature_by_name.pop(value_key)
  except KeyError:
    raise ValueError(
        'sparse_feature "{}" referred to value feature "{}" which did not '
        'exist in the schema or was referred to as an index or value multiple '
        'times.'.format(feature.name, value_key))

  shape = []
  for index_feature, index_key in zip(index_features, index_keys):
    if index_feature.HasField('int_domain'):
      # Currently we only handle O-based INT index features whose minimum
      # domain value must be zero.
      if not index_feature.int_domain.HasField('min'):
        raise ValueError('Cannot determine dense shape of sparse feature '
                         '"{}". The minimum domain value of index feature "{}"'
                         ' is not set.'.format(feature.name, index_key))
      if index_feature.int_domain.min != 0:
        raise ValueError('Only 0-based index features are supported. Sparse '
                         'feature "{}" has index feature "{}" whose minimum '
                         'domain value is {}.'.format(
                             feature.name, index_key,
                             index_feature.int_domain.min))

      if not index_feature.int_domain.HasField('max'):
        raise ValueError('Cannot determine dense shape of sparse feature '
                         '"{}". The maximum domain value of index feature "{}"'
                         ' is not set.'.format(feature.name, index_key))
      shape.append(index_feature.int_domain.max + 1)
    elif len(index_keys) == 1:
      raise ValueError('Cannot determine dense shape of sparse feature "{}".'
                       ' The index feature "{}" had no int_domain set.'.format(
                           feature.name, index_key))
    else:
      shape.append(-1)

  dtype = _feature_dtype(value_feature)
  if len(index_keys) != len(shape):
    raise ValueError(
        'sparse_feature "{}" had rank {} (shape {}) but {} index keys were'
        ' given'.format(feature.name, len(shape), shape, len(index_keys)))
  spec = tf.io.SparseFeature(index_keys, value_key, dtype, shape,
                             feature.is_sorted)
  domain = _get_domain(value_feature, string_domains)
  return spec, domain


def _feature_as_feature_spec(feature, string_domains):
  """Returns a representation of a Feature as a feature spec."""
  dtype = _feature_dtype(feature)
  if feature.HasField('shape'):
    if feature.presence.min_fraction != 1:
      raise ValueError(
          'Feature "{}" had shape {} set but min_fraction {} != 1.  Use'
          ' value_count not shape field when min_fraction != 1.'.format(
              feature.name, feature.shape, feature.presence.min_fraction))
    spec = tf.io.FixedLenFeature(
        _fixed_shape_as_tf_shape(feature.shape), dtype, default_value=None)
  else:
    spec = tf.io.VarLenFeature(dtype)
  domain = _get_domain(feature, string_domains)
  return spec, domain


def _feature_dtype(feature):
  """Returns a representation of a Feature's type as a tensorflow dtype."""
  if feature.type == schema_pb2.BYTES:
    return tf.string
  elif feature.type == schema_pb2.INT:
    return tf.int64
  elif feature.type == schema_pb2.FLOAT:
    return tf.float32
  else:
    raise ValueError('Feature "{}" had invalid type {}'.format(
        feature.name, schema_pb2.FeatureType.Name(feature.type)))


def _fixed_shape_as_tf_shape(fixed_shape):
  """Returns a representation of a FixedShape as a tensorflow shape."""
  # TODO(b/120869660): Remove the cast to int.  Casting to int is currently
  # needed as some TF code explicitly checks for `int` and does not allow `long`
  # in tensor shapes.
  return [int(dim.size) for dim in fixed_shape.dim]


_DEPRECATED_LIFECYCLE_STAGES = [
    schema_pb2.DEPRECATED, schema_pb2.DISABLED, schema_pb2.PLANNED,
    schema_pb2.ALPHA, schema_pb2.DEBUG_ONLY
]


def _include_in_parsing_spec(feature):
  return not (
      schema_utils_legacy.get_deprecated(feature) or
      feature.lifecycle_stage in _DEPRECATED_LIFECYCLE_STAGES)


def _legacy_schema_from_feature_spec(feature_spec, domains=None):
  """Infer a Schema from a feature spec, using the legacy feature spec logic.

  Infers a Schema proto that with generate_legacy_feature_spec set to true,
  which will result in the given feature spec and domains when
  schema_as_feature_spec is called.  This is used to represent feature specs
  that can only be represented when generate_legacy_feature_spec is true.  In
  particular, feature specs with a default value set.

  Args:
    feature_spec: A TensorFlow feature spec
    domains: A dict from key names to `IntDomain`s

  Returns:
    A Schema proto.

  Raises:
    ValueError: If a default value is invalid.
    TypeError: If an unknown type of feature spec is encountered.
  """
  result = schema_pb2.Schema()
  result.generate_legacy_feature_spec = True
  for name, spec in sorted(feature_spec.items()):
    if isinstance(spec, tf.io.FixedLenFeature):
      # Validate shape first as shape governs which default values are valid.
      if len(spec.shape) == 0:  # pylint: disable=g-explicit-length-test
        size = 1
        expected_default_value = '' if spec.dtype == tf.string else -1
      elif len(spec.shape) == 1 and spec.shape[0] > 1:
        size = spec.shape[0]
        expected_default_value = ['' if spec.dtype == tf.string else -1] * size
      else:
        raise ValueError(
            'When inferring legacy schema from feature spec, feature "{}" had '
            'shape {}, but FixedLenFeature must have shape [] or [k] where '
            'k > 1.'.format(name, spec.shape))

      if spec.default_value is None:
        min_fraction = 1
      elif spec.default_value == expected_default_value:
        min_fraction = 0
      else:
        raise ValueError(
            'When inferring legacy schema from feature spec, feature "{}" had '
            'default_value {}, but FixedLenFeature must have '
            'default_value=None or {}'.format(
                name, spec.default_value, expected_default_value))

      feature = result.feature.add(
          name=name,
          presence=schema_pb2.FeaturePresence(min_fraction=min_fraction),
          value_count=schema_pb2.ValueCount(min=size, max=size))
    elif isinstance(spec, tf.io.VarLenFeature):
      feature = result.feature.add(name=name)
    else:
      raise TypeError(
          'When inferring legacy schema from feature spec, spec for feature '
          '"{}" was {} of type {}, expected a FixedLenFeature or '
          'VarLenFeature '.format(name, spec, type(spec)))

    _set_type(name, feature, spec.dtype)
    _set_domain(name, feature, domains.get(name))

  return result


def _legacy_schema_as_feature_spec(schema_proto):
  """Generate a feature spec and domains using legacy feature spec."""
  feature_spec = {}
  # Will hold the domain_info (IntDomain, FloatDomain etc.) of the feature.  For
  # sparse features, will hold the domain_info of the values feature.  Features
  # that do not have a domain set will not be present in `domains`.
  domains = {}
  feature_by_name = {feature.name: feature for feature in schema_proto.feature}
  string_domains = _get_string_domains(schema_proto)

  for name, feature in feature_by_name.items():
    if _include_in_parsing_spec(feature):
      feature_spec[name] = _legacy_feature_as_feature_spec(feature)
      domain = _get_domain(feature, string_domains)
      if domain is not None:
        domains[name] = domain

  return SchemaAsFeatureSpecResult(feature_spec, domains)


def _legacy_feature_as_feature_spec(feature):
  """Translate a Feature proto into a TensorFlow feature spec.

  This function applies heuristics to deduce the shape and other information
  from a FeatureProto.  The FeatureProto contains information about the feature
  in an ExampleProto, but the feature spec proto also requires enough
  information to parse the feature into a tensor.  We apply the following rules:

    1. The dtype is determined from the feature's type according to the mapping
       BYTES -> string, INT -> int64, FLOAT -> float32.  TYPE_UNKNOWN or any
       other type results in a ValueError.

    2. The shape and representation of the column are determined by the
       following rules:
         * if the value_count.min and value_count.max are both 1 then the shape
           is scalar and the representation is fixed length.
         * If value_count.min and value_count.max are equal but greater than 1,
           then the shape is a vector whose length is value_count.max and the
           representation is fixed length.
         * If value_count.min and value_count.max are equal and are less than 1,
           then the shape is a vector of unknown length and the representation
           is variable length.
         * If value_count.min and value_count.max are not equal then
           the shape is a vector of unknown length and the representation is
           variable length.

    3. If the feature is always present or is variable length (based on the
        above rule), no default value is set but if the feature is not always
        present and is fixed length, then a canonical default value is chosen
        based on _DEFAULT_VALUE_FOR_DTYPE.

    4. Features that are deprecated are completely ignored and removed.

  Args:
    feature: A FeatureProto

  Returns:
    A `tf.FixedLenFeature` or `tf.VarLenFeature`.

  Raises:
    ValueError: If the feature's type is not supported or the schema is invalid.
  """
  # Infer canonical tensorflow dtype.
  dtype = _feature_dtype(feature)

  if feature.value_count.min < 0:
    raise ValueError(
        'Feature "{}" has value_count.min < 0 (value was {}).'.format(
            feature.name, feature.value_count.min))

  if feature.value_count.max < 0:
    raise ValueError(
        'Feature "{}" has value_count.max < 0 (value was {}).'.format(
            feature.name, feature.value_count.max))

  # Use heuristics to infer the shape and representation.
  if (feature.value_count.min == feature.value_count.max
      and feature.value_count.min == 1):
    # Case 1: value_count.min == value_count.max == 1.  Infer a FixedLenFeature
    # with rank 0 and a default value.
    tf.compat.v1.logging.info(
        'Features %s has value_count.min == value_count.max == 1.  Setting to '
        'fixed length scalar.', feature.name)
    default_value = _legacy_infer_default_value(feature, dtype)
    return tf.io.FixedLenFeature([], dtype, default_value)

  elif (feature.value_count.min == feature.value_count.max
        and feature.value_count.min > 1):
    # Case 2: value_count.min == value_count.max > 1.  Infer a FixedLenFeature
    # with rank 1 and a default value.
    tf.compat.v1.logging.info(
        'Feature %s has value_count.min == value_count.max > 1.  Setting to '
        'fixed length vector.', feature.name)
    default_value = _legacy_infer_default_value(feature, dtype)
    return tf.io.FixedLenFeature([feature.value_count.min], dtype,
                                 default_value)

  else:
    # Case 3: Either value_count.min != value_count.max or
    # value_count.min == value_count.max == 0.  Infer a VarLenFeature.
    tf.compat.v1.logging.info(
        'Feature %s has value_count.min != value_count.max or '
        ' value_count.min == value_count.max == 0.  Setting to variable length '
        ' vector.', feature.name)
    return tf.io.VarLenFeature(dtype)


# For numeric values, set defaults that are less likely to occur in the actual
# data so that users can test for missing values.
_LEGACY_DEFAULT_VALUE_FOR_DTYPE = {tf.string: '', tf.int64: -1, tf.float32: -1}


def _legacy_infer_default_value(feature_proto, dtype):
  """Returns a canonical default value if min_fraction < 1 or else None."""
  if feature_proto.presence.min_fraction < 1:
    default_value = _LEGACY_DEFAULT_VALUE_FOR_DTYPE[dtype]
    tf.compat.v1.logging.info(
        'Feature %s has min_fraction (%f) != 1.  Setting default value %r',
        feature_proto.name, feature_proto.presence.min_fraction, default_value)
    if feature_proto.value_count.min == 1:
      # neglecting vector of size 1 because that never happens.
      return default_value
    else:
      return [default_value] * feature_proto.value_count.min
  else:
    tf.compat.v1.logging.info(
        'Feature %s has min_fraction = 1 (%s). Setting default value to None.',
        feature_proto.name, feature_proto.presence)
    return None

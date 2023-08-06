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
"""Test cases associated with schema_utils_legacy."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# GOOGLE-INITIALIZATION

import tensorflow as tf

from tensorflow_metadata.proto.v0 import schema_pb2

EQUIVALENT_FEATURE_SPEC_AND_SCHEMAS = [
    # Test different dtypes
    {
        'testcase_name': 'int',
        'ascii_proto': '''feature: {name: "x" type: INT}''',
        'feature_spec': {
            'x': tf.io.VarLenFeature(tf.int64)
        }
    },
    {
        'testcase_name': 'string',
        'ascii_proto': '''feature: {name: "x" type: BYTES}''',
        'feature_spec': {
            'x': tf.io.VarLenFeature(tf.string)
        }
    },
    {
        'testcase_name': 'float',
        'ascii_proto': '''feature: {name: "x" type: FLOAT}''',
        'feature_spec': {
            'x': tf.io.VarLenFeature(tf.float32)
        }
    },
    # Test different shapes
    {
        'testcase_name':
            'fixed_len_vector',
        'ascii_proto':
            """
          feature: {
            name: "x" type: INT shape: {dim {size: 1}}
            presence: {min_fraction: 1}
          }
        """,
        'feature_spec': {
            'x': tf.io.FixedLenFeature([1], tf.int64, None)
        }
    },
    {
        'testcase_name':
            'fixed_len_matrix',
        'ascii_proto':
            """
          feature: {
            name: "x" type: INT shape: {dim {size: 2} dim {size: 2}}
            presence: {min_fraction: 1}
          }
        """,
        'feature_spec': {
            'x': tf.io.FixedLenFeature([2, 2], tf.int64, None)
        }
    },
    {
        'testcase_name': 'var_len',
        'ascii_proto': '''feature: {name: "x" type: INT}''',
        'feature_spec': {
            'x': tf.io.VarLenFeature(tf.int64)
        }
    },
    {
        'testcase_name':
            'sparse',
        'ascii_proto':
            """
          feature {
            name: "index_key"
            type: INT
            int_domain { min: 0 max: 9 }
          }
          feature {
            name: "value_key"
            type: INT
          }
          sparse_feature {
            name: "x"
            index_feature {name: "index_key"}
            value_feature {name: "value_key"}
          }
        """,
        'feature_spec': {
            'x':
                tf.io.SparseFeature(['index_key'],
                                    'value_key',
                                    tf.int64, [10],
                                    already_sorted=False)
        }
    },
    {
        'testcase_name':
            'sparse_sorted',
        'ascii_proto':
            """
          feature {
            name: "index_key"
            type: INT
            int_domain { min: 0 max: 9 }
          }
          feature {
            name: "value_key"
            type: INT
          }
          sparse_feature {
            name: "x"
            is_sorted: true
            index_feature {name: "index_key"}
            value_feature {name: "value_key"}
          }
        """,
        'feature_spec': {
            'x':
                tf.io.SparseFeature(['index_key'],
                                    'value_key',
                                    tf.int64, [10],
                                    already_sorted=True)
        }
    },
    # Test domains
    {
        'testcase_name':
            'int_domain',
        'ascii_proto':
            """
          feature: {
            name: "x" type: INT
            int_domain {min: 0 max: 5 is_categorical: true}
          }
        """,
        'feature_spec': {
            'x': tf.io.VarLenFeature(tf.int64)
        },
        'domains': {
            'x': schema_pb2.IntDomain(min=0, max=5, is_categorical=True)
        }
    },
    {
        'testcase_name':
            'string_domain',
        'ascii_proto':
            """
          feature: {
            name: "x" type: BYTES
            string_domain {value: "a" value: "b"}
          }
        """,
        'feature_spec': {
            'x': tf.io.VarLenFeature(tf.string)
        },
        'domains': {
            'x': schema_pb2.StringDomain(value=['a', 'b'])
        }
    },
    {
        'testcase_name':
            'float_domain',
        'ascii_proto':
            """
          feature: {
            name: "x" type: FLOAT
            float_domain {min: 0.0 max: 0.5}
          }
        """,
        'feature_spec': {
            'x': tf.io.VarLenFeature(tf.float32)
        },
        'domains': {
            'x': schema_pb2.FloatDomain(min=0.0, max=0.5)
        }
    },
    {
        'testcase_name':
            'sparse_feature_rank_0',
        'ascii_proto':
            """
          feature {
            name: "value_key"
            type: INT
          }
          sparse_feature {
            name: "x"
            value_feature {name: "value_key"}
          }
        """,
        'feature_spec': {
            'x': tf.io.SparseFeature([], 'value_key', tf.int64, [])
        }
    },
    {
        'testcase_name':
            'sparse_feature_rank_2',
        'ascii_proto':
            """
          feature {
            name: "index_key_1"
            type: INT
            int_domain { min: 0 max: 0 }
          }
          feature {
            name: "index_key_2"
            type: INT
            int_domain { min: 0 max: 0 }
          }
          feature {
            name: "value_key"
            type: INT
          }
          sparse_feature {
            name: "x"
            index_feature {name: "index_key_1"}
            index_feature {name: "index_key_2"}
            value_feature {name: "value_key"}
          }
        """,
        'feature_spec': {
            'x':
                tf.io.SparseFeature(['index_key_1', 'index_key_2'], 'value_key',
                                    tf.int64, [1, 1])
        }
    },
]

NON_ROUNDTRIP_SCHEMAS = [
    {
        'testcase_name':
            'deprecated_feature',
        'ascii_proto':
            """
          feature: {name: "x" type: INT lifecycle_stage: DEPRECATED}
        """,
        'feature_spec': {}
    },
    {
        'testcase_name':
            'schema_level_string_domain',
        'ascii_proto':
            """
          feature: {name: "x" type: BYTES domain: "my_domain"}
          string_domain {name: "my_domain" value: "a" value: "b"}
        """,
        'feature_spec': {
            'x': tf.io.VarLenFeature(tf.string)
        },
        'domains': {
            'x': schema_pb2.StringDomain(name='my_domain', value=['a', 'b'])
        }
    },
    {
        'testcase_name':
            'missing_schema_level_string_domain',
        'ascii_proto':
            """
          feature: {name: "x" type: BYTES domain: "my_domain"}
        """,
        'feature_spec': {
            'x': tf.io.VarLenFeature(tf.string)
        }
    },
]

INVALID_SCHEMA_PROTOS = [
    {
        'testcase_name': 'no_type',
        'ascii_proto': '''
          feature: {name: "x"}
          ''',
        'error_msg': 'Feature "x" had invalid type TYPE_UNKNOWN'
    },
    {
        'testcase_name':
            'feature_has_shape_but_not_always_present',
        'ascii_proto':
            """
          feature: {name: "x" type: INT shape: {}}
        """,
        'error_msg':
            r'Feature "x" had shape  set but min_fraction 0.0 != 1.  '
            r'Use value_count not shape field when min_fraction != 1.'
    },
    {
        'testcase_name':
            'sparse_feature_no_index_int_domain',
        'ascii_proto':
            '''
          feature {
            name: "index_key"
            type: INT
          }
          feature {
            name: "value_key"
            type: INT
          }
          sparse_feature {
            name: "x"
            index_feature {name: "index_key"}
            value_feature {name: "value_key"}
          }
          ''',
        'error_msg':
            r'Cannot determine dense shape of sparse feature "x"'
    },
    {
        'testcase_name':
            'sparse_feature_no_index_int_domain_min',
        'ascii_proto':
            """
          feature {
            name: "index_key"
            type: INT
            int_domain { max: 9 }
          }
          feature {
            name: "value_key"
            type: INT
          }
          sparse_feature {
            name: "x"
            index_feature {name: "index_key"}
            value_feature {name: "value_key"}
          }
          """,
        'error_msg':
            r'Cannot determine dense shape of sparse feature "x". '
            r'The minimum domain value of index feature "index_key"'
            r' is not set.'
    },
    {
        'testcase_name':
            'sparse_feature_non_zero_index_int_domain_min',
        'ascii_proto':
            """
          feature {
            name: "index_key"
            type: INT
            int_domain { min: 1 max: 9 }
          }
          feature {
            name: "value_key"
            type: INT
          }
          sparse_feature {
            name: "x"
            index_feature {name: "index_key"}
            value_feature {name: "value_key"}
          }
          """,
        'error_msg':
            r'Only 0-based index features are supported. Sparse '
            r'feature "x" has index feature "index_key" whose '
            r'minimum domain value is 1'
    },
    {
        'testcase_name':
            'sparse_feature_no_index_int_domain_max',
        'ascii_proto':
            """
          feature {
            name: "index_key"
            type: INT
            int_domain { min: 0 }
          }
          feature {
            name: "value_key"
            type: INT
          }
          sparse_feature {
            name: "x"
            index_feature {name: "index_key"}
            value_feature {name: "value_key"}
          }
          """,
        'error_msg':
            r'Cannot determine dense shape of sparse feature "x". '
            r'The maximum domain value of index feature "index_key"'
            r' is not set.'
    },
    {
        'testcase_name':
            'sparse_feature_missing_index_key',
        'ascii_proto':
            """
          feature {
            name: "value_key"
            type: INT
          }
          sparse_feature {
            name: "x"
            is_sorted: true
            index_feature {name: "index_key"}
            value_feature {name: "value_key"}
          }
        """,
        'error_msg':
            r'sparse_feature "x" referred to index feature '
            r'"index_key" which did not exist in the schema'
    },
    {
        'testcase_name':
            'sparse_feature_missing_value_key',
        'ascii_proto':
            """
          feature {
            name: "index_key"
            type: INT
            int_domain { min: 0 max: 9 }
          }
          sparse_feature {
            name: "x"
            is_sorted: true
            index_feature {name: "index_key"}
            value_feature {name: "value_key"}
          }
        """,
        'error_msg':
            r'sparse_feature "x" referred to value feature '
            r'"value_key" which did not exist in the schema'
    },
]

INVALID_FEATURE_SPECS = [
    {
        'testcase_name': 'bad_type',
        'feature_spec': {
            'x': tf.io.FixedLenFeature([], tf.bool)
        },
        'error_msg': 'Feature "x" has invalid dtype'
    },
    {
        'testcase_name': 'unsupported_type',
        'feature_spec': {
            'x': tf.io.FixedLenSequenceFeature([], tf.int64)
        },
        'error_msg': r'Spec for feature "x" was .* of type .*, expected a '
                     r'FixedLenFeature, VarLenFeature or SparseFeature',
        'error_class': TypeError
    },
]

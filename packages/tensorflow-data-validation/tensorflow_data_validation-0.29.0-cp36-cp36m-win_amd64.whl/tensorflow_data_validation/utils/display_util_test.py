# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for display_util."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl.testing import absltest
from google.protobuf import text_format
from tensorflow_data_validation import types
from tensorflow_data_validation.utils import display_util
from tensorflow_data_validation.utils import test_util
from tensorflow_metadata.proto.v0 import anomalies_pb2
from tensorflow_metadata.proto.v0 import schema_pb2
from tensorflow_metadata.proto.v0 import statistics_pb2


class DisplayUtilTest(absltest.TestCase):

  def test_get_statistics_html(self):
    statistics = text_format.Parse("""
    datasets {
      num_examples: 3
      features {
        name: 'a'
        type: FLOAT
        num_stats {
          common_stats {
            num_non_missing: 3
            num_missing: 0
            min_num_values: 1
            max_num_values: 4
            avg_num_values: 2.33333333
            tot_num_values: 7
            num_values_histogram {
              buckets {
                low_value: 1.0
                high_value: 1.0
                sample_count: 1.0
              }
              buckets {
                low_value: 1.0
                high_value: 4.0
                sample_count: 1.0
              }
              buckets {
                low_value: 4.0
                high_value: 4.0
                sample_count: 1.0
              }
              type: QUANTILES
            }
          }
          mean: 2.66666666
          std_dev: 1.49071198
          num_zeros: 0
          min: 1.0
          max: 5.0
          median: 3.0
          histograms {
            num_nan: 1
            buckets {
              low_value: 1.0
              high_value: 2.3333333
              sample_count: 2.9866667
            }
            buckets {
              low_value: 2.3333333
              high_value: 3.6666667
              sample_count: 1.0066667
            }
            buckets {
              low_value: 3.6666667
              high_value: 5.0
              sample_count: 2.0066667
            }
            type: STANDARD
          }
          histograms {
            num_nan: 1
            buckets {
              low_value: 1.0
              high_value: 1.0
              sample_count: 1.5
            }
            buckets {
              low_value: 1.0
              high_value: 3.0
              sample_count: 1.5
            }
            buckets {
              low_value: 3.0
              high_value: 4.0
              sample_count: 1.5
            }
            buckets {
              low_value: 4.0
              high_value: 5.0
              sample_count: 1.5
            }
            type: QUANTILES
          }
        }
      }
      features {
        name: 'c'
        type: INT
        num_stats {
          common_stats {
            num_non_missing: 3
            num_missing: 0
            min_num_values: 500
            max_num_values: 1750
            avg_num_values: 1000.0
            tot_num_values: 3000
            num_values_histogram {
              buckets {
                low_value: 500.0
                high_value: 500.0
                sample_count: 1.0
              }
              buckets {
                low_value: 500.0
                high_value: 1750.0
                sample_count: 1.0
              }
              buckets {
                low_value: 1750.0
                high_value: 1750.0
                sample_count: 1.0
              }
              type: QUANTILES
            }
          }
          mean: 1500.5
          std_dev: 866.025355672
          min: 1.0
          max: 3000.0
          median: 1501.0
          histograms {
            buckets {
              low_value: 1.0
              high_value: 1000.66666667
              sample_count: 999.666666667
            }
            buckets {
              low_value: 1000.66666667
              high_value: 2000.33333333
              sample_count: 999.666666667
            }
            buckets {
              low_value: 2000.33333333
              high_value: 3000.0
              sample_count: 1000.66666667
            }
            type: STANDARD
          }
          histograms {
            buckets {
              low_value: 1.0
              high_value: 751.0
              sample_count: 750.0
            }
            buckets {
              low_value: 751.0
              high_value: 1501.0
              sample_count: 750.0
            }
            buckets {
              low_value: 1501.0
              high_value: 2250.0
              sample_count: 750.0
            }
            buckets {
              low_value: 2250.0
              high_value: 3000.0
              sample_count: 750.0
            }
            type: QUANTILES
          }
        }
      }
      features {
        name: 'b'
        type: STRING
        string_stats {
          common_stats {
            num_non_missing: 3
            min_num_values: 4
            max_num_values: 4
            avg_num_values: 4.0
            tot_num_values: 12
            num_values_histogram {
              buckets {
                low_value: 4.0
                high_value: 4.0
                sample_count: 1.0
              }
              buckets {
                low_value: 4.0
                high_value: 4.0
                sample_count: 1.0
              }
              buckets {
                low_value: 4.0
                high_value: 4.0
                sample_count: 1.0
              }
              type: QUANTILES
            }
          }
          unique: 5
          top_values {
            value: "a"
            frequency: 4.0
          }
          top_values {
            value: "c"
            frequency: 3.0
          }
          avg_length: 1.0
          rank_histogram {
            buckets {
              low_rank: 0
              high_rank: 0
              label: "a"
              sample_count: 4.0
            }
            buckets {
              low_rank: 1
              high_rank: 1
              label: "c"
              sample_count: 3.0
            }
            buckets {
              low_rank: 2
              high_rank: 2
              label: "d"
              sample_count: 2.0
            }
          }
        }
      }
    }
    """, statistics_pb2.DatasetFeatureStatisticsList())

    # pylint: disable=line-too-long,anomalous-backslash-in-string
    expected_output = """<iframe id='facets-iframe' width="100%" height="500px"></iframe>
        <script>
        facets_iframe = document.getElementById('facets-iframe');
        facets_html = '<script src="https://cdnjs.cloudflare.com/ajax/libs/webcomponentsjs/1.3.3/webcomponents-lite.js"><\/script><link rel="import" href="https://raw.githubusercontent.com/PAIR-code/facets/master/facets-dist/facets-jupyter.html"><facets-overview proto-input="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"></facets-overview>';
        facets_iframe.srcdoc = facets_html;
         facets_iframe.id = "";
         setTimeout(() => {
           facets_iframe.setAttribute('height', facets_iframe.contentWindow.document.body.offsetHeight + 'px')
         }, 1500)
         </script>"""
    # pylint: enable=line-too-long

    display_html = display_util.get_statistics_html(statistics, statistics)

    self.assertEqual(display_html, expected_output)

  def test_visualize_statistics_invalid_allowlist_denylist(self):
    statistics = text_format.Parse("""
    datasets {
      name: 'test'
      features {
        path { step: 'a' }
        type: FLOAT
      }
      features {
        path { step: 'c' }
        type: INT
      }
      features {
        path { step: 'b' }
        type: STRING
      }
    }
    """, statistics_pb2.DatasetFeatureStatisticsList())
    with self.assertRaisesRegex(AssertionError, '.*specify one of.*'):
      display_util.visualize_statistics(
          statistics, allowlist_features=[types.FeaturePath(['a'])],
          denylist_features=[types.FeaturePath(['c'])])

  def test_get_combined_statistics_allowlist_features(self):
    statistics = text_format.Parse("""
    datasets {
      name: 'test'
      features {
        path { step: 'a' }
        type: FLOAT
      }
      features {
        path { step: 'c' }
        type: INT
      }
      features {
        path { step: 'b' }
        type: STRING
      }
    }
    """, statistics_pb2.DatasetFeatureStatisticsList())

    expected_output = text_format.Parse("""
    datasets {
      name: 'test'
      features {
        path { step: 'a' }
        type: FLOAT
      }
      features {
        path { step: 'b' }
        type: STRING
      }
    }
    """, statistics_pb2.DatasetFeatureStatisticsList())

    actual_output = display_util._get_combined_statistics(
        statistics, allowlist_features=[
            types.FeaturePath(['a']), types.FeaturePath(['b'])])
    self.assertLen(actual_output.datasets, 1)
    test_util.assert_dataset_feature_stats_proto_equal(
        self, actual_output.datasets[0], expected_output.datasets[0])

  def test_get_combined_statistics_denylist_features(self):
    statistics = text_format.Parse("""
    datasets {
      name: 'test'
      features {
        path { step: 'a' }
        type: FLOAT
      }
      features {
        path { step: 'c' }
        type: INT
      }
      features {
        path { step: 'b' }
        type: STRING
      }
    }
    """, statistics_pb2.DatasetFeatureStatisticsList())

    expected_output = text_format.Parse("""
    datasets {
      name: 'test'
      features {
        path { step: 'a' }
        type: FLOAT
      }
      features {
        path { step: 'b' }
        type: STRING
      }
    }
    """, statistics_pb2.DatasetFeatureStatisticsList())

    actual_output = display_util._get_combined_statistics(
        statistics, denylist_features=[types.FeaturePath(['c'])])
    self.assertLen(actual_output.datasets, 1)
    test_util.assert_dataset_feature_stats_proto_equal(
        self, actual_output.datasets[0], expected_output.datasets[0])

  def test_get_schema_dataframe(self):
    schema = text_format.Parse("""
        feature {
          name: "fa"
          type: INT
          int_domain {
            is_categorical: true
          }
        }
        feature {
          name: "fb"
          type: BYTES
        }
        feature {
          name: "fc"
          type: FLOAT
        }
        """, schema_pb2.Schema())
    actual_output = display_util.get_schema_dataframe(schema)
    # The resulting DataFrame has a row for each feature and columns for type,
    # presence, valency, and domain.
    self.assertEqual(actual_output.shape, (3, 4))

  def test_get_anomalies_dataframe(self):
    anomalies = text_format.Parse(
        """
    anomaly_info {
     key: "feature_1"
     value {
        description: "Expected bytes but got string."
        severity: ERROR
        short_description: "Bytes not string"
        reason {
          type: ENUM_TYPE_BYTES_NOT_STRING
          short_description: "Bytes not string"
          description: "Expected bytes but got string."
        }
      }
    }
    anomaly_info {
      key: "feature_2"
      value {
        description: "Examples contain values missing from the schema."
        severity: ERROR
        short_description: "Unexpected string values"
        reason {
          type: ENUM_TYPE_UNEXPECTED_STRING_VALUES
          short_description: "Unexpected string values"
          description: "Examples contain values missing from the "
            "schema."
        }
      }
    }
    """, anomalies_pb2.Anomalies())
    actual_output = display_util.get_anomalies_dataframe(anomalies)
    # The resulting DataFrame has a row for each feature and a column for each
    # of the short description and long description.
    self.assertEqual(actual_output.shape, (2, 2))

  def test_get_anomalies_dataframe_no_anomalies(self):
    anomalies = anomalies_pb2.Anomalies()
    actual_output = display_util.get_anomalies_dataframe(anomalies)
    self.assertEqual(actual_output.shape, (0, 2))


if __name__ == '__main__':
  absltest.main()

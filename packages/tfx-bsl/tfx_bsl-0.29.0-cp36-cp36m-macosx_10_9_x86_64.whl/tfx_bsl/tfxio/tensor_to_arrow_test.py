# Copyright 2020 Google LLC
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
"""Tests for tfx_bsl.tfxio.tensor_to_arrow."""

import numpy as np
import pyarrow as pa
import tensorflow as tf
from tfx_bsl.tfxio import tensor_adapter
from tfx_bsl.tfxio import tensor_to_arrow
from google.protobuf import text_format
from absl.testing import absltest
from absl.testing import parameterized
from tensorflow_metadata.proto.v0 import schema_pb2

_TF_TYPE_TO_ARROW_TYPE = {
    tf.int8: pa.int8(),
    tf.int16: pa.int16(),
    tf.int32: pa.int32(),
    tf.int64: pa.int64(),
    tf.uint8: pa.uint8(),
    tf.uint16: pa.uint16(),
    tf.uint32: pa.uint32(),
    tf.uint64: pa.uint64(),
    tf.float32: pa.float32(),
    tf.float64: pa.float64(),
    tf.string: pa.large_binary(),
}

_ROW_PARTITION_DTYPES = {
    "INT64": np.int64,
    "INT32": np.int32
}


def _make_2d_dense_tensor_test_cases():
  result = []
  for tf_type, arrow_type in _TF_TYPE_TO_ARROW_TYPE.items():
    if tf_type == tf.string:
      tensor = tf.constant([[b"1", b"2"], [b"3", b"4"]], dtype=tf.string)
      expected_array = pa.array([[b"1", b"2"], [b"3", b"4"]],
                                type=pa.large_list(arrow_type))
    else:
      tensor = tf.constant([[1, 2], [3, 4]], dtype=tf_type)
      expected_array = pa.array([[1, 2], [3, 4]],
                                type=pa.large_list(arrow_type))
    result.append(
        dict(
            testcase_name="2d_dense_tensor_%s" % tf_type.name,
            type_specs={"dt": tf.TensorSpec([None, 2], tf_type)},
            expected_schema={"dt": pa.large_list(arrow_type)},
            expected_tensor_representations={
                "dt":
                    """dense_tensor {
                         column_name: "dt"
                         shape { dim { size: 2} }
                       }""",
            },
            tensor_input={"dt": tensor},
            expected_record_batch={"dt": expected_array},
            test_values_conversion=True))
  return result


def _make_2d_varlen_sparse_tensor_test_cases():
  result = []
  for tf_type, arrow_type in _TF_TYPE_TO_ARROW_TYPE.items():
    if tf_type == tf.string:
      values = tf.constant([b"1", b"2", b"3"], dtype=tf.string)
      expected_array = pa.array([[b"1"], [], [b"2", b"3"], []],
                                type=pa.large_list(arrow_type))
    else:
      values = tf.constant([1, 2, 3], dtype=tf_type)
      expected_array = pa.array([[1], [], [2, 3], []],
                                type=pa.large_list(arrow_type))
    result.append(
        dict(
            testcase_name="2d_varlen_sparse_tensor_%s" % tf_type.name,
            type_specs={"sp1": tf.SparseTensorSpec([None, None], tf_type)},
            expected_schema={"sp1": pa.large_list(arrow_type)},
            expected_tensor_representations={
                "sp1": """varlen_sparse_tensor { column_name: "sp1" }""",
            },
            tensor_input={
                "sp1":
                    tf.SparseTensor(
                        values=values,
                        indices=[[0, 0], [2, 0], [2, 1]],
                        dense_shape=[4, 2]),
            },
            expected_record_batch={"sp1": expected_array},
            test_values_conversion=True))
  return result


def _make_3d_ragged_tensor_test_cases():
  result = []
  for row_partition_dtype in _ROW_PARTITION_DTYPES:
    row_partition_numpy_type = _ROW_PARTITION_DTYPES[row_partition_dtype]
    for tf_type, arrow_type in _TF_TYPE_TO_ARROW_TYPE.items():
      if tf_type == tf.string:
        values = tf.RaggedTensor.from_row_splits(
            values=tf.constant([b"1", b"2", b"3"], dtype=tf_type),
            row_splits=np.asarray([0, 1, 1, 3, 3],
                                  dtype=row_partition_numpy_type))
        expected_array = pa.array([[[b"1"], [], [b"2", b"3"]], [[]]],
                                  type=pa.large_list(pa.large_list(arrow_type)))
      else:
        values = tf.RaggedTensor.from_row_splits(
            values=tf.constant([1, 2, 3], dtype=tf_type),
            row_splits=np.asarray([0, 1, 1, 3, 3],
                                  dtype=row_partition_numpy_type))
        expected_array = pa.array([[[1], [], [2, 3]], [[]]],
                                  type=pa.large_list(pa.large_list(arrow_type)))
      result.append(
          dict(
              testcase_name="3d_ragged_tensor_%s_row_partition_dtype_%s" %
              (tf_type.name, row_partition_dtype),
              type_specs={
                  "sp1":
                      tf.RaggedTensorSpec(
                          tf.TensorShape([2, None, None]),
                          tf_type,
                          ragged_rank=2,
                          row_splits_dtype=tf.dtypes.as_dtype(
                              row_partition_numpy_type))
              },
              expected_schema={"sp1": pa.large_list(pa.large_list(arrow_type))},
              expected_tensor_representations={
                  "sp1":
                      """ragged_tensor {
                          feature_path {
                            step: "sp1"
                          }
                          row_partition_dtype: %s
                        }""" % row_partition_dtype,
              },
              tensor_input={
                  "sp1":
                      tf.RaggedTensor.from_row_splits(
                          values=values,
                          row_splits=np.asarray([0, 3, 4],
                                                dtype=row_partition_numpy_type))
              },
              expected_record_batch={"sp1": expected_array}))
  return result


def _make_3d_sparse_tensor_test_cases():
  result = []
  for tf_type, arrow_type in _TF_TYPE_TO_ARROW_TYPE.items():
    if tf_type == tf.string:
      values = tf.constant([b"1", b"2", b"3", b"4"], dtype=tf.string)
      expected_value_array = pa.array([[b"1", b"2", b"3"], [], [b"4"], []],
                                      type=pa.large_list(arrow_type))
    else:
      values = tf.constant([1, 2, 3, 4], dtype=tf_type)
      expected_value_array = pa.array([[1, 2, 3], [], [4], []],
                                      type=pa.large_list(arrow_type))

    result.append(
        dict(
            testcase_name="3d_sparse_tensor_%s" % tf_type.name,
            type_specs={"sp1": tf.SparseTensorSpec([None, 4, 5], tf_type)},
            expected_schema={
                "sp1$values": pa.large_list(arrow_type),
                "sp1$index0": pa.large_list(pa.int64()),
                "sp1$index1": pa.large_list(pa.int64()),
            },
            expected_tensor_representations={
                "sp1": """sparse_tensor {
                dense_shape {
                  dim {
                    size: 4
                  }
                  dim {
                    size: 5
                  }
                }
                value_column_name: "sp1$values"
                index_column_names: "sp1$index0"
                index_column_names: "sp1$index1"
                }""",
            },
            tensor_input={
                "sp1":
                    tf.SparseTensor(
                        values=values,
                        indices=[[0, 0, 0], [0, 2, 2], [0, 2, 4],
                                 [2, 3, 1]],
                        dense_shape=[4, 4, 5]),
            },
            expected_record_batch={
                "sp1$values": expected_value_array,
                "sp1$index0": pa.array([[0, 2, 2], [], [3], []],
                                       type=pa.large_list(pa.int64())),
                "sp1$index1": pa.array([[0, 2, 4], [], [1], []],
                                       type=pa.large_list(pa.int64())),
            },
            test_values_conversion=True))
  return result


_CONVERT_TEST_CASES = [
    dict(
        testcase_name="multiple_tensors",
        type_specs={
            "sp1": tf.SparseTensorSpec([None, None], tf.int32),
            "sp2": tf.SparseTensorSpec([None, None], tf.string),
        },
        expected_schema={
            "sp1": pa.large_list(pa.int32()),
            "sp2": pa.large_list(pa.large_binary()),
        },
        expected_tensor_representations={
            "sp1": """varlen_sparse_tensor { column_name: "sp1" }""",
            "sp2": """varlen_sparse_tensor { column_name: "sp2" }""",
        },
        tensor_input={
            "sp1":
                tf.SparseTensor(
                    values=tf.constant([1, 2], dtype=tf.int32),
                    indices=[[0, 0], [2, 0]],
                    dense_shape=[4, 1]),
            "sp2":
                tf.SparseTensor(
                    values=[b"aa", b"bb"],
                    indices=[[2, 0], [2, 1]],
                    dense_shape=[4, 2])
        },
        expected_record_batch={
            "sp1":
                pa.array([[1], [], [2], []], type=pa.large_list(pa.int32())),
            "sp2":
                pa.array([[], [], [b"aa", b"bb"], []],
                         type=pa.large_list(pa.large_binary()))
        },
        test_values_conversion=True),
    dict(
        testcase_name="ragged_tensors",
        type_specs={
            "sp1":
                tf.RaggedTensorSpec(
                    tf.TensorShape([3, None]),
                    tf.int64,
                    ragged_rank=1,
                    row_splits_dtype=tf.int64),
            "sp2":
                tf.RaggedTensorSpec(
                    tf.TensorShape([3, None]),
                    tf.string,
                    ragged_rank=1,
                    row_splits_dtype=tf.int64),
        },
        expected_schema={
            "sp1": pa.large_list(pa.int64()),
            "sp2": pa.large_list(pa.large_binary()),
        },
        expected_tensor_representations={
            "sp1":
                """ragged_tensor {
                        feature_path {
                          step: "sp1"
                        }
                        row_partition_dtype: INT64
                      }""",
            "sp2":
                """ragged_tensor {
                        feature_path {
                          step: "sp2"
                        }
                        row_partition_dtype: INT64
                      }""",
        },
        tensor_input={
            "sp1":
                tf.RaggedTensor.from_row_splits(
                    values=np.asarray([1, 5, 9], dtype=np.int64),
                    row_splits=np.asarray([0, 2, 2, 3], dtype=np.int64)),
            "sp2":
                tf.RaggedTensor.from_row_splits(
                    values=np.asarray([b"x", b"y", b"z"], dtype=np.str),
                    row_splits=np.asarray([0, 2, 2, 3], dtype=np.int64))
        },
        expected_record_batch={
            "sp1":
                pa.array([[1, 5], [], [9]], type=pa.large_list(pa.int64())),
            "sp2":
                pa.array([[b"x", b"y"], [], [b"z"]],
                         type=pa.large_list(pa.large_binary())),
        }),
    dict(
        testcase_name="sparse_tensor_no_value",
        type_specs={
            "sp1": tf.SparseTensorSpec([None, None], tf.int32),
        },
        expected_schema={
            "sp1": pa.large_list(pa.int32()),
        },
        expected_tensor_representations={
            "sp1": """varlen_sparse_tensor { column_name: "sp1" }""",
        },
        tensor_input={
            "sp1":
                tf.SparseTensor(
                    values=tf.constant([], dtype=tf.int32),
                    indices=tf.constant([], shape=(0, 2), dtype=tf.int64),
                    dense_shape=[2, 0]),
        },
        expected_record_batch={
            "sp1": pa.array([[], []], type=pa.large_list(pa.int32())),
        },
        test_values_conversion=True),
    dict(
        testcase_name="1d_dense",
        type_specs={
            "dt1": tf.TensorSpec([None], tf.int32),
        },
        expected_schema={
            "dt1": pa.large_list(pa.int32()),
        },
        expected_tensor_representations={
            "dt1": """dense_tensor { column_name: "dt1" }""",
        },
        tensor_input={
            "dt1": tf.constant([1, 2, 3], dtype=tf.int32),
        },
        expected_record_batch={
            "dt1": pa.array([[1], [2], [3]], type=pa.large_list(pa.int32())),
        },
        test_values_conversion=True),
] + _make_2d_varlen_sparse_tensor_test_cases(
) + _make_3d_ragged_tensor_test_cases() + _make_2d_dense_tensor_test_cases(
) + _make_3d_sparse_tensor_test_cases()


class TensorToArrowTest(tf.test.TestCase, parameterized.TestCase):

  def _assert_tensor_alike_equal(self, left, right):
    self.assertIsInstance(left, type(right))
    if isinstance(left, (tf.SparseTensor, tf.compat.v1.SparseTensorValue)):
      self.assertAllEqual(left.values, right.values)
      self.assertAllEqual(left.indices, right.indices)
      self.assertAllEqual(left.dense_shape, right.dense_shape)
    else:
      self.assertAllEqual(left, right)

  @parameterized.named_parameters(*_CONVERT_TEST_CASES)
  def test_convert(self,
                   type_specs,
                   expected_schema,
                   expected_tensor_representations,
                   tensor_input,
                   expected_record_batch,
                   test_values_conversion=False):
    def convert_and_check(tensors, test_values_conversion):
      converter = tensor_to_arrow.TensorsToRecordBatchConverter(type_specs)

      self.assertEqual({f.name: f.type for f in converter.arrow_schema()},
                       expected_schema,
                       "actual: {}".format(converter.arrow_schema()))

      canonical_expected_tensor_representations = {}
      for n, r in expected_tensor_representations.items():
        if not isinstance(r, schema_pb2.TensorRepresentation):
          r = text_format.Parse(r, schema_pb2.TensorRepresentation())
        canonical_expected_tensor_representations[n] = r

      self.assertEqual(canonical_expected_tensor_representations,
                       converter.tensor_representations())

      rb = converter.convert(tensors)
      self.assertLen(expected_record_batch, rb.num_columns)
      for i, column in enumerate(rb):
        expected = expected_record_batch[rb.schema[i].name]
        self.assertTrue(
            column.equals(expected),
            "{}: actual: {}, expected: {}".format(rb.schema[i].name, column,
                                                  expected))
      # Test that TensorAdapter(TensorsToRecordBatchConverter()) is identity.
      adapter = tensor_adapter.TensorAdapter(
          tensor_adapter.TensorAdapterConfig(
              arrow_schema=converter.arrow_schema(),
              tensor_representations=converter.tensor_representations()))
      adapter_output = adapter.ToBatchTensors(
          rb, produce_eager_tensors=not test_values_conversion)
      self.assertEqual(adapter_output.keys(), tensors.keys())
      for k in adapter_output.keys():
        if "value" not in k:
          self._assert_tensor_alike_equal(adapter_output[k], tensors[k])

    def convert_eager_to_value(tensor):
      if isinstance(tensor, tf.SparseTensor):
        return tf.compat.v1.SparseTensorValue(
            tensor.indices, tensor.values, tensor.dense_shape)
      elif isinstance(tensor, tf.Tensor):
        return tensor.numpy()
      else:
        raise NotImplementedError(
            "Only support converting SparseTensors or Tensors. Got: {}"
            .format(type(tensor)))

    if tf.__version__ >= "2":
      convert_and_check(tensor_input, test_values_conversion=False)
    elif not test_values_conversion:
      raise absltest.SkipTest("Test case is disabled for TF 1.x: ragged "
                                "tensor value support is not implemented. ")

    if test_values_conversion:
      if tf.executing_eagerly():
        values_input = {
            k: convert_eager_to_value(v) for k, v in tensor_input.items()
        }
      else:
        with tf.compat.v1.Session(
            graph=next(iter(tensor_input.values())).graph) as s:
          values_input = s.run(tensor_input)
      convert_and_check(values_input, test_values_conversion=True)

  def test_relaxed_varlen_sparse_tensor(self):
    # Demonstrates that TensorAdapter(TensorsToRecordBatchConverter()) is not
    # an identity if the second dense dimension of SparseTensor is not tight.
    type_specs = {"sp": tf.SparseTensorSpec([None, None], tf.int32)}
    sp = tf.compat.v1.SparseTensorValue(
        values=np.array([1, 2], np.int32),
        indices=[[0, 0], [2, 0]],
        dense_shape=[4, 2])
    if tf.__version__ >= "2":
      sp = tf.SparseTensor.from_value(sp)
    converter = tensor_to_arrow.TensorsToRecordBatchConverter(type_specs)
    rb = converter.convert({"sp": sp})
    adapter = tensor_adapter.TensorAdapter(
        tensor_adapter.TensorAdapterConfig(
            arrow_schema=converter.arrow_schema(),
            tensor_representations=converter.tensor_representations()))
    adapter_output = adapter.ToBatchTensors(
        rb, produce_eager_tensors=tf.__version__ >= "2")
    self.assertAllEqual(sp.values, adapter_output["sp"].values)
    self.assertAllEqual(sp.indices, adapter_output["sp"].indices)
    self.assertAllEqual(adapter_output["sp"].dense_shape, [4, 1])

  def test_unable_to_handle(self):
    with self.assertRaisesRegex(ValueError, "No handler found"):
      tensor_to_arrow.TensorsToRecordBatchConverter(
          {"sp": tf.SparseTensorSpec([None, None, None], tf.int32)})

    with self.assertRaisesRegex(ValueError, "No handler found"):
      tensor_to_arrow.TensorsToRecordBatchConverter(
          {"sp": tf.SparseTensorSpec([None, None], tf.bool)})

  def test_incompatible_type_spec(self):
    converter = tensor_to_arrow.TensorsToRecordBatchConverter(
        {"sp": tf.SparseTensorSpec([None, None], tf.int32)})
    sp_cls = tf.SparseTensor if tf.__version__ >= "2" else \
        tf.compat.v1.SparseTensorValue
    with self.assertRaisesRegex(TypeError, "Expected SparseTensorSpec"):
      converter.convert({
          "sp":
              sp_cls(
                  indices=[[0, 1]],
                  values=tf.constant([0], dtype=tf.int64),
                  dense_shape=[4, 1])
      })

  @parameterized.named_parameters(*[
      dict(
          testcase_name="bool_value_type",
          spec=tf.RaggedTensorSpec(
              shape=[2, None, None],
              dtype=tf.bool,
              ragged_rank=2,
              row_splits_dtype=tf.int64)),
      dict(
          testcase_name="2d_leaf_value",
          spec=tf.RaggedTensorSpec(
              shape=[2, None, None],
              dtype=tf.int32,
              ragged_rank=1,
              row_splits_dtype=tf.int64)),
      dict(
          testcase_name="ragged_rank_less_than_one",
          spec=tf.RaggedTensorSpec(
              shape=[2],
              dtype=tf.int32,
              ragged_rank=0,
              row_splits_dtype=tf.int64)),
  ])
  def test_unable_to_handle_ragged(self, spec):
    with self.assertRaisesRegex(ValueError, "No handler found"):
      tensor_to_arrow.TensorsToRecordBatchConverter({"rt": spec})


if __name__ == "__main__":
  absltest.main()

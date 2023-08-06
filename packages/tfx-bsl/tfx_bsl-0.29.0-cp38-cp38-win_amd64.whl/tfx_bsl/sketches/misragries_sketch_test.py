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
"""Tests for tfx_bsl.sketches.MisraGriesSketch."""

import pickle

import pyarrow as pa
from tfx_bsl import sketches

from absl.testing import absltest
from absl.testing import parameterized

_NUM_BUCKETS = 128


def _create_basic_sketch(items, weights=None, num_buckets=_NUM_BUCKETS):
  sketch = sketches.MisraGriesSketch(num_buckets)
  if weights:
    sketch.AddValues(items, weights)
  else:
    sketch.AddValues(items)
  return sketch


class MisraGriesSketchTest(parameterized.TestCase):

  @parameterized.named_parameters(
      ("binary", [b"a", b"a", b"b", b"c", None], pa.binary()),
      ("large_binary", [b"a", b"a", b"b", b"c"], pa.large_binary()),
      ("string", ["a", "a", "b", "c", None], pa.string()),
      ("large_string", ["a", "a", "b", "c"], pa.large_string()),
  )
  def test_add_binary_like(self, values, binary_like_type):
    expected_counts = [{
        "values": b"a",
        "counts": 2.0
    }, {
        "values": b"b",
        "counts": 1.0
    }, {
        "values": b"c",
        "counts": 1.0
    }]
    sketch = _create_basic_sketch(pa.array(values, type=binary_like_type))
    estimate = sketch.Estimate()
    estimate.validate(full=True)
    self.assertEqual(estimate.to_pylist(), expected_counts)

  @parameterized.named_parameters(
      ("int8", [1, 1, 2, 3, None], pa.int8()),
      ("int16", [1, 1, 2, 3], pa.int16()),
      ("int32", [1, 1, 2, 3, None], pa.int32()),
      ("int64", [1, 1, 2, 3], pa.int64()),
      ("uint8", [1, 1, 2, 3], pa.uint8()),
      ("uint16", [1, None, 1, 2, 3], pa.uint16()),
      ("uint32", [1, 1, 2, 3], pa.uint32()),
      ("uint64", [1, 1, 2, 3, None], pa.uint64()),
  )
  def test_add_integer(self, values, integer_type):
    expected_counts = [{
        "values": b"1",
        "counts": 2.0
    }, {
        "values": b"2",
        "counts": 1.0
    }, {
        "values": b"3",
        "counts": 1.0
    }]
    sketch = _create_basic_sketch(pa.array(values, type=integer_type))
    estimate = sketch.Estimate()
    estimate.validate(full=True)
    self.assertEqual(estimate.to_pylist(), expected_counts)

  def test_add_weighted_values(self):
    items = pa.array(["a", "a", "b", "c"], type=pa.string())
    weights = pa.array([4, 3, 2, 1], type=pa.float32())
    sketch = _create_basic_sketch(items, weights=weights)

    expected_counts = [{
        "values": b"a",
        "counts": 7.0
    }, {
        "values": b"b",
        "counts": 2.0
    }, {
        "values": b"c",
        "counts": 1.0
    }]
    estimate = sketch.Estimate()
    estimate.validate(full=True)

    self.assertEqual(estimate.to_pylist(), expected_counts)

  def test_add_invalid_weights(self):
    items = pa.array(["a", "a", "b", "c"], type=pa.string())
    weights = pa.array([4, 3, 2, 1], type=pa.int64())
    with self.assertRaisesRegex(
        RuntimeError, "Invalid argument: Weight array must be float type."):
      _create_basic_sketch(items, weights=weights)

  def test_add_unsupported_type(self):
    values = pa.array([True, False], pa.bool_())
    sketch = sketches.MisraGriesSketch(_NUM_BUCKETS)
    with self.assertRaisesRegex(RuntimeError, "Unimplemented: bool"):
      sketch.AddValues(values)

  def test_merge(self):
    sketch1 = _create_basic_sketch(pa.array(["a", "b", "c", "a"]))
    sketch2 = _create_basic_sketch(pa.array(["d", "a"]))

    sketch1.Merge(sketch2)
    estimate = sketch1.Estimate()
    estimate.validate(full=True)
    expected_counts = [{
        "values": b"a",
        "counts": 3.0
    }, {
        "values": b"b",
        "counts": 1.0
    }, {
        "values": b"c",
        "counts": 1.0
    }, {
        "values": b"d",
        "counts": 1.0
    }]

    self.assertEqual(estimate.to_pylist(), expected_counts)

  def test_picklable(self):
    sketch = _create_basic_sketch(pa.array(["a", "b", "c", "a"]))
    pickled = pickle.dumps(sketch, 2)
    self.assertIsInstance(pickled, bytes)
    unpickled = pickle.loads(pickled)
    self.assertIsInstance(unpickled, sketches.MisraGriesSketch)

    estimate = unpickled.Estimate()
    estimate.validate(full=True)
    expected_counts = [{
        "values": b"a",
        "counts": 2.0
    }, {
        "values": b"b",
        "counts": 1.0
    }, {
        "values": b"c",
        "counts": 1.0
    }]

    self.assertEqual(estimate.to_pylist(), expected_counts)

  def test_serialization(self):
    sketch = _create_basic_sketch(pa.array(["a", "b", "c", "a"]))

    serialized = sketch.Serialize()
    self.assertIsInstance(serialized, bytes)

    deserialized = sketches.MisraGriesSketch.Deserialize(serialized)
    self.assertIsInstance(deserialized, sketches.MisraGriesSketch)

    estimate = deserialized.Estimate()
    estimate.validate(full=True)
    expected_counts = [{
        "values": b"a",
        "counts": 2.0
    }, {
        "values": b"b",
        "counts": 1.0
    }, {
        "values": b"c",
        "counts": 1.0
    }]

    self.assertEqual(estimate.to_pylist(), expected_counts)

if __name__ == "__main__":
  absltest.main()

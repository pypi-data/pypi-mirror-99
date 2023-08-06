# Copyright 2021 Google LLC
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
"""Types common to tfx_bsl.tfxio."""

from typing import Union
import tensorflow as tf

# TODO(b/146402007): Replace references with tf.TypeSpec and remove this once
# pytype starts recognizing subclasses of TF classes.
TensorTypeSpec = Union[tf.TensorSpec, tf.SparseTensorSpec, tf.RaggedTensorSpec,
                       tf.TypeSpec]

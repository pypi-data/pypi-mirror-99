# Copyright 2020 The FastEstimator Authors. All Rights Reserved.
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
# ==============================================================================
import unittest

import tensorflow as tf

import fastestimator as fe


class TestHadamardCode(unittest.TestCase):
    def test_single_input(self):
        batch_size = 27
        n_features = 123
        n_classes = 10
        x = tf.ones((batch_size, n_features))
        layer = fe.layers.tensorflow.HadamardCode(n_classes=n_classes)
        y = layer(x)
        self.assertEqual(tf.TensorShape(dims=(batch_size, n_classes)), y.shape)
        for row in y:
            # Should have produced a probability vector, so each row must be equal to 1
            self.assertAlmostEqual(1, tf.reduce_sum(row).numpy(), delta=0.000001)

    def test_multi_input(self):
        batch_size = 32
        n_features = 18
        n_classes = 18
        x = [tf.ones((batch_size, n_features)) for _ in range(6)]
        layer = fe.layers.tensorflow.HadamardCode(n_classes=n_classes)
        y = layer(x)
        self.assertEqual(tf.TensorShape(dims=(batch_size, n_classes)), y.shape)
        for row in y:
            # Should have produced a probability vector, so each row must be equal to 1
            self.assertAlmostEqual(1, tf.reduce_sum(row).numpy(), delta=0.000001)

    def test_longer_code(self):
        batch_size = 16
        n_features = 11
        n_classes = 13
        x = tf.ones((batch_size, n_features))
        layer = fe.layers.tensorflow.HadamardCode(n_classes=n_classes, code_length=256)
        y = layer(x)
        self.assertEqual(tf.TensorShape(dims=(batch_size, n_classes)), y.shape)
        for row in y:
            # Should have produced a probability vector, so each row must be equal to 1
            self.assertAlmostEqual(1, tf.reduce_sum(row).numpy(), delta=0.000001)

    def test_shorter_code(self):
        n_classes = 10
        self.assertRaises(ValueError, lambda: fe.layers.tensorflow.HadamardCode(n_classes=n_classes, code_length=8))

    def test_non_power_of_two_code_length(self):
        n_classes = 10
        self.assertRaises(ValueError, lambda: fe.layers.tensorflow.HadamardCode(n_classes=n_classes, code_length=18))

    def test_negative_code_length(self):
        self.assertRaises(ValueError, lambda: fe.layers.tensorflow.HadamardCode(n_classes=5, code_length=-2))

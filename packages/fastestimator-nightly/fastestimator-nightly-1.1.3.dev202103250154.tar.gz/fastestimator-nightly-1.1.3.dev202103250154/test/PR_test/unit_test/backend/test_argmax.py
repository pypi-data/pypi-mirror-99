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

import numpy as np
import tensorflow as tf
import torch

import fastestimator as fe
from fastestimator.test.unittest_util import is_equal


class TestArgmax(unittest.TestCase):
    def test_argmax_np_input_axis_0(self):
        n = np.array([[2, 7, 5], [9, 1, 3], [4, 8, 2]])
        obj1 = fe.backend.argmax(n, axis=0)
        obj2 = np.array([1, 2, 0])
        self.assertTrue(is_equal(obj1, obj2))

    def test_argmax_np_input_axis_1(self):
        n = np.array([[2, 7, 5], [9, 1, 3], [4, 8, 2]])
        obj1 = fe.backend.argmax(n, axis=1)
        obj2 = np.array([1, 0, 1])
        self.assertTrue(is_equal(obj1, obj2))

    def test_argmax_tf_input_axis_0(self):
        t = tf.constant([[2, 7, 5], [9, 1, 3], [4, 8, 2]])
        obj1 = fe.backend.argmax(t, axis=0)
        obj2 = tf.constant([1, 2, 0])
        self.assertTrue(is_equal(obj1, obj2))

    def test_argmax_tf_input_axis_1(self):
        t = tf.constant([[2, 7, 5], [9, 1, 3], [4, 8, 2]])
        obj1 = fe.backend.argmax(t, axis=1)
        obj2 = tf.constant([1, 0, 1])
        self.assertTrue(is_equal(obj1, obj2))

    def test_argmax_torch_input_axis_0(self):
        p = torch.tensor([[2, 7, 5], [9, 1, 3], [4, 8, 2]])
        obj1 = fe.backend.argmax(p, axis=0)
        obj2 = torch.tensor([1, 2, 0])
        self.assertTrue(is_equal(obj1, obj2))

    def test_argmax_torch_input_axis_1(self):
        p = torch.tensor([[2, 7, 5], [9, 1, 3], [4, 8, 2]])
        obj1 = fe.backend.argmax(p, axis=1)
        obj2 = torch.tensor([1, 0, 1])
        self.assertTrue(is_equal(obj1, obj2))

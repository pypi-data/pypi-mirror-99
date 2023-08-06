import unittest
from copy import deepcopy

import tensorflow as tf
import torch

import fastestimator as fe
from fastestimator.test.unittest_util import OneLayerTorchModel, is_equal, one_layer_tf_model


def get_torch_model_weight(model):
    if torch.cuda.device_count() > 1:
        model = model.module

    weight = []
    weight.append(deepcopy(model.fc1.weight.data.numpy()))

    return weight


def get_tf_model_weight(model):
    weight = []
    for layer in model.layers:
        weight.append(layer.get_weights())

    return weight


class TestUpdateModel(unittest.TestCase):
    def test_tf_model_with_loss(self):
        def update(x, model):
            with tf.GradientTape(persistent=True) as tape:
                y = fe.backend.feed_forward(model, x)
                fe.backend.update_model(model, loss=y, tape=tape)

        model = fe.build(model_fn=one_layer_tf_model, optimizer_fn="adam")
        init_weight = get_tf_model_weight(model)
        x = tf.constant([[1, 1, 1]])
        strategy = tf.distribute.get_strategy()
        if isinstance(strategy, tf.distribute.MirroredStrategy):
            strategy.run(update, args=(x, model))
        else:
            update(x, model)
        new_weight = get_tf_model_weight(model)
        self.assertTrue(not is_equal(init_weight, new_weight))

    def test_tf_model_with_gradient(self):
        def update(x, model):
            with tf.GradientTape(persistent=True) as tape:
                y = fe.backend.feed_forward(model, x)
                gradient = fe.backend.get_gradient(target=y, sources=model.trainable_variables, tape=tape)
                fe.backend.update_model(model, gradients=gradient, tape=tape)

        model = fe.build(model_fn=one_layer_tf_model, optimizer_fn="adam")
        init_weight = get_tf_model_weight(model)
        x = tf.constant([[1, 1, 1]])
        strategy = tf.distribute.get_strategy()
        if isinstance(strategy, tf.distribute.MirroredStrategy):
            strategy.run(update, args=(x, model))
        else:
            update(x, model)
        new_weight = get_tf_model_weight(model)
        self.assertTrue(not is_equal(init_weight, new_weight))

    def test_torch_model_with_loss(self):
        model = fe.build(model_fn=OneLayerTorchModel, optimizer_fn="adam")
        init_weight = get_torch_model_weight(model)

        x = torch.tensor([1.0, 1.0, 1.0])
        y = fe.backend.feed_forward(model.module if torch.cuda.device_count() > 1 else model, x)
        fe.backend.update_model(model, loss=y)

        new_weight = get_torch_model_weight(model)

        self.assertTrue(not is_equal(init_weight, new_weight))

    def test_torch_model_with_gradient(self):
        model = fe.build(model_fn=OneLayerTorchModel, optimizer_fn="adam")
        init_weight = get_torch_model_weight(model)

        x = torch.tensor([1.0, 1.0, 1.0])
        y = fe.backend.feed_forward(model.module if torch.cuda.device_count() > 1 else model, x)
        gradient = fe.backend.get_gradient(
            target=y, sources=[model.module.fc1.weight if torch.cuda.device_count() > 1 else model.fc1.weight])
        fe.backend.update_model(model, gradients=gradient)

        new_weight = get_torch_model_weight(model)

        self.assertTrue(not is_equal(init_weight, new_weight))

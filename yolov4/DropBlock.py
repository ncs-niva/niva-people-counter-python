# -*- coding: utf-8 -*-
from tensorflow.keras import layers, backend
import numpy as np


class DropBlock2D(layers.Layer):

    def __init__(self, block_size, keep_prob, **kwargs):
        super(DropBlock2D, self).__init__(**kwargs)
        self.block_size = block_size
        self.keep_prob = keep_prob
        self.height, self.width = None, None

    def build(self, input_shape):
        self.height = input_shape[1]
        self.width = input_shape[2]

    def _get_gamma(self):
        x1 = (1.0 - self.keep_prob) / (self.block_size ** 2)
        x2 = self.height * self.width / ((self.height - self.block_size + 1.0) * (self.width - self.block_size + 1.0))
        gamma = x1 * x2

        return gamma

    def _get_seed_shape(self):
        padding = self._get_padding()
        seed_shape = (self.height - (padding * 2), self.width - (padding * 2))

        return seed_shape

    def _get_padding(self):
        padding = self.block_size // 2

        return padding

    def call(self, inputs, training=None):
        outputs = inputs

        gamma = self._get_gamma()
        shape = self._get_seed_shape()
        padding = self._get_padding()

        sample = np.random.binomial(n=1, size=shape, p=gamma)

        sample = 1 - sample

        mask = np.pad(sample, pad_width=padding, mode='constant', constant_values=1)

        index = np.argwhere(mask == 0)
        for idx in index:
            i, j = idx
            mask[i-padding: i+padding+1, j-padding: j+padding+1] = 0

        mask = np.expand_dims(mask, axis=-1)

        outputs = outputs * np.repeat(mask, inputs.shape[-1], -1)

        count = np.prod(mask.shape)
        count_ones = np.count_nonzero(mask)
        outputs = outputs * count / count_ones

        return backend.in_train_phase(outputs, inputs, training=training)

    def get_config(self):
        config = {'block_size': self.block_size,
                  'gamma': self.gamma,
                  'seed': self.seed}
        base_config = super(DropBlock2D, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def compute_output_shape(self, input_shape):
        return input_shape

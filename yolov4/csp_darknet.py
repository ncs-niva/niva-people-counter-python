# -*- coding: utf-8 -*-

from tensorflow.keras import layers, regularizers
from DropBlock import DropBlock2D
import tensorflow as tf
import config as cfg


class Mish(layers.Layer):
    def __init__(self, **kwargs):
        super(Mish, self).__init__(**kwargs)
        self.supports_masking = True

    @staticmethod
    def call(inputs, **kwargs):
        return inputs * tf.tanh(tf.nn.softplus(inputs))

    def get_config(self):
        config = super(Mish, self).get_config()
        return config

    @staticmethod
    def compute_output_shape(input_shape, **kwargs):
        return input_shape


def darknetConv2D_BN_Mish(inputs, num_filter, kernel_size, strides=(1, 1), bn=True):
    if strides == (1, 1) or strides == 1:
        padding = 'same'
    else:
        padding = 'valid'

    x = layers.Conv2D(num_filter, kernel_size=kernel_size,
                      strides=strides, padding=padding,
                      use_bias=not bn, kernel_regularizer=regularizers.l2(5e-4),  # 只有添加正则化参数，才能调用model.losses方法
                      kernel_initializer=tf.random_normal_initializer(stddev=0.01))(inputs)

    if bn:
        x = layers.BatchNormalization()(x)
        x = Mish()(x)

    return x


def darknetConv2D_BN_Leaky(inputs, num_filter, kernel_size, strides=(1, 1), bn=True):
    if strides == (1, 1) or strides == 1:
        padding = 'same'
    else:
        padding = 'valid'

    x = layers.Conv2D(num_filter, kernel_size=kernel_size,
                      strides=strides, padding=padding,              # 这里的参数是只l2求和之后所乘上的系数
                      use_bias=not bn, kernel_regularizer=regularizers.l2(5e-4),
                      kernel_initializer=tf.random_normal_initializer(stddev=0.01))(inputs)

    if bn:
        x = layers.BatchNormalization()(x)
        x = layers.LeakyReLU(alpha=0.1)(x)

    return x


def resblock_body(inputs, filters, num_blocks, all_narrow=True):
    preconv1 = layers.ZeroPadding2D(((1, 0), (1, 0)))(inputs)
    preconv1 = darknetConv2D_BN_Mish(preconv1, filters, kernel_size=3, strides=(2, 2))

    shortconv = darknetConv2D_BN_Mish(preconv1, filters//2 if all_narrow else filters, kernel_size=1)

    mainconv = darknetConv2D_BN_Mish(preconv1, filters//2 if all_narrow else filters, kernel_size=1)
    for i in range(num_blocks):
        x = darknetConv2D_BN_Mish(mainconv, filters//2, kernel_size=1)
        x = darknetConv2D_BN_Mish(x, filters//2 if all_narrow else filters, kernel_size=3)

        mainconv = layers.Add()([mainconv, x])

    postconv = darknetConv2D_BN_Mish(mainconv, filters//2 if all_narrow else filters, kernel_size=1)
    route = layers.Concatenate()([postconv, shortconv])

    output = darknetConv2D_BN_Mish(route, filters, (1, 1))
    return output


def darknet_body(inputs):
    x = darknetConv2D_BN_Mish(inputs, 32, 3)
    x = resblock_body(x, 64, 1, False)
    x = resblock_body(x, 128, 2)
    x = resblock_body(x, 256, 8)
    x = DropBlock2D(block_size=7, keep_prob=0.9)(x)
    feat_52x52 = x

    x = resblock_body(x, 512, 8)
    x = DropBlock2D(block_size=7, keep_prob=0.9)(x)
    feat_26x26 = x

    x = resblock_body(x, 1024, 4)
    x = DropBlock2D(block_size=7, keep_prob=0.9)(x)
    feat_13x13 = x

    return feat_52x52, feat_26x26, feat_13x13

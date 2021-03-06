# Copyright 2018 The CapsLayer Authors. All Rights Reserved.
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
# ==========================================================================


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import numpy as np
from datasets.dataloader import DataLoader
import tensorflow as tf


class DataLoader(DataLoader):
    def __init__(self, path=None,
                 num_worker=1,
                 one_hot=False,
                 name=None, **kwargs):
        self.height = self.width = 256
        self.channels = 3
        self.num_classes = 1
        self.batched_shapes = {'images': [-1, self.height, self.width, self.channels],
                               'labels': [-1],
                               'attr': [-1, 40]}

        if path is None:
            path = os.path.join('data', 'celeba', "*")
        super(DataLoader, self).__init__(path=path,
                                         num_worker=num_worker,
                                         one_hot=one_hot,
                                         name=name, **kwargs)

    def tfrecorder(self, path):
        return path

    def parser(self, serialized_record):
        features = tf.parse_single_example(serialized_record,
                                           features={'shape': tf.FixedLenFeature([3], tf.int64),
                                                     'data': tf.FixedLenFeature([], tf.string),
                                                     'attr': tf.FixedLenFeature([40], tf.int64),
                                                     'label': tf.FixedLenFeature([1], tf.int64)})
        image = tf.decode_raw(features['data'], tf.uint8)
        label = tf.cast(features['label'], tf.int32)
        attr = tf.cast(features['attr'], tf.float32)

        features = {'images': image, 'labels': label, 'attr': attr}
        return(features)

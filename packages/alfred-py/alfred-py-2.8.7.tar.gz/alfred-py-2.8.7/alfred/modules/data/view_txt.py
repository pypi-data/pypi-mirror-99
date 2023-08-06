#
# Copyright (c) 2020 JinTian.
#
# This file is part of alfred
# (see http://jinfagang.github.io).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
"""

view txt labeled detection data


"""
import os
import sys
import cv2
from glob import glob
import os
import sys
import cv2
from alfred.utils.log import logger as logging


def vis_det_txt(img_root, label_root):
    logging.info('img root: {}, label root: {}'.format(img_root, label_root))
    # auto detection .jpg or .png images
    txt_files = glob(os.path.join(label_root, '*.txt'))
    for txt_f in txt_files:
        img_f = os.path.join(img_root, os.path.basename(txt_f).split('.')[0] + '.jpg')
        if os.path.exists(img_f):
            img = cv2.imread(img_f)
            if os.path.exists(txt_f):
                with open(txt_f) as f:
                    annos = f.readlines()
                    for ann in annos:
                        ann = ann.strip().split(' ')
                        if len(ann) == 5:
                            # not include prob
                            category = ann[0]
                            xmin = int(float(ann[1]))
                            ymin = int(float(ann[2]))
                            xmax = int(float(ann[3]))
                            ymax = int(float(ann[4]))
                            cv2.putText(img, category, (xmin, ymin), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255))
                            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2, 1)
                        elif len(ann) == 6:
                            # include prob
                            category = ann[0]
                            prob = float(ann[1])
                            xmin = int(float(ann[2]))
                            ymin = int(float(ann[3]))
                            xmax = int(float(ann[4]))
                            ymax = int(float(ann[5]))
                            cv2.putText(img, '{} {}'.format(category, prob), (xmin, ymin), 
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255))
                            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2, 1)
                cv2.imshow('txt check', img)
                cv2.waitKey(0)
            else:
                logging.warning('xxxx image: {} not found.'.format(img_f))


if __name__ == "__main__":
    vis_det_txt(sys.argv[1], sys.argv[2])

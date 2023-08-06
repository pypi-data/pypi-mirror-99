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

Simple demo

mother method of all demos


"""
import cv2
import os
import sys
import time
from deprecated import deprecated
from alfred.utils.log import logger as logging


class ImageInferEngine(object):

    def __init__(self, f, is_show=False, record=False):
        """
        run on

        1. single file
        2. video file
        3. webcam
        :param f:
        """
        self.img_ext = ['png', 'jpg', 'jpeg']
        self.video_ext = ['avi', 'mp4']
        self.f = f
        self.is_show = is_show
        self.record = record
        self.crt_cost = 0

        if not f:
            self.mode = 'webcam'
        elif os.path.basename(f).split('.')[-1] in self.img_ext:
            self.mode = 'image'
        elif os.path.basename(f).split('.')[-1] in self.video_ext:
            self.mode = 'video'
        logging.info('[Demo] in {} mode.'.format(self.mode))

    def read_image_file(self, img_f):
        """
        this method should return image read result

        :param img_f:
        :return:
        """
        if self.mode == 'image':
            raise NotImplementedError('read_image_file must be implemented when using image mode ')
        else:
            pass

    @deprecated(reason="This method has been deprecated, using solve_one_image instead")
    def solve_a_image(self, img):
        """
        this method must be implemented to solve a single image

        img must be a numpy array
        then return the detection or segmentation out
        :param img:
        :return:
        """
        raise NotImplementedError('solve_a_image method must be implemented')

    def solve_one_image(self, img):
        """
        this method must be implemented to solve a single image

        img must be a numpy array
        then return the detection or segmentation out
        :param img:
        :return:
        """
        raise NotImplementedError('solve_a_image method must be implemented')

    def vis_result(self, img, net_out):
        """
        this method must be implement to visualize result on image

        :param img
        :param net_out:
        :return:
        """
        raise NotImplementedError('Visualize network output on image')

    def run(self):
        if self.mode == 'image':
            img = self.read_image_file(self.f)
            res = self.solve_a_image(img)
            res_img = self.vis_result(img, res)
            if self.is_show:
                cv2.imshow('result', res_img)
                cv2.waitKey(0)
        elif self.mode == 'video' or self.mode == 'webcam':
            cap = cv2.VideoCapture(self.f)
            if self.record and self.mode == 'video':
                fps = cap.get(cv2.CAP_PROP_FPS)
                size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                save_f = os.path.join(os.path.dirname(self.f), 'result_' + os.path.basename(self.f))
                logging.info('Result video will record into {}'.format(save_f))
                video_writer = cv2.VideoWriter(save_f, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

            while cap.isOpened():
                ok, frame = cap.read()
                if ok:
                    tic = time.time()
                    res = self.solve_a_image(frame)
                    if self.is_show:
                        logging.info('fps: {}'.format(1 / (time.time() - tic)))
                    self.crt_cost = time.time() - tic
                    res_img = self.vis_result(frame, res)
                    if self.record and self.mode == 'video':
                        video_writer.write(res_img)

                    if self.is_show:
                        cv2.imshow('result', res_img)
                        cv2.waitKey(1)
                else:
                    logging.info('Done')
                    exit(0)







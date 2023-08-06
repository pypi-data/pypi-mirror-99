# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
文本分类模型预测

Authors: fubo
Date: 2019/11/28 00:00:00
"""
import sys
import argparse
import json
import torch
from typing import List, Dict
from ...base.common import DeviceSettings
from ...model.doc_classifier import DocClassify as DocClassify_
from ...model.doc_classifier import DocClassifySample
import copy
copy.deepcopy()

class DocClassify(object):
    def __init__(self, model_path: str):
        self.__classifier = DocClassify_(device_settings=DeviceSettings(gpu_idx=-1))
        if self.__classifier.load_released_model(model_path_script=model_path) is False:
            raise ValueError

    def inference(
            self,
            title: str, content: List[str], label: str = None
    ) -> (List[dict], torch.FloatTensor, torch.FloatTensor):
        """
        短文本分类
        :param title:
        :param content:
        :param label:
        :return:
        """
        label = label if label is not None else self.__classifier.labeler.id2tag(0)
        sample = DocClassifySample(title=title, content=content, labels=[label])
        return self.__classifier.inference(data_str=sample.json())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("release_path", type=str, help="Release path of model")
    parser.add_argument("data_path", type=str, help="Release path of model")
    args = parser.parse_args()
    classifier = DocClassify(args.release_path)
    with open(args.data_path, "r") as fp:
        line = "start"
        while line:
            line = fp.readline().strip("\r\n")
            if len(line) == 0:
                break
            data = json.loads(line)
            if "title" not in data:
                print("\t" + line)
                continue

            if "content" not in data:
                print("\t" + line)
                continue
            labels, term_weights, sent_weights = classifier.inference(title=data["title"], content=data["content"])
            print(labels[0]["label"] + "|" + str(labels[0]["score"]) + "\t" + line)


if __name__ == '__main__':
    main()

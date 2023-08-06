# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
Utils

Authors: fubo
Date: 2020/03/11 00:00:00
"""
import os
import requests
import hashlib
import tarfile
import torch

from typing import List
from pydantic import BaseModel
from argparse import ArgumentParser, Namespace

from nlp_nn.base.common import BerType


class Utils(object):
    """ 常用工具 """

    @staticmethod
    def data_sign_sha512(data):
        """
        data 签名
        :param data:
        :return:
        """
        sha512 = hashlib.sha512()
        sha512.update(data.encode("utf-8"))
        return sha512.hexdigest()

    @staticmethod
    def data_sign_md5(data):
        """
        data 签名
        :param data:
        :return:
        """
        md5 = hashlib.md5()
        md5.update(data.encode("utf-8"))
        return md5.hexdigest()

    @staticmethod
    def reciprocal_log_nature_sum(num: int, values: torch.LongTensor) -> float:
        """
        自然数迭代的log倒数和
        num: 序列数量 batch * num
        """
        return float(torch.sum(values / torch.log2(torch.linspace(1, num, steps=num) + 2), dim=0))

    @staticmethod
    def download_model(bert_type: BerType = BerType.LITE_BERT_TINY) -> str:
        """
        下载部署model
        :param bert_type:
        :return:
        """
        base_url = "https://transformer-models.fwh.bcebos.com"
        base_model_path = "/tmp/.nlp_nn_cache"

        model_name = ""
        if bert_type == BerType.LITE_BERT_SMALL:
            model_name = "voidful_albert_chinese_small"

        if bert_type == BerType.LITE_BERT_TINY:
            model_name = "voidful_albert_chinese_tiny"

        if bert_type == BerType.LITE_BERT_LARGE:
            model_name = "voidful_albert_chinese_large"

        if bert_type == BerType.LITE_BERT_XLARGE:
            model_name = "voidful_albert_chinese_xlarge"

        if bert_type == BerType.LITE_BERT_XXLARGE:
            model_name = "voidful_albert_chinese_large"

        if bert_type == BerType.BASE_BERT:
            model_name = "bert-base-chinese"

        if model_name == "":
            return ""

        if not os.path.exists(base_model_path):
            os.mkdir(base_model_path)

        gz_model_name = model_name + ".tar.gz"
        if os.path.exists(base_model_path + os.sep + model_name):
            return base_model_path + os.sep + model_name

        if os.path.exists(base_model_path + os.sep + gz_model_name):
            os.system("rm -rf " + base_model_path + os.sep + gz_model_name)

        try:
            r = requests.get(url=base_url + "/" + gz_model_name)
            with open(base_model_path + os.sep + gz_model_name, "wb") as fp:
                fp.write(r.content)

            with tarfile.open(base_model_path + os.sep + gz_model_name) as tar:
                for name in tar.getnames():
                    tar.extract(name, path=base_model_path)
            os.system("rm -rf " + base_model_path + os.sep + gz_model_name)
        except Exception as exp:
            raise exp
        return base_model_path + os.sep + model_name

    @staticmethod
    def split_sentence(section: str) -> List[str]:
        """
        分句
        :param section:
        :return:
        """
        section = section.strip("\r\n\t").strip(" ")
        for sign in ["。", "！", "？", "?"]:
            section = section.replace(sign, sign + "\n")
        return section.strip("\n").split("\n")

    @staticmethod
    def create_cmd_params(params: List[BaseModel]) -> Namespace:
        """
        参数结构体转参数命令行
        :param params:
        :return:
        """
        parser = ArgumentParser()
        if len(params) == 0:
            return parser.parse_args()

        for settings in params:
            for name in settings.__dict__:
                if "_" in name and name.index("_") == 0:
                    continue
                parser.add_argument(
                    "--" + name,
                    type=type(settings.__dict__[name]),
                    help=" ".join(name.split("_")),
                    default=settings.__dict__[name],
                    required=False
                )
        return parser.parse_args()
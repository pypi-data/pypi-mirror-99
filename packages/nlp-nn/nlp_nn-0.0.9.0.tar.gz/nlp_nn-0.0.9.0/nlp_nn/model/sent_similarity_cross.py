# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
文本相似度模型

Authors: fubo
Date: 2020/03/11 00:00:00
"""

import json
import os
import copy
import logging
from typing import List, Dict

import torch
import torch.jit
from torch.utils.data import Dataset, DataLoader

from ..base.abstract import AbstractModelApp, AbstractDataSet
from ..base.common import ModelDataType, BerType, ModelState, Const
from ..base.common import CoachSettings, ModelSettings, DeviceSettings, ExportModelSettings
from ..base.model import SentSimilarityCrossModel
from ..base.model_data import SentClassifySample
from ..base.tokenizer import BertTokenizer, AbstractTokenizer


class SentSimilarityModelSettings(ModelSettings):
    """ 模型配置 """

    # 注意力向量维度
    attention_vector_size: int = 0

    # 最大tokens长度
    max_tokens: int = 0


class SentSimilarityCoachSettings(CoachSettings):
    """ 训练参数配置 """
    pass


class SentSimilarityExportedModelSettings(ExportModelSettings):
    """ Query相似模型导出模型配置 """

    # 最大tokens长度
    max_tokens: int = 0


class SentSimilarityDataSet(AbstractDataSet):
    """
    文本相关性计算数据集管理
    {"queries": ["query1", "query2"], "labels": []}
    """

    def __init__(self, tokenizer: AbstractTokenizer):
        super().__init__()
        self.__tokenizer = tokenizer

    def parse_sample(self, line: str) -> Dict:
        """
        解析样本数据
        :param line:
        :return:
        """
        sample = SentClassifySample.parse_raw(line)
        if len(sample.queries) != 2:
            logging.warning("Not enough queries %s" % line)
            return {}
        if len(sample.labels) < 1:
            logging.warning("Error label %s" % line)
            return {}
        label_idx = int(sample.labels[0])
        if label_idx < 0:
            logging.warning("Error format of line %s" % line)
            return {}

        query1_tokens = self.__tokenizer.tokenize(sample.queries[0])
        query2_tokens = self.__tokenizer.tokenize(sample.queries[1])
        output = {
            "label": label_idx,
            "query1": copy.deepcopy(query1_tokens.padding_tokens),
            "query2": copy.deepcopy(query2_tokens.padding_tokens)
        }
        return output

    def __getitem__(self, index):
        return self.data[index]["label"], self.data[index]["query1"], self.data[index]["query2"]

    def __len__(self):
        return len(self.data)

    @staticmethod
    def collate_fn(batch):
        """
        数据封装
        :param batch: 数据batch
        :return:
        """
        label, tokens1, tokens2 = zip(*batch)
        return torch.LongTensor(list(label)), torch.LongTensor(tokens1), torch.LongTensor(tokens2)


class SentSimilarity(AbstractModelApp):
    """ 短文本相似度 """

    def __init__(
            self, device_settings: DeviceSettings,
            coach_settings: SentSimilarityCoachSettings = SentSimilarityCoachSettings(),
            model_settings: SentSimilarityModelSettings = SentSimilarityModelSettings(),
            export_settings: SentSimilarityExportedModelSettings = SentSimilarityExportedModelSettings()
    ):
        super().__init__(device_settings, coach_settings, model_settings, export_settings)
        self.device_settings = device_settings
        self.model_settings = model_settings
        self.coach_settings = coach_settings
        self.export_settings = export_settings
        self.tokenizer = AbstractTokenizer()

    def load_third_dict(self) -> bool:
        # 加载分词
        self.tokenizer = BertTokenizer(
            max_sent_len=self.model_settings.max_tokens,
            bert_type=BerType.LITE_BERT_TINY
        )
        return True

    def define_data_pipe(self) -> Dataset:
        """ 创建数据集计算pipe """
        return SentSimilarityDataSet(tokenizer=self.tokenizer)

    def define_model(self) -> bool:
        """
        定义模型
        :return: bool
        """
        self.model = SentSimilarityCrossModel(
            attention_vector_size=self.model_settings.attention_vector_size,
            max_tokens=self.model_settings.max_tokens
        )
        return True

    def load_model_ckpt(self, model_path_ckpt) -> bool:
        """
        加载ckpt模型
        :param model_path_ckpt:
        :return:
        """
        # 模型配置文件
        config_file = model_path_ckpt + "/" + self.coach_settings.model_conf_file
        with open(config_file, "r") as fp:
            config_data = json.load(fp)
        self.coach_settings = SentSimilarityCoachSettings.parse_obj(config_data["coach_settings"])
        self.model_settings = SentSimilarityModelSettings.parse_obj(config_data["model_settings"])

        # 加载模型文件
        model_file = model_path_ckpt + "/" + self.coach_settings.model_file
        if self.define_model() is False:
            logging.error("Failed to define sent_similarity_cross_model")
            return False
        try:
            self.model.load_state_dict(torch.load(model_file, map_location=torch.device("cpu")))
        except Exception as exp:
            logging.error("load sent_similarity_cross_model params failed %s" % exp)
            return False

        return True

    def create_loss_optimizer(self) -> bool:
        """
        创建loss function和optimizer
        :return: bool
        """
        self.loss_func = torch.nn.NLLLoss()
        self.optimizer = torch.optim.Adam(
            self.get_model_params(),
            lr=self.coach_settings.lr, weight_decay=self.coach_settings.lr_weight_decay
        )
        return True

    def stop_criteria(self) -> (bool, int):
        """
        停止训练条件，如果不重载，则默认训练最长次数
        :return: bool, int
        """
        return False, -1

    def show_network_tf(self) -> bool:
        """
        在tensor board上画出network
        不实现函数则不画出网络图
        :return: bool
        """
        self.set_model_state(ModelState.INFERENCE)
        x_token1, x_token2 = self.model.get_dummy_input()
        x_token1, x_token2 = self.set_tensor_gpu(x_token1), self.set_tensor_gpu(x_token2)
        self.tb_logger.add_graph(self.model, (x_token1, x_token2))
        self.set_model_state(ModelState.TRAIN)
        return True

    def batch_forward(self, params: List[torch.Tensor]):
        """
        一个batch forward计算
        :return:
        """
        x1, x2, y = params[0], params[1], params[2]
        y_ = self.model(x1, x2)
        return self.loss_func(y_, y)

    def release_model(self, model_path_ckpt: str, model_path_script: str) -> bool:
        """
        发布模型（TorchScript模型）
        :param model_path_ckpt ckpt的模型文件夹
        :param model_path_script torch script模型文件夹
        :return:
        """
        os.system("rm -rf %s" % model_path_script)
        os.system("mkdir -p %s" % model_path_script)

        # 生成模型配置清单
        export_model_settings = SentSimilarityExportedModelSettings(
            model_config_file="config.json",
            model_file="sent_similarity_cross_model.pt",
            third_dict_dir="dict",
            max_tokens=self.model_settings.max_tokens
        )
        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file
        config_file = model_path_script + "/" + export_model_settings.model_config_file
        try:
            with open(config_file, "w") as fp:
                fp.write(export_model_settings.json())
        except Exception as ex:
            logging.error("Failed to save sent_similarity_cross_model.config %s" % ex)
            return False

        # 打包第三方词典
        os.system("mkdir %s" % dict_path)

        # 生成torch script模型文件
        try:
            self.model.eval()
            dummy_input = self.model.get_dummy_input()
            torch.jit.trace(self.model, dummy_input).save(model_file)
        except Exception as ex:
            logging.error("Failed to export sent_similarity_cross_model %s" % ex)
            return False
        return True

    def load_released_model(self, model_path_script: str) -> bool:
        """
        加载发布的模型及其相关的词典（TorchScript模型）
        :param model_path_script torch script模型文件夹
        :return:
        """
        # 解析model config
        config_file = model_path_script + "/config.json"
        try:
            export_model_settings = SentSimilarityExportedModelSettings.parse_file(path=config_file)
        except Exception as ex:
            logging.error("Failed to load sent_similarity_cross_model config file %s " % ex)
            return False

        model_file = model_path_script + "/" + export_model_settings.model_file

        # 加载模型文件
        # 加载模型文件
        self.model = self.load_released_model_file(model_file=model_file)

        # 加载分词
        self.tokenizer = BertTokenizer(
            max_sent_len=export_model_settings.max_tokens,
            bert_type=BerType.LITE_BERT_TINY
        )

        # 定义data_pipe
        self.data_pipe = SentSimilarityDataSet(tokenizer=self.tokenizer)

        return True

    def inference(self, query1: str, query2: str) -> float:
        """
        inference 接口
        :param query1:
        :param query2:
        :return:
        """
        query1_tokens = torch.LongTensor([self.tokenizer.tokenize(query1).padding_tokens])
        query2_tokens = torch.LongTensor([self.tokenizer.tokenize(query2).padding_tokens])
        output = self.model(query1_tokens, query2_tokens)
        max_value = float(torch.max(torch.exp(output)))
        if int(torch.argmax(output)) == 1:
            return max_value
        return 1 - max_value

    def base_encode(self, queries: List[str]) -> torch.FloatTensor:
        """
        sentence encoding
        :param queries:
        :return:
        """
        tokens = torch.LongTensor([self.tokenizer.tokenize(query).padding_tokens for query in queries])
        tokens = self.set_tensor_gpu(tokens)
        y = self.model.sent_base_encoding(tokens)
        y = self.set_tensor_cpu(y)
        return y

    def base_encode_similarity(self, tokens1: torch.FloatTensor, tokens2: torch.FloatTensor) -> float:
        """

        """
        tokens1 = self.set_tensor_gpu(tokens1)
        tokens2 = self.set_tensor_gpu(tokens2)
        output = self.model.run_similarity_base_encoding(tokens1, tokens2)
        max_value = float(torch.max(torch.exp(output)))
        if int(torch.argmax(output)) == 1:
            return max_value
        return 1 - max_value

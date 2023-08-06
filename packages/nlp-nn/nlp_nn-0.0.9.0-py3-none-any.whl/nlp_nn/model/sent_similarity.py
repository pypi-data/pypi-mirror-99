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
from ..base.model import SentSimilarityModel
from ..base.model_data import SentClassifySample
from ..base.tokenizer import BertTokenizer, AbstractTokenizer


class SentSimilarityModelSettings(ModelSettings):
    """ 模型配置 """

    # sentence向量维度
    sent_encode_dim: int = 0

    # 注意力向量维度
    attention_vector_size: int = 0

    # Dropout prob
    drop_out_prob: float = 0.5

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
    {"queries": ["pivot", "positive", "negative"], "labels": []}
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
        if len(sample.queries) != 3:
            logging.warning("Not enough queries %s" % line)
            return {}

        pivot_tokens = self.__tokenizer.tokenize(sample.queries[0])
        positive_tokens = self.__tokenizer.tokenize(sample.queries[1])
        negative_tokens = self.__tokenizer.tokenize(sample.queries[2])
        output = {
            "pivot": copy.deepcopy(pivot_tokens.padding_tokens),
            "positive": copy.deepcopy(positive_tokens.padding_tokens),
            "negative": copy.deepcopy(negative_tokens.padding_tokens)
        }
        return output

    def __getitem__(self, index):
        return self.data[index]["pivot"], self.data[index]["positive"], self.data[index]["negative"]

    def __len__(self):
        return len(self.data)

    @staticmethod
    def collate_fn(batch):
        """
        数据封装
        :param batch: 数据batch
        :return:
        """
        pivot, positive, negative = zip(*batch)
        return torch.LongTensor(pivot), torch.LongTensor(positive), torch.LongTensor(negative)


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
        self.model = SentSimilarityModel(
            sent_encode_dim=self.model_settings.sent_encode_dim,
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
            logging.error("Failed to define sent_similarity_model")
            return False
        try:
            self.model.load_state_dict(torch.load(model_file, map_location=torch.device("cpu")))
        except Exception as exp:
            logging.error("load sent_similarity_model params failed %s" % exp)
            return False

        return True

    def create_loss_optimizer(self) -> bool:
        """
        创建loss function和optimizer
        :return: bool
        """
        self.loss_func = torch.nn.TripletMarginLoss()
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
        x_pivot, x_positive, x_negative = self.model.get_dummy_input()
        x_pivot = self.set_tensor_gpu(x_pivot)
        x_positive = self.set_tensor_gpu(x_positive)
        x_negative = self.set_tensor_gpu(x_negative)
        self.tb_logger.add_graph(self.model, (x_pivot, x_positive, x_negative))
        self.set_model_state(ModelState.TRAIN)
        return True

    def batch_forward(self, params: List[torch.Tensor]):
        """
        一个batch forward计算
        :return:
        """
        x1, x2, x3 = params[0], params[1], params[2]
        y1, y2, y3, _, _, _ = self.model(x1, x2, x3)
        return self.loss_func(y1, y2, y3)

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
            model_file="sent_similarity_model.pt",
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
            logging.error("Failed to save sent_similarity_model.config %s" % ex)
            return False

        # 打包第三方词典
        os.system("mkdir %s" % dict_path)

        # 生成torch script模型文件
        try:
            self.model.eval()
            dummy_input = self.model.get_dummy_input()
            torch.jit.trace(self.model, dummy_input).save(model_file)
        except Exception as ex:
            logging.error("Failed to export sent_similarity_model %s" % ex)
            return False

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
            logging.error("Failed to load sent_similarity_model config file %s " % ex)
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

    def inference(
            self,
            pivot_query: str, pos_query: str, neg_query: str
    ) -> (
            bool, int,
            torch.FloatTensor, torch.FloatTensor, torch.FloatTensor,
            torch.FloatTensor, torch.FloatTensor, torch.FloatTensor
    ):
        """
        inference 接口
        :param pivot_query:
        :param pos_query:
        :param neg_query:
        :return:
        """
        pivot_tokens = torch.LongTensor([self.tokenizer.tokenize(pivot_query).padding_tokens])
        positive_tokens = torch.LongTensor([self.tokenizer.tokenize(pos_query).padding_tokens])
        negative_tokens = torch.LongTensor([self.tokenizer.tokenize(neg_query).padding_tokens])
        pivot_tokens = self.set_tensor_gpu(pivot_tokens)
        positive_tokens = self.set_tensor_gpu(positive_tokens)
        negative_tokens = self.set_tensor_gpu(negative_tokens)
        y_pivot, y_pos, y_neg, y_pivot_attention_value, y_pos_attention_value, y_neg_attention_value = self.model(
            pivot_tokens, positive_tokens, negative_tokens
        )
        score1 = torch.cosine_similarity(y_pivot, y_pos)
        score2 = torch.cosine_similarity(y_pivot, y_neg)
        y_pivot = self.set_tensor_cpu(y_pivot)
        y_pos = self.set_tensor_cpu(y_pos)
        y_neg = self.set_tensor_cpu(y_neg)
        y_pivot_attention_value = self.set_tensor_cpu(y_pivot_attention_value)
        y_pos_attention_value = self.set_tensor_cpu(y_pos_attention_value)
        y_neg_attention_value = self.set_tensor_cpu(y_neg_attention_value)
        flag = 1 if score1 > score2 else 0
        return True, flag, y_pivot, y_pos, y_neg, y_pivot_attention_value, y_pos_attention_value, y_neg_attention_value

    def sent_encode(self, query: str) -> (torch.FloatTensor, torch.FloatTensor):
        """
        sentence encoding
        :param query:
        :return:
        """
        placeholder = self.tokenizer.tokenize("0").padding_tokens
        pivot_tokens = torch.LongTensor([self.tokenizer.tokenize(query).padding_tokens])
        positive_tokens = torch.LongTensor([placeholder])
        negative_tokens = torch.LongTensor([placeholder])

        pivot_tokens = self.set_tensor_gpu(pivot_tokens)
        positive_tokens = self.set_tensor_gpu(positive_tokens)
        negative_tokens = self.set_tensor_gpu(negative_tokens)

        y_pivot, _, _, y_pivot_attention_value, _, _ = self.model(pivot_tokens, positive_tokens, negative_tokens)
        y_pivot = self.set_tensor_cpu(y_pivot)
        y_pivot_attention_value = self.set_tensor_cpu(y_pivot_attention_value)
        return y_pivot, y_pivot_attention_value

    def sent_encode_batch(self, queries: List[str]) -> torch.FloatTensor:
        """
        sentence encoding
        :param queries:
        :return:
        """
        queries_count = len(queries)
        queries = queries + (["0"] * (3 - (queries_count % 3)) if queries_count % 3 > 0 else [])
        tokens = [self.tokenizer.tokenize(query).padding_tokens for query in queries]
        pos = int(len(tokens) / 3)
        pivot_tokens = torch.LongTensor(tokens[:pos])
        positive_tokens = torch.LongTensor(tokens[pos:2 * pos])
        negative_tokens = torch.LongTensor(tokens[2 * pos:])

        pivot_tokens = self.set_tensor_gpu(pivot_tokens)
        positive_tokens = self.set_tensor_gpu(positive_tokens)
        negative_tokens = self.set_tensor_gpu(negative_tokens)
        y_pivot, y_pos, y_neg, _, _, _ = self.model(pivot_tokens, positive_tokens, negative_tokens)
        y = torch.cat([y_pivot, y_pos, y_neg])[:queries_count, :]
        y = self.set_tensor_cpu(y)
        return y

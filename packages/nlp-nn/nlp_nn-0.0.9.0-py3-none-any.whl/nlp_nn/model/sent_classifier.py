# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
文本分类模型

Authors: fubo01
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
from ..base.model import SentClassifyModel
from ..base.model_dict import TagsDict, AbstractTagger
from ..base.model_data import SentClassifySample
from ..base.tokenizer import BertTokenizer, AbstractTokenizer


class SentClassifyModelSettings(ModelSettings):
    """ 文本分类模型配置 """

    # sentence向量维度
    sent_encode_dim: int = 0

    # 注意力向量维度
    attention_vector_size: int = 0

    # 类别数量
    class_count: int = 0

    # Dropout prob
    drop_out_prob: float = 0.5

    # 最大tokens长度
    max_tokens: int = 0


class SentClassifyCoachSettings(CoachSettings):
    """ 文本分类训练参数配置 """

    # 分类类别词典
    class_label: str = ""


class SentClassifyExportedModelSettings(ExportModelSettings):
    """ 文本分类模型导出模型配置 """

    # 分类类别词典
    class_label: str = ""

    # 最大tokens长度
    max_tokens: int = 0


class SentClassifyDataSet(AbstractDataSet):
    """
    文本分类问题数据格式
    {"queries": [""], "labels": [""]}
    """

    def __init__(self, labels: AbstractTagger, tokenizer: AbstractTokenizer):
        super().__init__()
        self.__labels = labels
        self.__tokenizer = tokenizer

    def get_label_size(self):
        """
        获取label的数量
        :return:
        """
        return self.__labels.get_size()

    def parse_sample(self, line: str) -> Dict:
        """
        解析json格式的sample数据
        :param line:
        :return:
        """
        output = {"data": [], "label": -1}
        sample = SentClassifySample.parse_raw(line)
        if len(sample.labels) < 1:
            logging.warning("Error labels %s" % line)
            return {}
        if len(sample.queries) < 1:
            logging.warning("Error queries %s" % line)
            return {}

        label_idx = self.__labels.tag2id(sample.labels[0])
        tokens = self.__tokenizer.tokenize(sample.queries[0])

        if sample.queries[0] == "" or len(tokens.padding_tokens) == 0:
            logging.warning("Error format of line %s" % line)
            return {}

        if label_idx < 0:
            logging.warning("Error format of line %s" % line)
            return {}

        output["data"] = copy.deepcopy(tokens.padding_tokens)
        output["label"] = label_idx
        return output

    def __getitem__(self, index):
        return self.data[index]["label"], self.data[index]["data"]

    def __len__(self):
        return len(self.data)

    @staticmethod
    def collate_fn(batch):
        """
        数据封装
        :param batch: 数据batch
        :return:
        """
        label, data = zip(*batch)
        return torch.LongTensor(list(label)), torch.LongTensor(data)


class SentClassify(AbstractModelApp):
    """ 文本分类 """

    def __init__(
            self, device_settings: DeviceSettings,
            coach_settings: SentClassifyCoachSettings = SentClassifyCoachSettings(),
            model_settings: SentClassifyModelSettings = SentClassifyModelSettings(),
            export_settings: SentClassifyExportedModelSettings = SentClassifyExportedModelSettings()
    ):
        super().__init__(device_settings, coach_settings, model_settings, export_settings)
        self.device_settings = device_settings
        self.model_settings = model_settings
        self.coach_settings = coach_settings
        self.export_settings = export_settings
        self.labeler = AbstractTagger()
        self.tokenizer = AbstractTokenizer()

    def load_third_dict(self) -> bool:
        # 加载类别词典
        self.labeler = TagsDict(tags_file=self.coach_settings.dict_dir + "/" + self.coach_settings.class_label)
        self.model_settings.class_count = self.labeler.get_size()

        # 加载分词
        self.tokenizer = BertTokenizer(
            max_sent_len=self.model_settings.max_tokens,
            bert_type=BerType.LITE_BERT_TINY
        )
        return True

    def define_data_pipe(self) -> Dataset:
        """ 创建数据集计算pipe """
        return SentClassifyDataSet(labels=self.labeler, tokenizer=self.tokenizer)

    def define_model(self) -> bool:
        """
        定义模型
        :return: bool
        """
        self.model = SentClassifyModel(
            sent_encode_dim=self.model_settings.sent_encode_dim,
            attention_vector_size=self.model_settings.attention_vector_size,
            class_count=self.model_settings.class_count,
            dropout_prob=self.model_settings.drop_out_prob,
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
        self.coach_settings = SentClassifyCoachSettings.parse_obj(config_data["coach_settings"])
        self.model_settings = SentClassifyModelSettings.parse_obj(config_data["model_settings"])

        # 加载模型文件
        model_file = model_path_ckpt + "/" + self.coach_settings.model_file
        if self.define_model() is False:
            logging.error("Failed to define sent_classify_model")
            return False
        try:
            self.model.load_state_dict(torch.load(model_file, map_location=torch.device("cpu")))
        except Exception as exp:
            logging.error("load sent_classify_model params failed %s" % exp)
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
        dummy_input = self.set_tensor_gpu(self.model.get_dummy_input())
        self.tb_logger.add_graph(self.model, dummy_input)
        self.set_model_state(ModelState.TRAIN)
        return True

    def batch_forward(self, params: List[torch.Tensor]):
        """
        一个batch forward计算
        :return:
        """
        y, x = params[0], params[1]
        y_, _ = self.model(x)
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
        export_model_settings = SentClassifyExportedModelSettings(
            model_config_file="config.json",
            model_file="model.pt",
            third_dict_dir="dict",
            class_label=self.coach_settings.class_label,
            max_tokens=self.model_settings.max_tokens
        )
        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file
        config_file = model_path_script + "/" + export_model_settings.model_config_file
        try:
            with open(config_file, "w") as fp:
                fp.write(export_model_settings.json())
        except Exception as ex:
            logging.error("Failed to save sent_classify_model.config %s" % ex)
            return False

        # 打包第三方词典
        os.system("mkdir %s" % dict_path)
        os.system("cp -rf %s %s/" % (self.coach_settings.dict_dir + "/" + self.coach_settings.class_label, dict_path))

        # 生成torch script模型文件
        try:
            self.model.eval()
            dummy_input = self.model.get_dummy_input()
            torch.jit.trace(self.model, dummy_input).save(model_file)
        except Exception as ex:
            logging.error("Failed to export sent_classify_model %s" % ex)
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
            export_model_settings = SentClassifyExportedModelSettings.parse_file(path=config_file)
        except Exception as ex:
            logging.error("Failed to load sent_classify_model config file %s " % ex)
            return False

        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file
        class_label = dict_path + "/" + export_model_settings.class_label

        # 加载模型文件
        self.model = self.load_released_model_file(model_file=model_file)

        # 读取分类词典
        self.labeler = TagsDict(tags_file=class_label)

        # 加载分词
        self.tokenizer = BertTokenizer(
            max_sent_len=export_model_settings.max_tokens,
            bert_type=BerType.LITE_BERT_TINY
        )

        # 定义data_pipe
        self.data_pipe = SentClassifyDataSet(labels=self.labeler, tokenizer=self.tokenizer)

        return True

    def inference(self, query: str) -> (List[dict], torch.FloatTensor):
        """
        inference 接口
        :param query:
        :return:
        """
        data_str = json.dumps({"queries": [query], "labels": [self.labeler.id2tag(0)]})
        if self.data_pipe is None:
            logging.error("No valid data pipe")
            return []
        data = self.data_pipe.parse_sample(data_str)
        scores, attention_value = self.model(self.set_tensor_gpu(torch.LongTensor([data["data"]])))
        scores = torch.exp(scores).tolist()[0]
        results = [{"label_idx": i, "label": self.labeler.id2tag(i), "score": score} for i, score in enumerate(scores)]
        return sorted(results, key=lambda elem: elem["score"], reverse=True), attention_value

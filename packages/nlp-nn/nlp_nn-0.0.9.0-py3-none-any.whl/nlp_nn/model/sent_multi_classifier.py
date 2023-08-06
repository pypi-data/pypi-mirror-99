# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
Tagging模型

Authors: fubo01
Date: 2020/03/11 00:00:00
"""

import json
import os
import copy
import logging

from typing import Dict, List

import torch
import torch.jit
from torch.utils.data import Dataset, DataLoader

from ..base.abstract import AbstractDataSet, AbstractModelApp
from ..base.common import ModelDataType, BerType, ModelState, Const
from ..base.common import CoachSettings, ModelSettings, DeviceSettings, ExportModelSettings
from ..base.model import SentMultiClassifyModel
from ..base.model_data import SentClassifySample
from ..base.model_dict import TagsDict, AbstractTagger
from ..base.tokenizer import BertTokenizer, AbstractTokenizer
from ..base.metrics import Metric


class SentMultiClassifyModelSettings(ModelSettings):
    """ Tagging模型配置 """

    # tag 类别数量
    tags_count: int = 0

    # Dropout prob
    drop_out_prob: float = 0.5

    # 最大tokens长度
    max_tokens: int = 0


class SentMultiClassifyCoachSettings(CoachSettings):
    """ Tagging训练参数配置 """

    # tag词典文件
    tag_label_dic: str = ""


class SentMultiClassifyExportedModelSettings(ExportModelSettings):
    """ Tagging模型导出模型配置 """

    # tag词典文件
    tag_label_dic: str = ""

    # 最大tokens长度
    max_tokens: int = 0


class SentMultiClassifyDataSet(AbstractDataSet):
    """
    Tagging 数据格式
    {"query": "", "intent_label": "", "entity_labels": [{"label": "", "pos":1, "len": 3}, ...]}
    """

    def __init__(
            self,
            tag_label: AbstractTagger,
            tokenizer: AbstractTokenizer
    ):
        super().__init__()
        self.__tag_label = tag_label
        self.__tokenizer = tokenizer

    def get_tag_label_size(self):
        """
        获取entity label的数量
        :return:
        """
        return self.__tag_label.get_size()

    def parse_sample(self, line: str) -> Dict:
        """
        解析json格式的sample数据
        {"queries": ["query"], "labels": ["label1", "label2", ...]}
        :param line:
        :return:
        """
        output = {
            "data": [],
            "tag_label": [self.__tag_label.tag2id(self.__tag_label.padding_tag)] * self.__tag_label.get_size()
        }

        sample = SentClassifySample.parse_raw(line)
        output["data"] = copy.deepcopy(self.__tokenizer.tokenize(sample.queries[0]).padding_tokens)
        for index, tag in enumerate(sample.labels):
            tag_idx = self.__tag_label.tag2id(tag)
            output["tag_label"][tag_idx] = 1

        return output

    def __getitem__(self, index):
        return self.data[index]["data"], self.data[index]["tag_label"]

    def __len__(self):
        return len(self.data)

    @staticmethod
    def collate_fn(batch):
        """
        数据封装
        :param batch: 数据batch
        :return:
        """
        data, tag_label = zip(*batch)
        return torch.LongTensor(data), torch.LongTensor(tag_label)


class SentMultiClassify(AbstractModelApp):
    """ Tagging """

    def __init__(
            self, device_settings: DeviceSettings,
            coach_settings: SentMultiClassifyCoachSettings = SentMultiClassifyCoachSettings(),
            model_settings: SentMultiClassifyModelSettings = SentMultiClassifyModelSettings(),
            export_settings: SentMultiClassifyExportedModelSettings = SentMultiClassifyExportedModelSettings()
    ):
        super().__init__(device_settings, coach_settings, model_settings, export_settings)
        self.device_settings = device_settings
        self.model_settings = model_settings
        self.coach_settings = coach_settings
        self.export_settings = export_settings
        self.tag_labeler = AbstractTagger()
        self.tokenizer = AbstractTokenizer()

    def load_third_dict(self) -> bool:

        # 加载外部entity类别词典
        self.tag_labeler = TagsDict(
            tags_file=self.coach_settings.dict_dir + "/" + self.coach_settings.tag_label_dic,
            need_padding_tag=True
        )
        self.model_settings.tags_count = self.tag_labeler.get_size()

        # 加载分词
        self.tokenizer = BertTokenizer(
            max_sent_len=self.model_settings.max_tokens,
            bert_type=BerType.LITE_BERT_TINY
        )
        return True

    def define_data_pipe(self) -> Dataset:
        """ 创建数据集计算pipe """
        return SentMultiClassifyDataSet(
            tag_label=self.tag_labeler,
            tokenizer=self.tokenizer
        )

    def define_model(self) -> bool:
        """
        定义模型
        :return: bool
        """
        self.model = SentMultiClassifyModel(
            tags_count=self.model_settings.tags_count,
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
        self.coach_settings = SentMultiClassifyCoachSettings.parse_obj(config_data["coach_settings"])
        self.model_settings = SentMultiClassifyModelSettings.parse_obj(config_data["model_settings"])

        # 加载模型文件
        model_file = model_path_ckpt + "/" + self.coach_settings.model_file
        if self.define_model() is False:
            logging.error("Failed to define tagging_model")
            return False
        try:
            self.model.load_state_dict(torch.load(model_file, map_location=torch.device("cpu")))
        except Exception as exp:
            logging.error("load tagging_model params failed %s" % exp)
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
            lr=self.coach_settings.lr,
            weight_decay=self.coach_settings.lr_weight_decay
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
        y_ = self.model(x)
        y_ = torch.transpose(y_, dim0=2, dim1=1)
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
        export_model_settings = SentMultiClassifyExportedModelSettings(
            model_config_file="config.json",
            model_file="tagging.pt",
            third_dict_dir="dict",
            tag_label_dic=self.coach_settings.tag_label_dic,
            max_tokens=self.model_settings.max_tokens
        )
        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file
        config_file = model_path_script + "/" + export_model_settings.model_config_file
        try:
            with open(config_file, "w") as fp:
                fp.write(export_model_settings.json())
        except Exception as ex:
            logging.error("Failed to save tagging_model.config %s" % ex)
            return False

        # 打包第三方词典
        os.system("mkdir %s" % dict_path)
        os.system(
            "cp -rf %s %s/" % (
                self.coach_settings.dict_dir + "/" + self.coach_settings.tag_label_dic, dict_path
            )
        )

        # 生成torch script模型文件
        try:
            self.model.eval()
            dummy_input = self.model.get_dummy_input()
            torch.jit.trace(self.model, dummy_input).save(model_file)
        except Exception as ex:
            logging.error("Failed to export tagging_model %s" % ex)
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
            export_model_settings = SentMultiClassifyExportedModelSettings.parse_file(path=config_file)
        except Exception as ex:
            logging.error("Failed to load tagging_model config file %s " % ex)
            return False

        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file
        tag_label_dic = dict_path + "/" + export_model_settings.tag_label_dic

        # 加载模型文件
        # 加载模型文件
        self.model = self.load_released_model_file(model_file=model_file)

        # 读取tags词典
        self.tag_labeler = TagsDict(tags_file=tag_label_dic, need_padding_tag=True)

        # 加载分词
        self.tokenizer = BertTokenizer(
            max_sent_len=export_model_settings.max_tokens,
            bert_type=BerType.LITE_BERT_TINY
        )

        # 定义data_pipe
        self.data_pipe = SentMultiClassifyDataSet(
            tag_label=self.tag_labeler,
            tokenizer=self.tokenizer
        )

        return True

    def inference(self, query: str) -> dict:
        """
        inference 接口
        :param query:
        :return:
        """
        tokens = torch.LongTensor([self.tokenizer.tokenize(query=query).padding_tokens])
        tags_result = self.model(self.set_tensor_gpu(tokens))
        tags_idx = torch.argmax(tags_result, dim=2)[0].tolist()

        output = {
            "query": query,
            "tags": []
        }
        for index, elem in enumerate(tags_idx):
            if elem == 0:
                continue
            output["tags"].append(self.tag_labeler.id2tag(index))
        return output

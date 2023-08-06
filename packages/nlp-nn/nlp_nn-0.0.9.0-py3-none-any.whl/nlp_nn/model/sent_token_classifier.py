# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
IntentEntity模型

Authors: fubo01
Date: 2020/03/11 00:00:00
"""

import json
import os
import copy
from typing import Dict, List

import torch
import torch.jit
from torch.utils.data import Dataset, DataLoader
import logging

from ..base.abstract import AbstractModelApp, AbstractDataSet
from ..base.common import ModelDataType, BerType, ModelState, Const
from ..base.common import CoachSettings, ModelSettings, DeviceSettings, ExportModelSettings
from ..base.model import SentTokenClassifyModel
from ..base.model_data import SentTokenSample
from ..base.model_dict import TagsDict, AbstractTagger
from ..base.tokenizer import BertTokenizer, AbstractTokenizer


class SentTokenClassifyModelSettings(ModelSettings):
    """ sent&token模型配置 """

    # intent 类别数量
    sent_class_count: int = 0

    # token 类别数量
    token_class_count: int = 0

    # Dropout prob
    drop_out_prob: float = 0.5

    # 最大tokens长度
    max_tokens: int = 0


class SentTokenClassifyCoachSettings(CoachSettings):
    """ sent&token训练参数配置 """

    # intent词典文件
    sent_class_label_dic: str = ""

    # 内部部token词典文件
    token_class_label_inner_dic: str = ""

    # 外部token词典文件
    token_class_label_dic: str = ""


class SentTokenClassifyExportedModelSettings(ExportModelSettings):
    """ sent&token模型导出模型配置 """

    # intent词典文件
    sent_class_label_dic: str = ""

    # 内部token词典文件
    token_class_label_inner_dic: str = ""

    # 外部token词典文件
    token_class_label_dic: str = ""

    # 最大tokens长度
    max_tokens: int = 0


class SentTokenClassifyDataSet(AbstractDataSet):
    """
    sent&token 数据集
    {"query": "", "sent_label": "", "token_labels": [{"label": "", "pos":1, "len": 3}, ...]}
    """

    def __init__(self, sent_class_label: AbstractTagger, token_class_label: AbstractTagger,
                 token_class_inner_label: AbstractTagger, tokenizer: AbstractTokenizer
                 ):
        super().__init__()
        self.__sent_class_label = sent_class_label
        self.__token_class_label = token_class_label
        self.__token_class_inner_label = token_class_inner_label
        self.__tokenizer = tokenizer

    def get_sent_class_label_size(self):
        """
        sent label的数量
        :return:
        """
        return self.__sent_class_label.get_size()

    def get_token_class_label_size(self):
        """
        token label的数量
        :return:
        """
        return self.__token_class_label.get_size()

    def get_token_class_inner_label_size(self):
        """
        token inner label的数量
        :return:
        """
        return self.__token_class_inner_label.get_size()

    def parse_sample(self, line: str) -> Dict:
        """
        解析json格式的sample数据
        :param line:
        :return:
        """
        output = {"data": []}
        sample = SentTokenSample.parse_raw(line)

        sent_class_label_idx = self.__sent_class_label.tag2id(sample.sent_label)
        if sent_class_label_idx < 0:
            logging.warning("Error format of line %s" % line)
            return {}

        tokens = self.__tokenizer.tokenize(sample.query)
        token_class_label_idx = [self.__token_class_inner_label.tag2id("O")] * self.__tokenizer.max_length

        tokens_str = "|".join([str(elem) for elem in tokens.padding_tokens])
        for pos, elem in enumerate(sample.token_labels):
            term_tokens = self.__tokenizer.tokenize(sample.query[elem.pos:elem.pos + elem.length])
            term_tokens_str = "|".join([str(elem) for elem in term_tokens.tokens])
            if term_tokens_str not in tokens_str:
                logging.warning("Error line intent label %s" % line)
                return {}
            pos = tokens_str.index(term_tokens_str)
            index = tokens_str[:pos].count("|")
            tokens_label = []
            if len(term_tokens.tokens) == 1:
                tokens_label = ["S-" + elem.label]

            if len(term_tokens.tokens) > 1:
                tokens_label_head = ["B-" + elem.label]
                tokens_label_tail = ["E-" + elem.label]
                tokens_label_body = ["I-" + elem.label] * (len(term_tokens.tokens) - 2)
                tokens_label = tokens_label_head + tokens_label_body + tokens_label_tail
            if len(tokens_label) == 0:
                logging.warning("Error line token label %s" % line)
                return {}
            tokens_label_idx = [self.__token_class_inner_label.tag2id(label) for label in tokens_label]
            token_class_label_idx[index:index + len(tokens_label)] = tokens_label_idx

        output["data"] = copy.deepcopy(tokens.padding_tokens)
        output["sent_class_label"] = sent_class_label_idx
        output["token_class_label"] = token_class_label_idx
        return output

    def __getitem__(self, index):
        return self.data[index]["data"], self.data[index]["sent_class_label"], self.data[index]["token_class_label"]

    def __len__(self):
        return len(self.data)

    @staticmethod
    def collate_fn(batch):
        """
        数据封装
        :param batch: 数据batch
        :return:
        """
        data, sent_class_label, token_class_label = zip(*batch)
        data = torch.LongTensor(data)
        sent_class_label = torch.LongTensor(list(sent_class_label))
        token_class_label = torch.LongTensor(list(token_class_label))
        return data, sent_class_label, token_class_label


class SentTokenClassify(AbstractModelApp):
    """ SentToken """

    def __init__(
            self, device_settings: DeviceSettings,
            coach_settings: SentTokenClassifyCoachSettings = SentTokenClassifyCoachSettings(),
            model_settings: SentTokenClassifyModelSettings = SentTokenClassifyModelSettings(),
            export_settings: SentTokenClassifyExportedModelSettings = SentTokenClassifyExportedModelSettings()
    ):
        super().__init__(device_settings, coach_settings, model_settings, export_settings)
        self.device_settings = device_settings
        self.model_settings = model_settings
        self.coach_settings = coach_settings
        self.export_settings = export_settings
        self.sent_class_labeler = AbstractTagger()
        self.token_class_labeler = AbstractTagger()
        self.token_class_inner_labeler = AbstractTagger()
        self.tokenizer = AbstractTokenizer()
        self.loss_sent_class_func = None
        self.loss_token_class_func = None

    def load_third_dict(self) -> bool:
        # 加载intent类别词典
        self.sent_class_labeler = TagsDict(
            tags_file=self.coach_settings.dict_dir + "/" + self.coach_settings.sent_class_label_dic
        )

        # 加载外部entity类别词典
        self.token_class_labeler = TagsDict(
            tags_file=self.coach_settings.dict_dir + "/" + self.coach_settings.token_class_label_dic
        )

        # 加载内部entity类别词典
        self.token_class_inner_labeler = TagsDict(
            tags_file=self.coach_settings.dict_dir + "/" + self.coach_settings.token_class_label_inner_dic
        )
        self.model_settings.sent_class_count = self.sent_class_labeler.get_size()
        self.model_settings.token_class_count = self.token_class_inner_labeler.get_size()

        # 加载分词
        self.tokenizer = BertTokenizer(
            max_sent_len=self.model_settings.max_tokens,
            bert_type=BerType.LITE_BERT_TINY
        )
        return True

    def define_data_pipe(self) -> Dataset:
        """ 创建数据集计算pipe """
        return SentTokenClassifyDataSet(
            sent_class_label=self.sent_class_labeler,
            token_class_label=self.token_class_labeler,
            token_class_inner_label=self.token_class_inner_labeler,
            tokenizer=self.tokenizer
        )

    def define_model(self) -> bool:
        """
        定义模型
        :return: bool
        """
        self.model = SentTokenClassifyModel(
            sent_class_count=self.model_settings.sent_class_count,
            token_class_count=self.model_settings.token_class_count,
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
        self.coach_settings = SentTokenClassifyCoachSettings.parse_obj(config_data["coach_settings"])
        self.model_settings = SentTokenClassifyModelSettings.parse_obj(config_data["model_settings"])

        # 加载模型文件
        model_file = model_path_ckpt + "/" + self.coach_settings.model_file
        if self.define_model() is False:
            logging.error("Failed to define sent_token_class_model")
            return False
        try:
            self.model.load_state_dict(torch.load(model_file, map_location=torch.device("cpu")))
        except Exception as exp:
            logging.error("load sent_token_class_model params failed %s" % exp)
            return False

        return True

    def create_loss_optimizer(self) -> bool:
        """
        创建loss function和optimizer
        :return: bool
        """
        self.loss_sent_class_func = torch.nn.NLLLoss()
        self.loss_token_class_func = torch.nn.NLLLoss()
        self.loss_func = torch.nn.NLLLoss()  # 未使用的loss function
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
        x, y1, y2 = params[0], params[1], params[2]
        y1_, y2_ = self.model(x)
        y2_ = torch.transpose(y2_, dim0=2, dim1=1)
        return self.loss_sent_class_func(y1_, y1) + self.loss_token_class_func(y2_, y2)

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
        export_model_settings = SentTokenClassifyExportedModelSettings(
            model_config_file="config.json",
            model_file="model.pt",
            third_dict_dir="dict",
            sent_class_label_dic=self.coach_settings.sent_class_label_dic,
            token_class_label_inner_dic=self.coach_settings.token_class_label_inner_dic,
            token_class_label_dic=self.coach_settings.token_class_label_dic,
            max_tokens=self.model_settings.max_tokens
        )
        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file
        config_file = model_path_script + "/" + export_model_settings.model_config_file
        try:
            with open(config_file, "w") as fp:
                fp.write(export_model_settings.json())
        except Exception as ex:
            logging.error("Failed to save sent_token_class_model.config %s" % ex)
            return False

        # 打包第三方词典
        os.system("mkdir %s" % dict_path)
        os.system(
            "cp -rf %s %s/" % (
                self.coach_settings.dict_dir + "/" + self.coach_settings.sent_class_label_dic, dict_path
            )
        )
        os.system(
            "cp -rf %s %s/" % (
                self.coach_settings.dict_dir + "/" + self.coach_settings.token_class_label_dic, dict_path
            )
        )
        os.system(
            "cp -rf %s %s/" % (
                self.coach_settings.dict_dir + "/" + self.coach_settings.token_class_label_inner_dic, dict_path
            )
        )

        # 生成torch script模型文件
        try:
            self.model.eval()
            dummy_input = self.model.get_dummy_input()
            torch.jit.trace(self.model, dummy_input).save(model_file)
        except Exception as ex:
            logging.error("Failed to export sent_token_class_model %s" % ex)
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
            export_model_settings = SentTokenClassifyExportedModelSettings.parse_file(path=config_file)
        except Exception as ex:
            logging.error("Failed to load sent_token_class_model config file %s " % ex)
            return False

        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file
        sent_class_label_dic = dict_path + "/" + export_model_settings.sent_class_label_dic
        token_class_label_dic = dict_path + "/" + export_model_settings.token_class_label_dic
        token_class_label_inner_dic = dict_path + "/" + export_model_settings.token_class_label_inner_dic

        # 加载模型文件
        # 加载模型文件
        self.model = self.load_released_model_file(model_file=model_file)

        # 读取Intent词典
        self.sent_class_labeler = TagsDict(tags_file=sent_class_label_dic)

        # 读取内部entity词典
        self.token_class_inner_labeler = TagsDict(tags_file=token_class_label_inner_dic)

        # 读取外部entity词典
        self.token_class_labeler = TagsDict(tags_file=token_class_label_dic)

        # 加载分词
        self.tokenizer = BertTokenizer(
            max_sent_len=export_model_settings.max_tokens,
            bert_type=BerType.LITE_BERT_TINY
        )

        # 定义datapipe
        self.data_pipe = SentTokenClassifyDataSet(
            sent_class_label=self.sent_class_labeler,
            token_class_label=self.token_class_labeler,
            token_class_inner_label=self.token_class_inner_labeler,
            tokenizer=self.tokenizer
        )

        return True

    def inference(self, query: str) -> dict:
        """
        inference 接口
        :param query:
        :return:
        """
        data_str = SentTokenSample(query=query, sent_label=self.sent_class_labeler.id2tag(0), token_labels=[]).json()
        if self.data_pipe is None:
            logging.error("No valid data pipe")
            return {}
        data = self.data_pipe.parse_sample(data_str)
        tokens = torch.LongTensor([data["data"]])
        tokens = self.set_tensor_gpu(tokens)
        sent_class_result, entity_result = self.model(tokens)
        sent_class_label_idx = int(torch.argmax(sent_class_result, dim=1)[0])
        token_class_labels_idx = torch.argmax(entity_result, dim=2)[0].tolist()

        output = {
            "query": query,
            "sent_class_label": self.sent_class_labeler.id2tag(sent_class_label_idx),
            "token_class_labels": [],
            "tokens": []
        }
        str_tokens = self.tokenizer.convert_ids_to_tokens(data["data"])
        for index, elem in enumerate(token_class_labels_idx):

            token = str_tokens[index]
            label = self.token_class_inner_labeler.id2tag(elem)

            if token == self.tokenizer.padding:
                break
            output["token_class_labels"].append({"token": token, "label": label})
        return output

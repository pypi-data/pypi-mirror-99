# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
篇章文本分类模型

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
from ..base.model import DocClassifyModel
from ..base.model_dict import TagsDict, AbstractTagger
from ..base.model_data import DocClassifySample
from ..base.tokenizer import BertTokenizer, AbstractTokenizer
from ..base.utils import Utils


class DocClassifyModelSettings(ModelSettings):
    """ 篇章文本分类模型配置 """

    # sentence向量维度
    sent_encode_dim: int = 0

    # doc向量维度
    doc_encode_dim: int = 0

    # 注意力向量维度
    attention_vector_size: int = 0

    # 类别数量
    class_count: int = 0

    # Dropout prob
    drop_out_prob: float = 0.5

    # 最大tokens长度
    max_tokens: int = 50

    # 最大句子数量
    max_sentences: int = 15

    # transformer encoder layer size
    sent_transformer_encode_layer_size: int = 6


class DocClassifyCoachSettings(CoachSettings):
    """ 篇章文本分类训练参数配置 """

    # 分类类别词典
    class_label: str = ""


class DocClassifyExportedModelSettings(ExportModelSettings):
    """ 篇章文本分类模型导出模型配置 """

    # 分类类别词典
    class_label: str = ""

    # 最大tokens长度
    max_tokens: int = 0

    # 最大句子数量
    max_sentences: int = 10

    # transformer encoder layer size
    sent_transformer_encode_layer_size: int = 6


class DocClassifyDataSet(AbstractDataSet):
    """
    篇章文本分类问题数据格式
    {"title": "", "content": [""], "labels": [""]}
    """

    def __init__(self, labels: AbstractTagger, tokenizer: AbstractTokenizer, max_sentence: int):
        super().__init__()
        self.__labels = labels
        self.__tokenizer = tokenizer
        self.__max_sentence = max_sentence

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
        output = {"data": [], "mask": [], "label": -1}
        sample = DocClassifySample.parse_raw(line)
        if len(sample.labels) < 1:
            logging.warning("Error labels %s" % line)
            return {}

        label_idx = self.__labels.tag2id(sample.labels[0])
        if label_idx < 0:
            logging.warning("Error format of line %s" % line)
            return {}

        data = []
        mask = []
        all_content = []

        if sample.title != "":
            all_content.append(sample.title)
        all_content = all_content + sample.content

        for sec in all_content:
            for sent in Utils.split_sentence(section=sec):
                if len(sent) == 0:
                    continue
                tk_output = self.__tokenizer.tokenize(sent)
                data.append(copy.deepcopy(tk_output.padding_tokens))
                mask.append(copy.deepcopy(tk_output.mask))

            # 添加段落分隔符
            sec_tokens = self.__tokenizer.tokenize("")
            sec_tokens.padding_tokens[0] = self.__tokenizer.section_segment_idx
            sec_tokens.mask[0] = 1
            data.append(copy.deepcopy(sec_tokens.padding_tokens))
            mask.append(copy.deepcopy(sec_tokens.mask))

        padding_tokens_result = self.__tokenizer.tokenize("")
        data_size = len(data)
        if data_size <= self.__max_sentence:
            data = data + [padding_tokens_result.padding_tokens] * (self.__max_sentence - data_size)
            mask = mask + [padding_tokens_result.padding_tokens] * (self.__max_sentence - data_size)
        else:
            data = data[:self.__max_sentence]
            mask = mask[:self.__max_sentence]

        output["data"] = copy.deepcopy(data)
        output["mask"] = copy.deepcopy(mask)
        output["label"] = label_idx

        return output

    def __getitem__(self, index):
        return self.data[index]["label"], self.data[index]["data"], self.data[index]["mask"]

    def __len__(self):
        return len(self.data)

    @staticmethod
    def collate_fn(batch):
        """
        数据封装
        :param batch: 数据batch
        :return:
        """
        label, data, mask = zip(*batch)
        return torch.LongTensor(list(label)), torch.LongTensor(data), torch.LongTensor(mask)


class DocClassify(AbstractModelApp):
    """ 篇章文本分类 """

    def __init__(
            self, device_settings: DeviceSettings,
            coach_settings: DocClassifyCoachSettings = DocClassifyCoachSettings(),
            model_settings: DocClassifyModelSettings = DocClassifyModelSettings(),
            export_settings: DocClassifyExportedModelSettings = DocClassifyExportedModelSettings()
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
        return DocClassifyDataSet(
            labels=self.labeler, tokenizer=self.tokenizer,
            max_sentence=self.model_settings.max_sentences
        )

    def define_model(self) -> bool:
        """
        定义模型
        :return: bool
        """
        self.model = DocClassifyModel(
            sent_encode_dim=self.model_settings.sent_encode_dim,
            doc_encode_dim=self.model_settings.doc_encode_dim,
            attention_vector_dim=self.model_settings.attention_vector_size,
            max_tokens=self.model_settings.max_tokens,
            max_sentences=self.model_settings.max_sentences,
            class_count=self.model_settings.class_count,
            sent_transformer_encode_layer_size=self.model_settings.sent_transformer_encode_layer_size,
            dropout_prob=self.model_settings.drop_out_prob
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
        self.coach_settings = DocClassifyCoachSettings.parse_obj(config_data["coach_settings"])
        self.model_settings = DocClassifyModelSettings.parse_obj(config_data["model_settings"])

        # 加载模型文件
        model_file = model_path_ckpt + "/" + self.coach_settings.model_file
        if self.define_model() is False:
            logging.error("Failed to define doc_classify_model")
            return False
        try:
            self.model.load_state_dict(torch.load(model_file, map_location=torch.device("cpu")))
        except Exception as exp:
            logging.error("load doc_classify_model params failed %s" % exp)
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
        y, x, mask = params[0], params[1], params[2]
        y_, _, _ = self.model(x, mask)
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
        export_model_settings = DocClassifyExportedModelSettings(
            model_config_file="config.json",
            model_file="model.pt",
            third_dict_dir="dict",
            class_label=self.coach_settings.class_label,
            max_tokens=self.model_settings.max_tokens,
            max_sentences=self.model_settings.max_sentences,
            sent_transformer_encode_layer_size=self.model_settings.sent_transformer_encode_layer_size
        )
        dict_path = model_path_script + "/" + export_model_settings.third_dict_dir
        model_file = model_path_script + "/" + export_model_settings.model_file
        config_file = model_path_script + "/" + export_model_settings.model_config_file
        try:
            with open(config_file, "w") as fp:
                fp.write(export_model_settings.json())
        except Exception as ex:
            logging.error("Failed to save doc_classify_model.config %s" % ex)
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
            logging.error("Failed to export doc_classify_model %s" % ex)
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
            export_model_settings = DocClassifyExportedModelSettings.parse_file(path=config_file)
        except Exception as ex:
            logging.error("Failed to load doc_classify_model config file %s " % ex)
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
        self.data_pipe = DocClassifyDataSet(
            labels=self.labeler, tokenizer=self.tokenizer,
            max_sentence=export_model_settings.max_sentences
        )

        return True

    def inference(self, data_str: str) -> (List[dict], torch.FloatTensor, torch.FloatTensor):
        """
        inference 接口
        :param query:
        :return:
        """
        if self.data_pipe is None:
            logging.error("No valid data pipe")
            return []
        data = self.data_pipe.parse_sample(data_str)
        scores, term_weights, sent_weights = self.model(self.set_tensor_gpu(x=torch.LongTensor([data["data"]])))
        scores = torch.exp(scores).tolist()[0]
        results = [{"label_idx": i, "label": self.labeler.id2tag(i), "score": score} for i, score in enumerate(scores)]
        return sorted(results, key=lambda elem: elem["score"], reverse=True), term_weights, sent_weights

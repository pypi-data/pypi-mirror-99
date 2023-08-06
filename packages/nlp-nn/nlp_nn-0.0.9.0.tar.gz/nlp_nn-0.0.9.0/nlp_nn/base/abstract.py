# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2020 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
接口

Authors: fubo
Date:    2020/02/08 11:23:42
"""

import os
import json
import logging
from abc import ABCMeta, abstractmethod
from typing import Dict, List
import torch
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
from torch.utils.tensorboard import SummaryWriter

from .common import ModelState, CoachSettings, ModelSettings, ModelDataType, DeviceSettings, ExportModelSettings
from .model_data import Tokens
from .common import Const


class AbstractTagger(metaclass=ABCMeta):
    """
    Tag或者label抽象接口
    """

    def __init__(self, need_padding_tag=False):
        self.padding_tag = "[PADDING]"
        self.tags = {}
        self.tags_idx = []
        self.need_padding_tag = need_padding_tag

    def get_size(self) -> int:
        """
        获取dict条目的数量
        :return:
        """
        return len(self.tags)

    def tag2id(self, tag: str) -> int:
        """
        label转ID
        :param tag:
        :return:
        """
        return -1

    def id2tag(self, idx: int) -> str:
        """
        ID转label
        :param idx: label id
        :return:
        """
        return ""


class AbstractTokenizer(metaclass=ABCMeta):
    """
    抽象query序列化接口
    """

    def __init__(self, max_sent_len: int = 0):
        self.max_length = max_sent_len
        self.padding = "<PAD>"
        self.padding_idx = 0
        self.section_segment_idx = 102
        self.section_segment = "[SEP]"

    def convert_ids_to_tokens(self, ids: List[int]) -> List[str]:
        """
        id转化token
        """
        return []

    def tokenize(self, query: str) -> Tokens:
        """
        query序列化
        :param query:
        :return:
        """
        return Tokens(query=query, tokens=[], padding_tokens=[])


class AbstractDataSet(Dataset, metaclass=ABCMeta):
    """ 数据集接口 """

    def __init__(self):
        self.data = []

    def parse_sample(self, line: str) -> Dict:
        """
        解析json数据
        :param line:
        :return:
        """
        pass

    @staticmethod
    def collate_fn(batch):
        """"""
        pass

    def load_data_set(self, data_file: str) -> bool:
        """
        读取数据集文件
        :param data_file: 数据文件
        :return:
        """
        self.data.clear()
        if not os.path.exists(data_file):
            logging.error("No such data set file %s" % data_file)
            return False

        with open(data_file, "r") as fp:
            for line in fp.readlines():
                data = self.parse_sample(line.strip("\r\n"))
                if len(data) == 0:
                    logging.warning("Error when parsing sample json %s" % line.strip("\r\n"))
                    continue
                self.data.append(data.copy())
        return True


class AbstractModel(torch.nn.Module, metaclass=ABCMeta):
    """ 模型接口 """

    def get_dummy_input(self) -> torch.Tensor:
        """
        获取dummy tensor
        :return:
        """
        return torch.zeros(0)


class AbstractModelApp(metaclass=ABCMeta):
    """
    模型应用接口
    """

    @abstractmethod
    def __init__(
            self, device_settings: DeviceSettings,
            coach_settings: CoachSettings = CoachSettings(),
            model_settings: ModelSettings = ModelSettings(),
            export_settings: ExportModelSettings = ExportModelSettings()
    ):
        """
        定义抽象应用模型 common
        :param device_settings: 设备参数
        :param coach_settings: 训练参数
        :param model_settings: 模型参数
        :param export_settings: 导出模型参数
        """
        self.device_settings = device_settings
        self.coach_settings = coach_settings
        self.coach_settings.model_conf_file = "config.json"
        self.model_settings = model_settings
        self.export_settings = export_settings

        # 模型使用的gpu device index
        self.gpu_device_idx = self.device_settings.gpu_idx

        # 模型定义
        self.model = AbstractModel()

        # 模型状态
        self.model_state = ModelState.TRAIN

        # 训练集定义
        self.data_pipe_train = AbstractDataSet()

        # 验证集定义
        self.data_pipe_valid = AbstractDataSet()

        # 在线预测data pipe
        self.data_pipe = AbstractDataSet()

        # loss function
        self.loss_func = None

        # optimizer
        self.optimizer = None

        # 设置tf log
        self.tb_logger = None

        # 是否使用GPU
        self.use_cuda = True if torch.cuda.is_available() and self.device_settings.gpu_idx >= 0 else False

    def __del__(self):
        """
        保存tensorboard 日志 common
        """
        if self.tb_logger is not None:
            self.tb_logger.close()

    def __load_data_set(self, data_pipe: AbstractDataSet, model_data_type: ModelDataType) -> bool:
        """
        加载数据集
        :param data_pipe: 数据处理pipe
        :param model_data_type: 数据类型
        :return:
        """
        if data_pipe is None:
            logging.error("The %s data pipe is None" % model_data_type)
            return False

        data_set_file = ""
        if model_data_type == ModelDataType.TRAIN:
            data_set_file = self.coach_settings.data_dir + "/" + self.coach_settings.train_data_set_file

        if model_data_type == ModelDataType.VALID:
            data_set_file = self.coach_settings.data_dir + "/" + self.coach_settings.valid_data_set_file

        if data_set_file == "":
            logging.error("Error data set name %s" % str(model_data_type))
            return False

        if not data_pipe.load_data_set(data_file=data_set_file):
            logging.error("Failed to load %s data set" % model_data_type)
            return False

        return True

    def __save_model_ckpt(self, epoch):
        """
        保存模型 (TRAIN)
        :param epoch 训练的轮次
        """
        # 创建train_dir
        if not os.path.exists(self.coach_settings.train_models_dir):
            os.mkdir(self.coach_settings.train_models_dir)

        # 创建epoch模型文件夹
        model_path = "/".join(
            [self.coach_settings.train_models_dir, self.model_settings.model_name + "_" + str(epoch)]
        )
        if not os.path.exists(model_path):
            os.mkdir(model_path)

        # 模型文件
        model_file = model_path + "/" + self.coach_settings.model_file

        # 模型配置文件
        config_file = model_path + "/" + self.coach_settings.model_conf_file

        # 第三方词典文件
        dict_path = model_path + "/dict"

        # 生成第三方词典软链
        os.system("ln -s %s %s" % (self.coach_settings.dict_dir, dict_path))

        # 生成配置文件
        config_data = {
            "coach_settings": self.coach_settings.dict(),
            "model_settings": self.model_settings.dict(),
            "epoch": epoch
        }

        # 生成model文件
        try:
            torch.save(self.get_state_dict(), model_file)
            with open(config_file, "w") as fp:
                json.dump(config_data, fp, ensure_ascii=False)
        except Exception as ex:
            logging.error("Failed to save model files epoch=%s %s" % (str(epoch), ex))
            return False

        return True

    @abstractmethod
    def load_model_ckpt(self, model_path_ckpt) -> bool:
        """
        加载ckpt模型
        :param model_path_ckpt:
        :return:
        """
        raise NotImplementedError

    def set_model_gpu(self):
        """
        模型拷贝到GPU中 common
        :return:
        """
        if self.use_cuda is False:
            return False

        try:
            self.model.cuda(device=self.gpu_device_idx)
        except Exception as ex:
            logging.error("Failed to set model to gpu gpu index=%d %s" % (self.device_settings.gpu_idx, ex))
            return False

        return True

    def set_model_cpu(self):
        """
        模型拷贝到CPU中 common
        :return:
        """
        try:
            self.model.cpu()
        except Exception as ex:
            logging.error("Failed to set model to cpu %s" % ex)
            return False

        return True

    def set_tensor_gpu(self, x: torch.Tensor) -> torch.Tensor:
        """
        tensor拷贝到gpu
        :param x:
        :return:
        """
        return x.cuda(device=self.gpu_device_idx) if self.use_cuda else x

    def set_tensor_cpu(self, x: torch.Tensor) -> torch.Tensor:
        """
        Tensor拷贝到cpu
        :param x:
        :return:
        """
        return x.cpu()

    def set_model_state(self, model_state: ModelState):
        """
        设置模型状态 common
        :param model_state:
        :return:
        """
        if self.model_state == model_state:
            return

        if model_state == ModelState.TRAIN:
            self.model.train()
        if model_state == ModelState.INFERENCE:
            self.model.eval()

        self.model_state = model_state
        return

    def get_state_dict(self):
        """
        获取模型的状态参数 common
        :return:
        """
        return self.model.state_dict()

    def get_model_params(self):
        """
        获取模型参数 common
        :return:
        """
        return self.model.parameters()

    def load_released_model_file(self, model_file: str):
        """
        加载released模型文件
        :param model_file:
        :return:
        """
        return torch.jit.load(
            model_file,
            map_location=torch.device(
                'cuda:%d' % self.device_settings.gpu_idx
            ) if self.use_cuda else torch.device(
                'cpu'
            )
        )

    def create_data_loader(self, data_type: ModelDataType= ModelDataType.TRAIN) -> DataLoader:
        """
        为训练/验证创建dataloader
        :param data_type:
        :return:
        """
        data_loader = None
        if data_type == ModelDataType.VALID:
            data_loader = DataLoader(
                self.data_pipe_valid,
                batch_size=self.coach_settings.valid_batch_size,
                shuffle=True,
                collate_fn=self.data_pipe_valid.collate_fn,
            )
        if data_type == ModelDataType.TRAIN:
            data_loader = DataLoader(
                self.data_pipe_train,
                batch_size=self.coach_settings.train_batch_size,
                shuffle=True,
                collate_fn=self.data_pipe_train.collate_fn,
            )
        return data_loader

    def prepare_for_training(self):
        """
        创建训练环境
        :return:
        """
        logging.info("Prepare for model training")
        logging.info("Create TensorBoard logger")
        # 定义tensor board
        if self.coach_settings.tf_log_dir == "":
            self.coach_settings.tf_log_dir = '.'

        self.tb_logger = SummaryWriter(
            self.coach_settings.tf_log_dir,
            comment=self.model_settings.model_name
        )

        logging.info("Load third dicts")
        # 加载第三方词典
        if self.load_third_dict() is False:
            logging.error("Failed to load third dict")
            return False

        logging.info("Define model")
        # 定义模型
        if self.define_model() is False:
            logging.error("Failed to define playground")
            return False

        logging.info("Create training set")
        # 定义训练数据集
        self.data_pipe_train = self.define_data_pipe()
        if self.__load_data_set(data_pipe=self.data_pipe_train, model_data_type=ModelDataType.TRAIN) is False:
            logging.error("Failed to load train data set")
            return False

        logging.info("Create validation set")
        # 定义验证数据集
        self.data_pipe_valid = self.define_data_pipe()
        if self.__load_data_set(data_pipe=self.data_pipe_valid, model_data_type=ModelDataType.VALID) is False:
            logging.error("Failed to load valid data set")
            return False

        # 定义预测的data pipe
        self.data_pipe = self.define_data_pipe()

        logging.info("Define loss function and optimizer")
        # 定义loss function或者optimizer
        if self.create_loss_optimizer() is False:
            logging.error("Failed to create loss function or optimizer")
            return False

        logging.info("Set model state TRAIN")
        self.set_model_state(ModelState.TRAIN)

        if self.use_cuda is True:
            self.set_model_gpu()
        return True

    def validation(self, data_loader: DataLoader) -> float:
        """
        验证当前效果
        :param data_loader:
        :return: average loss
        """
        batch_count = 0
        all_loss = 0.0
        self.set_model_state(model_state=ModelState.INFERENCE)
        for index, params in enumerate(data_loader):
            loss = self.batch_forward(params=list(map(self.set_tensor_gpu, params)))
            all_loss = all_loss + float(loss)
            batch_count = batch_count + 1
        self.set_model_state(model_state=ModelState.TRAIN)
        return (1.0 * all_loss) / (batch_count + Const.MIN_POSITIVE_NUMBER)

    def start_training(self):
        """
        训练接口 (TRAIN)
        :return:
        """
        logging.info("Log model network")
        if self.show_network_tf() is False:
            logging.error("Failed to draw network on tensor board")
            return False

        logging.info("Check dataset")
        # 检查dataset是否准备好
        if self.data_pipe_train is None or self.data_pipe_valid is None:
            logging.error("No sample data for training")
            return False

        logging.info("Check loss function")
        # 检查loss function是否准备好
        if self.loss_func is None:
            logging.error("No loss function has been defined")
            return False

        # 检查优化算子是否准备好
        if self.optimizer is None:
            logging.error("No optimizer has been defined")
            return False

        # 开始训练
        logging.info("Model training start")

        # 设置模型状态为可训练状态
        step = 0
        self.set_model_state(model_state=ModelState.TRAIN)
        for epoch in range(self.coach_settings.max_epoch_times):
            logging.info("Start epoch %d step %d ..." % (epoch, step))
            # 创建训练集和验证集的dataloader
            logging.info("Create dataloader for training and validation")
            data_loader_train = self.create_data_loader(data_type=ModelDataType.TRAIN)
            # data_loader_valid = self.create_data_loader(data_type=ModelDataType.VALID)
            for _, params in enumerate(data_loader_train):
                # 参数是否放入GPU
                loss = self.batch_forward(params=list(map(self.set_tensor_gpu, params)))
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                logging.info("[Batch train] Epoch=%d Step=%d train_loss=%f" % (epoch, step, float(loss)))
                if self.tb_logger:
                    self.tb_logger.add_scalar("TrainBatchLoss", float(loss), step)

                # 经历几个step后进行valid
                if step % self.coach_settings.valid_interval != (self.coach_settings.valid_interval - 1):
                    step = step + 1
                    continue

                # 使用train数据进行验证
                ave_train_loss = self.validation(data_loader=self.create_data_loader(data_type=ModelDataType.TRAIN))
                logging.info(
                    "[Validation] DataType=%s Epoch=%d Step=%d train_loss=%f" % (
                        ModelDataType.TRAIN, epoch, step, float(ave_train_loss)
                    )
                )

                # 使用valid数据进行验证
                ave_valid_loss = self.validation(data_loader=self.create_data_loader(data_type=ModelDataType.VALID))
                logging.info(
                    "[Validation] DataType=%s Epoch=%d Step=%d valid_loss=%f" % (
                        ModelDataType.VALID, epoch, step, float(ave_valid_loss)
                    )
                )
                if self.tb_logger:
                    self.tb_logger.add_scalars(
                        "StepLoss",
                        {
                            "ValidLoss": float(ave_valid_loss),
                            "TrainLoss": float(ave_train_loss)
                        },
                        step
                    )

                # save check point
                if self.__save_model_ckpt(step) is False:
                    logging.error("Failed to save playground at step=%s" % str(step))
                    return False

                # check stop criteria
                is_stop, best_epoch = self.stop_criteria()
                if is_stop is True:
                    logging.info("Stop training, The Best Model is %d" % best_epoch)
                    break

                step = step + 1
        return True

    @abstractmethod
    def load_third_dict(self) -> bool:
        """
        加载第三方资源
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def release_model(self, model_path_ckpt: str, model_path_script: str) -> bool:
        """
        发布模型（TorchScript模型）
        :param model_path_ckpt ckpt的模型文件夹
        :param model_path_script torch script模型文件夹
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def load_released_model(self, model_path_script: str) -> bool:
        """
        加载发布的模型及其相关的词典（TorchScript模型）
        :param model_path_script torch script模型文件夹
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def define_data_pipe(self) -> AbstractDataSet:
        """
        定义数据pipe
        :return: bool
        """
        raise NotImplementedError

    @abstractmethod
    def define_model(self) -> bool:
        """
        定义模型
        :return: bool
        """
        raise NotImplementedError

    @abstractmethod
    def create_loss_optimizer(self) -> bool:
        """
        创建loss function和optimizer
        :return: bool
        """
        raise NotImplementedError

    @abstractmethod
    def stop_criteria(self) -> (bool, int):
        """
        停止训练条件，如果不重载，则默认训练最长次数
        :return: bool, int
        """
        return False, -1

    @abstractmethod
    def batch_forward(self, params: List[torch.Tensor]):
        """
        一个batch forward计算
        :return:
        """
        raise NotImplementedError

    # @abstractmethod
    # def epoch_train(self) -> bool:
    #     """
    #     使用训练数据进行一个epoch的训练
    #     :return: bool
    #     """
    #     raise NotImplementedError

    @abstractmethod
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

    @abstractmethod
    def inference(self, *args):
        """
        inference 接口
        :param args:
        :return:
        """
        raise NotImplementedError

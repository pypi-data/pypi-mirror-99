# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
文本分类模型训练

Authors: fubo
Date: 2019/11/28 00:00:00
"""

import sys
import logging
from ...model.sent_classifier import SentClassifyModelSettings, SentClassifyCoachSettings, DeviceSettings
from ...model.sent_classifier import SentClassify
from ...base.utils import Utils


def main():
    log_format_string = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format_string, stream=sys.stderr)
    args = Utils.create_cmd_params([SentClassifyCoachSettings(), SentClassifyModelSettings(), DeviceSettings()])
    device_settings = DeviceSettings(gpu_idx=args.gpu_idx)
    coach_settings = SentClassifyCoachSettings(
        tf_log_dir=args.tf_log_dir,
        train_models_dir=args.train_models_dir,
        dict_dir=args.dict_dir,
        data_dir=args.data_dir,
        model_file=args.model_file,
        class_label=args.class_label,
        train_data_set_file=args.train_data_set_file,
        valid_data_set_file=args.valid_data_set_file,
        train_batch_size=args.train_batch_size,
        valid_batch_size=args.valid_batch_size,
        lr=args.lr,
        lr_weight_decay=args.lr_weight_decay,
        valid_interval=args.valid_interval
    )
    model_settings = SentClassifyModelSettings(
        model_name=args.model_name,
        model_describe=args.model_describe,
        max_tokens=args.max_tokens,
        sent_encode_dim=args.sent_encode_dim,
        attention_vector_size=args.attention_vector_size,
        drop_out_prob=args.drop_out_prob
    )

    model = SentClassify(
        device_settings=device_settings,
        coach_settings=coach_settings,
        model_settings=model_settings
    )
    model.prepare_for_training()
    model.start_training()


if __name__ == '__main__':
    main()

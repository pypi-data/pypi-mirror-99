# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
模型定义

Authors: fubo
Date: 2019/11/28 00:00:00
"""

import torch

from .layer import LinearLayer, SelfAttentionLayer
from .layer import BertSentEncodeSelfAttentionLayer, BertEmbeddingLayer, BertSentEncodeTermLevelLayer, BertDocEncodeLayer
from .abstract import AbstractModel


class SentClassifyModel(AbstractModel):

    def __init__(
            self, sent_encode_dim: int, attention_vector_size: int, class_count: int,
            dropout_prob: float, max_tokens: int = 20
    ):
        """
        :param sent_encode_dim: 句向量维度
        :param attention_vector_size: attention 向量维度
        :param class_count: 类别数量
        :param dropout_prob: dropout概率
        :param max_tokens: 最大token长度
        """
        super().__init__()
        self.max_tokens = max_tokens
        # query layer
        self.sent_encoding_layer = BertSentEncodeSelfAttentionLayer(
            sent_encode_dim=sent_encode_dim,
            attention_vector_size=attention_vector_size
        )

        # drop out layer
        self.drop_out_layer = torch.nn.Dropout(p=dropout_prob)

        # classify layer
        self.classify_layer = LinearLayer(n_input_dim=sent_encode_dim, n_output_dim=class_count, with_bias=False)

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        x = torch.LongTensor([[0] * self.max_tokens])
        return x

    def forward(self, x):
        """
        forward 计算
        :param x:
        :return:
        """
        x, attention_value = self.sent_encoding_layer(x)
        x = self.drop_out_layer(x)
        x = self.classify_layer(x)
        x = torch.log_softmax(x, dim=1)
        return x, attention_value


class DocClassifyModel(AbstractModel):
    def __init__(
            self,
            sent_encode_dim: int, doc_encode_dim: int, attention_vector_dim: int,
            class_count: int, dropout_prob: float,
            max_tokens: int = 20, max_sentences: int = 10,
            sent_transformer_encode_layer_size: int = 6
    ):
        """
        HAN Model from "Hierarchical Attention Networks for Document Classification"
        :param sent_encode_dim: 句向量维度
        :param attention_vector_size: attention 向量维度
        :param class_count: 类别数量
        :param dropout_prob: dropout概率
        :param max_tokens: 最大token长度
        :param max_sentences: 每个段落最大sentence数量
        """
        super().__init__()
        self.max_sentences, self.max_tokens = max_sentences, max_tokens

        # doc level layer
        self.doc_encode_layer = BertDocEncodeLayer(
            sent_encode_dim=sent_encode_dim, doc_encode_dim=doc_encode_dim, attention_vector_dim=attention_vector_dim,
            max_tokens=max_tokens, max_sentences=max_sentences,
            sent_transformer_encode_layer_size=sent_transformer_encode_layer_size
        )

        # drop out layer
        self.drop_out_layer = torch.nn.Dropout(p=dropout_prob)

        # classify layer
        self.classify_layer = LinearLayer(n_input_dim=doc_encode_dim, n_output_dim=class_count, with_bias=False)

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        return torch.randint(0, 1, [1, self.max_sentences, self.max_tokens])

    def forward(self, x: torch.LongTensor, mask: torch.LongTensor = None):
        """
        forward 计算
        :param x: (batch_size, segment_size, sentence_size, token_size)
        :return:
        """
        x, term_weights, sent_weights = self.doc_encode_layer(x, mask=mask)
        x = self.drop_out_layer(x)
        x = self.classify_layer(x)
        x = torch.log_softmax(x, dim=1)
        return x, term_weights, sent_weights


class SentTokenClassifyModel(AbstractModel):

    def __init__(
            self, sent_class_count: int, token_class_count: int,
            dropout_prob: float = 0.3, max_tokens: int = 20
    ):
        """
        :param dropout_prob: dropout概率
        :param max_tokens: 最大token长度
        """
        super().__init__()
        self.max_tokens = max_tokens
        # bert embedding layer
        self.bert_embedding_layer = BertEmbeddingLayer()

        # drop out layer
        self.drop_out_layer = torch.nn.Dropout(p=dropout_prob)

        # sent classifier
        self.sent_class_layer = LinearLayer(
            n_input_dim=self.bert_embedding_layer.hidden_size,
            n_output_dim=sent_class_count
        )

        # token classifier
        self.token_class_layer = LinearLayer(
            n_input_dim=self.bert_embedding_layer.hidden_size,
            n_output_dim=token_class_count
        )

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        x = torch.LongTensor([[0] * self.max_tokens])
        return x

    def forward(self, x):
        """
        forward 计算
        :param x:
        :return:
        """
        res = self.bert_embedding_layer(x)
        x_token, x_intent = res[0], res[1]
        x_token = self.token_class_layer(self.drop_out_layer(x_token))
        x_intent = self.sent_class_layer(self.drop_out_layer(x_intent))
        x_token = torch.log_softmax(x_token, dim=2)
        x_intent = torch.log_softmax(x_intent, dim=1)

        return x_intent, x_token


class TokenClassifyModel(AbstractModel):

    def __init__(self, token_class_count: int, dropout_prob: float = 0.3, max_tokens: int = 20):
        """
        :param dropout_prob: dropout概率
        :param max_tokens: 最大token长度
        """
        super().__init__()
        self.max_tokens = max_tokens
        # bert embedding layer
        self.bert_embedding_layer = BertEmbeddingLayer()

        # drop out layer
        self.drop_out_layer = torch.nn.Dropout(p=dropout_prob)

        # entity classifier
        self.token_linear_layer = LinearLayer(
            n_input_dim=self.bert_embedding_layer.hidden_size,
            n_output_dim=token_class_count
        )

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        x = torch.LongTensor([[0] * self.max_tokens])
        return x

    def forward(self, x):
        """
        forward 计算
        :param x:
        :return:
        """
        res = self.bert_embedding_layer(x)
        x_token, _ = res[0], res[1]
        x_token = self.token_linear_layer(self.drop_out_layer(x_token))
        x_token = torch.log_softmax(x_token, dim=2)
        return x_token


class SentMultiClassifyModel(AbstractModel):

    def __init__(self, tags_count: int, dropout_prob: float = 0.3, max_tokens: int = 20):
        """
        :param dropout_prob: dropout概率
        :param max_tokens: 最大token长度
        """
        super().__init__()
        self.max_tokens = max_tokens
        # bert embedding layer
        self.bert_embedding_layer = BertEmbeddingLayer()

        # drop out layer
        self.drop_out_layer = torch.nn.Dropout(p=dropout_prob)

        # expand tags seq layer
        self.expand_layer = LinearLayer(
            n_input_dim=self.max_tokens,
            n_output_dim=tags_count
        )

        # tags classifier
        self.entity_layer = LinearLayer(
            n_input_dim=self.bert_embedding_layer.hidden_size,
            n_output_dim=2
        )

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        x = torch.LongTensor([[0] * self.max_tokens])
        return x

    def forward(self, x):
        """
        forward 计算
        :param x:
        :return:
        """
        res = self.bert_embedding_layer(x)
        x_token, _ = res[0], res[1]
        x_token = torch.transpose(x_token, dim0=2, dim1=1)
        x_token = self.expand_layer(self.drop_out_layer(x_token))
        x_token = torch.transpose(x_token, dim0=2, dim1=1)
        x_token = self.entity_layer(self.drop_out_layer(x_token))
        x_token = torch.log_softmax(x_token, dim=2)
        return x_token


class SentSimilarityModel(AbstractModel):

    def __init__(self, sent_encode_dim: int, attention_vector_size: int, max_tokens: int = 20):
        """
        :param sent_encode_dim: 句向量维度
        :param attention_vector_size: attention 向量维度
        :param max_tokens: 类别数量
        :param max_tokens: 最大token长度
        """
        super().__init__()
        self.max_tokens = max_tokens
        # query layer
        self.sent_encoding_layer = BertSentEncodeSelfAttentionLayer(
            sent_encode_dim=sent_encode_dim,
            attention_vector_size=attention_vector_size
        )

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        x_pivot = torch.LongTensor([[0] * self.max_tokens])
        x_positive = torch.LongTensor([[0] * self.max_tokens])
        x_negative = torch.LongTensor([[0] * self.max_tokens])
        return x_pivot, x_positive, x_negative

    def sent_encoding(self, x):
        """

        :param x:
        :return:
        """
        return self.sent_encoding_layer(x)

    def forward(self, x_pivot, x_positive, x_negative):
        """
        forward 计算
        :param x_pivot:
        :param x_positive:
        :param x_negative:
        :return:
        """
        x_pivot, x_pivot_attention_value = self.sent_encoding(x_pivot)
        x_positive, x_positive_attention_value = self.sent_encoding(x_positive)
        x_negative, x_negative_attention_value = self.sent_encoding(x_negative)
        return x_pivot, x_positive, x_negative, \
               x_pivot_attention_value, x_positive_attention_value, x_negative_attention_value


class SentSimilarityCrossModel(AbstractModel):

    def __init__(self, attention_vector_size: int, max_tokens: int = 20):
        """
        :param attention_vector_size: attention 向量维度
        :param max_tokens: 类别数量
        :param max_tokens: 最大token长度
        """
        super().__init__()
        self.max_tokens = max_tokens
        self.bert_term_layer = BertSentEncodeTermLevelLayer()
        # # query layer
        self.converge_layer = SelfAttentionLayer(
            embedding_size=self.bert_term_layer.embedding_layer.hidden_size,
            attention_vector_size=attention_vector_size
        )
        self.output_layer = LinearLayer(
            n_input_dim=self.bert_term_layer.embedding_layer.hidden_size,
            n_output_dim=2,
            with_bias=True
        )

    def get_dummy_input(self):
        """
        获取dummy数据
        :return:
        """
        x_token1 = torch.LongTensor([[0] * self.max_tokens])
        x_token2 = torch.LongTensor([[0] * self.max_tokens])
        return x_token1, x_token2

    def sent_base_encoding(self, x):
        """
        base共享部分 sent encoding
        :param x:
        :return:
        """
        return self.bert_term_layer(x)

    def converge_encoding(self, x_encoding_terms1, x_encoding_terms2):
        """
        汇聚层 两个encoding向量交互计算
        """
        converge_vec, attention = self.converge_layer(x_encoding_terms1 + x_encoding_terms2)
        converge_output = self.output_layer(converge_vec)
        return converge_output, attention

    def run_similarity_base_encoding(self, x_encoding1, x_encoding2):
        """
        base encoding计算相关性
        """
        output, _ = self.converge_encoding(x_encoding1, x_encoding2)
        return torch.log_softmax(output, dim=1)

    def forward(self, x_token1, x_token2):
        """
        forward 计算
        :param x_token1:
        :param x_token2:
        :return:
        """
        vec1 = self.sent_base_encoding(x_token1)
        vec2 = self.sent_base_encoding(x_token2)
        output, _ = self.converge_encoding(vec1, vec2)
        return torch.log_softmax(output, dim=1)

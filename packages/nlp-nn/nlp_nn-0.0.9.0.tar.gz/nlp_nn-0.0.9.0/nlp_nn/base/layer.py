# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019 p-cube.cn, Inc. All Rights Reserved
#
###############################################################################
"""
模型层管理

Authors: fubo
Date: 2019/11/28 00:00:00
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import torch
import transformers
from ..base.common import BerType
from ..base.utils import Utils


class EmbeddingLayer(torch.nn.Module):
    """
    Embedding lookup table层
    """
    def __init__(self, vocab_size, dim):
        super().__init__()
        self.layer = torch.nn.Embedding(vocab_size, dim)
        torch.nn.init.uniform_(self.layer.weight)

    def forward(self, x: torch.LongTensor) -> torch.Tensor:
        """
        :param x:
        :return:
        """
        return self.layer(x)


class BertEmbeddingLayer(torch.nn.Module):
    """
    Bert embedding 层
    """
    def __init__(self, bert_type=BerType.LITE_BERT_TINY):
        super().__init__()
        self.layer = transformers.AutoModel.from_config(
            transformers.AlbertConfig.from_pretrained(
                Utils.download_model(bert_type=bert_type)
            )
        )

        self.hidden_size = self.layer.config.hidden_size

    def forward(self, x: torch.LongTensor, mask: torch.LongTensor = None) -> torch.Tensor:
        """
        向后计算
        :param x:
        :return:
        """
        return self.layer(x) if mask is None else self.layer(x, attention_mask=mask)


class SelfAttentionLayer(torch.nn.Module):
    """
    自注意力层
    """
    def __init__(self, embedding_size, attention_vector_size):
        super().__init__()
        self.converge_layer = torch.nn.Linear(
            in_features=embedding_size,
            out_features=attention_vector_size,
            bias=False
        )
        self.attention_layer = torch.nn.Linear(in_features=attention_vector_size, out_features=1, bias=False)
        torch.nn.init.xavier_uniform_(self.converge_layer.weight)
        torch.nn.init.xavier_uniform_(self.attention_layer.weight)

    def forward(self, x: torch.Tensor) -> (torch.Tensor, torch.Tensor):
        """
        向后计算
        :param x:
        :return:
        """
        y = torch.tanh(self.converge_layer(x))
        attention = torch.softmax(self.attention_layer(y), dim=1)
        x = torch.bmm(attention.transpose(1, 2), x).squeeze(dim=1)
        return x, attention.squeeze(dim=2)


class LinearLayer(torch.nn.Module):
    """
    全连接层
    """
    def __init__(self, n_input_dim, n_output_dim, with_bias=False):
        super().__init__()
        self.linear_layer = torch.nn.Linear(
            in_features=n_input_dim,
            out_features=n_output_dim,
            bias=with_bias
        )
        torch.nn.init.xavier_uniform_(self.linear_layer.weight)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        向后计算
        :param x:
        :return:
        """
        return self.linear_layer(x)


class BertSentEncodeAvePoolingLayer(torch.nn.Module):
    """
    基于bert average pooling句编码layer
    """
    def __init__(self, sent_encode_dim, bert_type=BerType.LITE_BERT_TINY):
        """
        :param sent_encode_dim:
        :param bert_type:
        """
        super().__init__()
        # Embedding映射层##########
        self.embedding_layer = BertEmbeddingLayer(bert_type=bert_type)
        embedding_dim = self.embedding_layer.hidden_size

        # Encode linear layer
        self.linear_layer = LinearLayer(embedding_dim, sent_encode_dim)

    def forward(self, x: torch.LongTensor, mask: torch.LongTensor = None) -> torch.Tensor:
        """
        :param x:
        :return:
        """
        return self.linear_layer(self.embedding_layer(x, mask=mask)[1])


class BertSentEncodeTermLevelLayer(torch.nn.Module):
    """
    基于bert layer，term粒度
    """
    def __init__(self, bert_type=BerType.LITE_BERT_TINY):
        """
        :param bert_type:
        """
        super().__init__()
        # Embedding映射层##########
        self.embedding_layer = BertEmbeddingLayer(bert_type=bert_type)

    def forward(self, x: torch.LongTensor, mask: torch.LongTensor = None) -> torch.Tensor:
        """
        :param x:
        :return:
        """
        return self.embedding_layer(x, mask=mask)[0]


class BertSentEncodeSelfAttentionLayer(torch.nn.Module):
    """
    基于bert self-attention句编码layer
    """
    def __init__(self, sent_encode_dim, attention_vector_size=64, bert_type=BerType.LITE_BERT_TINY):
        """
        基于bert的句向量编码
        :param sent_encode_dim:
        :param attention_vector_size:
        :param bert_type:
        """
        super().__init__()

        # Embedding映射层##########
        self.embedding_layer = BertEmbeddingLayer(bert_type=bert_type)
        embedding_dim = self.embedding_layer.hidden_size

        # 自注意力layer
        self.self_attention_layer = SelfAttentionLayer(
            embedding_size=embedding_dim,
            attention_vector_size=attention_vector_size
        )

        # Encode linear layer
        self.linear_layer = LinearLayer(embedding_dim, sent_encode_dim)

    def forward(self, x: torch.LongTensor, mask: torch.LongTensor = None) -> (torch.Tensor, torch.Tensor):
        """

        :param x:
        :return:
        """
        attention_output, attention_value = self.self_attention_layer(self.embedding_layer(x, mask=mask)[0])
        return self.linear_layer(attention_output), attention_value


class BertDocEncodeLayer(torch.nn.Module):
    """
    文档编码 Hierarchical Attention Networks
    """
    def __init__(
            self, sent_encode_dim: int, doc_encode_dim: int, attention_vector_dim: int,
            max_tokens: int = 20, max_sentences: int = 10, sent_transformer_encode_layer_size: int = 6,
            bert_type=BerType.LITE_BERT_TINY
    ):
        super().__init__()
        self.max_tokens = max_tokens
        self.max_sentences = max_sentences
        self.sent_encode_dim = sent_encode_dim
        self.doc_encode_dim = doc_encode_dim
        # term level layer
        self.embedding_layer = BertSentEncodeTermLevelLayer(bert_type=bert_type)

        # sent level layer
        self.sent_self_attention_layer = SelfAttentionLayer(
            embedding_size=self.embedding_layer.embedding_layer.hidden_size,
            attention_vector_size=attention_vector_dim
        )
        self.sent_linear_layer = LinearLayer(self.embedding_layer.embedding_layer.hidden_size, self.sent_encode_dim)

        # doc level layer
        self.doc_transformer_layer = torch.nn.TransformerEncoder(
            torch.nn.TransformerEncoderLayer(d_model=self.sent_encode_dim, nhead=8),
            num_layers=sent_transformer_encode_layer_size
        )
        self.doc_self_attention_layer = SelfAttentionLayer(
            embedding_size=self.sent_encode_dim,
            attention_vector_size=attention_vector_dim
        )
        self.doc_linear_layer = LinearLayer(self.sent_encode_dim, self.doc_encode_dim)

    def sent_level_encode(self, x: torch.LongTensor, mask: torch.LongTensor = None):
        """
        sentence level encode
        :param x: (sent_size * token_size)
        :param mask: (sent_size * token_size)
        :return: encode_vector (sent_size * sent_dim), attention_weights (sent_size * token_size)
        """
        # term embedding
        term_embedding = self.embedding_layer(x, mask=mask)
        encode_vector, attention_weights = self.sent_self_attention_layer(term_embedding)
        attention_weights = attention_weights * mask if mask is not None else attention_weights
        encode_vector = self.sent_linear_layer(encode_vector)
        return encode_vector, attention_weights

    def doc_level_encode(self, x, mask: torch.FloatTensor = None):
        """
        doc level encode
        :param x: (batch_size * sent_size * sent_dim)
        :param mask: (batch_size * sent_size)
        :return: encode_vector (batch_size * doc_dim), attention_weights (batch_size * sec_size)
        """
        # value = self.doc_transformer_layer(
        #     x.transpose(dim0=1, dim1=0), src_key_padding_mask=mask
        # ).transpose(dim0=1, dim1=0)
        # value = torch.nan_to_num(value)
        value = x
        encode_vector, attention_weights = self.doc_self_attention_layer(value)
        encode_vector = self.doc_linear_layer(encode_vector)
        attention_weights = mask * attention_weights if mask is not None else attention_weights
        return encode_vector, attention_weights

    def forward(self, x: torch.LongTensor, mask: torch.LongTensor = None) -> (
            torch.Tensor, torch.Tensor, torch.Tensor
    ):
        """
        计算doc encoding
        :param x: (batch_size * sent_size * token_size) 每篇文档表示成为多句。段落用[unused1] token分割
        :param mask: 掩码 (batch_size * sent_size * token_size)
        :return:
        doc encoding (batch_size * doc_encoding_dim)
        token level attention (batch_size * sent_size * token_size)
        sent level attention (batch_size * sent_size)
        """
        shape_input = x.shape
        if mask is None:
            term_mask = None
            sent_mask = None
        else:
            term_mask = torch.flatten(mask, start_dim=0, end_dim=1)
            sent_mask = (torch.sum(term_mask, dim=1, dtype=float) > 0).reshape(shape_input[:2])

        # sentence level encode
        term_x = torch.flatten(x, start_dim=0, end_dim=1)
        value, term_attention_weights = self.sent_level_encode(term_x, mask=term_mask)
        term_attention_weights = term_attention_weights.reshape(shape_input)

        # 计算sent mask
        value = value.reshape(list(shape_input[:2]) + [self.sent_encode_dim])
        value, sent_attention_weights = self.doc_level_encode(x=value, mask=sent_mask)

        return value, term_attention_weights, sent_attention_weights


class CrossLayer(torch.nn.Module):
    """
    Cross layer part in Cross and Deep Network
    The ops in this module is x_0 * x_l^T * w_l + x_l + b_l for each layer l, and x_0 is the init input of this module
    """

    def __init__(self, input_feature_num, cross_layer):
        """
        :param input_feature_num: total num of input_feature, including of the embedding feature and dense feature
        :param cross_layer: the number of layer in this module expect of init op
        """
        super().__init__()
        self.cross_layer = cross_layer + 1  # add the first calculate
        weight_w = []
        weight_b = []
        batch_norm = []
        for i in range(self.cross_layer):
            weight_w.append(torch.nn.Parameter(torch.nn.init.normal_(torch.empty(input_feature_num))))
            weight_b.append(torch.nn.Parameter(torch.nn.init.normal_(torch.empty(input_feature_num))))
            batch_norm.append(torch.nn.BatchNorm1d(input_feature_num, affine=False))
        self.weight_w = torch.nn.ParameterList(weight_w)
        self.weight_b = torch.nn.ParameterList(weight_b)
        self.batch_norm = torch.nn.ModuleList(batch_norm)

    def forward(self, x):
        """
        向后计算
        :param x:
        :return:
        """
        output = x
        x = x.reshape(x.shape[0], -1, 1)
        for i in range(self.cross_layer):
            output = torch.matmul(torch.bmm(x, torch.transpose(output.reshape(output.shape[0], -1, 1), 1, 2)),
                                  self.weight_w[i]) + self.weight_b[i] + output
            output = self.batch_norm[i](output)
        return output

# -*- coding=utf-8 -*-
# library: jionlp
# author: dongrixinyu
# license: Apache License 2.0
# Email: dongrixinyu.89@163.com
# github: https://github.com/dongrixinyu/JioNLP
# description: Preprocessing tool for Chinese NLP


"""
DESCRIPTION:
    1、功能包括：文本分类标注数据集的分割，列出各个类别的数据量以及占比，并计算训练集
        (training set)、验证集(validation set / dev set)、测试集(test set)的相对熵
        判断数据集分割是否合理。
    2、info dismatch 信息，百分比越小，说明数据子集类别分布越合理

"""


import os
import pdb
import random
import collections

import numpy as np

from jionlp import logging


def _stat_class(dataset_y, multi_label=False):
    """ 统计标签集合的结果
    """
    if not multi_label:
        dataset_res = collections.Counter(dataset_y).most_common()

        stat_result = dict()
        for item in dataset_res:
            stat_result.update({item[0]: [item[1], item[1] / len(dataset_y)]})
    else:
        convert_y = list()
        for item in dataset_y:
            convert_y.extend(item)
        
        dataset_res = collections.Counter(convert_y).most_common()
        stat_result = dict()
        for item in dataset_res:
            stat_result.update({item[0]: [item[1], item[1] / len(dataset_y)]})
            
    return stat_result


def _compute_kl_divergence(vector_1, vector_2):
    """ 计算两个概率分布的 kl 散度，其中 vector_1 为真实分布，vector_2 为估计分布 """
    kl_value = np.sum(np.multiply(vector_1, np.log2(
        np.multiply(vector_1, 1 / vector_2))))

    entropy_value = np.sum(np.multiply(vector_1, np.log2(1 / vector_1)))  # 交叉熵
    
    ratio = kl_value / entropy_value  # 信息量损失比例
    return kl_value, ratio


def analyse_dataset(dataset_x, dataset_y, 
                    ratio=[0.8, 0.05, 0.15],
                    shuffle=True, multi_label=False):
    """ 将数据集按照训练、验证、测试进行划分，统计数据集中各个类别的数量和占比，计算训练、
    验证、测试集的相对熵，判断数据集分割是否合理。其中，dismatch 信息比例越低，证明数据集
    划分的各类别比例越贴近数据全集的分布。

    Args:
        dataset_x: 数据集的输入数据部分
        dataset_y: 数据集的输出标签
        ratio: 训练集、验证集、测试集的比例
        shuffle: 打散数据集
        multi_label: 数据集为多标签

    Return:
        train_x, train_y, valid_x, valid_y, test_x, test_y, stats(dict):
            stats 为数据集的统计信息(数量、占比、相对熵)

    Examples:
        >>> import jionlp as jio
        >>> dataset_x = ['美股大涨...', '金融市场开放...', '小米无屏电视...', ...]
        >>> dataset_y = ['财经', '财经', '科技', ...]
        >>> train_x, train_y, valid_x, valid_y, test_x, test_y, stats = \
            ... jio.text_classification.analyse_dataset(dataset_x, dataset_y)
        >>> print(stats)

            whole dataset:
            财经                            32,268        84.52%
            科技                             5,910        15.48%
            total                           38,178       100.00%

            train dataset: 80.00%
            财经                            25,848        84.63%
            科技                             4,694        15.37%
            total                           30,542       100.00%

            valid dataset: 5.00%
            财经                            32,268        84.52%
            科技                             5,910        15.48%
            total                            1,908       100.00%

            test dataset: 15.00%
            财经                             4,840        84.53%
            科技                               886        15.47%
            total                            5,726       100.00%

            train KL divergence: 0.000007, info dismatch: 0.00%
            valid KL divergence: 0.001616, info dismatch: 0.26%
            test KL divergence: 0.000000, info dismatch: 0.00%

    """
    dataset = [[sample_x, sample_y] for sample_x, sample_y
               in zip(dataset_x, dataset_y)]
    
    if shuffle:
        random.shuffle(dataset)

    has_kl = False
    for i in range(3):
        # 为获得最佳的数据子集切分，在切分情况不好（相对熵较高，类别不全）时，需要重新
        # 切分，以获得最佳的子集类别分布。在三次都不满足的情况下，则照常返回。
        # 统计各个类别的数据数量及占比
        stats = {'train': None, 'valid': None, 'test': None, 'total': None}
        dataset_stat = _stat_class(dataset_y, multi_label=multi_label)
        stats['total'] = dataset_stat

        tmp_ds = list()
        current = 0
        for s in ratio:
            num = int(len(dataset) * s)
            tmp_ds.append(dataset[current: current + num])
            current += num

        train_x = [item[0] for item in tmp_ds[0]]
        train_y = [item[1] for item in tmp_ds[0]]
        valid_x = [item[0] for item in tmp_ds[1]]
        valid_y = [item[1] for item in tmp_ds[1]]
        test_x = [item[0] for item in tmp_ds[2]]
        test_y = [item[1] for item in tmp_ds[2]]

        # 统计各数据子集的统计信息
        train_stat = _stat_class(train_y, multi_label=multi_label)
        stats['train'] = train_stat
        valid_stat = _stat_class(valid_y, multi_label=multi_label)
        stats['valid'] = valid_stat
        test_stat = _stat_class(test_y, multi_label=multi_label)
        stats['test'] = test_stat
        
        if not (len(train_stat) == len(valid_stat) == len(test_stat)):
            # 各子集的类别数量不一致，则重新进行切分
            continue

        # 计算 KL 散度
        has_kl = True
        train_kl_value, train_ratio = _compute_kl_divergence(
            np.array([item[1][1] for item in sorted(dataset_stat.items())]),
            np.array([item[1][1] for item in sorted(train_stat.items())]))
        valid_kl_value, valid_ratio = _compute_kl_divergence(
            np.array([item[1][1] for item in sorted(dataset_stat.items())]),
            np.array([item[1][1] for item in sorted(valid_stat.items())]))
        test_kl_value, test_ratio = _compute_kl_divergence(
            np.array([item[1][1] for item in sorted(dataset_stat.items())]),
            np.array([item[1][1] for item in sorted(test_stat.items())]))

        if (train_ratio > 0.05) or (valid_ratio > 0.05) or (test_ratio > 0.05):
            # kl 散度阈值过大，说明切分的类别分布比例不一致，需要重新切分
            continue
            
        break

    # 打印信息
    stats_fmt = '{0:<20s}\t{1:>8,d}\t{2:>2.2%}'
    total_fmt = stats_fmt + '\n'
    logging.info('whole dataset:')
    for _class, info in stats['total'].items():
        logging.info(stats_fmt.format(_class, info[0], info[1]))
    sum_res = sum([info[1] for info in stats['total'].values()])
    logging.info(total_fmt.format('total', len(dataset_y), sum_res))
    
    logging.info('train dataset: {:.2%}'.format(ratio[0]))
    for _class, info in stats['train'].items():
        logging.info(stats_fmt.format(_class, info[0], info[1]))
    sum_res = sum([info[1] for info in stats['train'].values()])

    logging.info(total_fmt.format('total', len(train_y), sum_res))
    
    logging.info('valid dataset: {:.2%}'.format(ratio[1]))
    for _class, info in stats['valid'].items():
        logging.info(stats_fmt.format(_class, info[0], info[1]))
    sum_res = sum([info[1] for info in stats['valid'].values()])
    logging.info(total_fmt.format('total', len(valid_y), sum_res))
    
    logging.info('test dataset: {:.2%}'.format(ratio[2]))
    for _class, info in stats['test'].items():
        logging.info(stats_fmt.format(_class, info[0], info[1]))
    sum_res = sum([info[1] for info in stats['test'].values()])
    logging.info(total_fmt.format('total', len(test_y), sum_res))
    
    if has_kl:
        kl_fmt = 'KL divergence: {0:.>2f}, info dismatch: {1:.2%}'
        logging.info('train ' + kl_fmt.format(train_kl_value, train_ratio))
        logging.info('valid ' + kl_fmt.format(valid_kl_value, valid_ratio))
        logging.info('test ' + kl_fmt.format(test_kl_value, test_ratio))
    
    return train_x, train_y, valid_x, valid_y, test_x, test_y, stats

# -*- coding：utf-8 -*-
# &Author  AnFany

#  读取存储的城市之间的距离以及城市对应的代码
import pandas as pd

# 存储距离的csv文件
distance_csv = r'C:\Users\GWT9\Desktop\city_distance.csv'

# 存储地址对应编号的csv文件
sign_csv = r'C:\Users\GWT9\Desktop\city_sign.csv'


# 读取距离的文件，并且用字典存储
def read_distance(d_csv=distance_csv):
    """
    地址编号小的在前面,例如(2. 9):38283。编号为2的与编号为9的距离为38283米
    :param d_csv: 存储距离的文件
    :return: 地址编号对为键，距离为值的字典
    """
    d_data = pd.read_csv(d_csv, encoding='gbk')  # 因为有中文，需要设置encoding='gbk'
    d_dict = {}
    # 数据的列
    column = d_data.keys()
    for c in column[1:]:
        for s in d_data[column[0]]:
            dis = d_data[c][s]
            if dis != 0:
                d_dict[(int(c), s)] = dis
    return d_dict


# 读取地址对应的城市，用于结果的展示
def read_sign(d_csv=sign_csv):
    """
    获得中文地址和数字编号的对应字典，数字编号为键，中文地址为值
    :param d_csv: 存储对应关系的文件
    :return: 数字编号为键，中文地址为值的字典
    """
    s_data = pd.read_csv(d_csv, encoding='gbk')  # 因为有中文，需要设置encoding='gbk'
    s_dict = {sign: address for address, sign in s_data.values}
    return s_dict



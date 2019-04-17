# -*- coding：utf-8 -*-
# &Author  AnFany

#  读取城市的经纬度excel表格，然后利用公式计算得到经纬度之间的地球表面距离。
#  并将城市的对应编号以及城市间的距离存储在文件中，

from math import pi, cos, sin, asin
import pandas as pd  # 将结果存储到表格中

# 城市的经纬度的文件
city_lng_lat_file = r'C:\Users\GWT9\Desktop\城市经纬度.csv'
# 存储距离的csv文件
distance_csv = r'C:\Users\GWT9\Desktop\city_distance.csv'
# 存储地址对应编号的csv文件
sign_csv = r'C:\Users\GWT9\Desktop\city_sign.csv'


#  读取文件，获取相应的经纬度
def read_latlon(file=city_lng_lat_file):
    data = pd.read_csv(file,  encoding='gbk')
    city_dict = {c: [lng, lat] for c, lng, lat in data.values}
    return city_dict


#  根据经纬度获得直线距离
def distance_lng_lat(add1, add2, r_earth=6378137):
    """
    根据两个地址的经纬度获取这2个地址之间的地球表面距离
    :param add1: 地址1的经纬度
    :param add2: 地址2的经纬度
    :param r_earth: 地球的平均半径米
    :return: 直线距离
    """
    # 转为弧度
    add1_radian = [float(a) * pi / 180 for a in add1]
    add2_radian = [float(b) * pi / 180 for b in add2]

    # 计算经纬度之差
    d_lng = add1_radian[0] - add2_radian[0]
    d_lat = add1_radian[1] - add2_radian[1]

    # 计算距离
    sanj = sin(d_lat / 2) ** 2 + cos(add1_radian[1]) * cos(add2_radian[1]) * sin(d_lng / 2) ** 2
    dis = 2 * asin(sanj ** 0.5)
    return dis * r_earth


#  获取城市之间距离，以及城市的编号信息，并存储到表格
def save_distance(d_csv=distance_csv, s_csv=sign_csv):
    """
    获取地址列表中的任意2个地址之间的驾车距离，以及地址的对应的编号，并存储
    :param d_csv: 存储距离的csv文件
    :param s_csv: 存储地址编号的csv文件
    :return: 存到到csv文件中
    """
    # 地址的经纬度字典
    add_dict = read_latlon()

    # 地址列表
    add_list = list(add_dict.keys())

    # 便于后面的计算，将中文地址变为数字标识
    sorted_city_list = sorted(add_list)

    # 编号和城市的对应字典
    sign_city = pd.DataFrame()
    sign_city['中文'] = [s for s in sorted_city_list]
    sign_city['编号'] = list(range(len(sorted_city_list)))

    # 防止调用次数的限制，将得到距离存储到表格中
    city_distance = pd.DataFrame()
    city_distance['城市编号'] = list(range(len(sorted_city_list)))
    for i, j in enumerate(sorted_city_list):
        distance = []
        for a, b in enumerate(sorted_city_list):
            if i >= a:
                distance.append(0)
            else:
                distance.append(distance_lng_lat(add_dict[j], add_dict[b]))
        city_distance[i] = distance

    city_distance.to_csv(d_csv, index=False, encoding="gb2312")
    sign_city.to_csv(s_csv, index=False, encoding="gb2312")
    return print('写入完毕')


# 主函数
if __name__ == "__main__":
    save_distance()


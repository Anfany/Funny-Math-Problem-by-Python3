# -*- coding：utf-8 -*-
# &Author  AnFany

#  基于百度地图API得到34个城市的各自之间的距离


import urllib.request as ur  # WEB服务接口地址
import urllib.parse  # URL中的中文转码
import json  # 读取内容
import pandas as pd  # 将结果存储到表格中


# 34城市列表
City_List = ['北京', '天津', '上海', '重庆', '石家庄', '太原', '西安', '济南', '郑州',
             '沈阳', '长春', '哈尔滨', '南京', '杭州', '合肥', '南昌', '福州', '武汉',
             '长沙', '成都', '贵阳', '昆明', '广州', '海口', '兰州', '西宁', '台北',
             '呼和浩特', '乌鲁木齐', '拉萨', '南宁', '银川', '香港', '澳门']
# 存储距离的csv文件
distance_csv = r'C:\Users\GWT9\Desktop\city_distance.csv'

# 存储地址对应编号的csv文件
sign_csv = r'C:\Users\GWT9\Desktop\city_sign.csv'

#  百度地图开发者中心注册后获得个人密钥
privatekey = 'gXBXU61wkWtymp1vTPuc5pBGZA4VyzCe'  # 请换成自己的密钥，否则无法运行


#  根据中文地址获得相应的经纬度
def latlon(address, ak):
    """
    获取中文地址对应的经纬度
    :param address: 中文地址
    :param ak: 个人密钥
    :return: 经纬度
    """
    base = 'http://api.map.baidu.com/geocoder/v2/?'
    add = urllib.parse.quote(address)  # 网址中出现中文，需要转码
    start = 'address=%s' % add
    end = 'output=json&'
    miyao = 'ak=%s' % ak
    url = base + start + '&' + end + miyao + '&callback=showLocation// '
    req = ur.urlopen(url)
    du = req.read()
    hjson = json.loads(du.decode('utf-8'))  # jason形式需要转码
    return hjson['result']['location']  # 根据jason格式


#  根据经纬度获得驾车距离
def distance(add1, add2, ak):
    """
    根据两个地址的经纬度获取这2个地址之间的驾车距离
    :param add1: 地址1的经纬度
    :param add2: 地址2的经纬度
    :param ak: 个人密钥
    :return: 驾车距离
    """
    base = 'http://api.map.baidu.com/direction/v2/driving?'
    start = 'origin=%s,%s' % (add1[0], add1[1])
    end = 'destination=%s,%s' % (add2[0], add2[1])
    miyao = '&ak=%s' % ak
    url = base + start + '&' + end + miyao
    req = ur.urlopen(url)
    du = req.read()
    hjson = json.loads(du.decode('utf-8'))
    return hjson['result']['routes'][0]['distance']  # 根据jason格式


#  获得距离的函数
def drive(address1, address2, ak=privatekey):
    """
    获取2个中文地址间的驾车距离
    :param address1: 中文地址1
    :param address2: 中文地址2
    :param ak: 个人密钥
    :return: 驾车距离
    """
    jingwei1 = latlon(address1, ak)
    add1 = ['%.6f' % jingwei1['lat'], '%.6f' % jingwei1['lng']]  # 接口要求最多6位

    jingwei2 = latlon(address2, ak)
    add2 = ['%.6f' % jingwei2['lat'], '%.6f' % jingwei2['lng']]  # 接口要求最多6位

    juli = distance(add1, add2, ak)  # 获得驾车距离

    return juli


#  获取城市之间距离，并存储到表格里的函数
def save_distance(city_list=City_List, d_csv=distance_csv, s_csv=sign_csv):
    """
    获取地址列表中的任意2个地址之间的驾车距离，以及地址的对应的编号，并存储
    :param city_list: 地址列表
    :param d_csv: 存储距离的csv文件
    :param s_csv: 存储地址编号的csv文件
    :return: 存到到csv文件中
    """
    # 便于后面的计算，将中文地址变为数字标识
    sorted_city_list = sorted(city_list)
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
            print(j, b)
            if i >= a:
                distance.append(0)
            else:
                distance.append(drive(j, b))
        city_distance[i] = distance

    city_distance.to_csv(d_csv, index=False, encoding="gb2312")
    sign_city.to_csv(s_csv, index=False, encoding="gb2312")
    return print('写入完毕')


# 主函数
if __name__ == "__main__":
    save_distance()





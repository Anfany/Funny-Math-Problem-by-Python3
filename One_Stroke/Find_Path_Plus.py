# -*- coding：utf-8 -*-
# &Author  AnFany
# 一笔画完问题自动获取谜题

"""
自动读取谜题的图片，获取谜题
然后利用DFS算法快速解决一笔画完问题，
也就是获得从起始网格开始，经过所有可以经过的网格，并且没有重复网格的路径
"""
import numpy as np
import matplotlib.pylab as plt
from PIL import Image
import matplotlib.patches as mpatches  # 图例的设置
import matplotlib.colors as col
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号

# 变量声明
Fig_Name = r'C:\Users\GWT9\Desktop\7.png'  # 谜题图片的绝对路径，图片尽量贴近谜题边框、清晰

# 颜色转换为灰度模式，颜色越浅数值越大。默认起始节点的颜色 深于 可走节点的颜色  深于不可走节点的颜色(以微信小游戏一笔画完设置)

Color_list = ['no_walk', 'walk', 'start']  # 可根据谜题图片自动调节


# 此时需要用户提供谜题中垂直方向有几个表格，水平方向有几个表格
Height = int(input('竖直方向网格数：'))
Length = int(input('水平方向网格数：'))


#  根据谜题图片以及高度、宽度自动读取各种节点的函数

def read_puzzle_fig(fig=Fig_Name, h=Height, l=Length, error_tolerant_rate=0.4):
    """
    根据一笔画完的谜题的图片，自动识别各个节点
    :param fig: 图片的绝对路径
    :param h: 图片竖直方向上的网格的个数
    :param l: 图片水平方向上的网格的个数
    :param error_tolerant_rate: 容错率，图片质量越低，这数设置越小
    :return: 自动识别的结果
    """
    # 展示谜题照片
    puzzle_fig = Image.open(fig)
    plt.imshow(puzzle_fig)
    plt.axis('off')

    # 图片转为灰度模式
    im = Image.open(fig).convert('L')
    im_array = np.array(im)

    # 根据每一块中代表颜色数值的大小来确定节点的种类
    pixel_height, pixel_length = im_array.shape
    # 每个网格大致占有的高度和宽度
    per_h = int(pixel_height / h)
    per_l = int(pixel_length / l)
    # 记录每个网格的代表颜色的数值,分别记录网格的均值和标准差
    node_index_mean = {}
    node_index_std = {}
    # 从左上  右上 到左下  右下开始
    for i in range(h):
        for j in range(l):
            # 首先计算容错的高度和宽度
            t_h = int(round(per_h / 2 * (1 - error_tolerant_rate), 0))
            t_l = int(round(per_l / 2 * (1 - error_tolerant_rate), 0))
            # 选取审查的范围
            all_number = im_array[(i * per_h + t_h): ((i + 1) * per_h - t_h), (j * per_l + t_l): ((j + 1) * per_l - t_l)]
            arr = sorted(all_number.flatten())  # 平铺为一维的
            # 计算网格数值
            node_index_mean[(i, j)] = np.mean(arr)
            node_index_std[(i, j)] = np.std(arr)

            # 将数值展示在图像上，看看,注意xy互换
            plt.text((j + 0.3) * per_l, (i + 0.6) * per_h, 'm=%.2f\ns=%.2f' % (node_index_mean[(i, j)], node_index_std[(i, j)]))

            # 在图像上绘制取数的范围,左上，右上，右下，左下
            plt.plot([j * per_l + t_l, (j + 1) * per_l - t_l, (j + 1) * per_l - t_l, j * per_l + t_l, j * per_l + t_l],
                     [i * per_h + t_h, i * per_h + t_h, (i + 1) * per_h - t_h, (i + 1) * per_h - t_h, i * per_h + t_h], c='r')

    #  下面挨个分析每一个网格是什么
    #  判断标准，大于周围网格值的优先考虑是Color_list中的第一个，小于周围网格值得优先考虑Color_list中的最后一个
    #  标准差作为辅助判断









    # 获取当前展示的图片
    plt.title('谜题，获取不可走以及初始点节点……')



    plt.ioff()
    plt.show()



read_puzzle_fig()
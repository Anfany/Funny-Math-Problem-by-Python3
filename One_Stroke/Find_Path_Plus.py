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
from pylab import mpl
import Find_One_Path_Dfs as f_p  #  计算路径
import time

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号

# 变量声明
Fig_Name = r'C:\Users\anaifan\Desktop\1350.jpg'  # 谜题图片的绝对路径，图片尽量贴近谜题边框、清晰

# 颜色转换为灰度模式，颜色越浅数值越大。默认起始网格的颜色 深于 可走网格的颜色  深于不可走网格的颜色(以微信小游戏一笔画完设置)

Color_list = ['no_walk', 'walk', 'start']  # 可根据谜题图片自动调节

# 此时需要用户提供谜题中垂直方向有几个网格，水平方向有几个网格
find_one_path = f_p.Find_Path_DFS()
find_one_path.Map_Height = int(input('竖直方向网格数：'))
find_one_path.Map_Width = int(input('水平方向网格数：'))

#  根据谜题图片以及高度、宽度自动读取各种网格的函数

def read_puzzle_fig(fig=Fig_Name, error_tolerant_rate=0.8):
    """
    根据一笔画完的谜题的图片，自动识别各个节点
    :param fig: 图片的绝对路径
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
    per_h = int(pixel_height / find_one_path.Map_Height)
    per_l = int(pixel_length / find_one_path.Map_Width)
    # 记录每个网格的代表颜色的数值,分别记录网格的均值和标准差
    node_index_mean = {}
    node_index_std = {}
    # 从左上  右上 到左下  右下开始
    for i in range(find_one_path.Map_Height):
        for j in range(find_one_path.Map_Width):
            # 首先计算容错的高度和宽度
            t_h = int(round(per_h / 2 * (1 - error_tolerant_rate), 0))
            t_l = int(round(per_l / 2 * (1 - error_tolerant_rate), 0))
            # 选取审查的范围
            all_number = im_array[(i * per_h + t_h): ((i + 1) * per_h - t_h), (j * per_l + t_l): ((j + 1) * per_l - t_l)]
            arr = sorted(all_number.flatten())  # 平铺为一维的
            # 计算网格数值
            node_index_mean[(i, j)] = int(np.mean(arr))
            node_index_std[(i, j)] = int(np.std(arr))

            # # 将数值展示在图像上，看看,注意xy互换
            # plt.text((j + 0.3) * per_l, (i + 0.6) * per_h, 'm=%.0f\ns=%.0f' % (node_index_mean[(i, j)], node_index_std[(i, j)]))

            # # 在图像上绘制取数的范围,左上，右上，右下，左下
            # plt.plot([j * per_l + t_l, (j + 1) * per_l - t_l, (j + 1) * per_l - t_l, j * per_l + t_l, j * per_l + t_l],
            #          [i * per_h + t_h, i * per_h + t_h, (i + 1) * per_h - t_h, (i + 1) * per_h - t_h, i * per_h + t_h], c='r')

    #  标准差和均值系列
    mean_list = sorted(list(node_index_mean.items()), key= lambda s: s[1], reverse=True)
    std_list = sorted(node_index_std.items(), key= lambda s: s[1], reverse=True)
    #  图片质量高，标准差高的视为初始点
    start_index = list(std_list[0][0])
    #  计算均值序列前后2部分的标准差之和，最小的作为分界线
    std_dict = {}
    mean_number_list = [k[1] for k in mean_list]
    for i in range(1, len(mean_number_list) - 1):  #  初始的不算在内
        std_dict[i] = np.std(np.array(mean_number_list[:i]), ddof=0) + np.std(np.array(mean_number_list[i:]), ddof=0)
    # 选择最小的标准差对应的键值
    min_index = sorted(std_dict.items(), key= lambda s: s[1])[0][0]
    #  不可走的网格
    stone_index = [[s_h[0][0], s_h[0][1]] for s_h in mean_list[:min_index]]
    # 获取当前展示的图片
    plt.title('识别各个网格完毕')
    #  在图上绘制出
    #  在初始网格绘制标记
    plt.text(start_index[1] * per_l, (start_index[0] + 0.6) * per_h, '初始' )
    # 绘制不可走的网格标记
    for no in stone_index:
        plt.text(no[1] * per_l, (no[0] + 0.6) * per_h, '不可走')
    plt.pause(1)
    plt.title('计算路径中……')
    plt.pause(1)
    #  获得谜题数组
    find_one_path.Start_Index = start_index
    find_one_path.Stone_Index = stone_index

    start_time = time.perf_counter()
    # 更新数组
    find_one_path.problem_array = find_one_path.nodes()
    path_list = find_one_path.find_one_path_dfs([[find_one_path.Start_Index, 0]])
    # 在图中添加路径
    if not path_list:
        plt.title('不存在解, 用时：%.3fs' % (time.perf_counter() - start_time))
    else:
        x = [(p[0][1] + .5) * per_l for p in path_list]
        y = [(p[0][0] + .5) * per_h for p in path_list]
        plt.plot(x, y, '-o', c='r', lw=13)
        plt.title('路径添加完毕，方法：dfs, 用时：%.3fs' % (time.perf_counter() - start_time))
    plt.pause(2)
    plt.ioff()
    plt.show()

read_puzzle_fig()
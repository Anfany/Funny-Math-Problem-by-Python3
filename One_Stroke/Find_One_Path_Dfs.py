# -*- coding：utf-8 -*-
# &Author  AnFany
# 一笔画完问题

"""
利用DFS算法快速解决一笔画完问题，只得到一个解
也就是获得从起始网格开始，经过所有网格的，并且没有重复网格的路径
"""
import time
import sys  # 尾递归优化
import matplotlib.patches as mpatches  # 图例的设置
import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号

# 用不同数值表示不同意义的网格
Start_Node = 2
Walk_Node = 1
Stone_Node = 0


# 用不同颜色表示不同网格
Start_Color = '#457896'
Walk_Color = (198 / 255, 198 / 255, 198 / 255)
Stone_Color = 'whitesmoke'
Path_Color = 'tab:red'


# 图的竖直、水平方向网格的个数
Map_Height = 9
Map_Width = 7


# 起始网格和不能经过的网格的索引
Start_Index = [1, 0]
Stone_Index = [[0, 3], [0, 6], [1, 6], [2, 6], [3, 1], [7, 1], [8, 3], [8, 5], [8, 6]]


# 表示图的数组
def nodes(h=Map_Height, w=Map_Width, start=Start_Index, stone=Stone_Index):
    """
    在数组中将对应的网格变为对应的值
    :param h: 图的竖直方向网格的个数
    :param w: 图的水平方向网格的个数
    :param start: 开始网格的索引
    :param stone: 不能走的网格的索引
    :return: 变换后的数组
    """
    node_array = np.ones((h, w))
    # 起始网格标记
    node_array[start[0], start[1]] = Start_Node
    # 不能走的网格
    for i in stone:
        node_array[i[0], i[1]] = Stone_Node
    return node_array


def can_go(index, array):
    """
    对于一个网格而言，可以去的网格，上下左右四个方向
    :param index: 索引
    :param array: 数组
    :return: 可以去的网格索引的列表
    """
    x, y = index
    node_list = []
    if x > 0:
        if array[x - 1, y] == Walk_Node:
            node_list.append([x - 1, y])
    if x < Map_Height - 1:
        if array[x + 1, y] == Walk_Node:
            node_list.append([x + 1, y])
    if y > 0:
        if array[x, y - 1] == Walk_Node:
            node_list.append([x, y - 1])
    if y < Map_Width - 1:
        if array[x, y + 1] == Walk_Node:
            node_list.append([x, y + 1])
    return node_list


def judge_area_indived(have_walk, map, no_walk=Stone_Index, h=Map_Height, w=Map_Width):
    """
    判断走过的网格和不能走的网格是否把剩下的还没有走过的网格分为了不能连通的2部分，是的话就说明刚才加的网格不合理
    为了避免在一些本就不可能的路径上耽误时间
    选择任何一个没有走过的网格，然后扩展为这个网格可以去的区域，如果区域内的网格数等于剩下的网格数，则剩下的部分是连通的
    :param have_walk: 已经走过的网格 [[2, 3],[3, 4],[4, 5]]
    :param map: 数组
    :param no_walk: 不能走的网格集合
    :param h: 图的竖直方向网格的个数
    :param w: 图的水平方向网格的个数
    :return: 合理返回True，不合理返回False
    """
    all_cannot_node = have_walk + no_walk
    count_nodes = h * w  # 网格总个数
    if len(all_cannot_node) == count_nodes:  # 此时已经走完所有的网格
        return True
    # 随机选择一个不在上面集合中的网格
    center_node = []
    for i in range(h):
        for j in range(w):
            if [i, j] not in all_cannot_node:
                center_node = [i, j]
                break
    # 下面就开始扩展这个center_node可以去的区域
    current = [center_node]
    area_node = [center_node]  # 连通区域内的网格列表
    while current:  # 只要不为空存在就扩展
        copy_current = []
        for n in current:
            can_go_to = can_go(n, map)
            for d in can_go_to:
                if d not in area_node and d not in have_walk:
                    copy_current.append(d)
                    area_node.append(d)
        current = copy_current

    if len(area_node) == count_nodes - len(all_cannot_node):  # 全部连通
        return True
    else:  # 存在不连通的区域
        return False


class TailRecurseException(BaseException):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


# 尾递归优化的程序
def tail_call_optimized(g):
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs
    func.__doc__ = g.__doc__
    return func


@tail_call_optimized
def find_one_path_dfs(node_list, map, h=Map_Height, w=Map_Width, s_i=Stone_Index):
    """
    利用dfs深度优先算法快速求解满足条件的一条路径，只要经过的网格的个数等于可以走的网格的个数，就是一个解
    :param node_list: 表示走过的网格列表，[[node_index], node_sign]]，元素为网格索引和这个网格已经去往周围网格的个数，用于回溯
    :param map: 表示图的数组
    :param solution_list: 存储所有的是解的路径
    :param h: 图的竖直方向网格的个数
    :param w: 图的水平方向网格的个数
    :param s_i: 不可以走的网格的索引
    :return: 路径列表
    """
    if not node_list:  # 所有的情况已经遍历完，node_list为[].不存在解
        return []
    if len(node_list) == h * w - len(s_i):  # 找到一个解
        return node_list
    else:
        # 判断最后一个网格是否有可以去的网格
        node, sign = node_list[-1]
        can_go_list = can_go(node, map)
        if sign > len(can_go_list) - 1:  # 都去过了
            next_node = node_list[:-1]  # 就把最后一个网格去除掉
            if not next_node:
                return []
            else:
                # 开始往前回溯到还有选择余地的网格
                for l in range(len(node_list) - 2, -1, -1):
                    current_node, node_sign = node_list[l]
                    can_g = can_go(current_node, map)
                    if node_sign <= len(can_g) - 1:  # 说明有选择的余地
                        next_node = node_list[:l + 1]
                        if not next_node:
                            break
                        else:
                            next_node[-1][1] += 1
                            return find_one_path_dfs(next_node, map)
                # 所有的都没有选择的余地了
                return []

        else:  # 有可以去的网格，
            #  选择之前没有出现过的网格,并且要保证添加的网格是合理的
            have_node = [c[0] for c in node_list]  # 已经在路径中的网格
            next_node = node_list
            #  只有之前没有出现过，并且是合理的网格，才可以添加到路径中
            try:
                if can_go_list[sign] in have_node:
                    judge_reason = have_node
                else:
                    judge_reason = have_node + [can_go_list[sign]]
                while can_go_list[sign] in have_node or (not judge_area_indived(judge_reason, map)):
                    next_node[-1][1] += 1
                    sign += 1
                    # 判断这个节点是否是合理的
                    if can_go_list[sign] in have_node:
                        judge_reason = have_node
                    else:
                        judge_reason = have_node + [can_go_list[sign]]

                next_node.append([can_go_list[sign], 0])
                return find_one_path_dfs(next_node, map)
            except IndexError:
                next_node = node_list[:-1]
                if not next_node:
                    return []
                else:
                    next_node[-1][1] += 1
                    return find_one_path_dfs(next_node, map)


def find_one_path_plot(map):
    """
    展示寻找到的一条路径
    :param map: 表示图的数组
    :return: 图示
    """
    plt.ion()
    # 首先绘制图
    fig, ax1 = plt.subplots()
    # 主刻度
    ax1.set_xticks(np.arange(Map_Width))
    ax1.set_yticks(np.arange(Map_Height))
    # 绘图
    af = col.LinearSegmentedColormap.from_list('anfany', [Stone_Color, Walk_Color, Start_Color])
    ax1.imshow(map, cmap=af)
    # 像相当于次刻度
    ax1.set_xticks(np.arange(Map_Width) + 0.5, minor=True)
    ax1.set_yticks(np.arange(Map_Height) + 0.5, minor=True)
    # 添加网格
    ax1.xaxis.grid(True, which='minor', lw=2, c='snow')
    ax1.yaxis.grid(True, which='minor', lw=2, c='snow')

    #  不同的节点
    walk = mpatches.Patch(color=Walk_Color, label='可走')
    stone = mpatches.Patch(color=Stone_Color, label='不可走')
    start = mpatches.Patch(color=Start_Color, label='开始点')
    path = mpatches.Patch(color=Path_Color, label='路径')

    # 添加图例
    plt.legend(handles=[walk, stone, start],
               bbox_to_anchor=(0.0, -0.13, 1, .102), loc='lower left',
               ncol=3, mode="expand", borderaxespad=0.)

    plt.title('一笔画完问题，方法：dfs，寻找路径…………')
    plt.pause(0.0001)
    start_time = time.clock()
    path_list = find_one_path_dfs([[Start_Index, 0]], map)
    # 添加路径倒计时

    # 在图中添加路径
    if not path_list:
        plt.title('不存在解, 用时：%.3fs' % (time.clock() - start_time))
    else:
        x = [p[0][1] for p in path_list]
        y = [p[0][0] for p in path_list]
        ax1.plot(x, y, '-o', c=Path_Color, lw=18)
        plt.title('路径添加完毕，方法：dfs, 用时：%.3fs' % (time.clock() - start_time))
        # 添加图例
        plt.legend(handles=[walk, stone, start, path],
                   bbox_to_anchor=(-0.1, -0.13, 1.2, .102), loc='lower left',
                   ncol=4, mode="expand", borderaxespad=0.)

    plt.ioff()
    plt.show()


hh = nodes()

find_one_path_plot(hh)
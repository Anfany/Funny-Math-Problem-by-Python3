# -*- coding：utf-8 -*-
# &Author  AnFany

"""
根据描述迷宫的数组，利用A*算法获得从开始网格到结束网格的路径
因为解决的迷宫是完美迷宫，任何的两点之间只存在唯一的路径，
但是A*算法是可以获得多条路径中的最优的
"""


#  利用A*获得起始点到结束点的最优路径
def point_go(np_array, cell_index):
    """
    获得索引为[x, y]的网格的周围的网格
    :param np_array: 描述迷宫的二维数组
    :param cell_index: 网格索引
    :return: 可以去的索引的集合，索引为tuple形式
    """
    point_list = []
    height, length = len(np_array[0]), len(np_array)
    x, y = cell_index
    # 上
    if x >= 1:
        if np_array[x - 1, y] != 1:
            point_list.append((x - 1, y))
    # 下
    if x < length - 1:
        if np_array[x + 1, y] != 1:
            point_list.append((x + 1, y))
    # 左
    if y >= 1:
        if np_array[x, y - 1] != 1:
            point_list.append((x, y - 1))
    # 右
    if y < height - 1:
        if np_array[x, y + 1] != 1:
            point_list.append((x, y + 1))
    return point_list


def manhattan(s_cell_index, e_cell_index):
    """
    计算索引为s_cell_index, 和e_cell_index网格之间的曼哈顿距离
    曼哈顿距离：对应网格的横坐标差的绝对值与纵坐标的差的绝对值之和
    :param s_cell_index: 开始网格的索引
    :param e_cell_index: 结束网格的索引
    :return: 曼哈顿距离
    """
    a, b = s_cell_index
    c, d = e_cell_index
    return abs(a - c) + abs(b - d)


def a_star_best_path(np_array, start_cell, end_cell):
    """
    利用A*算法，返回迷宫中从起始点到结束点的最短路径
    :param np_array: 描述迷宫的数组
    :param start_cell: 起始点的索引
    :param end_cell: 结束点的索引
    :return: 最短路径经过的网格的索引列表
    """
    # 需要进行索引的转换
    start_cell = [2 * s + 1 for s in start_cell]
    end_cell = [2 * e + 1 for e in end_cell]

    # 开始A*算法
    close_list = {}  # 已经走过的网格的集合,
    open_list = {tuple(start_cell): [start_cell, 0]}   # 将要走的网格的集合
    while tuple(end_cell) not in open_list and open_list:
        #  选择open_list里面代价函数最小的网格
        cost_least = min(open_list.items(), key=lambda k: k[1][1])[0]

        # 计算可以去的相邻的网格
        point_list = point_go(np_array, cost_least)

        copy_open_list = open_list.copy()
        if point_list:
            for j in point_list:
                if j in close_list:  # 忽略
                    pass
                elif j in open_list:  # 需要对比值，选择较小的，并且更改父亲的节点
                    new_cost = 1 + manhattan(j, end_cell)
                    if new_cost < open_list[j][1]:
                        copy_open_list[j][0] = list(cost_least)
                else:
                    copy_open_list[j] = [list(cost_least), 1 + manhattan(j, end_cell) + open_list[tuple(cost_least)][1]]

        #  存储到已经走过的网格中
        close_list[cost_least] = open_list[cost_least][0]
        del copy_open_list[cost_least]

        open_list = copy_open_list

    if not open_list:  # 无解
        return []
    else:  # 获得最佳的路径
        close_list[tuple(end_cell)] = open_list[tuple(end_cell)][0]
        end_sign = 0
        path_list = [end_cell]
        while end_sign != start_cell:
            end_sign = close_list[tuple(path_list[-1])]
            path_list.append(end_sign)
        return path_list[::-1]




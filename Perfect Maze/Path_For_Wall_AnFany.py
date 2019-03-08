# -*- coding：utf-8 -*-
# &Author  AnFany

"""
根据描述迷宫的字典，利用A*算法获得从开始网格到结束网格的路径
因为解决的迷宫是完美迷宫，任何的两点之间只存在唯一的路径，
但是A*算法是可以获得多条路径中的最优的
"""


def judge_cell_go(a, b, cell_sign, wall_dict):
    """
    判断从编号为cell_sign的网格，可以去的网格的集合
    :param a: 表示迷宫的大小
    :param b: 网格的横坐标
    :param cell_sign: 网格的编号
    :param wall_dict: 描述迷宫墙的字典，值为1的没有墙，值为0的不可以过去
    :return: 可以去的网格的编号集合
    """
    walkable_cell_sign = []
    all_cells = a * b
    row, column = cell_sign // b, cell_sign % b
    # 上面的网格编号
    up_sign = (row - 1) * b + column
    if 0 <= up_sign:
        if wall_dict[(cell_sign, 'u')] == 1 and wall_dict[(up_sign, 'd')] == 1:
            walkable_cell_sign.append(up_sign)

    # 下面的网格编号
    down_sign = (row + 1) * b + column
    if down_sign < all_cells:
        if wall_dict[(cell_sign, 'd')] == 1 and wall_dict[(down_sign, 'u')] == 1:
            walkable_cell_sign.append(down_sign)

    # 右面的网格编号
    right_sign = cell_sign + 1
    if right_sign % b != 0:
        if wall_dict[(cell_sign, 'r')] == 1 and wall_dict[(right_sign, 'l')] == 1:
            walkable_cell_sign.append(right_sign)

    # 上面的网格编号
    left_sign = cell_sign - 1
    if left_sign % b != b - 1:
        if wall_dict[(cell_sign, 'l')] == 1 and wall_dict[(left_sign, 'r')] == 1:
            walkable_cell_sign.append(left_sign)

    return walkable_cell_sign


def manhattan(a, b, cell_1, cell_2):
    """
    计算网格编号为cell_1, cell_2的网格之间的曼哈顿距离，返回网格中心点坐标对应的距离
    曼哈顿距离：对应网格的横坐标差的绝对值与纵坐标的差的绝对值之和
    :param a: 迷宫的行数
    :param b: 迷宫的列数
    :param cell_1: 开始的网格编号
    :param cell_2: 结束的网格编号
    :return: 曼哈顿距离
    """
    cell_1_center_x, cell_1_center_y = cell_1 % b + 0.5, a - cell_1 // b - 1 + 0.5
    cell_2_center_x, cell_2_center_y = cell_2 % b + 0.5 , a - cell_2 // b - 1 + 0.5
    return abs(cell_1_center_x - cell_2_center_x) + abs(cell_1_center_y - cell_2_center_y)


def a_star_best_path(a, b, maze_dict, enter_cell_sign, outer_cell_sign):
    """
    利用A*算法，返回迷宫中从起始网格到结束网格的最短路径
    :param a: 迷宫的行数
    :param b: 迷宫的列数
    :param maze_dict: 描述迷宫墙的字典
    :param enter_cell_sign: 起始的网格编号
    :param outer_cell_sign: 结束的网格编号
    :return: 最短的路径
    """

    # 开始A*算法
    close_list = {}  # 已经走过的网格的集合
    open_list = {enter_cell_sign: [enter_cell_sign, 0]}   # 存储将要走的网格的集合

    # 当结束网格在已经遍历的路径里，或者将要走的网格为空时，结束循环。前者说明找到答案，后者说明题目无解
    while outer_cell_sign not in open_list and open_list:
        #  选择open_list里面代价函数最小的网格
        cost_least_cell = min(open_list.items(), key=lambda k: k[1][1])[0]

        # 计算可以去的相邻的网格
        cell_list = judge_cell_go(a, b, cost_least_cell, maze_dict)

        copy_open_list = open_list.copy()

        if cell_list:
            for j in cell_list:
                if j in close_list:  # 忽略
                    pass
                elif j in open_list:  # 需要对比值，选择较小的，并且更改父亲的节点
                    new_cost = 1 + manhattan(a, b, j, outer_cell_sign)
                    if new_cost < open_list[j][1]:
                        copy_open_list[j][0] = cost_least_cell
                else:
                    copy_open_list[j] = [cost_least_cell,
                                         1 + manhattan(a, b, j, outer_cell_sign) + open_list[cost_least_cell][1]]

        #  存储到已经走过的网格中
        close_list[cost_least_cell] = open_list[cost_least_cell][0]
        del copy_open_list[cost_least_cell]

        open_list = copy_open_list

    if not open_list:  # 无解
        path_list = []
    else:  # 获得最佳的路径
        close_list[outer_cell_sign] = open_list[outer_cell_sign][0]
        end_sign = -1
        path_list = [outer_cell_sign]
        while end_sign != enter_cell_sign:
            end_sign = close_list[path_list[-1]]
            path_list.append(end_sign)

    # 将路径中的网格编号，转换为网格的中心点的坐标序列，便于绘图
    coordinate_x, coordinate_y = [], []

    #  因为路径是从终点，一步步寻找到起点的，因此需要逆序
    path_list = path_list[::-1]
    for p in path_list:
        coordinate_x.append(p % b + 0.5)
        coordinate_y.append(a - p // b - 0.5)
    return path_list, coordinate_x, coordinate_y





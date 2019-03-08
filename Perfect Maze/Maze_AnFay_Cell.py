# -*- coding：utf-8 -*-
# &Author  AnFany

"""
Prim算法，遍历表示路的网格生成完美迷宫，A*算法获得从出口到入口的最优路径
"""
import Path_For_Cell_AnFany as p_c  # A*算法
import matplotlib.patches as mpatches  # 图例的设置
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as col
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号


# 因为迷宫采用网格的形式，也就是可以利用数组形式绘图，需要根据数值的大小来区分颜色
# 数字最好是连续的，否则颜色容易不对
Wall_Color = 'k'  # 保留的墙
Wall_Number = 1

Path_Color = 'lightcyan'  # 路
Path_Number = 0

Current_Wall_Color = 'r'  # 当前选中的网格
Current_Wall_Number = 2

Candidate_Wall_Color = 'b'  # 候选区的墙
Candidate_Wall_Number = 3

#  定义出口和入口的表示，
Enter_Color = 'brown'
Enter_Number = 2
Outer_Color = 'g'
Outer_Number = 3

#  迷宫的行数和列数
Row = 9
Column = 13

#  出口和入口的索引, 设置时不要超出范围，绘图时，真正的索引就是2倍加1
Enter_Coordinate = [0, 0]  # 默认[0,0]
Outer_Coordinate = [Row-1, Column-1]  # 默认[Row-1, Column-1]

# 中间每一步的间隔时间
Tap_Time = 0.2  # 需要大于0

# 路径的颜色
Road_Color = 'purple'


def prim_generate_maze_cell(a, b, path=False):
    """
    根据Prim算法，遍历网格生成迷宫，并且动态展示迷宫的生成过程
    开始时所有的网格(表示路的，和表示墙的)均看作墙，
    :param a: 迷宫的行数
    :param b: 迷宫的列数
    :param path: 是否添加路径，默认为Ture
    :return: 表示迷宫的数组
    """
    #  因为墙和路是同等的宽度，再加上外围的墙，因此迷宫的高度和宽度会变化
    height = 2 * a + 1
    length = 2 * b + 1

    maze_array = []
    for i in range(height):
        maze_array.append([Wall_Number] * length)  # 初始所有网格为墙
    maze_array = np.array(maze_array)  # 转换为np格式的数组

    # 绘制图
    fig, ax = plt.subplots()
    plt.title('正在生成%d*%d的迷宫…………，方法：Prim算法，遍历网格' % (Row, Column))
    plt.axis('off')

    #  定义不同状态的网格
    candidate_patch = mpatches.Patch(color=Candidate_Wall_Color, label='候选')
    current_patch = mpatches.Patch(color=Current_Wall_Color, label='当前选中')
    keep_patch = mpatches.Patch(color=Wall_Color, label='保留/未曾遍历')
    remove_patch = mpatches.Patch(color=Path_Color, label='路')

    #  添加图例
    plt.legend(handles=[candidate_patch, current_patch, keep_patch, remove_patch],
               bbox_to_anchor=(0.1, -0.1, 0.8, .102), loc='lower left',
               ncol=5, mode="expand", borderaxespad=0.)

    plt.ion()
    cmap_af = col.LinearSegmentedColormap.from_list('anfany', [Wall_Color, Wall_Color])  # 开始所有的均看作墙
    ax.imshow(maze_array, cmap=cmap_af)
    plt.pause(Tap_Time)  # 展示一开始，全为墙

    # 所有网格cell的集合
    cell_list = {(i, j): 0 for i in range(1, height, 2) for j in range(1, length, 2)}  # 因为有外墙，所以从1，并且间隔1才是路。

    # 开始利用prim算法生成迷宫
    # 随机选取一个开始的网格
    key_list = list(cell_list.keys())
    random_start_sign = np.random.randint(0, len(key_list), 1)[0]
    x, y = key_list[random_start_sign]

    # 将这个网格设置为路，也就是数组中的值变为代表路的数字
    maze_array[x, y] = Path_Number

    # 计算这个网格四周相邻的网格，加入到待选网格中
    selcted_cell_list = [s for s in [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
                         if s in cell_list]
    # 候选的墙改变颜色
    for hou in selcted_cell_list:
        maze_array[hou[0], hou[1]] = Candidate_Wall_Number
    #  绘图
    cmap_af = col.LinearSegmentedColormap.from_list('anfany',  [Path_Color, Wall_Color, Candidate_Wall_Color])
    ax.imshow(maze_array, cmap=cmap_af)

    # 当候选区中有表示路的网格时，就继续，直到所有的路遍历完
    while selcted_cell_list:
        plt.pause(Tap_Time)
        #  在候选的网格系列中，随机选择一个网格
        random_sign = np.random.randint(0, len(selcted_cell_list), 1)[0]
        # 在选中的网格
        selected_x, selected_y = selcted_cell_list[random_sign]
        #  被选中的设置颜色
        maze_array[selected_x, selected_y] = Current_Wall_Number
        if len(selcted_cell_list) == 1:  # 此时只有3个数，因此只能设置3个颜色，不加判断，颜色对应不对
            cmap_af = col.LinearSegmentedColormap.from_list('anfany', [Path_Color, Wall_Color, Current_Wall_Color])
        else:
            cmap_af = col.LinearSegmentedColormap.from_list('anfany', [Path_Color, Wall_Color,
                                                                       Current_Wall_Color, Candidate_Wall_Color])
        ax.imshow(maze_array, cmap=cmap_af)
        plt.pause(Tap_Time)
        #  只要这个网格的相邻网格中，如果相邻的网格已经遍历，并且之间的墙也变为通路了
        #  则直接把选中的网格变为通路就可以了，然后再把这个网格周围的没有遍历过的加到候选区里
        #  如果虽然周围有网格已经遍历过，但是墙没有设置通路，
        #  就随机选择一个墙，变为通路就可以了

        # 也就是说如果这个网格可以直接通往别的网格，就把这个网格设置为通路，如果过不去，就在周围那些已经可以到达的网格里，随机选取一个
        # 把与其之间的墙打通就可以了

        round_cell_0 = []  # 如果不为空，说明这个网格可以直接通往别的网格，
        round_cell_1 = []  # 只有round_cell_0为空的前提下，才随机砸墙

        x, y = selected_x, selected_y
        for k in [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]:
            if k in cell_list and maze_array[k[0], k[1]] == 0:
                if maze_array[int((k[0] + x) / 2), int((k[1] + y) / 2)] == 0:
                    round_cell_0.append(k)
                else:
                    round_cell_1.append(k)

        selcted_cell_list.remove((x, y))

        if round_cell_0:
            pass
        else:
            round_cell_sign = np.random.randint(0, len(round_cell_1), 1)[0]
            se_x, se_y = round_cell_1[round_cell_sign]
            # 将这2个网格之间的网格也设为通路
            x_mid, y_mid = int((x + se_x) / 2), int((y + se_y) / 2)
            maze_array[x_mid, y_mid] = Path_Number

        # 设置为0
        maze_array[x, y] = Path_Number
        cmap_af = col.LinearSegmentedColormap.from_list('anfany', [Path_Color, Wall_Color,
                                                                   Current_Wall_Color, Candidate_Wall_Color])

        ax.imshow(maze_array, cmap=cmap_af)
        #  添加当前网格的周围网格
        for h in [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]:
            if h in cell_list and maze_array[h[0], h[1]] == Wall_Number:
                selcted_cell_list.append(h)
                maze_array[h[0], h[1]] = Candidate_Wall_Number

        cmap_af = col.LinearSegmentedColormap.from_list('anfany', [Path_Color, Wall_Color,
                                                                   Current_Wall_Color, Candidate_Wall_Color])
        ax.imshow(maze_array, cmap=cmap_af)
    # 开始添加入口，如果使用默认入口，则显示入口2字，否则显示起点
    if Enter_Coordinate == [0, 0]:
        # 迷宫的外墙去掉一部分
        maze_array[1, 0] = Enter_Number
        enter_patch = mpatches.Patch(color=Enter_Color, label='入口')
    else:
        row, column = Enter_Coordinate
        maze_array[2 * row + 1, 2 * column + 1] = Enter_Number
        enter_patch = mpatches.Patch(color=Enter_Color, label='起点')
    # 开始添加出口，如果使用默认出口，则显示出口2字，否则显示终点
    if Outer_Coordinate == [a-1, b-1]:
        # 迷宫的外墙去掉一部分
        maze_array[-2, -1] = Outer_Number
        outer_patch = mpatches.Patch(color=Outer_Color, label='出口')
    else:
        row, column = Outer_Coordinate
        maze_array[2 * row + 1, 2 * column + 1] = Outer_Number
        outer_patch = mpatches.Patch(color=Outer_Color, label='终点')

    # 有路，有墙，有出，有入 ,有4种颜色
    cmap_af = col.LinearSegmentedColormap.from_list('anfany', [Path_Color, Wall_Color, Enter_Color, Outer_Color])
    ax.imshow(maze_array, cmap=cmap_af)
    # 更新图例
    keep_patch = mpatches.Patch(color=Wall_Color, label='墙')
    plt.legend(handles=[keep_patch, remove_patch, enter_patch, outer_patch],
               bbox_to_anchor=(0.1, -0.1, 0.8, .102), loc='lower left',
               ncol=4, mode="expand", borderaxespad=0.)

    if path:
        plt.title('迷宫生成完毕,添加路径…………')
        plt.pause(Tap_Time)
        path_list = p_c.a_star_best_path(maze_array, Enter_Coordinate, Outer_Coordinate)
        if not path_list:
            plt.title('迷宫生成完毕,路径未找到')
        else:
            # 为了绘制路径，需要把索引变为图像中网格的中心坐标
            if Enter_Coordinate == [0, 0]:
                path_list.insert(0, [1, 0])
            if Outer_Coordinate == [a - 1, b - 1]:
                path_list += [[2 * a - 1, 2 * b]]
            center_x = [p[1] for p in path_list]
            center_y = [p[0] for p in path_list]
            plt.plot(center_x, center_y, 's', c=Road_Color, mfc=Road_Color, lw=2)
            road_patch = mpatches.Patch(color=Road_Color, label='路径')
            plt.legend(handles=[keep_patch, remove_patch, enter_patch, outer_patch, road_patch],
                       bbox_to_anchor=(0.1, -0.1, 0.8, .102), loc='lower left',
                       ncol=5, mode="expand", borderaxespad=0.)
            plt.title('迷宫生成完毕,路径添加完毕')

    else:
        plt.title('迷宫生成完毕')

    plt.ioff()
    plt.show()
    return maze_array


prim_generate_maze_cell(Row, Column)


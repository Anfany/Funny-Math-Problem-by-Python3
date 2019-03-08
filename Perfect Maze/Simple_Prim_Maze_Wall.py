# -*- coding：utf-8 -*-
# &Author  AnFany

"""
Prim算法生成完美迷宫，A*算法获得从出口到入口的最优路径，并用图展示
"""
import Path_For_Wall_AnFany as p_w   # A*算法获得路径

import matplotlib.patches as mpatches  # 图例的设置
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False # 显示负号

# 根据墙的不同状态，定义不同的颜色，便于观察迷宫是怎么形成的

Keep_Color = 'k'  # 固定下来的墙
Remove_Color = 'whitesmoke'  # 删除的墙

# 根据绘制墙的线条宽度
Wall_Width = 4
Remove_Width = 4.3  # 需要比普通的墙的粗度稍微大点，否则会有删除的痕迹
Side_Width = 5  # 最终，迷宫四周的墙稍微厚点，美观

# 设置迷宫的行数和列数
Row = 28
Column = 39

# 设置迷宫的入口和出口
Enter = 0  # [0, Row*Column)区间内的整数，默认为0
Outer = Row * Column - 1  # [0, Row*Column)区间内的不等于Enter的整数，默认为a*b-1

# 定义出口，入口的标识颜色
Enter_Color = 'tab:red'
Outer_Color = 'tab:green'

# 设置迷宫中的路径以及中间节点的颜色
Path_Color = 'g'
Node_Color = 'orange'


def prim_generate_maze_wall(a, b, path=True):
    """
    根据Prim算法，遍历墙生成a*b大小的迷宫，动态展示迷宫的生成过程
    :param a: 迷宫的行数
    :param b: 迷宫的列数
    :param path: 是否在最终的迷宫中添加路径，默认添加
    :return: 表示迷宫内所有墙的状态的字典
    """
    cell_number = a * b  # 迷宫的网格数，迷宫的最左上角的网格编号为0

    # 所有墙的字典，每个网格均有4面墙，存在重复的墙
    wall_dict = {(i, h): 0 for i in range(cell_number) for h in ['u', 'd', 'r', 'l']}
    wall_direction = {'u': 'd', 'd': 'u', 'l': 'r', 'r': 'l'}  # 因为存在重复的墙，删除墙的时候需要用到

    #  绘制图形
    plt.figure()
    plt.style.use('ggplot')
    # 首先设置坐标轴的刻度
    plt.xticks(list(range(b)))
    plt.yticks(list(range(a)))
    # 关闭坐标轴
    plt.axis('off')
    #  开始绘制初始的迷宫，为了美观， 内部的墙和迷宫外围的墙分开绘制
    #  为了绘图方便，存储绘制的墙
    save_wall_plot = {}
    for w in wall_dict:
        sign, direction = w
        if direction == 'd':  # 下墙
            point1_x = sign % b
            point1_y = a - sign // b - 1
            point2_x = point1_x + 1
            point2_y = point1_y
            if point2_y != 0:  # 避过下边
                plt.plot([point1_x, point2_x], [point1_y, point2_y], c=Keep_Color, lw=Wall_Width)
                save_wall_plot[(sign, 'd')] = [[point1_x, point2_x], [point1_y, point2_y]]
        if direction == 'r':  # 右墙
            point1_x = sign % b + 1
            point1_y = a - sign // b - 1
            point2_x = sign % b + 1
            point2_y = a - sign // b
            if point2_x != b:  # 避过右边
                plt.plot([point1_x, point2_x], [point1_y, point2_y], c=Keep_Color, lw=Wall_Width)
                save_wall_plot[(sign, 'r')] = [[point1_x, point2_x], [point1_y, point2_y]]
    # 开始进行Prim算法

    #  随机选择一个网格
    random_cell = np.random.randint(0, cell_number, 1)[0]
    #  将这个网格的所有的墙存进待选的墙中
    wall_list = [(random_cell, 'd'), (random_cell, 'u'), (random_cell, 'r'), (random_cell, 'l')]

    arrive_wall = [random_cell]  # 已经处理过的网格

    # 只要墙的候选列表还有没有遍历过的墙，就继续
    while wall_list:
        #  在墙的候选列表中随机选择一堵墙
        random_wall_sign = np.random.randint(0, len(wall_list), 1)[0]
        selected_wall = wall_list[random_wall_sign]

        # 根据选择的墙, 得到另一网格的编号
        current_wall_sign, current_wall_direction = selected_wall
        if current_wall_direction == 'd':  # 下面的网格
            other = (current_wall_sign // b + 1) * b + current_wall_sign % b

        elif current_wall_direction == 'u':  # 上面的网格
            other = (current_wall_sign // b - 1) * b + current_wall_sign % b

        elif current_wall_direction == 'l':  # 左面的网格
            other = current_wall_sign - 1
            if other % b == b - 1:
                other = -1  # 为了表示在迷宫外
        else:   # 右面的网格
            other = current_wall_sign + 1
            if other % b == 0:
                other = -1  # 为了表示在迷宫外

        # 判断这个墙分割的2个网格，是否在已经到达过的网格列表中，
        if 0 <= other < cell_number:
            judge_cell = [j_c for j_c in [other, current_wall_sign] if j_c not in arrive_wall]

            if len(judge_cell) == 1:
                #  需要删除两个网格之间的墙
                wall_dict[selected_wall] = 1
                wall_dict[(other, wall_direction[current_wall_direction])] = 1

                # 在图像中删除墙
                for wall in [selected_wall, (other, wall_direction[current_wall_direction])]:
                    if wall in save_wall_plot:
                        point_x, point_y = save_wall_plot[wall]
                        # 删除的墙，设置为白色，线条粗度稍微大于墙的线粗
                        plt.plot(point_x, point_y, '-o', c=Remove_Color, lw=Remove_Width, mfc=Keep_Color)
                        break
                arrive_wall.append(judge_cell[0])
                # 然后将网格周围的墙加入当前的墙的列表
                for s in [(judge_cell[0], 'd'), (judge_cell[0], 'u'), (judge_cell[0], 'r'), (judge_cell[0], 'l')]:
                    if wall_dict[s] == 0:
                        wall_list.append(s)
        # 需要从wall_list删除这个墙
        wall_list.remove(selected_wall)

    # 为了美观，加上迷宫四周
    plt.plot([0, 0], [0, a], c=Keep_Color, lw=Side_Width)  # 左边
    plt.plot([0, b], [a, a], c=Keep_Color, lw=Side_Width)  # 上边
    plt.plot([b, b], [0, a], c=Keep_Color, lw=Side_Width)  # 右边
    plt.plot([0, b], [0, 0], c=Keep_Color, lw=Side_Width)  # 下边

    # 添加入口和出口的表示,根据网格编号判断坐标
    # 如果出口或者入口是默认值, 则相应的删除掉相应的围墙
    enter_x1, enter_y1 = Enter % b, a - Enter // b - 1
    if enter_x1 == 0 and enter_y1 == a - 1:
        plt.plot([enter_x1, enter_x1], [enter_y1, enter_y1+1], '-o', c=Remove_Color,
                 lw=Side_Width, mfc=Keep_Color)
        plt.scatter([enter_x1 + .3], [enter_y1 + .5], marker='*', c=Enter_Color, s=29, alpha=1, label='入口')
    else:
        plt.scatter([enter_x1 + .3], [enter_y1 + .5], marker='*', c=Enter_Color, s=29, alpha=1, label='起点')

    outer_x1, outer_y1 = Outer % b, a - Outer // b - 1
    if outer_x1 == b - 1 and outer_y1 == 0:
        plt.plot([outer_x1+1, outer_x1+1], [outer_y1, outer_y1+1], '-o', c=Remove_Color,
                 lw=Side_Width, mfc=Keep_Color)
        plt.scatter([outer_x1 + .7], [outer_y1 + .5], marker='o', c=Outer_Color, s=29, alpha=1, label='出口')
    else:
        plt.scatter([outer_x1 + .7], [outer_y1 + .5], marker='o', c=Outer_Color, s=29, alpha=1, label='终点')

    # 更新标题
    if path:
        plt.title('%d*%d的迷宫生成完毕，添加路径……………' % (a, b))
    else:
        plt.title('%d*%d的迷宫已经生成完毕' % (a, b))
    # 更新图例
    plt.legend(bbox_to_anchor=(0.1, -0.1, 0.8, .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.)

    # 则在迷宫中添加路径
    if path:
        path_cell_sign, path_x, path_y = p_w.a_star_best_path(a, b, wall_dict, Enter, Outer)
        if not path_cell_sign:
            plt.title('未寻找到路径')
        else:
            plt.plot(path_x, path_y, '--s', c=Path_Color, mfc=Node_Color, lw=Wall_Width, label='路径')
            #  路径中添加编号
            for p_x, p_y, tip in zip(path_x, path_y, path_cell_sign):
                plt.text(p_x, p_y + 0.1, '%d' % tip, ha='center', va='bottom', fontsize=10, color=Keep_Color)
            plt.title('%d*%d的迷宫、添加路径完毕' % (a, b))
            # 更新图例
            plt.legend(bbox_to_anchor=(0.1, -0.1, 0.8, .102), loc='lower left', ncol=3, mode="expand", borderaxespad=0.)

    plt.show()
    return print('')


#  最终的函数

if __name__ == "__main__":
    prim_generate_maze_wall(Row, Column)




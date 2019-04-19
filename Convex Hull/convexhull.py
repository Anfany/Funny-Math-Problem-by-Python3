# -*- coding：utf-8 -*-
# &Author  AnFany


"""
利用利用Graham Scan算法获得凸包，并动态展示凸包的形成过程
"""

import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl
import matplotlib.patches as mpatches  # 图例的设置

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号

# 定义点的颜色
P_Init_Color = 'k'  # 初始点的颜色
P_In_Color = 'gold'  # 凸包内部的点
P_On_Color = 'brown'  # 凸包上的点
P_Judge_Color = 'magenta'  # 当前评判点

# 定义线段的颜色
L_Convex_Color = 'crimson'  # 凸包线段
L_Delete_Color = 'w'  # 被删除的线段颜色
L_Judge_Color = 'c'  # 当前评判的线段

# 定义线的粗度
L_Convex_Width = 2
L_Delete_Width = 2.2

# 定义点的size大小
P_Size = 20

# 动态显示，定义时间
Gap_Time = 1


def generate_points(n=50, x_min=-10, x_max=10, y_min=8, y_max=29):
    """
    随机生成没有重复的点的坐标,坐标值小数点后有1位数字
    :param n: 点的个数
    :param x_min: 横坐标的最小值
    :param x_max: 横坐标的最大值
    :param y_min: 纵坐标的最小值
    :param y_max: 纵坐标的最大值
    :return: 点坐标的列表
    """
    # 横坐标
    random_x = np.random.random(n)
    # 转换到定义的区间中
    transfer_x = lambda s: np.around(s * (x_max - x_min) + x_min, 1)
    x = transfer_x(random_x)

    # 纵坐标
    random_y = np.random.random(n)
    # 转换到定义的区间内
    transfer_y = lambda s: np.around(s * (y_max - y_min) + y_min, 1)
    y = transfer_y(random_y)

    #  合并
    p = np.vstack((x, y)).T
    #  去除坐标相同的点
    p = np.unique(p, axis=0)

    return p


def computer_cross_product(p1, p2, p3):
    """
    计算向量p1p2与p1p3的叉积
    :param p1: 点p1，转换后的坐标
    :param p2: 点p2，转换后的坐标
    :param p3: 点p3，转换后的坐标
    :return: 叉积
    """
    p1p2 = p2[0] - p1[0], p2[1] - p1[1]  # 向量p1p2
    p1p3 = p3[0] - p1[0], p3[1] - p1[1]  # 向量p1p3
    product = p1p3[0] * p1p2[1] - p1p3[1] * p1p2[0]  # 计算叉积
    return product


def convexhull(point_set, show_line=False):
    """
    获得这些点构成的多边形的凸包，并动态展示凸包的形成过程
    注意：计算凸包用的是转移后的坐标，绘制凸包用的是真实坐标，注意区分
    :param point_set: 点集，不包括相同的点
    :param show_line: 是否显示夹角的连线
    :return: 凸包上的点
    """
    if len(point_set) < 3:
        return print('点数少于3个，无法构成凸包')

    #  绘制图形
    plt.figure(figsize=(10, 18))
    plt.ion()
    plt.style.use('ggplot')
    plt.title('散点图')
    plt.scatter([i[0] for i in point_set], [i[1] for i in point_set], c=P_Init_Color, s=P_Size)

    #  说明不同颜色的点代表的含义
    init_point = mpatches.Patch(color=P_Init_Color, label='原始点')
    on_point = mpatches.Patch(color=P_On_Color, label='凸包上的点')
    in_point = mpatches.Patch(color=P_In_Color, label='凸包内的点')
    judge_point = mpatches.Patch(color=P_Judge_Color, label='当前评判点')

    #  说明不同颜色的线代表的含义
    convex_line = mpatches.Patch(color=L_Convex_Color, label='凸包线')
    judge_line = mpatches.Patch(color=L_Judge_Color, label='当前评判线')
    delete_line = mpatches.Patch(color=L_Delete_Color, label='删除的线')

    # 添加图例
    plt.legend(handles=[init_point, on_point, in_point, judge_point, convex_line, judge_line, delete_line],
               bbox_to_anchor=(0.1, -0.1, 0.8, .102), loc='lower left',
               ncol=5, mode="expand", borderaxespad=0.)

    #  设置显示的间隔时间
    plt.pause(Gap_Time)

    # 选出所有点中纵坐标最小的点，纵坐标相同的选择横坐标最小的点
    point_set = list(point_set)
    point_set.sort(key=lambda s: [s[1], s[0]])
    min_y_point = point_set[0]  # 参考点编号为0

    # 将上面选择的点，转移到原点，计算其他所有点转移后和原点构成的向量和x轴正向的夹角
    # 按照夹角从小到大排列，相同角度的, 按照y的降序排列
    # 这里只计算tan的值，并将tan的值分为大于等于0，小于0, 无穷三部分
    greater_equal_zero = []
    less_zero = []
    p_i = []
    for p in point_set[1:]:
        point = [p[0] - min_y_point[0], p[1] - min_y_point[1]]  # 转移后的点的坐标
        if point[0] != 0:
            tan = point[1] / point[0]
            if tan >= 0:
                greater_equal_zero.append([tan, point[1], point, p])  # tan值，y值，转移后的值(计算凸包)，转移前的值(绘图)
            else:
                less_zero.append([tan, point[1], point, p])  # tan值，y值，转移后的值(计算凸包)，转移前的值(绘图)
        else:
            p_i.append([0, point[1], point, p])  # tan值，y值，转移后的值(计算凸包)，转移前的值(绘图)

    # 大于等于0的升序排列，相同值但不为0的按照y的升序排列，相同值为0的按照x的升序排列(这个条件，选点的时候已经设置过，此处无需在设置)
    greater_equal_zero.sort(key=lambda m: [m[0], m[1]])
    # 小于0的升序排列，相同值的按照y的降序排列
    less_zero.sort(key=lambda m: [m[0], -m[1]])
    # 等于正无穷的按照y值的降序排列
    if not greater_equal_zero:
        p_i.sort(key=lambda m: m[1])
    else:
        p_i.sort(key=lambda m: -m[1])

    # 合并后，所有点是按着夹角逆时针排列的
    trans_point_angle = greater_equal_zero + p_i + less_zero  # 先是大于等于0，然后无穷，最后小于0，顺序不能错

    print(trans_point_angle)

    # 可知，trans_point_angle序列中的第一个点和最后一个点肯定在凸包上
    #  trans_point_angle序列开始位置添加第一个点P0
    trans_point_angle.insert(0, [0, 0, [0, 0], min_y_point])

    # 绘制带有编号的散点图
    plt.title('按照逆时针排列给点进行编号')
    t_p = [j[3] for j in trans_point_angle]
    for h in range(len(t_p)):
        # 绘制编号
        plt.text(t_p[h][0], t_p[h][1], '$P_{%s}$' % str(h), fontsize=14, style='oblique', ha='right', wrap=True)
        # 绘制各个点与参考点的夹角连线
        if h != 0 and show_line:
            plt.plot([t_p[0][0], t_p[h][0]], [t_p[0][1], t_p[h][1]], '--', lw=0.8, c='k')
    plt.pause(Gap_Time)

    # trans_point_angle中的前2个点p0, p1，和最后一个点一定在凸包上
    # 把前2个点p0, p1放入栈中，把p1后面的点p2作为评判点，如果向量的叉积V_p0p2*V_p0p1<0,说明p2在p0p1的逆时针方向，是对的，如果为0，
    # 说明三点共线;如果大于0，说明p2在p0p1的顺时针方向，说明P1点是凹进去的
    # 开始挨个评判
    c = [trans_point_angle[0][2], trans_point_angle[1][2]]  # 在凸包上的点的集合
    real_c = [trans_point_angle[0][3], trans_point_angle[1][3]]  # 在凸包上的点的真正的坐标

    # 绘制线段
    plt.title('凸包绘制………')
    # 绘制前2个点
    plt.plot([real_c[0][0], real_c[1][0]], [real_c[0][1], real_c[1][1]], '-', c=L_Convex_Color, lw=L_Convex_Width)
    plt.scatter([real_c[0][0], real_c[1][0]], [real_c[0][1], real_c[1][1]], c=P_On_Color, s=P_Size)
    # 绘制最后一个点和参考点
    plt.plot([real_c[0][0], trans_point_angle[-1][3][0]], [real_c[0][1], trans_point_angle[-1][3][1]],
             '-', c=L_Convex_Color, lw=L_Convex_Width)
    plt.scatter([trans_point_angle[-1][3][0]], [trans_point_angle[-1][3][1]], c=P_On_Color, s=P_Size)

    plt.pause(Gap_Time)

    for index in trans_point_angle[2:]:
        # 绘制评判的点
        plt.scatter([index[3][0]], [index[3][1]], c=P_Judge_Color)
        plt.pause(Gap_Time)

        c.append(index[2])
        real_c.append(index[3])
        #  绘制评判的曲线
        plt.plot([real_c[-2][0], real_c[-1][0]], [real_c[-2][1], real_c[-1][1]], '-', c=L_Judge_Color)
        plt.pause(Gap_Time)

        product = computer_cross_product(c[-3], c[-2], c[-1])
        if product > 0:
            c.pop(-2)
            # 连接这个点的2条线都要去掉
            plt.plot([real_c[-3][0], real_c[-2][0], real_c[-1][0]], [real_c[-3][1], real_c[-2][1], real_c[-1][1]],
                     '-', c=L_Delete_Color, lw=L_Delete_Width)
            # 说明刚才加入的点是内部的点
            plt.scatter([real_c[-2][0]], [real_c[-2][1]], c=P_In_Color)
            plt.pause(Gap_Time)
            real_c.pop(-2)

            product = computer_cross_product(c[-3], c[-2], c[-1])

            # 添加需要评判的线段
            plt.plot([real_c[-2][0], real_c[-1][0]], [real_c[-2][1], real_c[-1][1]], '-', c=L_Judge_Color)
            plt.pause(Gap_Time)

            while product > 0:
                c.pop(-2)

                # 刚才的线也要去掉
                plt.plot([real_c[-3][0], real_c[-2][0], real_c[-1][0]], [real_c[-3][1], real_c[-2][1], real_c[-1][1]],
                         '-', c=L_Delete_Color, lw=L_Delete_Width)
                # 说明刚才加入的点是内部的点
                plt.scatter([real_c[-2][0]], [real_c[-2][1]], c=P_In_Color)
                plt.pause(Gap_Time)
                real_c.pop(-2)

                # 添加需要评判的线段
                plt.plot([real_c[-2][0], real_c[-1][0]], [real_c[-2][1], real_c[-1][1]], '-', c=L_Judge_Color)
                plt.pause(Gap_Time)

                product = computer_cross_product(c[-3], c[-2], c[-1])
            # 此时需要将最后的点添加为凸包上的点
            plt.scatter([index[-1][0]], [index[-1][1]], c=P_On_Color)
            # 将线转变颜色
            plt.plot([real_c[-3][0], real_c[-2][0], real_c[-1][0]], [real_c[-3][1], real_c[-2][1], real_c[-1][1]],
                     '-', c=L_Convex_Color)
            plt.pause(Gap_Time)
        #  绘制图
        else:
            # 说明刚才加入的点是凸包上的点
            plt.scatter([index[-1][0]], [index[-1][1]], c=P_On_Color)
            # 刚才的线也要变为凸包上的
            plt.plot([real_c[-3][0], real_c[-2][0], real_c[-1][0]], [real_c[-3][1], real_c[-2][1], real_c[-1][1]],
                     '-', c=L_Convex_Color)
            plt.pause(Gap_Time)
            pass

    plt.title('凸包绘制完成')
    # 更新图例
    plt.legend(handles=[on_point, in_point, convex_line, delete_line],
               bbox_to_anchor=(0.1, -0.1, 0.8, .102), loc='lower left',
               ncol=5, mode="expand", borderaxespad=0.)
    plt.ioff()
    plt.show()
    return c

#  最终的函数


if __name__ == "__main__":
    p_s = generate_points()
    convexhull(p_s)












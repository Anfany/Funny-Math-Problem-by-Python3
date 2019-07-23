# -*- coding：utf-8 -*-
# &Author  AnFany

# 引入绘图库包
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号
import numpy as np
from scipy.integrate import quad


# 保存结果的路径
File_Path = r'C:\Users\GWT9\Desktop'


def computer_node(a_x, a_y, b_x, b_y):
    """
    计算点(a_x, 0)和点(0, a_y)构成的直线与点(b_x, 0)和点(0, b_y)构成的直线的交点的坐标
    :param a_x: 某点的x轴坐标，大于0
    :param a_y: 某点的y轴坐标，大于0
    :param b_x: 某点的x轴坐标，大于0
    :param b_y: 某点的y轴坐标，大于0
    :return: 交点坐标
    """
    if a_x == 0:
        return [0, b_y]

    if b_x == 0:
        return [0, a_y]

    if a_y == 0:
        return [b_x, 0]

    if b_y == 0:
        return [a_x, 0]

    else:
        x = (b_y - a_y) / (b_y / b_x - a_y / a_x)
        y = (b_x - a_x) / (b_x / b_y - a_x / a_y)
    return [x, y]


def get_piont(x, y, n):
    """
    返回构成直线的2个点的坐标序列
    :param x: x轴的间隔
    :param y: y轴的间隔
    :param n: 直线的条数
    :return: 构成直线的点对的序列
    """
    point_pair = []

    for i in range(n):
        # 一条直线的2个点
        # x轴上的点
        x_one_point = [x * (i + 1), 0]
        # 对应的y轴上的点
        y_one_point = [0, y * (n - i)]
        point_pair.append([x_one_point, y_one_point])
    return point_pair


def get_area(x, y, n):
    """
    图形与XY轴原点构成的面积
    :param x: x轴的间隔
    :param y: y轴的间隔
    :param n: 直线的条数
    :return: 交点序列，以及构成的面积
    """
    point_pair = get_piont(x, y, n)

    # 存储面积
    area = 0

    # 存储交点序列
    node_list = []

    # 首先添加上y轴
    point_pair.insert(0, [[0, 0], [0, point_pair[0][1][1]]])
    for a, b in zip(point_pair[:-1], point_pair[1:]):
        # 计算交点
        n_a_b = computer_node(a[0][0], a[1][1], b[0][0], b[1][1])
        node_list.append(n_a_b)
        area += (n_a_b[1] * x) / 2

    # 交点添加直线与X轴的交点
    node_list.append([point_pair[-1][0][0], 0])
    return node_list, area


def get_area_list(x, y, n):
    """
    图形的个数n(n+1)/2,输出每个图形的面积。直线按照从上到线依次编号，
    图形右下角顶点的直线标识作为该图形的标识
    将结果写入到txt文件中
    :param x: x轴的间隔
    :param y: y轴的间隔
    :param n: 直线的条数
    :return: 被直线簇切割的所有图形的面积列表
    """
    # 获取直线的字典：字典的键从0到n，值为代表一条直线的3个点
    line_dict = {}
    for i in range(0, n):
        line_dict[i] = [[x * (i + 1), 0], [0, y * (n - i)]]
    line_dict[n] = [[x * n, 0], [0, 0]]

    # 存储总的面积
    sum_area = 0
    # 存储最小的面积,初始的值
    min_area = 0
    # 存储面积的字典
    area_dict = {}
    # 存储面积的列表
    area_list = []  # 按照从上到下，从左到右的顺序开始计算面积
    # 开始遍历
    for k in range(n):
        column_list = []  # 一列中的面积，
        for h in range(k + 1, n + 1):
            # 计算图形编号为kh的图形的面积
            # 首先计算交点
            point_node = computer_node(line_dict[k][0][0], line_dict[k][1][1], line_dict[h][0][0], line_dict[h][1][1])
            # 计算这2条直线与整个Y轴构成的大三角形的面积
            big_area = point_node[0] * (h - k) * y / 2
            # 需要减去其中包含的其他的小图形的面积
            for s in range(k+1):
                for b in range(k+1, h+1):
                    if '%d_%d' % (s, b) in area_dict:
                        big_area -= area_dict['%d_%d' % (s, b)]
            sum_area += big_area
            if min_area:
                min_area = min(min_area, big_area)
            else:
                min_area = big_area
            # 剩下的就存储起来
            area_dict['%d_%d' % (k, h)] = big_area
            # 存储在列表里
            column_list.append(str('%.8f' % big_area))  # 便于展示，采用字符串形式
        if not area_list:
            area_list.append(column_list)
        else:
            area_list.append([' ' * len(column_list[0]) for j in range(k)] + column_list)

    # 开始计算面积的比值
    computer = [[str('%.2f' % (eval(j) / min_area)) if ' ' not in j else j for j in t] for t in area_list]

    # 字符串内容
    str_start = 'X轴间隔：%d个单位 Y轴间隔：%d个单位 直线条数为：%d \n \n' % (x, y, n)
    str_area = '面积总和为：%.3f 最小面积为：%.3f \n \n' % (sum_area, min_area)
    str_doc = '以下是%d个图形的面积 \n \n' % (n*(n+1)/2)
    # 将结果写入到txt文本中
    with open(r'%s/result.txt' % File_Path, "w") as f:
        f.write(str_start + str_area + str_doc)
        area_str = np.array(area_list, dtype=object).T
        for h in area_str:
            str_a = ''
            for s in h:
                if ' ' not in s:
                    str_a += str(s) + ' '
                else:
                    break
            f.write(str_a + '\n')
        f.write('\n下面是各个图形的面积与最小图形的面积的比值\n\n')
        c_str = np.array(computer, dtype=object).T
        for m in c_str:
            str_p = ''
            for l in m:
                if ' ' not in l:
                    str_p += str(l) + ' '
                else:
                    break
            f.write(str_p + '\n')
    print('面积结果写入完毕')
    return '面积和：', sum_area, '最小面积：', min_area


def fit_func(num, x, y, n):
    """
    绘制图形
    :param num: 根据x值返回拟合的函数值
    :param x: x轴的间隔
    :param y: y轴的间隔
    :param n: 直线的条数
    :return: 拟合的函数
    """
    return ((n + 1) ** 0.5 - (num / x) ** 0.5) ** 2 * y


def plot_fig(x, y, n, s=7, a_c='k', c_c='b'):
    """
    绘制图形
    :param x: x轴的间隔
    :param y: y轴的间隔
    :param n: 直线的条数
    :param s: 图片的大小
    :param a_c: 坐标轴的颜色
    :param c_c: 连线的颜色
    :return: 图像
    """
    point_pair = get_piont(x, y, n)
    fig = plt.figure(figsize=(s+3, s))
    ax = fig.add_subplot(121)
    # 绘制竖直、水平方向的线
    ax.plot([0, 0], [0, point_pair[0][1][1]], c=a_c, lw=2)
    ax.plot([0, point_pair[-1][0][0]], [0, 0], c=a_c, lw=2)
    # 绘制直线
    sign = 0  # 图例标识
    for i in point_pair:
        if not sign:
            ax.plot(i[0], i[1], c=c_c, lw=0.8, label='直线簇')
            sign = 1
        else:
            ax.plot(i[0], i[1], c=c_c, lw=0.8)

    # 设置为横纵刻度间距离是一样的
    ax.set_aspect('equal', 'box')

    # 删除掉原始的坐标轴
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')

    # 设为原点相交
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))

    if n <= 15:
        # 添加x轴,y轴刻度,n过大时，标签回覆盖，因此在用默认的标签
        plt.xticks(np.linspace(start=0, stop=point_pair[-1][0][0], num=n+1))
        plt.yticks(np.linspace(start=0, stop=point_pair[0][1][1], num=n+1))

    # 散点展示交点
    node_list, area = get_area(x, y, n)
    node_list_x = [s[0] for s in node_list]
    node_list_y = [s[1] for s in node_list]
    ax.scatter(node_list_x, node_list_y, marker='o', s=29, c='g', label='直线簇的交点')

    # 绘制拟合图像，为了使得到的曲线光滑，需要多取一些点
    y_list = []  # y值
    x_list = np.linspace(0, point_pair[-1][0][0], n * 10)
    for num in x_list:
        y_list.append(fit_func(num, x, y, n))

    # 绘制拟合函数的图像
    ax.plot(x_list, y_list, '--', c='r', lw=1, label='拟合交点的曲线')

    # 展示图例
    plt.legend(loc='upper right')

    # 展示x，y轴标题
    plt.xlabel('x轴间隔$\mathbf{a}$：%d个单位' % x)
    plt.ylabel('y轴间隔$\mathbf{b}$：%d个单位' % y)

    # 面积分布
    get_area_list(x, y, n)
    plt.title('直线簇围成的%d个图形的面积分布参见txt文件\n \n 其中最小图形的面积为：\n$\mathbf{MS=\\frac{ab}{n+1}}=\\frac{%d*%d}{%d+1}=%.4f$'
              % (n*(n+1)/2, x, y, n, x * y / (n + 1)))
    # 说明
    str_title = '直线簇中直线的条数为：\n$n=%d$ \n直线簇与XY轴围成的面积：\n$\mathbf{SL=\\frac{abn(n+2)}{6}} =\\frac{%d*%d*%d*(%d+2)}{6}=%.4f$' \
                % (n, x, y, n, n, x*y*n * (n+2) / 6)

    ax = fig.add_subplot(222)
    # 拟合曲线与XY轴构成的面积通过积分可以得到
    area = quad(lambda a: ((n + 1) ** 0.5 - (a / x) ** 0.5) ** 2 * y, 0, point_pair[-1][0][0])
    # 文字说明
    str_curve = '拟合的曲线方程为：$\mathbf{Y=(\sqrt{n+1}-\sqrt{\\frac{X}{a}})^2 * b}$ \n' \
                '通过曲线积分计算得到的面积：\n$\mathbf{SC=\int_{0}^{n}Ydx}=\int_{0}^{%d}[(\sqrt{%d}-\sqrt{\\frac{X}{%d}})^2*%d]dx=%.4f$' \
                % (n, n+1, x, y, area[0])
    # 面积差
    area_str = 'n从1到无穷大面积误差范围：$ \mathbf{\\frac{a * b * (6 - 4\sqrt{2})}{3} \leq SC-SL ' \
               '\less \\frac{a * b}{6}}$ ' \
               '\n此时$\\frac{%d * %d * (6 - 4\sqrt{2})}{3} =%.3f \leq SC-SL= %.3f \less \\frac{%d * %d}{6}=%.3f $' \
               % (x, y, x * y * (6- 4 * 2 ** 0.5)/3, area[0] - x*y*n * (n+2) / 6, x, y, x*y/6)

    plt.axis('off')
    ax.text(0, 0, str_title + '\n' * 2 + str_curve + '\n' * 2 + area_str, fontsize=11)

    # 计算交点横坐标对应的拟合曲线的值与纵坐标的差
    ax = fig.add_subplot(224)
    sub_number = []
    x_number = []
    for no in node_list:
        sub_number.append(fit_func(no[0], x, y, n) - no[1])
        x_number.append(no[0])
    ax.plot(x_number, sub_number, '.-', c='tab:red')
    plt.grid()
    plt.title('交点横坐标对应的曲线的值减去交点的纵坐标')
    # 图片显示
    plt.show()
    return print('图片生成完毕')


# 主函数
if __name__ == "__main__":
    # 标准形式，XY轴间隔均为1
    plot_fig(3, 4, 35)



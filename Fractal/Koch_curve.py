# -*- coding：utf-8 -*-
# &Author  AnFany


# 利用python绘制科赫雪花曲线
from math import cos, sin, radians
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl  # 作图显示中文

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 设置中文字体为新宋体


class KOCH():
    def __init__(self):

        # 设定图像的横纵坐标最大最小值, 最大最小值
        self.x_min_max = [4, 10]
        self.y_min_max = [1, 8]

        # 初始的三角形三个点的位置的横纵坐标系列，因为要保证凸起的点是逆时针旋转的，因此下面的点的顺序要是顺时针的
        self.initial_point = [[sum(self.x_min_max) / 2,  self.x_min_max[1] - 1, self.x_min_max[0] + 1],
                              [self.y_min_max[1] - 1, self.y_min_max[0] + 1, self.y_min_max[0] + 1]]

        # 迭代次数
        self.t = 3

        self.p_fig = r'C:\Users\GWT9\Desktop'  # 保存图片的地址

    def plot_koch(self):
        """
        利用迭代的方法生成科赫雪花曲线
        :return: 科赫雪花曲线
        """
        # 初始的三个点的坐标

        times = 1
        # 存储需要连接的点的横、纵坐标

        need_to_line_x = self.initial_point[0] + [self.initial_point[0][0]]
        need_to_line_y = self.initial_point[1] + [self.initial_point[0][0]]

        while 1:

            # 遍历当前所有需要连接的点
            cc_x = []
            cc_y = []
            for nx1, ny1, nx2, ny2 in zip(need_to_line_x[:-1], need_to_line_y[:-1],
                                          need_to_line_x[1:], need_to_line_y[1:]):

                cc_x.append(nx1)
                cc_y.append(ny1)

                # 两点之间线段的，2个三分点的坐标
                x1 = nx1 + (nx2 - nx1) / 3
                x2 = nx1 + 2 * (nx2 - nx1) / 3

                y1 = ny1 + (ny2 - ny1) / 3
                y2 = ny1 + 2 * (ny2 - ny1) / 3

                cc_x.append(x1)
                cc_y.append(y1)

                # 计算突出的点，
                new_x = (x2 - x1) * cos(radians(60)) - (y2 - y1) * sin(radians(60)) + x1

                new_y = (x2 - x1) * sin(radians(60)) + (y2 - y1) * cos(radians(60)) + y1

                cc_x.append(new_x)
                cc_y.append(new_y)

                cc_x.append(x2)
                cc_y.append(y2)

            cc_x.append(cc_x[0])
            cc_y.append(cc_y[0])

            need_to_line_x = cc_x.copy()
            need_to_line_y = cc_y.copy()

            times += 1
            if times > self.t:
                break

        plt.plot(need_to_line_x, need_to_line_y, c='k', lw=1)
        plt.axis('off')
        plt.title('koch雪花曲线迭代图 迭代次数%d' % self.t)
        plt.show()
        plt.savefig(r'%s\koch.png' % self.p_fig)
        return print('koch雪花曲线迭代图片保存完毕')


# 主函数
if __name__ == "__main__":
    # 随机方法
    k = KOCH()
    k.plot_koch()



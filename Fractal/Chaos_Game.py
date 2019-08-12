# -*- coding：utf-8 -*-
# &Author  AnFany


# 利用python绘制混沌游戏产生的图形，也就是

from matplotlib.path import Path
from matplotlib.patches import PathPatch
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl  # 作图显示中文

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 设置中文字体为新宋体


class CHAOS():
    def __init__(self):

        # 设定图像的横纵坐标最大最小值, 最大最小值
        self.x_min_max = [4, 10]
        self.y_min_max = [1, 8]

        # 初始的三个点的位置的横纵坐标系列
        self.initial_point = [[sum(self.x_min_max) / 2, self.x_min_max[0] + 1, self.x_min_max[1] - 1],
                              [self.y_min_max[1] - 1, self.y_min_max[0] + 1, self.y_min_max[0] + 1]]

        # 迭代次数
        self.t = 8  # 该数值越大，产生的图像越接近于谢尔宾斯基三角形

        # 初始三个点的颜色
        self.i_c = 'tab:red'
        # 第四个随机点的颜色
        self.f_c = 'tab:green'
        # 其他点的颜色
        self.o_c = 'tab:blue'

        self.p_fig = r'C:\Users\GWT9\Desktop'  # 保存图片的地址

    def SierpinskiTriangle_chaos_game(self):
        """
        绘制混沌游戏产生的图形，也就是利用随机方法生成谢尔宾斯基三角形
        :return: 图形
        """
        # 需要绘制的散点的集合
        need_plot = self.initial_point
        # 随机选取第四个点的位置，为了便于展示，在横纵坐标的范围内随机选取一点。
        the_firth_point = [np.random.randint(self.x_min_max[0], self.x_min_max[1] + 1, 1),
                           np.random.randint(self.y_min_max[0], self.y_min_max[1] + 1, 1)]
        times = 0

        # 第四个点添加到集合中
        need_plot[0].append(the_firth_point[0])
        need_plot[1].append(the_firth_point[1])

        while 1:
            # 在初始的3个点中随机选择1个。
            random = np.random.randint(0, 3, 1)[0]
            # 被选中的点
            selected_point_x = self.initial_point[0][random]
            selected_point_y = self.initial_point[1][random]

            # 选取这个点和最后一个新加入的点的中点作为下一个新加入的点
            next_point = [(selected_point_x + need_plot[0][-1]) / 2,
                          (selected_point_y + need_plot[1][-1]) / 2]

            need_plot[0].append(next_point[0])
            need_plot[1].append(next_point[1])

            times += 1
            if times > self.t:
                break

        # 开始绘制散点图
        plt.scatter(need_plot[0][:3], need_plot[1][:3], s=25, marker='^', c=self.i_c, label='初始点')
        plt.scatter(need_plot[0][3:4], need_plot[1][3:4], s=25, marker='*', c=self.f_c, label='第四个点')
        plt.scatter(need_plot[0][4:], need_plot[1][4:], s=5, marker='o', c=self.o_c, label='其他点')
        plt.title('谢尔宾斯基三角形:随机方法, 加入点的个数%d' % self.t)
        plt.rcParams['savefig.dpi'] = 1000  # 数值越大，图片越清晰
        plt.legend()
        plt.axis('off')

        plt.savefig(r'%s\SierpinskiTriangle_chaos.png' % self.p_fig)
        return print('SierpinskiTriangle随机图片保存完毕')

    def SierpinskiTriangle_iter_game(self):
        """
        利用迭代的方法生成谢尔宾斯基三角形
        :return: 谢尔宾斯基三角形
        """
        # 初始的三个点的坐标
        initial_point_set = [[self.initial_point[0][0], self.initial_point[1][0]],
                             [self.initial_point[0][1], self.initial_point[1][1]],
                             [self.initial_point[0][2], self.initial_point[1][2]]]

        codes = [Path.MOVETO] + [Path.LINETO] * 2 + [Path.CLOSEPOLY]
        vertices = np.array(initial_point_set + [[0, 0]], float)
        path = Path(vertices, codes)
        pathpatch = PathPatch(path, facecolor='k', edgecolor=None)

        # 开始绘图
        fig, ax = plt.subplots()
        ax.add_patch(pathpatch)

        times = 0

        # 存储需要切割的三角形
        need_to_cut = [initial_point_set]
        while 1:
            # 遍历当前所有需要切割的三角形
            cc = []
            for t in need_to_cut:
                # 获取这个三角形的三边的中点
                center_point = []
                for o, l in zip(t, t[1:] + [t[0]]):
                    center_point.append([(o[0] + l[0]) / 2, (o[1] + l[1]) / 2])
                # 新组成的三角形需要被挖空
                codes = [Path.MOVETO] + [Path.LINETO] * 2 + [Path.CLOSEPOLY]
                vertices = np.array(center_point + [[0, 0]], float)
                path = Path(vertices, codes)
                pathpatch = PathPatch(path, facecolor='white', edgecolor=None)
                ax.add_patch(pathpatch)

                # 此时需要将新形成的三个三角形添加到需要切割的三角形集合中

                cc.append([t[0], center_point[0], center_point[2]])
                cc.append([center_point[0], t[1], center_point[1]])
                cc.append([center_point[1], t[2], center_point[2]])

            need_to_cut = cc.copy()

            times += 1
            if times > self.t:
                break
        ax.set_title('谢尔宾斯基三角形:迭代方法, 迭代次数%d' % self.t)
        ax.set_xlim(self.x_min_max[0], self.x_min_max[1])
        ax.set_ylim(self.y_min_max[0], self.y_min_max[1])
        plt.axis('off')
        plt.savefig(r'%s\SierpinskiTriangle_iter.png' % self.p_fig)
        return print('SierpinskiTriangle迭代图片保存完毕')


# 主函数
if __name__ == "__main__":
    # 随机方法
    s = CHAOS()
    s.t = 20000
    s.SierpinskiTriangle_chaos_game()

    # 迭代方法
    s = CHAOS()
    s.t = 8
    s.SierpinskiTriangle_iter_game()

# !/usr/bin/env python3.8.8
# author:Anfany
# datetime:2021/4/8 15:31

# 经过N个控制点的贝塞尔曲线的绘制

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
from scipy.special import comb  # 直接法

# 显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']


class BEZIERPRO:

    def __init__(self, N, pointlist=None, closed=True):
        self.n = N  # 最小值为2
        self.pl = pointlist  # 如果为None，则随机选择N个点。如果不为空，则以此列表中的个数为准
        self.c = closed  # 曲线是否封闭

        self.t_tap = 0.008
        self.t_list = np.arange(0, 1, self.t_tap)
        self.generate_point()

        # 新的控制点
        self.control_p, self.new_pl = self.get_point()
        self.n_list = [len(k) for k in self.new_pl]
        # 贝塞尔曲线的点
        self.bezier_list = {}

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.fig.subplots_adjust(bottom=0.2)
        self.clist = self.get_color_list()

    # 不同阶的颜色
    def get_color_list(self):
        colorlist = {}
        for j in range(len(self.n_list)):
            color_list = []
            for i in range(self.n_list[j]):
                color_list.append(cm.rainbow(i / self.n_list[j]))
            colorlist[j] = color_list[::-1]
        return colorlist

    # 产生随机点:横纵坐标在-5到5
    def generate_point(self):
        def gp(tap=10):
            xp = tap * np.random.random(self.n) - tap / 2
            yp = tap * np.random.random(self.n) - tap / 2
            pointlist = [np.array([i, j]) for i, j in zip(xp, yp)]
            return pointlist

        if self.pl is None:
            self.pl = gp()
        else:
            self.pl = [np.array(h) for h in self.pl]
            self.n = len(self.pl)

    # 根据给定的点生成虚拟的控制点
    def get_point(self):
        if list(self.pl[0]) != list(self.pl[-1]):
            self.pl += list(self.pl[:2])
        control_point = []
        for pin, pva in enumerate(self.pl[:-2]):
            middle_1 = (pva + self.pl[pin + 1]) / 2
            middle_2 = (self.pl[pin + 1] + self.pl[pin + 2]) / 2
            h1 = (pva[0] - self.pl[pin + 1][0]) ** 2 + (pva[1] - self.pl[pin + 1][1]) ** 2
            h2 = (self.pl[pin + 1][0] - self.pl[pin + 2][0]) ** 2 + (self.pl[pin + 1][1] - self.pl[pin + 2][1]) ** 2
            h = (h1 / h2) ** 0.5
            middle_d = (middle_1 + h * middle_2) / (1 + h)
            # 根据平行四边形对角线互相平分
            no_1 = self.pl[pin + 1] + middle_1 - middle_d
            no_2 = self.pl[pin + 1] + middle_2 - middle_d

            control_point.append(no_1)
            control_point.append(no_2)

        # 根据控制点 形成多条贝塞尔曲线
        if self.c:
            new_control = [control_point[-1]] + control_point[:-1]
            sign = 0
        else:
            new_control = [control_point[-1]] + control_point[:-3]
            sign = 1
        new_pl = []
        for kinp, kvap in enumerate(self.pl[:(-2 - sign)]):
            cc = [kvap, new_control[2 * kinp], new_control[2 * kinp + 1], self.pl[kinp + 1]]
            new_pl.append(cc)

        return new_control, new_pl

    def b_m(self, t):
        self.ax.clear()  # 清空已存在的图像
        # 隐藏边
        self.ax.axis('off')
        self.ax.set_title('t=%.4ss' % str(t), fontsize=15)
        # 绘制顶点
        for pdin, pp in enumerate(self.pl[:-1]):
            self.ax.text(pp[0], pp[1], '$P_{%s}$' % pdin, fontsize=13)
            if pdin == 0:
                self.ax.scatter(pp[0], pp[1], label='$P$顶点', s=50, color='tab:green')
            else:
                self.ax.scatter(pp[0], pp[1], s=50, color='tab:green')
        # 绘制新添加的控制点
        for pdin, pp in enumerate(self.control_p):
            self.ax.text(pp[0], pp[1], '$N_{%s}$' % pdin, fontsize=13)
            if pdin == 0:
                self.ax.scatter(pp[0], pp[1], marker='^', label='$N$控制点', s=30, color='tab:red')
            else:
                self.ax.scatter(pp[0], pp[1], marker='^', s=30, color='tab:red')

        # 绘制多个控制组的原始点
        for pdin, pp in enumerate(self.new_pl):
            # 开始绘制多阶直线
            line_list = pp
            while len(line_list) > 2:
                new_list = []
                for kp, kz in zip(line_list[:-1], line_list[1:]):
                    ss = np.float64(kp + t * (kz - kp))
                    new_list.append(ss)
                # 中间的线
                xp = [op[0] for op in new_list]
                yp = [op[1] for op in new_list]
                self.ax.plot(xp, yp, '-', lw=2, marker='.', color=self.clist[pdin][self.n_list[pdin] - len(new_list)],
                             markerfacecolor=self.clist[pdin][self.n_list[pdin] - len(new_list)], markersize=15)
                line_list = new_list

            # 添加点
            x, y = np.float64(line_list[0] + t * (line_list[1] - line_list[0]))

            if pdin in self.bezier_list:
                self.bezier_list[pdin][0].append(x)
                self.bezier_list[pdin][1].append(y)
            else:
                self.bezier_list[pdin] = [[x], [y]]
            if pdin == 0:
                self.ax.plot(self.bezier_list[pdin][0], self.bezier_list[pdin][1], lw=4, color=self.clist[pdin][-1],
                             label=r'$de Casteljau$算法-$B\acute{e}zierCurve$')
            else:
                self.ax.plot(self.bezier_list[pdin][0], self.bezier_list[pdin][1], lw=4, color=self.clist[pdin][-1])

            self.ax.scatter(x, y, s=50, color=self.clist[pdin][-1])

        # 根据直接法绘制的
        for pdin, pp in enumerate(self.new_pl):
            forward_point = []
            for t in self.t_list:
                sum_p = np.array([0., 0.])
                for plin, plva in enumerate(pp):
                    sum_p += comb(3, plin) * plva * np.power(1 - t, 3 - plin) * np.power(t, plin)
                forward_point.append(sum_p)
            xpll = [op[0] for op in forward_point]
            ypll = [op[1] for op in forward_point]
            if pdin == 0:
                self.ax.plot(xpll, ypll, '--', lw=2, label=r'直接法-$B\acute{e}zierCurve$', color='gray')
            else:
                self.ax.plot(xpll, ypll, '--', lw=2, color='gray')

        self.ax.legend(fontsize=13, ncol=2, framealpha=0.1, loc=2, bbox_to_anchor=(0.0, 0.0))

    # 动态图实现
    def auto_fig(self):
        animator = animation.FuncAnimation(self.fig, self.b_m, self.t_list, interval=90)
        # 可将动图输出为gif或者视频mp4
        animator.save('Bezier_IU.gif')


# 实例1：AF
AF = [[-7.88, -0.26], [-6.16, 4.2], [-4.76, -0.06], [-6.08, 0.46],
      [-6.16, 1.2], [-3.42, 3.98], [-2, 4], [-1.18, 4],
      [-3.36, 4.28], [-3.32, -2.62], [-3.26, 1.36], [-1.1, 1.42]]

# 实例2：IU
IU = [[5, -7], [5, -3], [5.6, -2.9], [5.6, -6.5], [8.4, -6.5], [7.58, -6.18], [6.78, -5.59],
      [6.42, -4.8], [6.6, -4], [7.21, -3.42], [7.78, -3.62], [8.36, -4], [8.8, -3.62], [9.36, -3.4],
      [10, -4], [10.2, -4.79], [9.8, -5.6], [9.2, -6.17], [8.4, -6.5], [10.8, -6.57], [11.01, -6],
      [11, -4.77], [11, -3], [11.38, -3], [11.38, -4.77], [11.42, -6], [11.41, -6.6], [12.6, -6.6],
      [12.6, -3], [13, -3], [13, -6.62], [13, -7], [11, -7], [9, -7], [7, -7]]

if __name__ == '__main__':
    bezier = BEZIERPRO(4, [[-0.56,1.96],[-6.7,0.2],[-5.02,-4.36],[-2.2,-3.18]], False)
    bezier.auto_fig()

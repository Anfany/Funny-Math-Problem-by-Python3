# !/usr/bin/env python3.8.8
# author:Anfany
# datetime:2021/4/2 16:15

# N个控制点的贝塞尔曲线的绘制


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
# 显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']


class BEZIER:

    def __init__(self, N, pointlist=None):
        self.n = N  # 最小值为2
        self.pl = pointlist  # 如果为None，则随机选择N个点。如果不为空，则以此列表中的个数为准

        self.t_tap = 0.008
        self.t_list = np.arange(0, 1, self.t_tap)

        self.generate_point()

        # 贝塞尔曲线的点
        self.bezier_list = [[], []]

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.clist = self.get_color_list()

    # 不同阶的颜色
    def get_color_list(self):
        color_list = []
        for i in range(self.n):
            color_list.append(cm.rainbow(i / self.n))
        return color_list[::-1]

    # 产生随机点:横纵坐标在-5到5
    def generate_point(self):
        def gp(tap=10):
            xp = tap * np.random.random(self.n) - tap / 2
            yp = tap * np.random.random(self.n) - tap / 2
            return [np.array([i, j]) for i, j in zip(xp, yp)]

        if self.pl is None:
            self.pl = gp()
        else:
            self.pl = [np.array(h) for h in self.pl]
            self.n = len(self.pl)

    # 贝塞尔曲线方程：根据t的变化真是不同的图像状态
    def b(self, t):
        self.ax.clear()  # 清空已存在的图像
        # 隐藏边
        self.ax.axis('off')
        # 绘制原始点
        for din, p in enumerate(self.pl):
            if din == 0:
                self.ax.text(p[0], p[1], '$P_{%s}$' % din, fontsize=13)
                self.ax.scatter(p[0], p[1], label='$P_{0}$初始点', s=50, color='tab:green')
            elif din == self.n - 1:
                self.ax.text(p[0], p[1], '$P_{%s}$' % din, fontsize=13)
                self.ax.scatter(p[0], p[1], label='$P_{%s}$锚点' % din, s=50, color='tab:red')
            else:
                self.ax.text(p[0], p[1], '$P_{%s}$' % din, fontsize=13)
                if din == self.n - 2:
                    self.ax.scatter(p[0], p[1], label='$P_{1}$至$P_{%s}$控制点' % (self.n - 2), s=45,
                                    color='gray')
                else:
                    self.ax.scatter(p[0], p[1], color='gray', s=45)
        # 绘制原始点之间的连接线
        xp = [op[0] for op in self.pl]
        yp = [op[1] for op in self.pl]
        self.ax.plot(xp, yp, '-', lw=2, color=self.clist[0])

        # 开始绘制多阶直线
        line_list = self.pl
        while len(line_list) > 2:
            new_list = []
            for kp, kz in zip(line_list[:-1], line_list[1:]):
                ss = np.float64(kp + t * (kz - kp))
                new_list.append(ss)

            xp = [op[0] for op in new_list]
            yp = [op[1] for op in new_list]
            self.ax.plot(xp, yp, '-', lw=2, marker='.', color=self.clist[self.n - len(new_list)],
                         markerfacecolor=self.clist[self.n - len(new_list)], markersize=15)
            line_list = new_list

        # 添加点
        x, y = np.float64(line_list[0] + t * (line_list[1] - line_list[0]))
        self.bezier_list[0].append(x)
        self.bezier_list[1].append(y)
        self.ax.plot(self.bezier_list[0], self.bezier_list[1], lw=4, color=self.clist[-1],
                     label=r'$B\acute{e}zier\quadcurve$')
        self.ax.scatter(x, y, s=50, color=self.clist[-1])
        self.ax.legend(fontsize=15, loc=8, ncol=4, framealpha=0.1)

    # 动态图实现
    def auto_fig(self):
        animator = animation.FuncAnimation(self.fig, self.b, self.t_list, interval=90)
        animator.save('Bezier.mp4')


# 实例1：陀螺
Example1 = [[0.82, 5.88], [4.76, 6.94], [8.94, 6.32], [12.46, 3.74],
            [13.84, -1.52], [11.04, -4.76],
            [7.34, -5.74], [1.24, -4.12], [0.38, -0.26], [1.56, 4.84],
            [7.34, 4.98], [11.86, 1.24],
            [10.96, -2.84], [5.56, -3.8], [2, -1], [3.46, 3.74]]

if __name__ == '__main__':

    bezier = BEZIER(0, Example1)
    bezier.auto_fig()

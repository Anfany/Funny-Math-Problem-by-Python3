# !/usr/bin/env python3.8.8
# author:Anfany
# datetime:2021/4/6 17:09

# 多条贝塞尔曲线的绘制：根据多组控制点集合绘制贝塞尔曲线


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm

# 显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']


class BEZIER:

    def __init__(self, pointlist):

        self.pl = self.handle_list(pointlist)  # 多组控制点的集合

        self.n_list = [len(k) for k in self.pl]

        self.t_tap = 0.01
        self.t_list = np.arange(0, 1, self.t_tap)

        # 存储多条贝塞尔曲线的点
        self.bezier_list = {}

        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.clist = self.get_color_list()

    # list变为np.array格式
    def handle_list(self, ex_list):
        new_pl = []
        for ll in ex_list:
            jj = []
            for kk in ll:
                jj.append(np.array(kk))
            new_pl.append(np.array(jj))
        return new_pl

    # 不同阶的颜色
    def get_color_list(self):
        colorlist = {}
        for j in range(len(self.n_list)):
            color_list = []
            for i in range(self.n_list[j]):
                color_list.append(cm.rainbow(i / self.n_list[j]))
            colorlist[j] = color_list[::-1]
        return colorlist

    # 贝塞尔曲线方程：根据t的变化真是不同的图像状态
    def b_m(self, t):
        self.ax.clear()  # 清空已存在的图像
        # 隐藏边
        self.ax.axis('off')
        # 绘制多个控制组的原始点
        for pdin, pp in enumerate(self.pl):
            # 绘制原始点
            for din, p in enumerate(pp):
                if din == 0:
                    self.ax.text(p[0], p[1], '$%sP_{%s}$' % (pdin, din), fontsize=13)
                    self.ax.scatter(p[0], p[1], s=50, color='tab:green')
                elif din == self.n_list[pdin] - 1:
                    self.ax.text(p[0], p[1], '$%sP_{%s}$' % (pdin, din), fontsize=13)
                    self.ax.scatter(p[0], p[1], s=50, color='tab:red')
                else:
                    self.ax.text(p[0], p[1], '$%sP_{%s}$' % (pdin, din), fontsize=13)
                    self.ax.scatter(p[0], p[1], color='gray', s=45)
            # 绘制原始点之间的连接线
            xp = [op[0] for op in pp]
            yp = [op[1] for op in pp]
            self.ax.plot(xp, yp, '-', lw=2, color=self.clist[pdin][0])

            # 开始绘制多阶直线
            line_list = pp
            while len(line_list) > 2:
                new_list = []
                for kp, kz in zip(line_list[:-1], line_list[1:]):
                    ss = np.float64(kp + t * (kz - kp))
                    new_list.append(ss)

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
            self.ax.plot(self.bezier_list[pdin][0], self.bezier_list[pdin][1], lw=4, color=self.clist[pdin][-1],
                         label=r'$B\acute{e}zier\quadcurve$')
            self.ax.scatter(x, y, s=50, color=self.clist[pdin][-1])

    # 动态图实现
    def auto_fig(self):
        animator = animation.FuncAnimation(self.fig, self.b_m, self.t_list, interval=90)
        animator.save('Bezier_m.mp4')


# 实例1：签名
Example1 = [[[1.06, 0.5], [1.065, 8], [1.07, 8], [1.075, 0.8]],
            [[1.065, 3.3], [1.09, 3.5]],
            [[1.075, -0.5], [1.08, -3], [1.085, 0], [1.085, 4.9], [1.091, 9.9], [1.097, 4.9]]]


if __name__ == '__main__':

    bezier_m = BEZIER(Example1)
    bezier_m.auto_fig()

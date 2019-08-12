# -*- coding：utf-8 -*-
# &Author  AnFany


# 利用Python实现分形图形：朱利亚集、曼德勃罗特集
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from pylab import mpl  # 作图显示中文
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 设置中文字体为新宋体


# 实现分形图形
class FRACTAL():

    def __init__(self, x_max, x_min, y_max, y_min, t):
        """

        :param x_max: 展示图形的横坐标的最大值
        :param x_min: 展示图形的横坐标的最小值
        :param y_max: 展示图形的纵坐标的最大值
        :param y_min: 展示图形的纵坐标的最小值
        :param t: # 迭代的次数
        """
        self.s = 1000  # 一行或者一列包括的点的个数，个数越大，图像越清晰，运行速度越慢
        self.max_number = 2  # 模的阈值。大于此值设置为2
        self.c_count = 100  # 显示颜色的个数
        self.dpi = 1000  # 此数越大，分辨率越高，图片越清晰
        self.l_count = 5  # 图片中的横纵坐标轴的标签的个数

        self.p_fig = r'C:\Users\GWT9\Desktop'  # 保存图片的地址

        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min

        self.t = t

        # 表示渐进颜色的列表
        self.c = self.get_color()

        # mandelbrot分形，需要放大局部，横坐标最小值，最大值，纵坐标的最小值，最大值，下面展示为放大3个局部
        # 注意后面的范围必须在前面的范围内
        self.m_p = [[-1.3, -0.5, 0, 0.8], [-0.72, -0.6, 0.4, 0.52], [-0.706, -0.696, 0.467, 0.477],
                    [-0.6982, -0.6972, 0.4682, 0.4692], [-0.6977, -0.6975, 0.4686, 0.4688]]

        # 复平面上一行具有的点的个数
        self.row_c = self.s if self.x_max - self.x_min < 1 else self.s * (self.x_max - self.x_min)

        # 复平面上一列具有的点的个数
        self.col_c = self.s if self.y_max - self.y_min < 1 else self.s * (self.y_max - self.y_min)

    def get_color(self):
        """
        获取表示渐进颜色的列表
        :return: 列表
        """
        s_number_list = int(self.c_count ** 0.5) + 1
        c_s = []
        for i in np.linspace(0.1, 1, s_number_list // 3):
            r = [(i, rr / 255, rr / 255) for rr in np.linspace(20, 255, s_number_list)]
            g = [(gg / 255, i, gg / 255) for gg in np.linspace(20, 255, s_number_list)]
            bl = [(bb / 255, bb / 255, i) for bb in np.linspace(20, 255, s_number_list)]
            c_s += r + g + bl
        cmp = ListedColormap(c_s + [[1, 1, 1]])  # 背景颜色设为白色
        return cmp

    def julia_set(self, a, b):
        """
        绘制朱利亚集分形图形
        :param a: 初始复数的实部
        :return: 分形图形
        """
        # 生成点的矩阵
        x = np.linspace(self.x_min, self.x_max, num=self.row_c)  # 实部
        y = np.linspace(self.y_max, self.y_min, num=self.col_c)  # 虚部
        X, Y = np.meshgrid(x, y)

        # 开始迭代
        times = 0
        while 1:
            z = np.square(X + 1j * Y)  # Z^2
            z += a + 1j * b  # Z^2+a+bj
            X = z.real  # 获取实部
            Y = z.imag  # 获取虚部
            times += 1
            print('迭代次数，当前%d，总共%d' % (times, self.t))
            if times >= self.t:
                break
        # 计算复数的模
        m = np.abs(z)
        # 控制模值的大小
        m[np.isnan(m)] = self.max_number
        m[m >= self.max_number] = self.max_number
        # 绘图显示
        plt.figure()

        # 获取渐进颜色，数组表示的列表
        plt.imshow(m, aspect='equal', cmap=self.c)

        plt.xticks(np.linspace(0, self.row_c, self.l_count),
                   ['%.2f' % i for i in np.linspace(self.x_min, self.x_max, self.l_count)])
        plt.yticks(np.linspace(0, self.col_c, self.l_count),
                   ['%.2f' % i for i in np.linspace(self.y_max, self.y_min, self.l_count)])

        plt.title(r'分形之$Julia$集$:f(z) = z^{2}%s%s%s%s$ 迭代次数：%d' %
                  ('+' if a > 0 else '', a if a != 0 else '', '+' if b > 0 else '',
                   str(b) + 'j' if b != 0 else '', self.t))

        plt.xlabel('实部$real$')
        plt.ylabel('虚部$imag$')

        plt.rcParams['savefig.dpi'] = self.dpi  # 数值越大，图片越清晰

        plt.savefig(r'%s\julia.png' % self.p_fig)
        return print('Julia分形图片保存完毕')

    def mandelbrot_data(self, power):
        """
        得到绘制曼德勃罗特集分形图形需要用到的数据
        :param power: 幂的次数
        :return: 曼德勃罗特集分形图形需要用到的数据
        """
        # 生成点的矩阵
        x = np.linspace(self.x_min, self.x_max, num=self.row_c)  # 实部
        y = np.linspace(self.y_max, self.y_min, num=self.col_c)  # 虚部
        X, Y = np.meshgrid(x, y)
        X1, Y1 = X, Y

        # 开始迭代
        times = 0
        # 记录逃脱次数的矩阵，就是记录迭代几次后模大于2
        escape_times = np.ones(X.shape) * 1

        while 1:
            c_s = np.power(X + 1j * Y, power)  # Z^power
            c_s += X1 + 1j * Y1  # Z^power + Z

            X = c_s.real  # 实部
            Y = c_s.imag  # 虚部

            # 计算复数的模, 控制模值的大小，最大值为2
            c_m = np.abs(c_s)
            c_m[escape_times != 1] = 1.9  # 只要是小于2的小数就可以，防止把记录的跳脱次数的数覆盖掉
            escape_times[c_m > 2] = self.t - times
            X[escape_times != 1] = 20
            Y[escape_times != 1] = 20

            print('迭代次数：当前%d，总共%d' % (times, self.t))
            times += 1
            if times >= self.t:
                break
        # 返回数据矩阵
        return escape_times

    def plot_mandelbrot(self, power, expand=True):
        """
        获取放大局部得到的数据，并进行绘图
        :param power: 幂
        :param expand: 是否显示局部放大的部分
        :return: 带有局部放大的图片
        """
        # 局部放大的部分加上整体的
        self.m_p.insert(0, [self.x_min, self.x_max, self.y_min, self.y_max])
        fig_count = len(self.m_p)

        # 一行的图片的个数
        row_fig_c = 3
        col_fig_c = fig_count // row_fig_c + 0 if fig_count % row_fig_c == 0 else 1

        if not expand:
            self.m_p = [self.m_p[0]]
            fig_count, row_fig_c, col_fig_c = 1, 1, 1

        plt.figure(figsize=(6 * row_fig_c, 6 * col_fig_c))  # 宽度，高度

        # 开始绘制图片,螺旋式的绘制图片
        fig_sign = np.array([list(range(row_fig_c * (i - 1), row_fig_c * i)) if i % 2 == 1
                             else list(range(row_fig_c * (i - 1), row_fig_c * i))[::-1]
                             for i in range(1, col_fig_c + 1)]).flatten()

        sign = 1
        for a, value in zip(fig_sign, self.m_p):
            # 获取数据
            self.x_min, self.x_max, self.y_min, self.y_max = value

            # 更新，复平面上一行具有的点的个数
            self.row_c = self.s if self.x_max - self.x_min < 1 else self.s * (self.x_max - self.x_min)
            # 更新，复平面上一列具有的点的个数
            self.col_c = self.s if self.y_max - self.y_min < 1 else self.s * (self.y_max - self.y_min)

            data = self.mandelbrot_data(power)
            # 获取渐进颜色，数组表示的列表
            plt.subplot(eval('%d%d%d' % (col_fig_c, row_fig_c, a + 1)))
            plt.imshow(data, aspect='equal', cmap=self.c)

            plt.xticks(np.linspace(0, self.row_c, self.l_count),
                       ['%.4f' % i for i in np.linspace(self.x_min, self.x_max, self.l_count)])
            plt.yticks(np.linspace(0, self.col_c, self.l_count),
                       ['%.4f' % i for i in np.linspace(self.y_max, self.y_min, self.l_count)])

            # 在当前图上标出放大的区域，最后一个图片不用标
            if sign < fig_count and expand:
                # 需要将后面的坐标变为原始图片的坐标，注意图片中的标签不是真实的刻度
                x_mi, x_ma, y_mi, y_ma = self.m_p[sign]

                trans_x_mi = (x_mi - self.x_min) * self.row_c / (self.x_max - self.x_min)
                trans_x_ma = (x_ma - self.x_min) * self.row_c / (self.x_max - self.x_min)

                trans_y_mi = self.col_c - (y_mi - self.y_min) * self.col_c / (self.y_max - self.y_min)
                trans_y_ma = self.col_c - (y_ma - self.y_min) * self.col_c / (self.y_max - self.y_min)

                # 开始绘制方框，绘制四条边
                plt.plot([trans_x_mi, trans_x_ma], [trans_y_mi, trans_y_mi], '--', c='tab:red', lw=2)
                plt.plot([trans_x_ma, trans_x_ma], [trans_y_mi, trans_y_ma], '--', c='tab:red', lw=2)
                plt.plot([trans_x_ma, trans_x_mi], [trans_y_ma, trans_y_ma], '--', c='tab:red', lw=2)
                plt.plot([trans_x_mi, trans_x_mi], [trans_y_ma, trans_y_mi], '--', c='tab:red', lw=2)

            plt.rcParams['savefig.dpi'] = self.dpi  # 数值越大，图片越清晰

            print('mandelbrot分形局部放大图，已经绘制%d张，共%d张' % (sign, fig_count))

            sign += 1

        if expand:
            plt.subplots_adjust(left=0.04, right=0.98, bottom=0.1, top=0.98, hspace=0.10, wspace=0.09)
        else:
            plt.title('分形Mandelbrot集：$F(Z)=Z^{%d}+Z0$，迭代次数%d' % (power, self.t))
        plt.savefig(r'%s\mandelbrot1.png' % self.p_fig)
        return print('mandelbrot分形图片保存完毕')


# 主函数
if __name__ == "__main__":
    # 绘制Julia集分形图形
    # ju = FRACTAL(1.7, -1.7, 0.9, -0.9, 20)
    # ju.julia_set(-0.70176, -0.3842)

    # 绘制具有局部放大的Mandelbrot分形图形
    m = FRACTAL(1, -2, 1.5, -1.5, 200)
    m.plot_mandelbrot(2, True)








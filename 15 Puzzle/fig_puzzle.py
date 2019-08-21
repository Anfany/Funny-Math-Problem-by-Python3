# -*- coding：utf-8 -*-
# &Author  AnFany


# 利用IDA*算法实现拼图谜题的生成和解决方案
import n_puzzle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import imageio  # 引入合成gif的库


class FigPuzzle(n_puzzle.MNPuzzle):
    def __init__(self):
        super(FigPuzzle, self).__init__()
        # 将图片分成的行数和列数
        self.m = 3
        self.n = 3

        # 分块后，缺失图片的编号，默认为最后一块:self.m * self.n
        self.miss_sign = 9

        # 图片的编号，缺失图片的位置用数字0代替
        self.e_p_list = list(range(1, self.m * self.n + 1))
        self.initial_e_p_list = self.e_p_list.copy()
        # 谜题的结束状态
        self.e_p_list[self.miss_sign - 1] = 0

        # 谜题的开始状态
        self.p_list = self.generate_puzzle()

        # 图片路径
        self.fig_file = r'C:\Users\GWT9\Desktop\love.jpg'
        # 切割线的宽度为多少像素
        self.cut_width = 5
        # 可以自定义切割线的颜色的RGB字典
        self.cut_color_number = 1

        # 需要作为谜题的图片的矩阵
        self.matrix = self.fig_to_matrix()

        self.height, self.width, self.channel = self.matrix.shape  # 矩阵是三维的，第三个值一般为4(RGBA)或者为3(RGB)，没有影响

        # 不考虑除不尽的情形，因为self.row, self.column都比较小。
        self.per_h = self.height // self.m
        self.per_w = self.width // self.n

        # 数字对应的图片的矩阵，依据数字不同排列，从而展示不同的组合的图片
        self.digital_matrix_dict = self.cut_matrix_dict()

    def fig_to_matrix(self):
        """
        将图片转化为分块的数据矩阵的字典
        :return:
        """
        plt.figure()
        matrix = plt.imread(self.fig_file)
        if self.fig_file[-3:] == 'jpg':
            return matrix / 255

        return matrix

    def cut_matrix_dict(self):
        # 下面就按照编号对矩阵矩阵进行分块

        # 开始分块
        sign_matrix_dict = {}
        for i in range(1, self.m * self.n + 1):
            r_i = (i - 1) // self.n
            c_i = (i - 1) % self.n
            sign_matrix_dict[i] = self.matrix[r_i * self.per_h: (r_i + 1) * self.per_h,
                                              c_i * self.per_w: (c_i + 1) * self.per_w, :]
        return sign_matrix_dict

    def matrix_to_fig(self, number_list):
        """
        根据数字的序列，返回重新排列的矩阵，重新排列的矩阵，需要包括中间的分割线。以及缺失的图片
        :param number_list: 数字的序列
        :return: 数字矩阵
        """
        # 计算新的矩阵需要的维度，初始值定义为cut_color_number
        new_matrix = np.ones((self.height + (self.m - 1) * self.cut_width,
                              self.width + (self.n - 1) * self.cut_width, self.channel)) * self.cut_color_number

        # 开始更新矩阵
        for index, value in enumerate(number_list):
            if value != 0:
                # 计算该数字对应的矩阵位置在哪里
                a_row = index // self.n
                a_column = index % self.n
                # 开始更新矩阵
                new_matrix[a_row * self.per_h + (a_row * self.cut_width):
                           (a_row + 1) * self.per_h + (a_row * self.cut_width),
                           a_column * self.per_w + (a_column * self.cut_width):
                           (a_column + 1) * self.per_w + (a_column * self.cut_width), :] \
                    = self.digital_matrix_dict[value]
        return new_matrix

    def generate_puzzle(self):
        """
        对于图片谜题而言，结束状态的逆序数一定为0，因此要保证随机生成的谜题的逆序数为偶数
        为了保证谜题的复杂。此时要使得谜题的逆序数稍微大点
        :return: 数码谜题
        """
        # 随机50次，获取其中最大的逆序数对应的谜题
        times = 0
        i_count = 0
        p_list = self.e_p_list.copy()
        start_p_list = []
        while times < 50:
            np.random.shuffle(p_list)
            # 计算逆序数
            new_i = self.inverse_count(p_list)
            # 根据列数的奇偶性判断
            if self.n % 2 == 1:
                if i_count < new_i and new_i % 2 == 0:
                    i_count = new_i
                    start_p_list = p_list.copy()
            else:
                z_index = p_list.index(0)
                z_row = z_index // self.n
                if i_count < new_i and (new_i + self.m - 1 - z_row) % 2 == 0:
                    i_count = new_i
                    start_p_list = p_list.copy()
            times += 1
        return start_p_list

    def get_state_list(self):
        """
        根据起始和结束状态，获取行为列表，根据行为列表获取状态列表
        :return: 状态列表
        """
        action_str = self.ida_star_puzzle()
        state_list = [self.p_list]
        for a in action_str:
            state_list.append(self.get_next_p(state_list[-1], a))
        return state_list

    def plot_fig_puzzle(self, state_list):
        """
        根据状态列表绘制图片
        :param state_list: 状态列表
        :return: 图片
        """
        for index, value in enumerate(state_list):
            # 首先根据起始和结束状态获取行为列表
            fig = plt.figure()
            gs = gridspec.GridSpec(2, 3)
            #  绘制初始状态
            ax = fig.add_subplot(gs[0, 0])
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title('起始')
            start_array = self.matrix_to_fig(self.p_list)
            ax.imshow(start_array)

            #  绘制结束状态
            ax = fig.add_subplot(gs[1, 0])
            ax.set_title('结束，第%d块空白' % self.miss_sign)
            ax.set_xticks([])
            ax.set_yticks([])
            end_array = self.matrix_to_fig(self.initial_e_p_list)
            ax.imshow(end_array)

            #  绘制中间状态
            ax = fig.add_subplot(gs[:, 1:])
            if index == 0:
                ax.set_title('中间转换：开始转换')
            elif index != len(state_list) - 1:
                ax.set_title('中间转换状态:总共$%d$步，当前$%d$步' % (len(state_list) - 1, index))
            else:
                ax.set_title('转换完成')
            ax.set_xticks([])
            ax.set_yticks([])
            end_array = self.matrix_to_fig(value)
            ax.imshow(end_array)
            plt.savefig(r'./fig_%d_%d.png' % (len(state_list), index+1))
            plt.close()

        image_list = ['fig_%d_%d.png' % (len(state_list), index+1) for index in range(len(state_list))]

        frames = []
        for image_name in image_list + [image_list[-1]] * 10:
            frames.append(imageio.imread(image_name))
        imageio.mimsave('fig_puzzle.gif', frames, 'GIF', duration=0.9)  # 图片合成为动图

        return print('gif生成完毕')

# 主函数


if __name__ == "__main__":

    f_p = FigPuzzle()
    print('谜题的初始状态为:\n', np.array(f_p.p_list).reshape(f_p.m, f_p.n))
    # 获取谜题移动的中间状态
    a = f_p.get_state_list()
    print('中间状态生成完毕，绘制动图……')
    # 绘制图
    f_p.plot_fig_puzzle(a)



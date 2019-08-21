# -*- coding：utf-8 -*-
# &Author  AnFany


# 利用IDA*算法实现M*N数码问题的求解
import numpy as np
import imageio  # 引入合成gif的库
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pylab import mpl  # 作图显示中文
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 设置中文字体为新宋体

# 谜题的初始状态，数组形式，数组由不重复的数字组成,其中用数字0代表空格.数字可以不连续，但是必须不重复。
# 数组为M*N的，行数M的最小值为2,
START_PUZZLE = np.array([[9, 11, 6],
                         [5, 0, 1],
                         [4, 2, 7],
                         [8, 3, 10]])


class MNPuzzle:
    def __init__(self, p=START_PUZZLE):

        self.p = p
        self.p_list = list(self.p.flatten())  # 将谜题的初始状态变为一维的列表形式
        self.m, self.n = self.p.shape  # 数组的行数和列数

        self.e_p = self.get_end_puzzle()  # 谜题的结束状态，二维数组，该数组可以自由设置，默认就是从1开始，空格结束。
        #
        # self.e_p = np.array([[515, 4, 245, 55],
        #                      [24, 0, 7, 8],
        #                      [67, 39, 85, 12]])  # 自由设置数组，要保证值均在开始状态数组中。

        self.e_p_list = list(self.e_p.flatten())  # 谜题的结束状态变为一维的列表形式

    def get_end_puzzle(self):  # 获取数码问题的最终的数组
        # 构成谜题数组的数字列表
        number_list = self.p_list.copy()
        number_list.remove(0)
        number_list.sort()
        number_list.append(0)
        end_puzzle = np.array(number_list).reshape(self.m, self.n)
        return end_puzzle

    def inverse_count(self, puzzle_list):
        """
        计算用一维列表表示的谜题的逆序数，注意不计算空格，也就是不计算数字0的逆序数。
        :param puzzle_list: 一维列表
        :return: 逆序数
        """
        # 逆序数
        i_count = 0
        for index, value in enumerate(puzzle_list[:-1]):
            if value != 0:  # 不计算数字0的逆序数
                for i in range(index+1, len(puzzle_list)):
                    if puzzle_list[i] != 0 and value > puzzle_list[i]:  # 数字0不参与计算
                        i_count += 1
        return i_count

    def judge_p_solved(self):  # 判断题目是否可以有解。
        # 开始、结束数组的逆序数
        start_inverse = self.inverse_count(self.p_list)
        end_inverse = self.inverse_count(self.e_p_list)

        # 初始数组中空格的行与结束数组中空格的行的差
        start_black = self.p_list.index(0) // self.n
        end_black = self.e_p_list.index(0) // self.n

        # 如果N为奇数，初始数组的逆序数要和结束数组的逆序数是一样的奇偶性
        if self.n % 2 == 1:
            if start_inverse % 2 == end_inverse % 2:
                print('该数码问题：有解')
                return True
        else:
            # 如果N为偶数。
            # 初始数组的逆序数与空格行间距的和的奇偶性 要和结束数组的逆序数相同
            if (start_inverse + end_black - start_black) % 2 == end_inverse % 2:
                print('该数码问题：有解')
                return True
        print('初始数组不可能达到结束数组，没有解')
        return False

    def get_h(self, current_p):
        """
        谜题的一个状态和结束状态之间的曼哈顿距离作为估计函数h(n)
        :param current_p: 当前的状态,一维列表形式
        :return: 曼哈顿距离
        """
        # 估价函数值
        h_n = 0
        for index, value in enumerate(current_p):
            if value != 0:
                # 获取该值在结束状态里面的位置
                end_index = self.e_p_list.index(value)
                # 计算行列
                e_row = end_index // self.n
                e_column = end_index % self.n
                # 计算当前位置的行列
                c_row = index // self.n
                c_column = index % self.n
                # 计算曼哈顿距离
                h_n += abs(c_column - e_column) + abs(c_row - e_row)
        return h_n

    def get_action(self, current_p):
        """
        根据谜题当前的状态计算上下左右哪几个方向的数字可以转移到空格
        :param current_p: 当前的谜题的状态，一维列表的形式
        :return: 上下左右分别用u,d,l,r表示
        """
        # 获取空格，也就是0值在的位置
        zero_index = current_p.index(0)
        # 计算空格所在的行列
        z_row = zero_index // self.n
        z_colmn = zero_index % self.n

        # 可以进行的动作集合
        action_list = []
        if z_row > 0:  # 上方的数字可以到达空格的位置
            action_list.append('u')

        if z_row < self.m - 1:  # 下方的数字可以到达空格的位置
            action_list.append('d')

        if z_colmn > 0:   # 左方的数字可以到达空格的位置
            action_list.append('l')

        if z_colmn < self.n - 1:   # 右方的数字可以到达空格的位置
            action_list.append('r')

        return action_list

    def get_next_p(self, current_p, a):
        """
        根据当前的谜题状态以及动作获取谜题的下一个状态
        :param current_p: 谜题的当前状态
        :param a: 哪个方向的数字移动到空格的位置
        :return: 谜题的下一个状态
        """
        #  首先获取空格的位置
        zero_index = current_p.index(0)
        z_row = zero_index // self.n
        z_column = zero_index % self.n

        # 根据方向，以及空格的位置，计算需要移动的数字的位置
        if a == 'u':  # 上方
            trans_row = z_row - 1
            trans_column = z_column
        elif a == 'd':  # 下方
            trans_row = z_row + 1
            trans_column = z_column

        elif a == 'r':  # 右方
            trans_row = z_row
            trans_column = z_column + 1
        else:  # 左方
            trans_row = z_row
            trans_column = z_column - 1
        # 将行和列的位置变为一维中的位置
        one_add = trans_row * self.n + trans_column

        # 需要将两个位置的值进行移动，实现数字与空格的互换
        copy_p = current_p.copy()
        copy_p[zero_index] = current_p[one_add]
        copy_p[one_add] = 0
        return copy_p

    def trans_state_str(self, current_p):
        """
        将状态变为字符串形式
        :param current_p: 表示状态的列表
        :return: 字符串格式
        """
        str_p = [str(i) for i in current_p]
        return '_'.join(str_p)

    def dfs_puzzle(self, max_depth):
        """
        利用dfs获取搜索指定深度中的解决方案
        :param max_depth: 指定的搜索深度
        """
        # 已经遍历的状态, 防止出现循环的动作
        yes_s = {self.trans_state_str(self.p_list): 0}
        # 当前枝叶上已经遍历的点，长度控制深度
        current_s = [self.p_list]
        # 记录每次选择的行为
        current_a = ''
        # 当前遍历的节点关系字典，后面的节点作为键，前面的节点为值
        node_realtion = {}
        # 记录每个节点当前选择的是第几个行为
        node_action = {self.trans_state_str(self.p_list): 0}
        # 记录所有的代价值
        hn_list = []

        while len(current_s) < max_depth:  # 以深度为限制，遍历完
            # 当前的状态
            c_s = current_s[-1]
            # 当前状态的字符串形式
            str_current_s = self.trans_state_str(c_s)
            # 获取这个状态的动作集合
            a_list = self.get_action(c_s)
            # 动作的个数
            a_count = len(a_list)
            # 字典中记录的需要选择第几个动作
            need_a_sign = node_action[str_current_s]
            #  判断是否有可选的动作
            if a_count > need_a_sign:
                # 说明动作有选择的余地
                select_action = a_list[need_a_sign]
                # 计算选择这个动作后的形态
                next_s = self.get_next_p(c_s, select_action)
                # 计算这个状态的字符串形式
                str_next_s = self.trans_state_str(next_s)
                # 判断这个新的状态是否是结束状态
                if str_next_s == self.trans_state_str(self.e_p_list):
                    # 说明取到了最后的结果,返回动作的序列
                    current_a += select_action
                    return '0', current_a

                # 计算这个状态的代价
                hn_next = self.get_h(next_s)
                if hn_next + len(current_s) + 1 > max_depth:
                    hn_list.append(hn_next + len(current_s) + 1)
                # 存储这个值
                # 判断这个状态的估值(该状态到结束状态的值与开始状态到该状态的值)总和是否小于阈值
                if hn_next + len(current_s) + 1 < max_depth:
                    # 以前没出现过
                    if str_next_s not in yes_s:
                        # 添加到遍历的字典中
                        yes_s[str_next_s] = 0
                        # 添加到当前枝叶上已经遍历的点
                        current_s.append(next_s)
                        # 记录该状态需要选择的行为的编号
                        node_action[str_next_s] = 0
                        # 关系字典
                        node_realtion[str_next_s] = str_current_s
                        # 添加行为
                        current_a += select_action
                    else:
                        # 以前出现过，说明需要选择下一个动作
                        node_action[str_current_s] += 1
                else:
                    # 需要剪枝，继续判断下一个动作
                    node_action[str_current_s] += 1

            else:
                # 如果没有可选的动作，需要回溯，判断此时是否回溯到开始的根节点
                if str_current_s in node_realtion:
                    # 获取这个状态的父亲节点
                    father_node = node_realtion[str_current_s]
                    del node_action[str_current_s]
                    del node_realtion[str_current_s]
                    del yes_s[str_current_s]
                    current_s = current_s[:-1].copy()
                    node_action[father_node] += 1
                    current_a = current_a[:-1]
                else:
                    if hn_list:
                        return '1', min(hn_list)
                    else:
                        return '1', max_depth + 1
        if hn_list:
            return '1', min(hn_list)
        else:
            return '1', max_depth + 1

    def ida_star_puzzle(self):
        """
        利用IDA*算法实现获取数码问题的解决方案
        :return: 搜索得到的动作序列
        """
        # 计算初始状态的估价值
        initial_hn = self.get_h(self.p_list)

        while 1:
            # dfs的结果
            dfs = self.dfs_puzzle(initial_hn)

            if dfs[0] == '0':
                # 说明得到解了
                return dfs[1]

            initial_hn = dfs[1]

            print('当前遍历深度：', initial_hn)

    def plot_puzzle(self, action_str):
        """
        根据动作序列的字符串真是梳着移动
        :param action_str: 动作序列字符串
        :return: gif动态图片
        """
        def create_gif(image_list, gif_name='puzzle.gif'):
            """
            创建gif格式的图片
            :param image_list: 合成图片的名称的列表
            :param gif_name: gif图片的名称
            :return:
            """
            frames = []
            for image_name in image_list + [image_list[-1]] * 10:
                frames.append(imageio.imread(image_name))
            imageio.mimsave(gif_name, frames, 'GIF', duration=0.9)  # duration控制动态图中每张图片的显示时间

        # 为谜题的状态生成图片
        def figure_p(data_p, digital_list, f_name):
            """
            图片展示二维数组
            :param data_p: 表示谜题状态的二维数组
            :param digital_list: 移动的数字序列
            :param f_name: 图片的标识，长度为2的列表，[总共的步数，当前的步数]
            :return: 图片
            """
            fig = plt.figure()
            alignment = {'horizontalalignment': 'center', 'verticalalignment': 'baseline'}
            gs = gridspec.GridSpec(2, 2)
            #  绘制初始状态
            ax = fig.add_subplot(gs[0, 0])
            ax.set_title('起始')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(True)
            ax.set_xlim(0, self.n)
            ax.set_ylim(0, self.m)
            for r in range(self.n):
                for c in range(self.m, 0, -1):
                    if self.p[self.m - c, r] == 0:
                        ax.text(r + 0.5, c - 0.5, ' ',
                                bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
                    else:
                        ax.text(r + 0.5, c - 0.5, self.p[self.m - c, r], color='tab:blue',
                                style='italic', weight='bold', size='x-large', **alignment)
            # 绘制结束状态
            ax = fig.add_subplot(gs[0, 1])
            ax.set_title('结束')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(True)
            ax.set_xlim(0, self.n)
            ax.set_ylim(0, self.m)
            for r in range(self.n):
                for c in range(self.m, 0, -1):
                    if self.e_p[self.m - c, r] == 0:
                        ax.text(r + 0.5, c - 0.5, ' ',
                                bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
                    else:
                        ax.text(r + 0.5, c - 0.5, self.e_p[self.m - c, r], color='tab:red',
                                style='italic', weight='bold', size='x-large', **alignment)

            # 绘制中间的转换状态
            ax = fig.add_subplot(gs[1, 1])
            ax.set_title('中间转换')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(True)
            ax.set_xlim(0, self.n)
            ax.set_ylim(0, self.m)
            for r in range(self.n):
                for c in range(self.m, 0, -1):
                    # 空格位置
                    if data_p[self.m - c, r] == 0:
                        ax.text(r + 0.5, c - 0.5, ' ',
                                bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
                    else:
                        ax.text(r + 0.5, c - 0.5, data_p[self.m - c, r], color='tab:red',
                                style='italic', weight='bold', size='x-large', **alignment)

            # 绘制移动的数字序列
            ax = fig.add_subplot(gs[1, 0])
            ax.set_title('移动的数字')
            length = len(digital_list)
            y_ss = int(length ** 0.5)
            x_ss = length / y_ss
            if x_ss - int(x_ss) != 0:
                x_ss = int(x_ss) + 1
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(True)
            ax.set_xlim(0, x_ss)
            ax.set_ylim(0, y_ss)
            for r in range(length):
                y_d = r // x_ss
                x_d = r % x_ss
                ax.text(x_d + 0.5, y_ss - (y_d + 0.5), digital_list[r], color='k',
                        style='italic', weight='bold', size='medium', **alignment)
            if f_name[0] != f_name[1]:
                plt.suptitle('$%d*%dPuzzle$，总共%d步, 当前%d步' % (self.m, self.n, f_name[0], f_name[1]))
            else:
                plt.suptitle('$%d*%dPuzzle$完成，总共%d步' % (self.m, self.n, f_name[0]))
            plt.savefig(r'./%d_%d.png' % (f_name[0], f_name[1]))
            plt.close()

        # 开始生成图片
        current_s = self.p_list
        # 存储移动的数字序列
        move_digital_list = []
        for index, value in enumerate(action_str):
            # 计算是哪个数字需要移动
            # 首先获取0的位置
            zero_index = current_s.index(0)
            z_row = zero_index // self.n
            z_column = zero_index % self.n
            # 根据方向，以及空格的位置，计算需要移动的数字的位置
            if value == 'u':  # 上方
                trans_row = z_row - 1
                trans_column = z_column
            elif value == 'd':  # 下方
                trans_row = z_row + 1
                trans_column = z_column

            elif value == 'r':  # 右方
                trans_row = z_row
                trans_column = z_column + 1
            else:  # 左方
                trans_row = z_row
                trans_column = z_column - 1
            # 将行和列的位置变为一维中的位置
            one_add = trans_row * self.n + trans_column
            # 移动的数字
            move_number = current_s[one_add]
            move_digital_list.append(move_number)

            # 当前状态添加行为后得到的状态
            fig_c_s = self.get_next_p(current_s, value)
            # 更新当前状态
            current_s = fig_c_s.copy()

            # 状态换为二维数组形式
            data_s = np.array(current_s).reshape(self.m, self.n)
            # 绘图
            figure_p(data_s, move_digital_list, [len(action_str), index+1])

        # 生成gif图片
        image_list = ['%d_%d.png' % (len(action_str), i+1) for i in range(len(action_str))]

        create_gif(image_list, gif_name='puzzle.gif')

        return print('动图生成完毕')

# 主函数


if __name__ == '__main__':
    a = MNPuzzle()
    if a.judge_p_solved():
        move_action = a.ida_star_puzzle()
        print('方案找到，动作序列为：%s。正在绘图' % move_action)
        a.plot_puzzle(move_action)














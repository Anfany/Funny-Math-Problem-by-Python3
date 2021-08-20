# -*- coding：utf-8 -*-
# &Author  AnFany

import k_problerms as k
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import imageio  # 引入合成gif的库
import time
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号


# 24局三国华容道

PEOPLE = ['曹操', '关羽', '张飞', '赵云', '马超', '黄忠', '兵一', '兵二', '兵三', '兵四']

# 因为五将在不同的布局中有横有竖，所以图片为2个，横竖各一张，前面的为竖的，后面的为横的
# 其中代表兵的图片的像素为80*80、曹操的为160*160，其他的为80*160或者160*80
PIXEL = 80
# 整个华容道德像素就是400*320
# 图片均为jpg格式
FIG = {0: ['0.jpg'], 1: ['1s.jpg', '1h.jpg'], 2: ['2s.jpg', '2h.jpg'], 3: ['3s.jpg', '3h.jpg'],
       4: ['4s.jpg', '4h.jpg'], 5: ['5s.jpg', '5h.jpg'],
       6: ['6.jpg'], 7: ['7.jpg'], 8: ['8.jpg'], 9: ['9.jpg']}


class ThreeKing:

    def __init__(self, name, position_list, people=PEOPLE, fig=FIG, p=PIXEL):
        """
        三国华容道开局的设置
        :param name: 局面的名称
        :param position_list: 人员列表中每个人员对应的左下角的坐标，以及高度和宽度占的格子数。
        :param people: 人员顺序列表
        :param fig: 对应人员顺序列表的各个人员的图片
        """
        # 华容道布局行和列数
        self.height = 5
        self.width = 4
        self.p = p

        self.name = name
        self.people_list = people
        self.position_list = position_list
        self.fig = fig

        self.p_list = [g[0] for g in self.position_list]

        # 编号人员对应的字典
        self.index_people_dict = {index: value for index, value in enumerate(self.people_list)}

        # 编号对应的图片数据字典
        self.index_fig_dict = self.read_fig_data()

        # 编号对应的人员位置的字典
        self.index_position_dict = {index: value for index, value in enumerate(self.position_list)}

    def read_fig_data(self):
        """
        获取人员对应的图片数据
        :return: 字典
        """
        people_data_dict = {}
        for key in self.index_people_dict:
            if len(self.fig[key]) == 1:
                plt.figure()
                matrix = plt.imread('./%s' % self.fig[key][0])
                people_data_dict[key] = matrix[:, :, :3]
                plt.close()
            else:
                # 根据题目中的设置选择对应的图片
                # 等于1说明是宽度大于高度的图片
                if self.position_list[key][1] == 1:
                    plt.figure()
                    matrix = plt.imread('./%s' % self.fig[key][1])
                    people_data_dict[key] = matrix[:, :, :3]
                    plt.close()
                else:
                    # 说明是高度大于宽度的图片
                    plt.figure()
                    matrix = plt.imread('./%s' % self.fig[key][0])
                    people_data_dict[key] = matrix[:, :, :3]
                    plt.close()
        return people_data_dict

    def judge_move(self, position):
        """
        根据位置序列，判断当前状态下可以移动的人员，以及相应的移动的方向
        :param position: 按照人员列表顺序给出的各个人员的位置
        :return: 表示移动的字符串列表['0r', '3u', '5l', '5d']分别表示，曹操可向右移动，赵云可向上移动，黄忠可向左，向下移动
        """
        # 定义一个数组
        number = len(self.people_list) + 1  # 标定值
        new_data = np.ones((5, 4)) * number
        for index, value in enumerate(position):
            row_min = value[0] - self.index_position_dict[index][1]
            row_max = value[0]
            column_min = value[1]
            column_max = value[1] + self.index_position_dict[index][2]
            new_data[row_min: row_max, column_min: column_max] = \
                np.ones((self.index_position_dict[index][1], self.index_position_dict[index][2])).copy() * index
        # 开始进行移动
        move_list = []
        for index, value in enumerate(position):
            a, b = value[0], value[1]
            row_min = a - self.index_position_dict[index][1]
            row_max = a
            column_min = b
            column_max = b + self.index_position_dict[index][2]
            # 向左移动
            if 0 < b < 4:
                # 首先保证在框内
                if column_min - 1 >= 0:
                    # 计算移动后的边框
                    in_data = list(new_data[row_min: row_max, column_min - 1: column_max - 1].flatten())
                    # 框内没有标定值和自身的值以外的值，说明可以移动
                    set_list = list(set(in_data))
                    if len(set_list) == 1:
                        if set_list[0] == number:
                            move_list.append('%sl' % index)
                    elif len(set_list) == 2:
                        if number in set_list and index in set_list:
                            move_list.append('%sl' % index)
            # 向右移动
            if 0 <= b < 3:
                # 首先保证在框内
                if column_max + 1 <= 4:
                    # 计算移动后的边框
                    in_data = list(new_data[row_min: row_max, column_min + 1: column_max + 1].flatten())
                    # 框内没有标定值和自身的值以外的值，说明可以移动
                    set_list = list(set(in_data))
                    if len(set_list) == 1:
                        if set_list[0] == number:
                            move_list.append('%sr' % index)
                    elif len(set_list) == 2:
                        if number in set_list and index in set_list:
                            move_list.append('%sr' % index)
            # 向上移动
            if 1 < a <= 5:
                # 首先保证在框内
                if row_min - 1 >= 0:
                    # 计算移动后的边框
                    in_data = list(new_data[row_min - 1: row_max - 1, column_min: column_max].flatten())
                    # 框内没有标定值和自身的值以外的值，说明可以移动
                    set_list = list(set(in_data))
                    if len(set_list) == 1:
                        if set_list[0] == number:
                            move_list.append('%su' % index)
                    elif len(set_list) == 2:
                        if number in set_list and index in set_list:
                            move_list.append('%su' % index)
            # 向下移动
            if 1 <= a < 5:
                # 首先保证在框内
                if row_max + 1 <= 5:
                    # 计算移动后的边框
                    in_data = list(new_data[row_min + 1: row_max + 1, column_min: column_max].flatten())
                    # 框内没有标定值和自身的值以外的值，说明可以移动
                    set_list = list(set(in_data))
                    if len(set_list) == 1:
                        if set_list[0] == number:
                            move_list.append('%sd' % index)
                    elif len(set_list) == 2:
                        if number in set_list and index in set_list:
                            move_list.append('%sd' % index)

        return move_list

    def trans_to_str(self, position):
        """
        将位置转变为字符串
        :param position: 位置列表
        :return: 字符串，可以把兵士看作相同的。也就是只要四个兵士所在的位置集合是相同的，就认定为同一状态。
        对于除去曹操外的其他角色而言，只要初始的状态是一样的(竖直或者水平)，都可视为一样的
        """
        # 字符串分为4部分，第一部分是曹操的位置
        cao_s = ''.join([str(d) for d in position[0]])
        # 第二部分是初始状态是竖直的人员和水平的人员
        s_sign = []
        h_sign = []
        for index, value in enumerate(self.position_list):
            if value[1] > value[2]:
                s_sign.append(index)
            if value[2] > value[1]:
                h_sign.append(index)

        s_s = ''.join(([str(h) for g in sorted([position[kk] for kk in s_sign]) for h in g]))
        h_s = ''.join(([str(h) for g in sorted([position[kk] for kk in h_sign]) for h in g]))

        # 第三部分是士兵的
        solider_s = ''.join([str(h) for g in sorted(position[-4:]) for h in g])
        return cao_s + s_s + '-' + h_s + solider_s

    def get_next_s(self, position, a):
        """
        根据状态以及动作获取下一个状态
        :param position: 状态
        :param a: 动作
        :return: 下一个状态
        """
        new_p = position.copy()
        p_s, a_s = list(a)
        row, column = position[int(p_s)]
        if a_s == 'l':
            column -= 1
        elif a_s == 'r':
            column += 1
        elif a_s == 'u':
            row -= 1
        else:
            row += 1
        new_p[int(p_s)] = [row, column]
        return new_p

    def bfs_search(self, position):
        """
        利用bfs搜索华容道问题的解
        :param position: 各个人员初始的位置
        :return: 曹操可以逃脱的动作的列表
        """
        # 已经遍历过的状态
        yes_k_dict = {self.trans_to_str(position): 0}
        # 当前需要遍历的状态列表
        yes_k_list = [position.copy()]
        # 对应的动作列表
        action_list = ['']
        # 当前状态的列表
        current_yes_dict = {self.trans_to_str(position): 0}

        # 保存最优的解
        best_action_list = []

        # 开始遍历，只要不为空就遍历
        while len(yes_k_list):
            print('BFS中需要遍历的状态的个数：%s' % len(yes_k_list))
            copy_yes_k_list = []
            copy_action_list = []
            for s, a in zip(yes_k_list, action_list):
                # 遍历每个动作
                for c_a in self.judge_move(s):
                    # 获取下一状态
                    next_s = self.get_next_s(s, c_a)
                    # 找到解
                    if next_s[0] == [5, 1]:
                        best_action_list.append(a+'-'+c_a)
                    else:
                        # 转变为字符串
                        str_next_s = self.trans_to_str(next_s)
                        if str_next_s not in yes_k_dict and str_next_s not in current_yes_dict:
                            yes_k_dict[str_next_s] = 0
                            current_yes_dict[str_next_s] = 0
                            # 添加到列表中
                            copy_yes_k_list.append(next_s)
                            copy_action_list.append(a+'-'+c_a)

            if best_action_list:
                # 说明找到解了，选择最短的
                print('找到的解', len(best_action_list))
                return min(best_action_list, key=len)
            else:
                yes_k_list = copy_yes_k_list.copy()
                action_list = copy_action_list.copy()
        return print('无解')

    def plot_klotski_data(self, position):
        """
        根据各个人员的位置，绘制华容道的布局需要的数据
        :param position: 只包括各个人员的左下角的坐标即可，因为长宽已经固定
        :return: 华容道布局的数据
        """
        fig_data = np.ones((self.p * 5, self.p * 4, 3)) * 255  # 空白处的颜色
        # 开始填充人员的数据
        for index, value in enumerate(position):
            row_min = self.p * (value[0] - self.index_position_dict[index][1])
            row_max = self.p * value[0]
            column_min = self.p * value[1]
            column_max = self.p * (value[1] + self.index_position_dict[index][2])
            fig_data[row_min: row_max, column_min: column_max] = self.index_fig_dict[index]
        return fig_data / 255

    def trans_p_people(self, a_str):
        """
        将动作转变为人员的动作
        :param a_str: 总做字符串
        :return: 人员动作字符串
        """
        p_sign, a_f = list(a_str)
        if a_f == 'r':
            return self.index_people_dict[int(p_sign)] + '右'
        if a_f == 'l':
            return self.index_people_dict[int(p_sign)] + '左'
        if a_f == 'u':
            return self.index_people_dict[int(p_sign)] + '上'
        if a_f == 'd':
            return self.index_people_dict[int(p_sign)] + '下'

    def combine_action_list(self, ac_list):
        """
        合并动作，一个人员的连续2次动作何为1个，然后翻译为人员动作。不会存在一个人员连续三次做动作。
        :param ac_list: 动作列表
        :return: 人员动作的表达列表
        """
        people_action_str_list = []
        start_ac = ac_list[0]
        sign = 0
        for j in ac_list[1:]:
            if sign == 0:
                # 说明人员一样
                if start_ac[0] == j[0]:
                    # 说明动作一样
                    if start_ac[1] == j[1]:
                        people_action_str_list.append(self.trans_p_people(j) + '二')
                    else:
                        people_action_str_list.append(self.trans_p_people(start_ac) + self.trans_p_people(j)[-1])
                    sign = 1
                else:
                    people_action_str_list.append(self.trans_p_people(start_ac))
                    start_ac = j
                    sign = 0
            else:
                start_ac = j
                sign = 0
        # 加上最后一个动作的翻译
        if sign == 0:
            people_action_str_list.append(self.trans_p_people(start_ac))
        return people_action_str_list

    def gif_klotski(self, p_sign, action_list, use_times):
        """
        根据动作绘制三国华容道的生成过程
        :param p_sign: 题目编号
        :param action_list: 动作列表
        :param use_times: 计算所用时间
        :return: 三国华容道移动的过程
        """
        p_p_d = self.p_list.copy()
        #  需要将动作列表变为间隔为2
        action_list = action_list[1:].split('-')
        print('第%s局：%s解的步数：' % (p_sign, k.K_SIGN[p_sign]), len(action_list))
        # 将合并后的移动方案保存到txt文件中
        fh = open(r'./%d.txt' % p_sign, 'w')
        fh.write(','.join(self.combine_action_list(action_list)))
        fh.close()
        print('绘图中')
        for index, value in enumerate(action_list):
            # 首先根据起始和结束状态获取行为列表
            fig = plt.figure()
            gs = gridspec.GridSpec(1, 2)
            #  绘制初始状态
            ax = fig.add_subplot(gs[0, 0])
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title('第%d局：%s，用时$%.2fs$' % (p_sign, self.name, use_times))
            start_array = self.plot_klotski_data(self.p_list)
            ax.imshow(start_array)

            #  绘制中间转换的状态
            next_p_d = self.get_next_s(p_p_d, value)
            p_p_d = next_p_d.copy()
            ax = fig.add_subplot(gs[0, 1])
            if index != len(action_list) - 1:
                ax.set_title('曹操逃脱中：总共$%d$步，当前$%d$步' % (len(action_list), index+1))
            else:
                ax.set_title('曹操逃脱')
            ax.set_xticks([])
            ax.set_yticks([])
            end_array = self.plot_klotski_data(p_p_d)
            ax.imshow(end_array)
            plt.subplots_adjust(top=0.95, bottom=0.05, right=0.95, left=0.05, hspace=0.05, wspace=0.03)
            plt.margins(0, 0)
            plt.savefig(r'./%d_%d_%d.png' % (p_sign, len(action_list), index+1))

            plt.close()

        image_list = ['%d_%d_%d.png' % (p_sign, len(action_list), index+1) for index in range(len(action_list))]

        frames = []
        for image_name in image_list + [image_list[-1]] * 10:
            frames.append(imageio.imread(image_name))
        imageio.mimsave('%s_k.gif' % p_sign, frames, 'GIF', duration=0.9)  # 图片合成为动图

        print('第%s局动图生成完毕' % p_sign)


# 主函数
if __name__ == "__main__":
    for pp in range(1, 25):
        pp_mame = k.K_SIGN[pp]
        pp_data = k.K_DICT[pp_mame]
        kl = ThreeKing(pp_mame, pp_data)
        p = [i[0] for i in pp_data]
        start_time = time.clock()
        aa = kl.bfs_search(p)
        end_time = time.clock()
        kl.gif_klotski(pp, aa, end_time - start_time)




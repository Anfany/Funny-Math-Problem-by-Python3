# -*- coding：utf-8 -*-
# &Author  AnFany


# 利用状态空间bfs搜索算法获取8人过河的方案

# 现在有8个人分别为：
# 1个父亲，带着他的2个儿子。1个母亲，带着她的2个女儿；1个警察，带着1个犯人；
# 开始时，8个人都是在河的左岸。现在需要过河，过河时需要注意下面5条说明：
# 1，只有警察、父亲和母亲可以划船；
# 2，警察如果离开犯人，犯人就会伤害其他人；
# 3，母亲不在时，这个父亲会伤害她的女儿。
# 4，父亲不在时，这个母亲也会伤害他的儿子。
# 5，船上一次最多只能坐两个人。
# 求出过河方案。

# 解决方案。获取从起始状态到结束状态的所有的转移过程的状态转移字典，然后利用bfs算法获取最短的路径，方案利用绘图展现出来

# 初始状态用一个8维的向量表示，每个位置为1或者0，0表示该角色在左岸，1表示该角色在右岸，
# 向量从左到右分别代表的角色是：警察，犯人，父亲，儿子1，儿子2，母亲，女儿1，女儿2

import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl  # 作图显示中文
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 设置中文字体为新宋体


class RIVER():
    def __init__(self):
        # 左岸状态中的0表示在左岸，1表示不在；右岸状态中的1表示在右岸，0表示不在；
        self.s_s = '00000000L'  # 起始状态，最后一位L表示在左岸
        self.e_s = '11111111R'  # 结束状态，最后一位R表示在右岸

        self.role_dict = {0: '警察', 1: '犯人',
                          2: '父亲', 3: '大儿', 4: '小儿',
                          5: '母亲', 6: '大女', 7: '小女'}  # 位置编号和角色的对应

        # 在船上的人们的可能的角色编号序列
        self.boat_sign = [[0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
                          [2], [2, 3], [2, 4], [2, 5],
                          [5], [5, 6], [5, 7]]

    def judge_state(self, c_state):
        """
        判断一个状态是不是合理的
        :param c_state: 状态
        :return: 合理返回True，否则返回False
        """
        # 针对说明2
        if c_state[0] != c_state[1]:  # 警察犯人没在一起
            if c_state[1] in list(c_state[2:-1]):  # 并且和其他人中的某个在同一岸边
                return False

        # 针对说明3
        if c_state[5] != c_state[6] or c_state[5] != c_state[7]:
            if c_state[5] != c_state[2]:
                return False
        # 针对说明4
        if c_state[2] != c_state[3] or c_state[2] != c_state[4]:
            if c_state[2] != c_state[5]:
                return False
        return True

    def get_state_trans_dict(self):
        """
        获取从起始状态到结束状态之间的所有可能状态之间的转移的字典
        :return: 字典形式的状态转移关系
        """

        # 存储状态转移关系的字典
        state_trans_dict = {}
        # 防止出现循环，之前遍历过的状态就不再遍历，用字典存储已经遍历过的状态
        s_tate_dict = {self.s_s: 0}

        # 需要遍历的状态的节点
        need_state_list = [self.s_s]

        # 获取所有可能出现的状态
        while 1:
            next_state_list = []

            for s in need_state_list:
                # 遍历船上人们的所有的可能的情形
                for j in self.boat_sign:
                    # 判断该角色在状态中的值是否在对应的岸上
                    judge_role = 1   # 判断的标识
                    # 上船后剩下的人的状态
                    rest_s = list(s[:-1])
                    # 对岸接受之前的状态,
                    side_s = list(s[:-1])

                    if s[-1] == 'L':
                        for a in j:
                            if s[a] != '0':  # 不在左岸
                                judge_role = 0
                            rest_s[a] = '1'   # 上船之后值为1
                            side_s[a] = '1'  # 对岸接受后的值为1
                    else:
                        for a in j:
                            if s[a] != '1':  # 不在右岸
                                judge_role = 0
                            rest_s[a] = '0'   # 上船之后值为0
                            side_s[a] = '0'  # 对岸接受后的值为0

                    if judge_role:
                        # 判断。这几个人上船后，需要判断余下的人的状态是否合理以及对岸接收后的状态是否合理
                        if s[-1] == 'L':
                            new_rest_s = ''.join(rest_s + ['L'])
                            new_side_s = ''.join(side_s + ['R'])
                        else:
                            new_rest_s = ''.join(rest_s + ['R'])
                            new_side_s = ''.join(side_s + ['L'])

                        # 余下人的状态、对岸接受后的状态合理
                        if self.judge_state(new_rest_s) and self.judge_state(new_side_s):
                            # 说明状态s可以转移到状态new_side_s
                            if s in state_trans_dict:
                                state_trans_dict[s].append(new_side_s)
                            else:
                                state_trans_dict[s] = [new_side_s]
                            if new_side_s not in s_tate_dict:  # 以前没出现过。出现过，说明出现了无实际用处的转移，因此不考虑
                                # 判断是否是结束状态，不是的话需要添加到下一次的列表中
                                if new_side_s != self.e_s:
                                    next_state_list.append(new_side_s)
                                    s_tate_dict[new_side_s] = 0
            need_state_list = next_state_list.copy()
            # 只要不为空就继续
            if not need_state_list:
                break
        return state_trans_dict

    def get_path(self, s_dict):
        """
        利用BFS算法，根据状态字典获取路径
        :param s_dict: 状态转移之间关系的字典
        return: 可能的路径的列表
        """
        path_list = [[self.s_s]]  # 存储所有路径的列表
        copy_dict = s_dict.copy()
        cross_s = [self.s_s]  # 当前需要遍历的转移字典中的状态键

        while copy_dict:  # 只要字典不为空就继续

            next_state_list = []  # 下一步需要遍历的转移字典中的状态键
            new_path_list = []  # 更新以后的路径的列表
            # 开始初始状态遍历
            for k in cross_s:
                if k in copy_dict:  # 说明该状态可以转移到其他的状态
                    next_s = s_dict[k]  # 该状态可以转移到的状态的列表
                    for ss in path_list:
                        if ss[-1] == k:   # 在当前的路径中寻找以当前路径结尾的路径
                            for dd in next_s:
                                new_path_list.append(ss + [dd])  # 将可以转移到的状态添加到该路径中
                    next_state_list += next_s  # 下一步要遍历的状态

                    del copy_dict[k]  # 在字典中删除

            path_list = new_path_list.copy()  # 更新
            cross_s = next_state_list.copy()  # 更新
        # 去除掉结尾不是最终状态的路径
        last_path = [p for p in path_list if p[-1] == self.e_s]
        return last_path

    def state_to_people(self, state):
        """
        将表示状态的向量变为角色
        :param state: 状态的向量
        :return: 角色
        """
        start_str = ''
        for index, value in enumerate(state[:-1]):
            if state[-1] == 'L':
                start_str += self.role_dict[index] if not int(value) else '  ' * 2
            else:
                start_str += self.role_dict[index] if int(value) else '  ' * 2
        return start_str

    def get_boat(self, s1, s2):
        """
        根据两个状态，获取在船上的人们的角色
        :param s1: 状态1
        :param s2: 状态2
        :return: 船上的人们的角色
        """
        boat_str = ''
        for index, value in enumerate(s1[:-1]):
            if value != s2[index]:
                boat_str += self.role_dict[index]
        return boat_str

    def plot_method(self, method):
        """
        绘制过河的方案。
        :param method: 方案的列表
        :return: 图片
        """
        plt.figure(figsize=(8, 6))
        plt.axis('off')

        x_point = [0.1, 0.3, 0.4, 0.6, 0.7]

        plt.text(x_point[0], 0.93, '左岸', size='large', color='tab:red')
        plt.text(x_point[1], 0.93, '上船', size='large', color='m')
        plt.text(x_point[2], 0.93, '右岸', size='large', color='tab:green')
        plt.text(x_point[3], 0.93, '上船', size='large', color='m')
        plt.text(x_point[4], 0.93, '左岸', size='large', color='tab:red')

        # 绘制方案，只绘制一种方案
        row_count = len(method[0]) // 2 + 1

        # 行与行之间的间距
        tap = 0.9 / row_count

        def change_str(role_str):
            """
            将一行的字符串变为2行
            :param role_str: 角色的字符串
            :return: 2行的字符串
            """
            first_row = ''
            second_row = ''
            for i in range(len(role_str)):
                if i % 2 == 0:
                    first_row += role_str[i]
                else:
                    second_row += role_str[i]
            return first_row + '\n' + second_row

        # 绘制横线
        plt.plot([x_point[0], x_point[4]+0.2], [0.9 - tap + 0.04, 0.9 - tap + 0.04], '-', c='k')

        for index, value in enumerate(method[0]):
            if index % 2 == 0:
                # 绘制步数
                plt.text(0.0, 0.9 - (index // 2 + 1) * tap, '第%d步：' % (index // 2 + 1), color='k')

                y_point = 0.9 - (index // 2 + 1) * tap - 0.02

                # 绘制左岸
                plt.text(x_point[0], y_point, change_str(self.state_to_people(value)), color='tab:red')
                # 绘制船上
                plt.text(x_point[1], y_point, change_str(self.get_boat(value, method[0][index + 1])), color='m')

                # 绘制右岸
                plt.text(x_point[2], y_point, change_str(self.state_to_people(method[0][index + 1])), color='tab:green')

                if index < len(method[0]) - 2:
                    # 绘制上船
                    plt.text(x_point[3], y_point, change_str(self.get_boat(method[0][index + 1], method[0][index + 2])),
                             color='m')

                    # 绘制左岸
                    plt.text(x_point[4], y_point, change_str(self.state_to_people(method[0][index + 2])),
                             color='tab:red')

                # 绘制横线
                plt.plot([x_point[0], x_point[4]+0.2], [y_point-0.01, y_point-0.01], '-', c='k')

        plt.show()


# 主函数
if __name__ == "__main__":
    r = RIVER()
    m = r.get_state_trans_dict()
    p = r.get_path(m)
    r.plot_method(p)



























# -*- coding：utf-8 -*-
# &Author  AnFany
# 一笔画完问题

"""
利用DFS算法快速解决一笔画完问题，只得到一个解
也就是获得从起始网格开始，经过所有网格的，并且没有重复网格的路径
"""
import time
import sys  # 尾递归优化
import matplotlib.patches as mpatches  # 图例的设置
import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号

# 尾递归优化的程序
class TailRecurseException(BaseException):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs
def tail_call_optimized(g):
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs
    func.__doc__ = g.__doc__
    return func

#   利用DFS寻找路径的类
class Find_Path_DFS():

    def __init__(self):
        # 用不同数值表示不同意义的网格
        self.__Start_Node = 2
        self.__Walk_Node = 1
        self.__Stone_Node = 0

        # 用不同颜色表示不同网格
        self.__Start_Color = '#457896'
        self.__Walk_Color = (198 / 255, 198 / 255, 198 / 255)
        self.__Stone_Color = 'whitesmoke'
        self.__Path_Color = 'tab:red'

        # 图的竖直、水平方向网格的个数
        self.Map_Height = 9
        self.Map_Width = 7

        # 起始网格和不能经过的网格的索引
        self.Start_Index = [0, 2]
        self.Stone_Index = [[0, 3], [0, 6], [1, 6], [2, 6], [3, 1], [7, 1], [8, 3], [8, 5], [8, 6]]

        self.problem_array = self.nodes()

    # 表示图的数组
    def nodes(self):
        """
        在数组中将对应的网格变为对应的值
        """
        node_array = np.ones((self.Map_Height, self.Map_Width))
        # 起始网格标记
        node_array[self.Start_Index[0], self.Start_Index[1]] = self.__Start_Node
        # 不能走的网格
        for i in self.Stone_Index:
            node_array[i[0], i[1]] = self.__Stone_Node
        return node_array

    def can_go(self, index):
        """
        对于一个网格而言，可以去的网格，上下左右四个方向
        :param index: 索引
        """
        x, y = index
        node_list = []
        if x > 0:
            if self.problem_array[x - 1, y] == self.__Walk_Node:
                node_list.append([x - 1, y])
        if x < self.Map_Height - 1:
            if self.problem_array[x + 1, y] == self.__Walk_Node:
                node_list.append([x + 1, y])
        if y > 0:
            if self.problem_array[x, y - 1] == self.__Walk_Node:
                node_list.append([x, y - 1])
        if y < self.Map_Width - 1:
            if self.problem_array[x, y + 1] == self.__Walk_Node:
                node_list.append([x, y + 1])
        return node_list

    def judge_area_indived(self, have_walk):
        """
        判断走过的网格和不能走的网格是否把剩下的还没有走过的网格分为了不能连通的2部分，是的话就说明刚才加的网格不合理
        为了避免在一些本就不可能的路径上耽误时间
        选择任何一个没有走过的网格，然后扩展为这个网格可以去的区域，如果区域内的网格数等于剩下的网格数，则剩下的部分是连通的
        :param have_walk: 已经走过的网格 [[2, 3],[3, 4],[4, 5]]
        :return: 合理返回True，不合理返回False
        """
        all_cannot_node = have_walk + self.Stone_Index
        count_nodes = self.Map_Width * self.Map_Height  # 网格总个数
        if len(all_cannot_node) == count_nodes:  # 此时已经走完所有的网格
            return True
        # 随机选择一个不在上面集合中的网格
        center_node = []
        for i in range(self.Map_Height):
            for j in range(self.Map_Width):
                if [i, j] not in all_cannot_node:
                    center_node = [i, j]
                    break
        # 下面就开始扩展这个center_node可以去的区域
        current = [center_node]
        area_node = [center_node]  # 连通区域内的网格列表
        while current:  # 只要不为空存在就扩展
            copy_current = []
            for n in current:
                can_go_to = self.can_go(n)
                for d in can_go_to:
                    if d not in area_node and d not in have_walk:
                        copy_current.append(d)
                        area_node.append(d)
            current = copy_current
        if len(area_node) == count_nodes - len(all_cannot_node):  # 全部连通
            return True
        else:  # 存在不连通的区域
            return False

    @tail_call_optimized
    def find_one_path_dfs(self, node_list):
        """
        利用dfs深度优先算法快速求解满足条件的一条路径，只要经过的网格的个数等于可以走的网格的个数，就是一个解
        :param node_list: 表示走过的网格列表，[[node_index], node_sign]]，元素为网格索引和这个网格已经去往周围网格的个数，用于回溯
        :return: 路径列表
        """
        if not node_list:  # 所有的情况已经遍历完，node_list为[].不存在解
            return []
        if len(node_list) == self.Map_Height * self.Map_Width - len(self.Stone_Index):  # 找到一个解
            return node_list
        else:
            # 判断最后一个网格是否有可以去的网格
            node, sign = node_list[-1]
            can_go_list = self.can_go(node)
            if sign > len(can_go_list) - 1:  # 都去过了
                next_node = node_list[:-1]  # 就把最后一个网格去除掉
                if not next_node:
                    return []
                else:
                    # 开始往前回溯到还有选择余地的网格
                    for l in range(len(node_list) - 2, -1, -1):
                        current_node, node_sign = node_list[l]
                        can_g = self.can_go(current_node)
                        if node_sign <= len(can_g) - 1:  # 说明有选择的余地
                            next_node = node_list[:l + 1]
                            if not next_node:
                                break
                            else:
                                next_node[-1][1] += 1
                                return self.find_one_path_dfs(next_node)
                    # 所有的都没有选择的余地了
                    return []

            else:  # 有可以去的网格，
                #  选择之前没有出现过的网格,并且要保证添加的网格是合理的
                have_node = [c[0] for c in node_list]  # 已经在路径中的网格
                next_node = node_list
                #  只有之前没有出现过，并且是合理的网格，才可以添加到路径中
                try:
                    if can_go_list[sign] in have_node:
                        judge_reason = have_node
                    else:
                        judge_reason = have_node + [can_go_list[sign]]
                    while can_go_list[sign] in have_node or (not self.judge_area_indived(judge_reason)):
                        next_node[-1][1] += 1
                        sign += 1
                        # 判断这个节点是否是合理的
                        if can_go_list[sign] in have_node:
                            judge_reason = have_node
                        else:
                            judge_reason = have_node + [can_go_list[sign]]
                    next_node.append([can_go_list[sign], 0])
                    return self.find_one_path_dfs(next_node)
                except IndexError:
                    next_node = node_list[:-1]
                    if not next_node:
                        return []
                    else:
                        next_node[-1][1] += 1
                        return self.find_one_path_dfs(next_node)

    def find_one_path_plot(self):
        """
        展示寻找到的一条路径
        :return: 图示
        """
        plt.ion()
        # 首先绘制图
        fig, ax1 = plt.subplots()
        # 主刻度
        ax1.set_xticks(np.arange(self.Map_Width))
        ax1.set_yticks(np.arange(self.Map_Height))
        # 绘图
        af = col.LinearSegmentedColormap.from_list('anfany',
                                                   [self.__Stone_Color, self.__Walk_Color, self.__Start_Color])
        ax1.imshow(self.problem_array, cmap=af)
        # 像相当于次刻度
        ax1.set_xticks(np.arange(self.Map_Width) + 0.5, minor=True)
        ax1.set_yticks(np.arange(self.Map_Height) + 0.5, minor=True)
        # 添加网格
        ax1.xaxis.grid(True, which='minor', lw=2, c='snow')
        ax1.yaxis.grid(True, which='minor', lw=2, c='snow')

        #  不同的节点
        walk = mpatches.Patch(color=self.__Walk_Color, label='可走')
        stone = mpatches.Patch(color=self.__Stone_Color, label='不可走')
        start = mpatches.Patch(color=self.__Start_Color, label='开始点')
        path = mpatches.Patch(color=self.__Path_Color, label='路径')

        # 添加图例
        plt.legend(handles=[walk, stone, start],
                   bbox_to_anchor=(0.0, -0.13, 1, .102), loc='lower left',
                   ncol=3, mode="expand", borderaxespad=0.)

        plt.title('一笔画完问题，方法：dfs，寻找路径…………')
        plt.pause(0.0001)
        start_time = time.perf_counter()
        path_list = self.find_one_path_dfs([[self.Start_Index, 0]])
        # 在图中添加路径
        if not path_list:
            plt.title('不存在解, 用时：%.3fs' % (time.perf_counter() - start_time))
        else:
            x = [p[0][1] for p in path_list]
            y = [p[0][0] for p in path_list]
            ax1.plot(x, y, '-o', c=self.__Path_Color, lw=18)
            plt.title('路径添加完毕，方法：dfs, 用时：%.3fs' % (time.perf_counter() - start_time))
            # 添加图例
            plt.legend(handles=[walk, stone, start, path],
                       bbox_to_anchor=(-0.1, -0.13, 1.2, .102), loc='lower left',
                       ncol=4, mode="expand", borderaxespad=0.)
        plt.ioff()
        plt.show()


# 最终的函数
if __name__ == "__main__":
    p = Find_Path_DFS()
    #  获得题面数组
    p.find_one_path_plot()
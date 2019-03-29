# -*- coding：utf-8 -*-
# &Author  AnFany
# 一笔画完问题

"""
利用BFS以及DFS算法解决一笔画完问题，得到全部解
也就是获得从起始点开始，经过所有节点的，并且没有重复节点的路径
"""
import time
import sys  # 尾递归优化
import matplotlib.patches as mpatches  # 图例的设置
import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np
from pylab import mpl
import threading

#  定义全局变量，用于停止计时进程
global SIGN
SIGN = 1

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号

# 保存最终路径的文件夹
Fig_File = r'C:\Users\GWT9\Desktop\one_stroke'

# 用不同数值表示不同节点
Start_Node = 2
Walk_Node = 1
Stone_Node = 0


# 用不同颜色表示不同节点
Start_Color = '#457896'
Walk_Color = (198 / 255, 198 / 255, 198 / 255)
Stone_Color = 'whitesmoke'
Path_Color = 'tab:red'


# 图的竖直、水平方向网格的个数
Map_Height = 9
Map_Width = 7


# 起始节点和不能经过的点的索引
Start_Index = [1, 0]
Stone_Index = [[0, 3], [0, 6], [1, 6], [2, 6], [3, 1], [7, 1], [8, 3], [8, 5], [8, 6]]


# 表示图的数组
def nodes(h=Map_Height, w=Map_Width, start=Start_Index, stone=Stone_Index):
    """
    在数组中将对应的节点变为对应的值
    :param h: 图的竖直方向网格的个数
    :param w: 图的水平方向网格的个数
    :param start: 开始节点的索引
    :param stone: 石块节点的索引
    :return: 变换后的数组
    """
    node_array = np.ones((h, w))
    # 起始点标记
    node_array[start[0], start[1]] = Start_Node
    # 石块标记
    for i in stone:
        node_array[i[0], i[1]] = Stone_Node
    return node_array


def can_go(index, array):
    """
    对于一个索引而言，可以去的节点，上下左右四个方向
    :param index: 索引
    :param array: 数组
    :return: 可以去的节点索引的列表
    """
    if not index:
        return []
    x, y = index
    node_list = []
    if x > 0:
        if array[x - 1, y] == Walk_Node:
            node_list.append([x - 1, y])
    if x < Map_Height - 1:
        if array[x + 1, y] == Walk_Node:
            node_list.append([x + 1, y])
    if y > 0:
        if array[x, y - 1] == Walk_Node:
            node_list.append([x, y - 1])
    if y < Map_Width - 1:
        if array[x, y + 1] == Walk_Node:
            node_list.append([x, y + 1])
    return node_list


def judge_area_indived(have_walk, map, no_walk=Stone_Index, h=Map_Height, w=Map_Width):
    """
    判断走过的网格和不能走的网格是否把剩下的还没有走过的网格分为了不能连通的2部分，是的话就说明刚才加的网格不合理
    为了避免在一些本就不可能的路径上耽误时间
    选择任何一个没有走过的网格，然后扩展为这个网格可以去的区域，如果区域内的网格数等于剩下的网格数，则剩下的部分是连通的
    :param have_walk: 已经走过的网格 [[2, 3],[3, 4],[4, 5]]
    :param map: 数组
    :param no_walk: 不能走的网格集合
    :param h: 图的竖直方向网格的个数
    :param w: 图的水平方向网格的个数
    :return: 合理返回True，不合理返回False
    """
    all_cannot_node = have_walk + no_walk
    count_nodes = h * w  # 网格总个数
    if len(all_cannot_node) == count_nodes:  # 此时已经走完所有的网格
        return True

    # 随机选择一个不在上面集合中的网格
    center_node = []
    for i in range(h):
        for j in range(w):
            if [i, j] not in all_cannot_node:
                center_node = [i, j]
                break
    # 下面就开始扩展这个center_node可以去的区域
    current = [center_node]
    area_node = [center_node]  # 连通区域内的网格列表
    while current:  # 只要不为空存在就扩展
        copy_current = []
        for n in current:
            can_go_to = can_go(n, map)
            for d in can_go_to:
                if d not in area_node and d not in have_walk:
                    copy_current.append(d)
                    area_node.append(d)
        current = copy_current

    if len(area_node) == count_nodes - len(all_cannot_node):  # 全部连通
        return True
    else:  # 存在不连通的区域
        return False


class TailRecurseException(BaseException):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


# 尾递归优化的程序
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


@tail_call_optimized
def find_path_dfs(node_list, map, solution_list, h=Map_Height, w=Map_Width, s_i=Stone_Index):
    """
    利用深度优先算法快速求解满足条件的所有的路径，只要经过的网格的个数等于可以走的网格的个数，就是一个解
    :param node_list: 表示走过的网格列表，[[node_index], node_sign]]，元素为网格索引和这个网格已经去往周围网格的个数，用于回溯
    :param map: 表示图的数组
    :param solution_list: 存储所有的是解的路径
    :param h: 图的竖直方向网格的个数
    :param w: 图的水平方向网格的个数
    :param s_i: 不可以走的网格的索引
    :return: 路径列表
    """
    print('找到解的个数：', len(solution_list))
    if not node_list:  # 所有的情况已经遍历完，node_list为[].
        return solution_list

    if len(node_list) == h * w - len(s_i):  # 找到一个解
        solution_list.append([s[0] for s in node_list])  # 存储路径解

        # 此时要从倒数第2个节点往前回溯，找到还有选择余地的节点，
        for l in range(len(node_list) - 2, -1, -1):
            current_node, node_sign = node_list[l]
            can_g = can_go(current_node, map)
            if node_sign <= len(can_g) - 1:  # 说明有选择的余地
                next_node = node_list[:l+1]
                if not next_node:
                    break
                else:
                    next_node[-1][1] += 1
                    return find_path_dfs(next_node, map, solution_list)
        # 所有的都没有选择的余地了
        return solution_list
    else:
        # 判断最后一个网格是否有可以去的网格
        node, sign = node_list[-1]
        can_go_list = can_go(node, map)
        if sign > len(can_go_list) - 1:  # 都去过了
            next_node = node_list[:-1]  # 就把最后一个网格去除掉
            if not next_node:
                return solution_list
            else:
                # 开始往前回溯到还有选择余地的网格
                for l in range(len(node_list) - 2, -1, -1):
                    current_node, node_sign = node_list[l]
                    can_g = can_go(current_node, map)
                    if node_sign <= len(can_g) - 1:  # 说明有选择的余地
                        next_node = node_list[:l + 1]
                        if not next_node:
                            break
                        next_node[-1][1] += 1
                        return find_path_dfs(next_node, map, solution_list)
                # 所有的都没有选择的余地了
                return solution_list

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
                while can_go_list[sign] in have_node or (not judge_area_indived(judge_reason, map)):
                    next_node[-1][1] += 1
                    sign += 1
                    # 判断这个节点是否是合理的
                    if can_go_list[sign] in have_node:
                        judge_reason = have_node
                    else:
                        judge_reason = have_node + [can_go_list[sign]]

                next_node.append([can_go_list[sign], 0])
                return find_path_dfs(next_node, map, solution_list)
            except IndexError:
                next_node = node_list[:-1]
                if not next_node:
                    return solution_list
                next_node[-1][1] += 1
                return find_path_dfs(next_node, map, solution_list)


def find_path_bfs(map, h=Map_Height, w=Map_Width):
    """
    利用广度优先算法求解满足条件的路径，需要占用较大的内存空间
    :param map: 表示图的数组
    :param h: 图的竖直方向网格的个数
    :param w: 图的水平方向网格的个数
    :return: 路径列表
    """
    # 需要走过的节点数
    node_count = h * w - len(Stone_Index)

    # 存储所有的路径
    current_path_list = [[Start_Index]]

    count_nodes = 1

    # 当走过的节点数等于需要走过的节点数或者没有可走的节点时停止迭代
    while len(current_path_list) != 0 and count_nodes < node_count:
        # 因为每一次都遍历当前的节点列表，所以所有路径走的步数是一样的
        count_nodes += 1
        new_join_path = []
        for n in current_path_list:
            # 索引为n的节点可以去的节点列表为
            n_can_go = can_go(n[-1], map)
            # 在可以去的节点列表中只选择以前没有去过的
            for p in n_can_go:
                if p not in n:
                    new_path = n + [p]
                    new_join_path.append(new_path)
        current_path_list = new_join_path

        reasonable = []  # 其中合理的路径
        if len(current_path_list) != 0:
            for y in current_path_list:
                if judge_area_indived(y, map):
                    reasonable.append(y)
            print('走过的网格数:%d' % count_nodes, '候选路径:%d条' % len(current_path_list), '合理路径:%d条' % len(reasonable))
            current_path_list = reasonable

    if count_nodes == node_count:
        return current_path_list
    else:
        return []


class MyThread(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()
        self.func = func

    def run(self):
        self.result = self.func()

    def get_result(self):
        threading.Thread.join(self)
        try:
            return self.result
        except Exception:
            return None


def find_path_plot(map, method='dfs', h=Map_Height, w=Map_Width):
    """
    展示寻找到的路径
    :param map: 表示图的数组
    :param method: 寻找路径的方法，默认为dfs
    :param h: 图的竖直方向网格的个数
    :param w: 图的水平方向网格的个数
    :return: 图示
    """
    plt.ion()
    # 首先绘制图
    fig, ax1 = plt.subplots()
    # 主刻度
    ax1.set_xticks(np.arange(w))
    ax1.set_yticks(np.arange(h))
    # 绘图
    af = col.LinearSegmentedColormap.from_list('anfany', [Stone_Color, Walk_Color, Start_Color])
    ax1.imshow(map, cmap=af)
    # 像相当于次刻度
    ax1.set_xticks(np.arange(w) + 0.5, minor=True)
    ax1.set_yticks(np.arange(h) + 0.5, minor=True)
    # 添加网格
    ax1.xaxis.grid(True, which='minor', lw=2, c='snow')
    ax1.yaxis.grid(True, which='minor', lw=2, c='snow')

    #  不同的节点
    walk = mpatches.Patch(color=Walk_Color, label='可走')
    stone = mpatches.Patch(color=Stone_Color, label='不可走')
    start = mpatches.Patch(color=Start_Color, label='开始点')
    path = mpatches.Patch(color=Path_Color, label='路径')

    # 添加图例
    plt.legend(handles=[walk, stone, start],
               bbox_to_anchor=(0.0, -0.13, 1, .102), loc='lower left',
               ncol=3, mode="expand", borderaxespad=0.)
    # 利用多线程实现，添加计算路径用时的计时器
    start_time = time.clock()
    # 计时的函数

    def count_time():
        while SIGN:
            plt.title('寻找路径方法：%s，用时%.3fs' % (method, time.clock() - start_time))
            plt.pause(0.001)

    # 寻找路径的函数
    def get_path():
        if method == 'bfs':
            path_list = find_path_bfs(map)
        elif method == 'dfs':
            path_list = find_path_dfs([[Start_Index, 0]], map, [])
        else:
            path_list = []
        global SIGN
        SIGN = 0
        # 在图中添加路径
        if not path_list:
            if method in ['bfs', 'dfs']:
                plt.title('不存在解')
            else:
                plt.title('寻找路径的方法名错误')
        else:
            count_solution = len(path_list)
            for c_s in range(count_solution):
                single = path_list[c_s]
                # 注意x，y的坐标
                x = [single[p][1] for p in range(len(single))]
                y = [single[p][0] for p in range(len(single))]
                solution = ax1.plot(x, y, '-o', c=Path_Color, lw=18)
                if count_solution == 1:
                    plt.title('路径添加完毕，方法：%s' % method)
                else:
                    plt.title('路径添加完毕，方法：%s，解决方案%d之%d' % (method, count_solution, c_s + 1))
                # 添加图例
                plt.legend(handles=[walk, stone, start, path],
                           bbox_to_anchor=(-0.1, -0.13, 1.2, .102), loc='lower left',
                           ncol=4, mode="expand", borderaxespad=0.)
                plt.savefig(r'%s/%s_%s_%s.png' % (Fig_File, method, count_solution, c_s + 1))
                plt.pause(0.8)
                if c_s != count_solution - 1:
                    solution.pop(0).remove()
    # 多线程
    threads = []
    t1 = MyThread(count_time)
    threads.append(t1)

    t2 = MyThread(get_path)
    threads.append(t2)

    for t in threads:
        t.start()

    plt.ioff()
    plt.show()
    plt.close()


hh = nodes()

find_path_plot(hh)
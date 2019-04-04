# -*- coding：utf-8 -*-
# &Author  AnFany

#  需要用户自己在网站https://www.geogebra.org/graphing绘制出谜题，绘制完成后导出作图过程的html文件
#  程序读取作图过程，然后展示谜题，以及利用Fleury算法求解路径

import read_fig_html as r_f  # 读取作图过程html文件的程序
import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号


#  欧拉通路又称为欧拉开迹• 欧拉回路又称为欧拉闭迹
def judge_euler(line):
    """
    如果所有的节点均出现了偶数次,也就是节点的度为偶数，说明是闭欧闭迹，则起点和终点是同一个
    如果仅有2个节点出现了奇数次，也就是仅有2个节点的度为奇数，说明是欧拉开迹，则其中一个是起点，另一个是终点
    其他情况均不能一笔画出
    :param line: 边的列表
    :return: 起点，终点，度为奇数的点的集合
    """
    node = sum(line, [])
    node_list = [i for i in list(set(node)) if node.count(i) % 2 == 1]
    if not node_list:
        return node[0], node[0], node_list  # 起始点，终点, 奇数次的节点
    else:
        if len(node_list) == 2:
            return node_list[0], node_list[1], node_list  # 起始点，终点, 奇数次的节点
        else:
            return "None", 0, node_list


def get_dict(line):
    """
    以每个节点为键，可以去的节点为值的字典
    :param line: 边的列表
    :return: 字典
    """
    node_dict = {}
    for j in line:
        if j[0] in node_dict:
            node_dict[j[0]].append(j[1])
        else:
            node_dict[j[0]] = [j[1]]
        if j[1] in node_dict:
            node_dict[j[1]].append(j[0])
        else:
            node_dict[j[1]] = [j[0]]
    return node_dict


def select_line(walk_line, current_node, next_node, line):
    """
    # 判断当前节点current_node 和next_node组成的边是否是桥。如果去除这条边以后，剩下的图不是连通的，
    也就是存在没有线可以连接的两点，说明这是桥。如果都是桥，则任意选取节点作为next_node。否则先选择不是桥的节点
    :param walk_line: 已经走过的边
    :param current_node: 当前的节点
    :param next_node: 下一个节点
    :param line: 全部的边
    :return: 是桥，返回True，不是返回False
    """
    # 已经走过的边添加上要判断的边
    min_node, max_node = sorted([current_node, next_node])
    copy_walk_line = walk_line.copy()
    copy_walk_line.append([min_node, max_node])
    # 没有走过的边
    no_walk_line = [h for h in line if h not in copy_walk_line]

    # 剩下的所有的节点
    all_nodes = list(set(sum(no_walk_line, [])))

    # 首先判断是不是桥
    #  首先将边变为字典
    line_dict = {}
    for i in no_walk_line:
        if i[0] in line_dict:
            line_dict[i[0]].append(i[1])
        else:
            line_dict[i[0]] = [i[1]]
        if i[1] in line_dict:
            line_dict[i[1]].append(i[0])
        else:
            line_dict[i[1]] = [i[0]]

    # 选取next_node。开始扩展
    need_borden = [next_node]

    have_node = [need_borden[-1]]  # 可以去的节点

    while need_borden:
        for p in need_borden:
            if p in line_dict:
                for t in line_dict[p]:
                    if t not in have_node:
                        have_node.append(t)
                        need_borden.append(t)
            need_borden.remove(p)

    return len(have_node) != len(all_nodes)  # 不相等说明剩余的部分不是连通的，说明当前节点和下一个节点构成的边是桥


def solve(line):
    """
    对于可以一笔画出的问题，给出节点走的顺序
    :param line: 边的列表
    :return: 经过节点的顺序，也就是一笔画出的路径
    """
    start_node, end_node, prime_node = judge_euler(line)
    node_dict = get_dict(line)

    if start_node == 'None':  # 不能一笔画出
        return [], prime_node

    # 下面利用
    # 当前的节点
    current_node = start_node
    # 所有边的字典
    line_dict = {}
    for l in line:
        line_dict[tuple(l)] = 1
    # 走过的节点
    walk_node = [current_node]
    # 走过的边
    walk_line = []

    # 利用Fleury算法求解路径
    while len(line_dict) != 0:
        # 下一个要去的节点，和当前的节点构成的边不能是桥
        can_go_node = []
        bridge = 0
        for n in node_dict[current_node]:
            # 节点next和current_node构成的边没有走过
            min_node, max_node = sorted([n, current_node])
            if (min_node, max_node) in line_dict:
                can_go_node.append(n)
                if not select_line(walk_line, current_node, n, line):  # 优先选择不是桥的,
                    current_node = n
                    bridge = 1
                    break
        # 都是桥。只好随便选择一个是桥的边
        if not bridge:
            for ee in can_go_node:
                current_node = ee
        # 要把这个边标记为走过
        min_node, max_node = sorted([walk_node[-1], current_node])

        del line_dict[(min_node, max_node)]
        walk_line.append([min_node, max_node])
        walk_node.append(current_node)

    return walk_node, prime_node


def plot_solution(line, node):
    """
    根据点的位置以及边的连接情况，绘制谜题并给出解
    :param line:  点的位置信息
    :param node:  边的连接情况
    :return: 问题的解
    """
    plt.ion()
    fig, (ax0, ax1) = plt.subplots(ncols=2)
    ax0.axis('off')
    ax1.axis('off')
    # 绘制谜题
    for n in line:
        o, s = n
        ax0.plot([node[o][0], node[s][0]], [node[o][1], node[s][1]], '-o', lw=2, c='#75664d', ms=8, mfc='#0c8918')
    for t in node:
        ax0.text(node[t][0], node[t][1], '$%d$' % t, fontsize=14, color='#bf3553')

    ax0.set_title('谜题，路径计算中')
    plt.pause(2)
    solution, prime_node = solve(line)

    if not solution:
        ax0.set_title('不能一笔画出')
        ax1.text(0.3, 0.5, '节点的连线个数是奇数的有\n%s' % prime_node, fontsize=13)
    else:
        # 开始绘制解
        ax0.set_title('谜题，路径添加中')
        ax1.set_title('点的经过顺序')
        for p in range(len(solution) - 1):
            o, s = solution[p], solution[p + 1]
            ax0.plot([node[o][0], node[s][0]], [node[o][1], node[s][1]], '-', lw=5, c='#1a94bc')
            # 显示具体的步骤
            grid = int(len(line) ** 0.5) + 1
            x = p % grid * (1 / grid)
            y = 0.9 - p // grid * (1 / grid)
            if p == 0:
                ax1.text(x, y, '始$%d->%d$' % (o, s), fontsize=10, color='#2d0c13')
            elif p == len(solution) - 2:
                ax1.text(x, y, '$->%d$终' % s, fontsize=10,  color='#2d0c13')
            else:
                ax1.text(x, y, '$-->%d$' % s, fontsize=10, color='#2d0c13')
            plt.pause(0.6)
        ax0.set_title('谜题，路径添加完毕')
    plt.ioff()
    plt.show()


# 主函数
if __name__ == "__main__":
    #  在网站绘图导出的作图过程的html文件的绝对路径
    fig_html = r'C:\Users\GWT9\Desktop\9.html'
    line, node = r_f.decode_fig(fig_html)
    plot_solution(line, node)

# -*- coding：utf-8 -*-
# &Author  AnFany

#  需要用户自己在网站https://www.geogebra.org/graphing绘制出谜题，绘制完成后导出作图过程的html文件
#  程序读取作图过程，然后展示谜题以及最终的求解过程

import read_fig_html as r_f  # 读取作图过程html文件的程序
import matplotlib.pyplot as plt

from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号


#  欧拉通路又称为欧拉开迹• 欧拉回路又称为欧拉闭迹
def judge_euler(line):
    """
    如果所有的节点均出现了偶数次，说明是闭欧闭迹，则起点和终点是同一个
    如果仅有2个节点出现了奇数次，说明是欧拉开迹，则其中一个是起点，另一个是终点
    其他情况均不能一笔画出
    :param line: 边的集合
    :return: 节点号
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


def solve(line):
    """
    对于可以一笔画的问题，给出节点走的顺序
    :param line: 边的列表
    :return: 顺着节点移动的顺序
    """
    start_node, end_node, prime_node = judge_euler(line)
    node_dict = get_dict(line)

    if start_node == 'None':
        return [], prime_node
    # 当前的节点
    current_node = start_node
    # 所有边的字典
    line_dict = {}
    for l in line:
        if tuple(l) in line_dict:
            line_dict[tuple(l)] += 1
        else:
            line_dict[tuple(l)] = 1
    # 走过的节点
    walk_node = [current_node]

    while len(line_dict) != 0:
        # 判断当前的节点可以去的节点中
        # 如果有没有走过的节点，则随便去一个就行
        # 如果都去过，则就去任意一个
        no_walk = []
        for i in node_dict[current_node]:
            if i not in walk_node:
                no_walk.append(i)
        if not no_walk:  # 如果都去过，首先选择不是终点的节点，如果没有别的节点，则选择终点
            no_end = 0
            for j in node_dict[current_node]:
                min_node, max_node = min(j, current_node), max(j, current_node)
                if (min_node, max_node) in line_dict:
                    if j != end_node:
                        current_node = j
                        no_end = 1
                        break
            if not no_end:
                current_node = end_node
        else:  # 如果存在没有去过的节点，就随便去一个就可以
            current_node = no_walk[0]

        if walk_node[-1] > current_node:
            min_node, max_node = current_node, walk_node[-1]
        else:
            min_node, max_node = walk_node[-1], current_node

        # 记录下这条边走过
        if line_dict[(min_node, max_node)] == 1:
            del line_dict[(min_node, max_node)]
        else:
            line_dict[(min_node, max_node)] -= 1
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

    plt.ioff()
    plt.show()


fig_html = r'C:\Users\anaifan\Desktop\geogebra-export.html'
line, node = r_f.decode_fig(fig_html)

plot_solution(line, node)
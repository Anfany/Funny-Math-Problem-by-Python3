


# -*- coding：utf-8 -*-
# &Author  AnFany

#  引入库
from matplotlib import colors as mcolors
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl  # 作图显示中文
import os
os.chdir(r'C:\Users\GWT9\Desktop')


#  题目和关键词对应关系字典
problem_dict = {'s': '数独', 'n': '八皇后', 'h': '汉诺塔', 'd': '二十四点', 'm': '幻方', 'p': '完美迷宫', 'c': '凸包',
                'b': '七桥', 'o': '一笔画完', 'a': '变态曲线', 't': '旅行商', 'e': '爱因斯坦问题', 'f': '分形',
                'r': '八人过河', 'w': '十五数码', 'z': '华容道', 'l': '生命游戏'}

method_dict = {'s': '回溯', 'n': '回溯', 'h': '公式', 'd': '正则', 'm': '公式', 'p': '普里姆算法', 'c': '葛立恒扫描法',
               'b': '弗罗莱算法', 'o': '深度、广度优先搜索', 'a': '积分与极限', 't': '遗传算法', 'e': '逻辑与回溯', 'f': '绘图',
               'r': '状态空间', 'w': '迭代加深启发', 'z': '广度优先搜索', 'l': '二维细胞自动机'}

#  选择颜色中比较重的
line_color = np.array([hco for hco in list(mcolors.cnames.keys()) if hco not
                       in ['k', 'w', 'whitesmoke', 'floarwhite', 'aliceblue',
                           'black', 'seashell', 'ivory', 'ghostwhite', 'beige', 'snow',
                           'white', 'gainsboro', 'mistyrose', 'peachpuff', 'linen', 'palegreen',
                           'honeydew', 'lightgoldenrodyellow', 'lightyellow', 'palegoldenrod',
                           'khaki', 'lemonchiffon', 'cornsilk', 'floralwhite', 'oldlace',
                           'wheat', 'moccasin', 'papayawhip', 'blanchedalmond', 'navajowhite',
                           'antiquewhite', 'bisque', 'mintcream', 'aquamarine', 'azure', 'lightcyan',
                           'paleturquoise', 'lavender', 'thistle', 'pink', 'lightpink', 'lavenderblush',
                           'aliceblue', 'lightblue', 'powderblue', 'plum', 'lightgray', 'lightgrey',
                           'silver', 'yellow', 'gold', 'greenyellow', 'chartreuse', 'lawngreen']])


def get_y_number(p_dict):
    """
    根据题目的个数，得到随机的纵坐标系列。
    :param p_dict: 题目字典
    :return: 随机的纵坐标系列
    """
    y_num_list = np.linspace(1.5, len(p_dict) + 0.5, len(p_dict))
    np.random.shuffle(y_num_list)
    return y_num_list


#  绘制图片
def figure(p_dict, m_dict, c=line_color, m_n=4):
    """
    根据题目字典以及方法字典绘制图片
    :param p_dict: 题目字典
    :param m_dict: 方法字典
    :param c: 可以选择的颜色
    :param m_n: 移动的步数
    :return: 图片
    """
    p_y = get_y_number(p_dict)  # 题目的纵坐标序列
    m_y = get_y_number(p_dict)  # 方法的纵坐标系列

    key_list = list(problem_dict.keys())  # 题目的关键词序列

    plt.figure(figsize=(8, 6))  # 绘图
    plt.xlim(0, len(p_dict) + 2)
    plt.ylim(0, len(p_dict) + 2)
    plt.axis('off')

    # 设置字体
    mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']

    # 保证题目是不一样的颜色
    c_p_list = []
    # 得到关键词和颜色的对应字典
    key_c_dict = {}

    # 获得位置与方法的字典
    a_method_dict = {}

    for h in range(len(key_list)):
        #  添加题目
        c_p = np.random.choice([f for f in c if f not in c_p_list], 1)[0]
        c_p_list.append(c_p)
        plt.text(1 - len(p_dict[key_list[h]]) / 2 * 0.45, p_y[h], p_dict[key_list[h]], color=c_p, size=13)
        # 添加字典
        key_c_dict[h] = c_p

        # 保证方法和题目的颜色是对应的
        plt.text(5 - len(m_dict[key_list[h]]) / 2 * 0.45, m_y[h], m_dict[key_list[h]], color=c_p, size=13)

        a_method_dict[m_y[h]] = key_list[h]

    # 按照所给字母的移动顺序确定关键词的顺序
    # 按照字典键的从小到大顺序得到关键词的顺序
    s_dict = sorted(a_method_dict.items(), key=lambda x: x[0], reverse=True)
    s_key_list = [k[1] for k in s_dict]
    # 按照移动的顺序获得新的次序列表
    new_list = s_key_list.copy()
    for index, value in enumerate(s_key_list):
        new_list[(index + m_n) % len(new_list)] = value
    # 添加关键词
    for k in range(len(s_dict)):
        plt.text(9, s_dict[k][0], new_list[k], color='k', size=13)

    plt.text(1 - 2 * 0.45, len(p_dict) + 1.5, '趣味谜题', size=15, color='k')
    plt.text(5 - 2 * 0.45, len(p_dict) + 1.5, '解题算法', size=15, color='k')
    plt.text(9 - 1.5 * 0.45, len(p_dict) + 1.5, '关键词', size=15, color='k')
    plt.plot([0, len(p_dict)-2], [len(p_dict)+1.2, len(p_dict)+1.2], c='k', lw=3)
    fu = '\downarrow' * m_n
    plt.text(len(p_dict)-1, len(p_dict)-1, '提示：\n\n(1)RGB' + '\n' + r'$(2)%s$' % fu, size=12,
             color=(152/255, 35/255, 156/3255))
    plt.savefig(r'.\puzzle.png')
    plt.show()


figure(problem_dict, method_dict)



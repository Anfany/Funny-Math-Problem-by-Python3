# -*- coding：utf-8 -*-
# &Author  AnFany

# 用户自己在网站https://www.geogebra.org/graphing绘制出谜题，
# 绘制谜题时，不要自定义点的标识，用网站的默认值即可
# 绘制完成后导出作图过程的html文件
# 本程序实现读取html文件

from bs4 import BeautifulSoup

# 解析绘图过程的函数
def decode_fig(html_file):
    """
    根据作图过程的html文件，获取解决谜题需要的信息
    :param html_file: 作图过程的html文件
    :return: 用于绘图的点的位置信息以及计算路径的边的信息
    """
    node_dict = {}  # 作图时的顶点为大写字母，此时利用数字, 键为顶点编号，值为坐标的位置
    line_list = []  # 存储连接的边，注意数字较小的在前面

    # 主要获取点的坐标信息以及边的连接信息
    with open(html_file, 'rb') as f:
        soup = BeautifulSoup(f.read(), 'html5lib')
        str_text = soup.select('td')

    for t in str_text:
        row_text = t.text.replace(' ', '')  # 替换掉空格
        if 'Segment' in row_text:  # 判断边
            # 因为Segment是固定的
            line_info = row_text[8:-1].split(',')  # 获取边的2个顶点
            line_list.append(line_info)

        if '=' in row_text and '(' in row_text:  # 判断点的位置
            equal_sign = row_text.index('=')  # 首先获取等号的位置
            line_info = row_text[equal_sign+2: -1].split(',')  # 获取点的坐标信息
            node_dict[row_text[:equal_sign]] = [float(x) for x in line_info]  # 转变为小数

    all_nodes = sorted(list(set(sum(line_list, []))))  # 获取所有的不重复的节点
    alpha_digit_dict = {value: index + 1 for index, value in enumerate(all_nodes)}

    # 开始将边中顶点的字母标识变为数字
    digit_line_list = []
    for l in line_list:
        c, d = l
        c_n, d_n = alpha_digit_dict[c], alpha_digit_dict[d]
        if c_n > d_n:
            digit_line_list.append([d_n, c_n])
        else:
            digit_line_list.append([c_n, d_n])

    # 将点的位置的字母标识同样变为数字标识
    digit_node_dict = {alpha_digit_dict[h]: node_dict[h] for h in node_dict}

    return digit_line_list, digit_node_dict







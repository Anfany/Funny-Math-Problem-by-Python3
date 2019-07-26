# -*- coding：utf-8 -*-
# &Author  AnFany

#  利用python解决爱因斯坦问题
#
# 在一条街上，有5座房子，喷了不同的5种颜色。 每个房子里住着不同国籍的人。
# 每个人喝着不同的饮料，抽不同品牌的香烟，养不同的宠物。 问：谁养鱼？
#
# 提示：
# 1、英国人住红色房子。
# 2、瑞典人养狗。
# 3、丹麦人喝茶。
# 4、绿色房子紧挨着白色房子，并在白色房子左边。
# 5、绿色房子主人喝咖啡。
# 6、抽Pall Mall香烟的人养鸟。
# 7、黄色房子主人抽Dunhill香烟。
# 8、住在中间房子的人喝牛奶。
# 9、挪威人住第一间房。
# 10、抽Blends香烟的人住在养猫的人隔壁。
# 11、养马的人住抽Dunhill香烟的人隔壁。
# 12、抽Blue Master的人喝啤酒。
# 13、德国人抽Prince香烟。
# 14、挪威人住蓝色房子隔壁。
# 15、抽Blends香烟的人有一个喝水的邻居。

from itertools import permutations as p
import copy
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号


Key_List = ['房子颜色', '哪的国籍', '喝的饮料', '抽的香烟', '养的宠物']


def get_information(r_dict, key1, key2):
    """
    根据key1, key2以及r_dict,得到当前的字典中可以添加条件的内容的位置
    :param r_dict: 关系字典
    :param key1: 字典键1
    :param key2: 字典键2
    :return: 位置序列
    """
    num1 = r_dict[key1]
    num2 = r_dict[key2]
    index_list = []
    for a, b in enumerate(num1):
        if not b and not num2[a]:
            index_list.append(a)
    return index_list


def judge_valid(r_dict, c_15, c_10, c_11):
    """
    根据r_dict确定的关系，判断此字典是否满足c_list中描述的条件
    :param r_dict: 关系字典
    :param c_15: 不确定条件c15
    :param c_10: 不确定条件c10
    :param c_11: 不确定条件c11
    :return: 不满足返回False，满足返回r_dict
    """
    # 存储所有的解
    all_solution = []
    # 首先根据c15判断
    # 获取内容香烟：Blends的位置
    b_no_index = r_dict[c_15[0]].index('')
    # 获取内容饮料：水的位置
    w_no_index = r_dict[c_15[2]].index('')
    # 判断是否为隔壁
    if abs(b_no_index - w_no_index) != 1:
        return all_solution
    else:
        # 添加条件中的内容
        r_dict[c_15[0]][b_no_index] = c_15[1]
        r_dict[c_15[2]][w_no_index] = c_15[3]
        # 此时只有宠物中还有3个未填内容。一共有6种可能性，遍历这6种可能，只要满足条件10和11，就可得到结果
        # 首选得到3个未填内容的位置
        index_sign = []
        for s, val in enumerate(r_dict['养的宠物']):
            if not val:
                index_sign.append(s)
        # 获取三个宠物的全排列
        for a in p(['猫', '马', '鱼']):
            for i_m, i_a in zip(index_sign, list(a)):
                r_dict['养的宠物'][i_m] = i_a
            # 判断r_dict是否满足条件10
            # 获取内容宠物：猫的位置
            cat_no_index = r_dict[c_10[2]].index(c_10[3])
            if abs(b_no_index - cat_no_index) == 1:
                # 判断r_dict是否满足条件11
                # 获取内容宠物：马的位置
                horse_no_index = r_dict[c_11[0]].index(c_11[1])
                # 获取内容香烟：Dunhill的位置
                dun_no_index = r_dict[c_11[2]].index(c_11[3])
                if abs(horse_no_index - dun_no_index) == 1:
                    # 说明满足条件10和条件11
                    uu = copy.deepcopy(r_dict)
                    all_solution.append(uu)
        return all_solution


def recall(r_dict, c_sign, c_set, result):
    """
    依据回溯算法，获取所有的方案
    :param r_dict: 关系字典
    :param c_sign: 当前需要添加条件的编号
    :param c_set: 条件的集合
    :param result: 存储方案
    :return: 最终的方案
    """
    # 判断回溯停止的条件
    if c_sign == 0 and c_set[0][-1] >= len(c_set[0][-2]):
        return result
    else:
        # 回溯
        # 获取当前需要添加的条件
        c_c = c_set[c_sign]
        # 获取可以添加条件的位置列表
        ad_c = c_c[4]
        # 此时要判断该条件的位置是否还有没有取到的可能性
        if c_c[-1] >= len(c_c[-2]):
            # 说明此位置已经没有可以取的值了
            # 需要回溯,当前的条件复原
            c_c[-1] = 0
            c_set[c_sign] = c_c
            try:
                one_index = r_dict[c_c[0]].index(c_c[1])
                r_dict[c_c[0]][one_index] = ''
                two_index = r_dict[c_c[2]].index(c_c[3])
                r_dict[c_c[2]][two_index] = ''
            except ValueError:
                pass
            # 此时的字典要返回到生一个条件之前的状态
            c_sign -= 1
            dd = c_set[c_sign]
            one_index = r_dict[dd[0]].index(dd[1])
            r_dict[dd[0]][one_index] = ''
            two_index = r_dict[dd[2]].index(dd[3])
            r_dict[dd[2]][two_index] = ''
            return recall(r_dict, c_sign, c_set, result)
        else:
            # 获取添加条件的位置
            a_c = ad_c[c_c[-1]]
            # 判断这个条件是否合理
            if r_dict[c_c[0]][a_c] == '' and r_dict[c_c[2]][a_c] == '' \
                    and c_c[1] not in r_dict[c_c[0]] and c_c[3] not in r_dict[c_c[2]]:
                # 添加内容
                r_dict[c_c[0]][a_c] = c_c[1]
                r_dict[c_c[2]][a_c] = c_c[3]
                # 说明当前是最后一个条件
                if c_sign == len(c_set) - 1:
                    hh = copy.deepcopy(r_dict)
                    # 存储起来
                    result.append(hh)
                    # 继续判断该条件的下一个可能性
                    c_c[-1] += 1
                    c_set[c_sign] = c_c
                    # 字典复原
                    one_index = r_dict[c_c[0]].index(c_c[1])
                    r_dict[c_c[0]][one_index] = ''
                    two_index = r_dict[c_c[2]].index(c_c[3])
                    r_dict[c_c[2]][two_index] = ''
                    return recall(r_dict, c_sign, c_set, result)
                else:
                    # 当前的条件需要改变
                    c_c[-1] += 1
                    c_set[c_sign] = c_c
                    # 条件编号需要改变
                    c_sign = (c_sign + 1) % len(c_set)
                    # 要继续回溯
                    return recall(r_dict, c_sign, c_set, result)
            else:
                # 不满足条件，则需要将该条件弄到下一个位置，条件编号不需要改变
                c_c[-1] += 1
                c_set[c_sign] = c_c
                try:
                    one_index = r_dict[c_c[0]].index(c_c[1])
                    r_dict[c_c[0]][one_index] = ''
                    two_index = r_dict[c_c[2]].index(c_c[3])
                    r_dict[c_c[2]][two_index] = ''
                except ValueError:
                    pass
                # 要继续回溯
                return recall(r_dict, c_sign, c_set, result)


def run():
    """
    :return: 无解返回False，有解返回最终的对应关系
    """
    # 存储关系的为字典，键分别代表'房子颜色', '哪的国籍', '喝的饮料', '抽的香烟', '养的宠物'。各自的值为长度为5的列表
    relation_dict = {}
    for key in Key_List:
        relation_dict[key] = ['' for j in range(5)]

    # 根据条件得到的信息，为字典添加内容。

    relation_dict['喝的饮料'][2] = '牛奶'  # 8、住在中间房子的人喝牛奶。
    relation_dict['哪的国籍'][0] = '挪威'  # 9、挪威人住第一间房。
    relation_dict['房子颜色'][1] = '蓝色'  # 14、挪威人住蓝色房子隔壁。

    # 4、4、绿色房子紧挨着白色房子，并在白色房子左边。结合条件1，第一个肯定不为红色房子。结合条件5，第三个肯定不为绿色房子
    house_set = []
    for h in p(['红', '白', '黄', '绿']):
        h_list = list(h)
        # 4、绿色房子在白色房子的相邻的左面和条件1、条件5。
        h_list.insert(1, '蓝')
        if h_list.index('绿') - h_list.index('白') == -1 and h_list[0] != '红' and h_list[2] != '绿':
        # 如果绿色房子和白色房子也可以不相邻，则有7种结果
        # if h_list.index('绿') - h_list.index('白') < 0 and h_list[0] != '红' and h_list[2] != '绿':
            house_set.append(h_list)
    # 存储所有的结果
    albert_result = []

    # 需要深度复制
    copy_relation_dict = copy.deepcopy(relation_dict)

    # 先选择一种房子的排列形式
    for h_c in house_set:
        relation_dict['房子颜色'] = h_c
        # 房子确定后。继续添加条件
        relation_dict['哪的国籍'][relation_dict['房子颜色'].index('红')] = '英国'  # 1、英国人住红色房子。
        relation_dict['喝的饮料'][relation_dict['房子颜色'].index('绿')] = '咖啡'  # 5、绿色房子主人喝咖啡。
        relation_dict['抽的香烟'][relation_dict['房子颜色'].index('黄')] = 'Dunhill'  # 7、黄色房子主人抽Dunhill香烟。

        # 提取条件中的信息：
        # 对应条件，添加下面的条件,因为需要用到回溯，因此需要把每个可以添加该条件的位置，以及当前选取哪一个位置记录上
        c2 = ['哪的国籍', '瑞典', '养的宠物', '狗', get_information(relation_dict, '哪的国籍', '养的宠物'), 0]  # 2、瑞典人养狗。
        c3 = ['哪的国籍', '丹麦', '喝的饮料', '茶', get_information(relation_dict, '哪的国籍', '喝的饮料'), 0]  # 3、丹麦人喝茶。
        # 6、抽Pall Mall香烟的人养鸟。
        c6 = ['抽的香烟', 'Pall Mall', '养的宠物', '鸟', get_information(relation_dict, '抽的香烟', '养的宠物'), 0]
        # 12、抽Blue Master的人喝啤酒。
        c12 = ['抽的香烟', 'Blue Master', '喝的饮料', '啤酒', get_information(relation_dict, '抽的香烟', '喝的饮料'), 0]
        # 13、德国人抽Prince香烟。
        c13 = ['哪的国籍', '德国', '抽的香烟', 'Prince', get_information(relation_dict, '哪的国籍', '抽的香烟'), 0]

        # 不确定条件。
        # 在下面的不确定条件以前，香烟已经出现4个品牌，因此可以得到香烟的整个序列。饮料也已经出现4个品牌。因此也可固定。
        # 因此先处理条件15，然后再判断是否满足条件10和11，如果满足则说明得到结果，否则就需要进行对应的条件的回溯。
        c15 = ['抽的香烟', 'Blends', '喝的饮料', '水']  # 15、抽Blends香烟的人有一个喝水的邻居。
        c10 = ['抽的香烟', 'Blends', '养的宠物', '猫']  # 10、抽Blends香烟的人住在养猫的人隔壁。
        c11 = ['养的宠物', '马', '抽的香烟', 'Dunhill']  # 11、养马的人住抽Dunhill香烟的人隔壁。

        # 回溯算法
        # 条件的组合
        resu = recall(relation_dict, 0, [c2, c3, c6, c12, c13], [])
        # 在得到的结果中选取满足条件15，10，11的
        for km in resu:
            middle_result = judge_valid(km, c15, c10, c11)
            if middle_result:
                for kk in middle_result:
                    albert_result.append(kk)

        relation_dict = copy.deepcopy(copy_relation_dict)

    return albert_result


# 将结果展示出来
def plot_result(r_dict, title, k_list=Key_List):
    """
    展示结果
    :param r_dict: 字典
    :param title: 方案的标识
    :param k_list: 键的顺序
    :return: 图片的表格
    """
    labelr = k_list
    chars = [[r_dict[b][i] for i in range(len(r_dict))] for b in k_list]
    # 获取鱼的位置以及相应的国籍
    fish_sign = [k_list.index('养的宠物'), r_dict['养的宠物'].index('鱼')]
    country_sign = [k_list.index('哪的国籍'), r_dict['养的宠物'].index('鱼')]
    r = r_dict['哪的国籍'][r_dict['养的宠物'].index('鱼')]
    plt.style.context('Solarize_Light2')
    fig, ax = plt.subplots()
    ax.set_title('爱因斯坦问题结果(%d-%d)：养鱼的是%s人' % (title[0], title[1], r))
    # 突出显示结果
    c_list = [["whitesmoke" for c in range(len(r_dict))] for r in range(len(r_dict))]
    c_list[fish_sign[0]][fish_sign[1]] = 'lightcoral'
    c_list[country_sign[0]][country_sign[1]] = 'lightcoral'
    ax.set_axis_off()
    table = ax.table(
        cellText=chars,
        rowLabels=labelr,
        rowColours=["orange"] * 5,
        cellColours=c_list,
        cellLoc='center',
        loc='upper right',
        colWidths=[0.18] * len(r_dict))
    table.set_fontsize(20)
    fig.tight_layout()
    plt.show()


# 主函数
if __name__ == "__main__":
    result = run()
    for index, value in enumerate(result):
        plot_result(value, [len(result), index+1])




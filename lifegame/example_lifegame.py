# -*- coding：utf-8 -*-
# &Author  AnFany
# WeChat: PythonFan

# 制作生命游戏震荡态的代码
from pylab import *
from matplotlib.colors import LinearSegmentedColormap
# 制作gif
import imageio  # 引入合成gif的库
mpl.rcParams['font.sans-serif'] = ['SimHei']


class LifeGame:
    def __init__(self, n, m, start_life_list):
        self.n = n
        self.m = m
        self.life_c = '#1a6840'  # 活细胞的颜色
        self.dead_c = '#f3f5e7'  # 死细胞的颜色
        self.life_n = 0  # 因为用热力图绘制，所以需要给细胞数字
        self.dead_n = 1

        # 开始的活细胞位置列表
        self.start_life_list = start_life_list
        # 开始局面
        self.initial_matrix = self.create_init_life()

    # 创建初始的情况
    def create_init_life(self):
        init_matrix = np.ones((self.n, self.m)) * self.dead_n
        for jj in self.start_life_list:
            cow = jj // self.m
            col = jj % self.m
            init_matrix[cow][col] = self.life_n
        return init_matrix

    # 获取相邻的细胞
    def get_round(self, r, c, lifematrix):
        number_list = []
        for i in range(max(0, r - 1), min(self.n, r + 2)):
            for j in range(max(0, c - 1), min(self.m, c + 2)):
                if i != r or j != c:
                    number_list.append(lifematrix[i][j])
        return number_list

    # 根据规则进行一代代的变化
    def create_by_rule(self):
        copy_matrix = self.initial_matrix.copy()
        for row in range(self.n):
            for column in range(self.m):
                l_count = self.get_round(row, column, self.initial_matrix).count(self.life_n)
                if self.initial_matrix[row][column] == self.life_n:
                    if l_count < 2 or l_count >= 4:
                        copy_matrix[row][column] = self.dead_n
                else:
                    if l_count == 3:
                        copy_matrix[row][column] = self.life_n
        self.initial_matrix = copy_matrix.copy()
        return self.initial_matrix


# 生成随机开局的活细胞位置列表
def start_random_life(n, m, p=0.375):
    sign_list = np.random.choice(np.arange(n * m),
                                 int(n * m * p), replace=False)
    return sign_list


# 周期为10
# start_life_list, n, m, t, sign = ([51, 52, 58, 59, 88, 89, 95, 96, 237, 238, 242, 243, 273, 274, 276, 278, 280, 281, 312, 313, 315, 316, 347, 348, 350, 352, 354, 355, 385, 386, 390, 391, 422, 428, 494, 495, 503, 504, 519, 520, 525, 527, 531, 532, 540, 541, 545, 547, 552, 553, 556, 557, 561, 562, 564, 565, 566, 580, 581, 582, 584, 585, 589, 590, 598, 600, 602, 618, 620, 622, 636, 637, 638, 656, 657, 658, 710, 711, 712, 730, 731, 732, 746, 748, 750, 766, 768, 770, 778, 779, 783, 784, 786, 787, 788, 802, 803, 804, 806, 807, 811, 812, 815, 816, 821, 823, 827, 828, 836, 837, 841, 843, 848, 849, 864, 865, 873, 874, 940, 946, 977, 978, 982, 983, 1013, 1014, 1016, 1018, 1020, 1021, 1052, 1053, 1055, 1056, 1087, 1088, 1090, 1092, 1094, 1095, 1125, 1126, 1130, 1131, 1272, 1273, 1279, 1280, 1309, 1310, 1316, 1317], 37, 37, 10, 1)

# # 周期为15
# start_life_list, n, m, t, sign = ([95, 97, 105, 107, 121, 122, 123, 125, 126, 134, 135, 137, 138, 139, 149, 151, 152, 154, 164, 166, 167, 169, 178, 179, 197, 198, 207, 208, 226, 227, 235, 244, 245, 247, 248, 257, 265, 266, 274, 276, 284, 285, 293, 294, 301, 303, 305, 307, 314, 315, 329, 331, 335, 337, 356, 359, 365, 368, 385, 386, 387, 395, 396, 397, 443, 444, 445, 453, 454, 455, 472, 475, 481, 484, 503, 505, 509, 511, 525, 526, 533, 535, 537, 539, 546, 547, 555, 556, 564, 566, 574, 575, 583, 592, 593, 595, 596, 605, 613, 614, 632, 633, 642, 643, 661, 662, 671, 673, 674, 676, 686, 688, 689, 691, 701, 702, 703, 705, 706, 714, 715, 717, 718, 719, 733, 735, 743, 745], 29, 29, 15, 1)

# # 周期为37
# start_life_list, n, m, t, sign = ([68, 117, 118, 119, 169, 217, 218, 267, 268, 269, 270, 271, 317, 318, 319, 320, 321, 327, 328, 365, 370, 376, 377, 509, 517, 519, 557, 558, 564, 565, 566, 567, 568, 604, 612, 615, 617, 618, 619, 653, 655, 661, 662, 663, 667, 669, 692, 693, 711, 712, 713, 719, 741, 742, 749, 762, 764, 767, 797, 799, 803, 804, 810, 811, 813, 815, 819, 820, 845, 849, 852, 853, 855, 856, 860, 861, 894, 895, 901, 902, 917, 919, 941, 942, 943, 946, 947, 954, 955, 961, 962, 963, 968, 969, 977, 978, 991, 997, 1003, 1005, 1010, 1011, 1012, 1026, 1035, 1036, 1039, 1040, 1041, 1043, 1044, 1045, 1046, 1073, 1075, 1083, 1084, 1089, 1091, 1092, 1094, 1101, 1103, 1109, 1119, 1121, 1122, 1123, 1132, 1133, 1138, 1140, 1141, 1147, 1149, 1150, 1152, 1153, 1155, 1156, 1158, 1169, 1170, 1181, 1182, 1188, 1189, 1195, 1205, 1211, 1212, 1218, 1219, 1230, 1231, 1242, 1244, 1245, 1247, 1248, 1250, 1251, 1253, 1259, 1260, 1262, 1267, 1268, 1277, 1278, 1279, 1281, 1291, 1297, 1299, 1306, 1308, 1309, 1311, 1316, 1317, 1325, 1327, 1354, 1355, 1356, 1357, 1359, 1360, 1361, 1364, 1365, 1374, 1388, 1389, 1390, 1395, 1397, 1403, 1409, 1422, 1423, 1431, 1432, 1437, 1438, 1439, 1445, 1446, 1453, 1454, 1457, 1458, 1459, 1481, 1483, 1498, 1499, 1505, 1506, 1539, 1540, 1544, 1545, 1547, 1548, 1551, 1555, 1580, 1581, 1585, 1587, 1589, 1590, 1596, 1597, 1601, 1603, 1633, 1636, 1638, 1651, 1658, 1659, 1681, 1687, 1688, 1689, 1707, 1708, 1731, 1733, 1737, 1738, 1739, 1745, 1747, 1781, 1782, 1783, 1785, 1788, 1796, 1832, 1833, 1834, 1835, 1836, 1842, 1843, 1881, 1883, 1891, 2023, 2024, 2030, 2035, 2072, 2073, 2079, 2080, 2081, 2082, 2083, 2129, 2130, 2131, 2132, 2133, 2182, 2183, 2231, 2281, 2282, 2283, 2332], 49, 49, 37, 1)


# 初始对角线活细胞
n, m = 43, 43
start_life_list, n, m, t, sign = ([i * n + j for i, j in zip(range(n), range(m))] +
                            [i * m + j for i, j in zip(range(n-1, -1, -1), range(m))], n, m, 75, 0)


lg = LifeGame(n, m, start_life_list)


def plot_life_game(data, figname, t, sign):
    m, n = data.shape
    # 绘图
    fig, ax = plt.subplots()
    # 设置主刻度
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    # 设置网格线
    ax.xaxis.grid(True, which='major', linestyle="-", linewidth=1.1, c='#ccccd6')
    ax.yaxis.grid(True, which='major', linestyle="-", linewidth=1.1, c='#ccccd6')
    # 设置刻度，保证对齐
    ax.set_xticks(list(np.linspace(-0.5, lg.m - 1.5, lg.m)))
    ax.set_yticks(list(np.linspace(-0.5, lg.n - 1.5, lg.n)))
    # 设置热力图数值对应的颜色
    my_colormap = LinearSegmentedColormap.from_list("颜色匹配", [lg.life_c, lg.dead_c] if
    lg.life_n < lg.dead_n else[lg.dead_c, lg.life_c])
    # 热力图
    ax.imshow(data, cmap=my_colormap)
    # 不显示刻度标签
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    # 设置主刻度线
    tick_params(which='major', length=0)
    # 图形四个边的颜色和粗度
    for a in ['bottom', 'top', 'left', 'right']:
        ax.spines[a].set_linewidth(1.1)
        ax.spines[a].set_color('#ccccd6')

    alignment = {'horizontalalignment': 'center', 'verticalalignment': 'baseline'}
    if sign:
        plt.title('周期为%d' % t)
    else:
        plt.title('%d*%d的网格：%d步趋于稳定, 当前%d步' % (m, n, t, figname+1))

    print('图片保存完成', figname)
    plt.savefig('%s.jpg' % figname, bbox_inches='tight')
    plt.close()


# 制作震荡态gif的代码
namelist = []
for i in range(t):
    plot_life_game(lg.initial_matrix, i, t, sign)
    lg.create_by_rule()
    namelist.append('%d.jpg' % i)


#  合成一个gif图片
def create_gif(image_list, gif_name=r'C:\Users\GWT9\Desktop\anfany.gif'):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=0.9)  # duration控制动态图中每张图片的显示时间


create_gif(namelist)





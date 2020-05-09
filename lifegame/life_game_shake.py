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


# 震荡态
start_life_list, n, m = (
    [66, 67, 98, 100, 132, 133, 134, 162, 164, 194, 195, 103, 135, 167, 75, 76, 106, 108, 138, 170, 172, 203, 204, 322,
     323, 324, 297, 298, 330, 359, 391, 392, 82, 83, 84, 88, 89, 90, 144, 176, 208, 149, 181, 213, 151, 183, 215, 156,
     188, 220, 242, 243, 244, 248, 249, 250, 306, 307, 308, 312, 313, 314, 341, 373, 405, 343, 375, 407, 348, 380, 412,
     466, 467, 468, 472, 473, 474, 336, 368, 400],
    18, 32)

lg = LifeGame(n, m, start_life_list)


def plot_life_game(data, figname):
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
    plt.figtext(0.21, 0.36, '信号灯', weight='bold', color='#3f48cc', size='large', **alignment)
    plt.figtext(0.305, 0.71, '活塞', weight='bold', color='#3f48cc', size='large', **alignment)
    plt.figtext(0.345, 0.3, '灯塔', weight='bold', color='#3f48cc', size='large', **alignment)
    plt.figtext(0.67, 0.25, '脉冲星', weight='bold', color='#3f48cc', size='large', **alignment)
    print('图片保存完成')
    plt.savefig('%s.jpg' % figname, bbox_inches='tight')
    plt.close()


# 制作震荡态gif的代码
for i in range(6):
    plot_life_game(lg.initial_matrix, str(i))
    lg.create_by_rule()


namelist = ['%s.jpg' % dd for dd in range(6)]


#  合成一个gif图片
def create_gif(image_list, gif_name=r'C:\Users\GWT9\Desktop\anfany.gif'):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=0.9)  # duration控制动态图中每张图片的显示时间


create_gif(namelist)


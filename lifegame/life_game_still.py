# -*- coding：utf-8 -*-
# &Author  AnFany
# WeChat: PythonFan

import matplotlib.animation as animation
from pylab import *
from matplotlib.colors import LinearSegmentedColormap


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


# 静止态
start_life_list, n, m = (
[30, 31, 35, 36, 41, 42, 47, 48, 52, 53, 58, 59, 62, 65, 68, 71, 74, 79, 82, 91, 93, 97, 98, 102, 103, 107, 109, 110,
 120, 134, 135, 137, 142, 143, 162, 165, 169, 172, 181, 182, 191, 192, 197, 200, 203, 204, 206, 209, 212, 226, 227, 231,
 233, 234, 239, 240, 273, 274, 302, 310, 311, 316, 317, 321, 329, 337, 340, 344, 346, 348, 350, 356, 366, 369, 373, 377,
 381, 383, 395, 396, 409, 410], 16, 28)

lg = LifeGame(n, m, start_life_list)



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
im = ax.imshow(lg.initial_matrix, cmap=my_colormap)
# 不显示刻度标签
plt.setp(ax.get_xticklabels(), visible=False)
plt.setp(ax.get_yticklabels(), visible=False)
# 设置主刻度线
tick_params(which='major', length=0)
# 图形四个边的颜色和粗度
for a in ['bottom', 'top', 'left', 'right']:
    ax.spines[a].set_linewidth(1.1)
    ax.spines[a].set_color('#ccccd6')


#
# 动画函数
def animate(frames):
    im.set_data(lg.create_by_rule())
    return im,


# 合成动画
anim = animation.FuncAnimation(fig, animate, frames=4, interval=10)

# 动画保存
anim.save(r'C:\Users\GWT9\Desktop\test_an.gif', writer='pillow')
print('动画保存完毕')
# 动画显示
plt.show()

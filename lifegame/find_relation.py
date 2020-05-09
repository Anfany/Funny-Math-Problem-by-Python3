# -*- coding：utf-8 -*-
# &Author  AnFany
# WeChat: PythonFan

import numpy as np
import pandas as pd

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


# 初始的局面为对角线活细胞，不同的正边形网格数和趋于稳定的步数的对应关系
# 最终趋于稳定的
still_grid = []
still_steps = []
# 经过一定步数变为周期的
period_grid = []
period_steps = []
period_counts = []

for k in range(3, 101):
    start_life_list = [i * k + j for i, j in zip(range(k), range(k))] + \
                      [i * k + j for i, j in zip(range(k - 1, -1, -1), range(k))]

    lg = LifeGame(k, k, start_life_list)
    sign_s = 0
    sign_p = 0
    gu = []
    num = '1'
    while 1:
        first_matrix = list(lg.initial_matrix.copy().flatten())
        gu.append(first_matrix)

        lg.create_by_rule()
        sign_s += 1

        two_matrix = list(lg.initial_matrix.copy().flatten())

        if two_matrix in gu:
            if two_matrix == first_matrix:
                break
            else:
                sign_p = 1
                num = gu.index(two_matrix)
                break

    if not sign_p:
        print('网格为%d, 趋于稳定，%s' % (k, sign_s))
    else:
        print('网格为%d, 经过%s步变为，周期性，%s' % (k, num, sign_s - num))

    # 将结果存储
    if sign_p:
        # 经过一定步数变为周期的
        period_grid.append(k)
        period_steps.append(num)
        period_counts.append(sign_s - num)
    else:
        still_grid.append(k)
        still_steps.append(sign_s)

# 将结果写入excel表格中

still_data = pd.DataFrame({'网格数m，n': still_grid, '趋于稳定的步数': still_steps},
                          columns=['网格数m，n', '趋于稳定的步数'])
period_data = pd.DataFrame({'网格数m，n': period_grid, '变为周期性的步数': period_steps,
                            '周期': period_counts}, columns=['网格数m，n', '变为周期性的步数', '周期'])


still_data.to_excel('data.xlsx', sheet_name='still', index=False)
period_data.to_excel('data1.xlsx', sheet_name='period', index=False)

print('完成')
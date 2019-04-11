# -*- coding：utf-8 -*-
# &Author  AnFany

#  利用遗传算法获得34个省会直辖市一次遍历的最短路径(不一定是最短距离，但很大可能是最短距离)

import read_distance as r_d  # 获取地址之间的距离，以及关系
import show_result as s_r  # 展示结果
import numpy as np
import itertools

# 引入绘图库包
import matplotlib.pyplot as plt
import imageio  # 引入合成gif的库
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 中文字体名称
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号

# 存储图片的文件夹
Save_file = r'C:\Users\GWT9\Desktop\tsp'


class GA():
    def __init__(self, d_dict=r_d.read_distance(), s_dict=r_d.read_sign()):

        # 初始种群内的个体数
        self.individual_count = 8  # 需要大于自身优化变异长度

        # 迭代次数
        self.iter_times = 30

        # 交叉概率
        self.crossover_rate = 0.32

        # 变异概率
        self.mutation_rate = 0.22

        # 自身优化变异长度
        self.mutation_length = 5  # 最大为5，最小为2，过大会导致运行过慢

        self.d_dict = d_dict  # 地址之间的距离字典
        self.s_dict = s_dict  # 地址对应的编号

        self.population = self.init_population()  # 初始的种群

    # 初始化种群的函数
    def init_population(self):
        population = []
        individual = np.arange(len(self.s_dict))
        for i in range(self.individual_count):
            np.random.shuffle(individual)
            # 变为列表形式
            in_list = list(individual)
            population.append(in_list)
        return population

    # 计算单条路径的总长度
    def fitness_path_distance(self, path):
        """
        计算当个个体的路径的总长度
        :param path: 一条路径
        :return: 适应度，也就是总长度
        """
        copy_path = path.copy()
        copy_path.append(copy_path[0])
        sum_distance = 0
        for p in range(len(copy_path) - 1):
            small, big = sorted([copy_path[p], copy_path[p + 1]])
            sum_distance += self.d_dict[(small, big)]
        return sum_distance

    # 适应度函数，也就是计算每条路径的总长度
    def fitness_population_distance(self):
        """
        计算种群中每个个体的适应度，也就是计算每条路径的总长度
        :return: 适应度，也就是该路径的总长度
        """
        all_fitness = []
        for individual_path in self.population:
            all_fitness.append(self.fitness_path_distance(individual_path))
        return all_fitness

    #  选择方法：轮盘赌
    def select_roulette_wheel(self):
        all_fitness = self.fitness_population_distance()
        sum_f = sum(all_fitness)
        percent = [f / sum_f for f in all_fitness]
        # 计算累计概率
        accumulate_percent = [percent[0]]
        for p in percent[1:]:
            accumulate_percent.append(p + accumulate_percent[-1])
        # 给出多个随机数
        random_number = list(np.random.random(self.individual_count))
        accumulate_percent.insert(0, 0)
        select_population = []  # 选中的样本
        for p in random_number:
            for j in range(len(accumulate_percent) - 1):
                if accumulate_percent[j] <= p < accumulate_percent[j + 1]:
                    select_population.append(self.population[j])
                    break
        self.population = select_population  # 更新种群
        return print('选择完毕')

    def greedy_crossover(self, fa1, fa2):
        """
        实现贪婪交叉
        :param fa1: 父辈1
        :param fa2: 父辈2
        :return: 交叉后产生的新的个体
        """
        # 随机选择一个小数
        random_num = np.random.random(1)[0]
        if random_num > self.crossover_rate:
            # 开始交叉
            # 随机选择的交叉位置的地址
            cross_pos = np.random.randint(0, len(fa1), 1)[0]
            # 开始贪心算法，在fa1和fa2中选择比较好的下一个去处
            new_individual = [fa1[cross_pos]]  # 第一个地址
            while len(new_individual) < len(fa1):
                # 找到fa1中的下一个地址
                next_address_fa1 = fa1[(cross_pos + 1) % len(fa1)]
                # 找到fa2中的地址fa1[cross_pos]对应的下一个地址
                current_address_sign = fa2.index(new_individual[-1])
                next_address_fa2 = fa2[(current_address_sign + 1) % len(fa2)]
                # 比较距离
                if next_address_fa1 not in new_individual :
                    if next_address_fa2 not in new_individual:
                        # 此时按照贪心算法选择地址之间的距离小的，作为下一个要去的
                        a_fa1, b_fa1 = sorted([new_individual[-1], next_address_fa1])
                        a_fa2, b_fa2 = sorted([new_individual[-1], next_address_fa2])
                        if self.d_dict[(a_fa1, b_fa1)] <= self.d_dict[(a_fa2, b_fa2)]:
                            new_individual.append(next_address_fa1)
                            cross_pos = fa1.index(next_address_fa1)
                        else:
                            new_individual.append(next_address_fa2)
                            cross_pos = fa1.index(next_address_fa2)
                    else:
                        new_individual.append(next_address_fa1)
                        cross_pos = fa1.index(next_address_fa1)
                else:
                    if next_address_fa2 not in new_individual:
                        new_individual.append(next_address_fa2)
                        cross_pos = fa1.index(next_address_fa2)
                    else:
                        # 如果都在里面
                        no_fa1 = [n for n in fa1 if n not in new_individual]
                        if not no_fa1:
                            break
                        else:
                            # 在里面随机选择一个
                            select_pos = np.random.randint(0, len(no_fa1), 1)[0]
                            # 选中的地址
                            select_address = no_fa1[select_pos]
                            # 添加到新的个体基因里
                            new_individual.append(select_address)
                            cross_pos = fa1.index(select_address)
            return new_individual
        else:
            return False

    # 交叉方法：贪婪交叉，同时保证种群的多样性以及保证优秀的父辈进入下一代
    def crossover(self):
        new_individual = []
        different_fitness = []
        #  随着遗传的进行，很多个体都是相似的,因此不以个数判断，而是以不同适应度的个数判断
        while len(different_fitness) < self.individual_count:
            # 在种群中随机选择2个不同的个体作为父辈
            random_sign = []
            while len(set(random_sign)) < 2:
                random_sign = np.random.randint(0, self.individual_count, 2)

            father_1 = self.population[random_sign[0]]
            father_2 = self.population[random_sign[1]]
            # 添加新产生的个体
            new_son_fa1 = self.greedy_crossover(father_1, father_2)
            new_son_fa2 = self.greedy_crossover(father_2, father_1)
            if new_son_fa1:
                # 计算这个路径的适应度
                new_fa1_fitness = self.fitness_path_distance(new_son_fa1)
                if new_fa1_fitness not in different_fitness:
                    different_fitness.append(new_fa1_fitness)
                    new_individual += [new_son_fa1]
            if new_son_fa2:
                # 计算这个路径的适应度
                new_fa2_fitness = self.fitness_path_distance(new_son_fa2)
                if new_fa2_fitness not in different_fitness:
                    different_fitness.append(new_fa2_fitness)
                    new_individual += [new_son_fa2]
        # 新的种群中，保证不存在相同适应度的个体，并且利用精英策略。
        self.population += new_individual  # 种群中父辈和新产生的所有个体
        fitness = self.fitness_population_distance()  # 所有个体的适应度
        fitness_dict = {i: j for i, j in enumerate(fitness)}
        path_sort = sorted(fitness_dict.items(), key=lambda s: s[1])
        fitness_num = []
        new_population = []
        for n in path_sort:
            if n[1] not in fitness_num:
                fitness_num.append(n[1])
                new_population.append(self.population[n[0]])
            if len(new_population) == self.individual_count:
                break
        self.population = new_population
        return print('贪心交叉完毕')

    # 变异方法：自身优化变异。随机选择一个片段，优化这个基因片段
    def mutation_improve_self(self):
        for i, j in enumerate(self.population):
            random_num = np.random.random(1)[0]
            if random_num > self.mutation_rate:  # 开始进行自身变异
                # 随机选择优化的位置
                random_poss = np.random.randint(0, len(j), 1)[0]
                # 优化的片段
                improve_gene = [j[random_poss - 1]]
                for c in range(self.mutation_length + 1):
                    improve_gene.append(j[(random_poss + c) % len(j)])
                # 这个基因片段原有的适应度
                init_fitness = self.fitness_path_distance(improve_gene)
                # 开始打乱这段基因，两头的基因不参与优化
                for gene in itertools.permutations(improve_gene[1:-1]):
                    new_gene = [improve_gene[0]] + list(gene) + [improve_gene[-1]]
                    # 计算这个新产生的基因片段的适应度
                    new_fitness = self.fitness_path_distance(new_gene)
                    if new_fitness < init_fitness:
                        # 说明找到了优化的，将原来的基因片段变为新产生的基因片段
                        for d in range(self.mutation_length):
                            j[(random_poss + d) % len(j)] = gene[d]
                self.population[i] = j
        return print('自身优化变异完毕')

    # 将数字变为真实的地址，转变为展示用到的数据结构
    def trans_path(self):
        """
        将种群中总距离最小个体，也就是数字表示的路径，变为真实的地址表示的路径
        :return: 真实地址表示的路径
        """
        all_fitness = self.fitness_population_distance()
        small_index = all_fitness.index(min(all_fitness))
        small_path = self.population[small_index].copy()
        small_path.append(small_path[0])
        real_address = []
        for j in range(len(small_path) - 1):
            real_address.append([self.s_dict[small_path[j]], self.s_dict[small_path[j + 1]]])
        return real_address, min(all_fitness)

    # 进行迭代的函数,
    def g_a(self):
        times = 0
        # 每一代的最优路径的总长度
        best_length = []
        # 存储制作动画需要的图片名称
        fig_name = []
        sorted_fitness = []
        all_fitness = sorted(self.fitness_population_distance())  # 初始种群
        best_length.append(all_fitness[0])  # 添加初始种群的
        # 开始遗传进化
        while times < self.iter_times:
            self.select_roulette_wheel()  # 选择
            self.crossover()  # 交叉
            self.mutation_improve_self()  # 变异

            all_fitness = sorted(self.fitness_population_distance())  # 计算适应度，也就是距离
            best_length.append(all_fitness[0])

            # 为了动画表明，路线是怎么变化的，只存储总距离从大到小的。动画展示，是没有初始种群的
            if not fig_name:
                fig_name.append('%s.png' % times)
                sorted_fitness.append(all_fitness[0])
            else:
                if all_fitness[0] < sorted_fitness[-1]:
                    fig_name.append('%s.png' % times)
                    sorted_fitness.append(all_fitness[0])

            # 存储结果
            path_real, title = self.trans_path()
            s_r.create_charts(path_real, r'%s\%s.html' % (Save_file, times),
                              r'%s\%s.png' % (Save_file, times), title)
            times += 1

        # 绘制每一代最优路径的曲线
        min_times = best_length.index(sorted_fitness[-1])
        plt.scatter([min_times], [sorted_fitness[-1]], marker='*', color='green', s=18,
                    label='最优：$%d$代，$%.3fkm$' % (min_times, sorted_fitness[-1] / 1000))
        plt.plot(list(range(len(best_length))), best_length, '-', lw=2, c='r')
        plt.title('每一次迭代最优路径的总长度曲线 \n 种群内个体数：$%d$' % self.individual_count)
        plt.legend(loc='best')
        plt.ylabel('长度($Km$)')
        plt.xlabel('代数')
        plt.xticks([0, min_times, self.iter_times], ['初始', '最优', '结束'])
        plt.savefig(r'%s\iter_path.png' % Save_file)
        return fig_name

    #  输出路线变化的动画，也就是将图片变为gif形式
    def create_gif(self, image_list, gif_name='tsp.gif'):
        frames = []
        image_list += [image_list[-1]] * 10  # 最后一张图片停留的时间稍长
        for image_name in image_list:
            frames.append(imageio.imread(r'%s/%s' % (Save_file, image_name)))
        imageio.mimsave(r'%s\%s' %(Save_file, gif_name), frames, 'GIF', duration=0.9)  # duration控制动态图中每张图片的显示时间
        return print('动画生成完毕')


# 最终的主函数
if __name__ == '__main__':
    # 遗传算法的类
    ga = GA()
    # 迭代
    fig_list = ga.g_a()
    # 绘制动画
    ga.create_gif(fig_list)


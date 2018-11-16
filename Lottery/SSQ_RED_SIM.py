#-*- coding：utf-8 -*-
# &Author  AnFany

import numpy as np
from scipy.special import comb
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号
import matplotlib.pyplot as plt
# 引入模型
import SSQ_RED as yanzheng
import pandas as pd

# 为了说明本文方法的概率和随机的概率分布是相同的
# 现在需要生成和随机选择的可能性同等数量的数据
# 并且以2000条数据作为基准数据

# 定义生成数据
def Generate(redfanwei, gehsu, jichu=2000):
    # 需要数据的个数
    shujugeshu = int(comb(redfanwei, gehsu))
    # 存储数据
    dafr = {}
    dafr['红球'] = []
    dafr['序号'] = []
    for i in list(range(shujugeshu + jichu))[::-1]:
        rdata = np.random.choice(list(range(1, redfanwei + 1)), gehsu, replace=False)
        dafr['红球'].append(rdata)
        dafr['序号'].append(i)

    dafr['期号'] = dafr['序号'].copy()

    daf = pd.DataFrame(dafr)
    return daf


# 主函数
if __name__ == "__main__":
    print('SSQ：生成模拟数据')
    ff = Generate(33, 6)
    print('SSQ：计算概率阶段')
    # 模型
    mm = yanzheng.MODEL(ff, list(range(1, 34)), 6)

    fu = mm.HuoDe(2000)

    maxcount = 9

    gail = mm.MingZhong(fu, maxcount)
    print('SSQ：绘图阶段')

    # 以1-9个球的结果为例
    for ss in range(1, maxcount + 1):
        # 转移
        yizhuan = gail[ss][: ss + 1]
        # 随机理论
        jisui = mm.Random_Method(ss)

        plt.figure()

        row_labels = ['本文方法', '理论概率']
        col_labels = ['%d球' % f for f in list(range(min(ss + 1, mm.redcount + 1)))]
        table_vals = [['%.5f' % f for f in yizhuan], ['%.5f' % f for f in jisui]]
        row_colors = ['teal', 'plum']
        my_table = plt.table(cellText=table_vals,
                             cellColours=[['teal'] * len(col_labels), ['plum'] * len(col_labels)], \
                             rowLoc='center', colLoc='center',
                             rowLabels=row_labels, colLabels=col_labels, rowColours=row_colors,
                             loc='bottom')

        plt.plot(list(range(len(yizhuan))), yizhuan, '--', marker='o', lw=2.5, c='teal')

        plt.plot(list(range(len(jisui))), jisui, '-.', marker='p', lw=2.5, c='plum')
        plt.legend(['本文方法(统计：%s条)' % int(comb(len(mm.red), mm.redcount)), '理论概率'])
        plt.title('SSQ：选择%s个球的命中情况概率对比' % ss)
        plt.xlim(- 0.5, len(col_labels) - 0.5)
        plt.xticks([])
        plt.grid()
        plt.savefig(r'C:\Users\GWT9\Desktop\%s_ssq_test.jpg' % ss)

    print('SSQ：程序完毕')





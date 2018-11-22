#-*- coding：utf-8 -*-
# &Author  AnFany

# 真实数据的结果
import MODEL as moxing
import SSQ_DATA as data_ssq # 双色球数据
import DLT_DATA as data_dlt # 大乐透数据
#  绘制概率对比

from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号
import matplotlib.pyplot as plt

# 主函数, 输出概率和随机选择概率的对比

if __name__ == "__main__":
    print('计算阶段')
    # 验证红球
    model = moxing.MODEL(data_ssq.ssq_data.oodata, data_ssq.ssq_data.red, data_ssq.ssq_data.rc, '红球', 1, 1239)
    # # 验证蓝球
    # model = moxing.MODEL(data_ssq.ssq_data.oodata, data_ssq.ssq_data.blue, data_ssq.ssq_data.bc, '蓝球', 9, 1500)

    # 验证前区
    # model = moxing.MODEL(data_dlt.dlt_data.oodata, data_dlt.dlt_data.qian, data_dlt.dlt_data.qc, '前区', 1, 1000)
    # # 验证后区
    # model = moxing.MODEL(data_dlt.dlt_data.oodata, data_dlt.dlt_data.hou, data_dlt.dlt_data.hc, '后区', 1, 1000)

    fu = model.HuoDe()
    # 选择选取不同球数的结果对比,
    maxcount = 8
    # 概率
    gail = model.MingZhong(fu, maxcount)

    if '期' in gail:  # 预测情况
        print(gail)
    else:
        # 以1-7个球的结果为例
        for ss in range(1, maxcount + 1):
            # 转移
            yizhuan = gail[ss][: ss + 1]
            # 随机理论
            jisui = model.Random_Method(ss)

            plt.figure()

            row_labels = ['本文方法', '理论概率']
            col_labels = ['%d球' % f for f in list(range(min(ss + 1, model.houxuangehsu + 1)))]
            table_vals = [['%.5f' % f for f in yizhuan], ['%.5f' % f for f in jisui]]
            row_colors = ['teal', 'plum']
            my_table = plt.table(cellText=table_vals,
                                 cellColours=[['teal'] * len(col_labels), ['plum'] * len(col_labels)], \
                                 rowLoc='center', colLoc='center',
                                 rowLabels=row_labels, colLabels=col_labels, rowColours=row_colors,
                                 loc='bottom')

            plt.plot(list(range(len(yizhuan))), yizhuan, '--', marker='o', lw=2.5, c='teal')

            plt.plot(list(range(len(jisui))), jisui, '-.', marker='p', lw=2.5, c='plum')
            plt.legend(['本文方法(真实数据：统计%d条)' % (max(list(model.data['序号'].values)) - model.qishu + 1), '理论概率'])
            plt.title('%s:选择%s个球的命中情况概率对比' % (model.name, ss))
            plt.xlim(- 0.5, len(col_labels) - 0.5)
            plt.xticks([])
            plt.grid()
            plt.savefig(r'C:\Users\GWT9\Desktop\%s_%s.jpg' % (ss, model.name))
            plt.show()

        print('计算完毕')





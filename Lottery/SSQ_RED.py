#-*- coding：utf-8 -*-
# &Author  AnFany

# 模型：根据历史数据得到前后同样位置号码之间的转移概率
#      选择当期号码对应的概率最大的前几个号码，作为预测号码
#      当前以及之前的所有数据作为历史数据。
from scipy.special import comb
import SSQ_DATA as data  # 引入数据
# 模型的类
class MODEL():
    def __init__(self, data, red, rc, name='红球'):
        '''
        data:dataframe格式， red：号码序列， re：号码个数
        '''

        self.data = data
        self.red = red
        self.redcount = rc

        # 要研究的字段名称
        self.name = name

        # 存储转移次数的字典

        self.transdict = self.InitGai()

        # 存储出现次数的字典
        self.chuxiandict = {h: 0 for h in self.red}

        # 存储转移概率的字典
        self.zhuanyidict = self.gailv()

    # 计算转移概率的字典
    def gailv(self):
        exdict = {}
        for jj in self.transdict:
            exdict[jj] = {}
            for hh in self.transdict[jj]:
                if self.chuxiandict[jj] != 0:
                    exdict[jj][hh] = self.transdict[jj][hh] / self.chuxiandict[jj]
                else:
                    exdict[jj][hh] = 0
        return exdict

    # 定义概率字典格式的函数
    def InitGai(self):
        ecdict = {}
        for jj in self.red:
            ecdict[jj] = {}
            for hh in self.red:
                ecdict[jj][hh] = 0
        return ecdict

    # 根据转移概率字典，返回当期号码下按照概率从大到小的号码序列
    def GetOrder(self, exlist):
        exdict = {i: 0 for i in self.red}
        for jj in exlist:
            for hh in self.zhuanyidict[jj]:
                exdict[hh] += self.zhuanyidict[jj][hh]
        # 按照从大到小输出键
        orderdict = sorted(exdict.items(), key=lambda du: du[1], reverse=True)

        # 号码序列
        haoma = [j[0] for j in orderdict]

        return haoma

    # 定义计算出现次数的函数字典
    def TongJICiShu(self, balldata):  # 输入号码序列
        for jj in balldata:
            for kk in jj:
                self.chuxiandict[kk] += 1
        return self.chuxiandict

    #  统计前后对应次数的关系
    def GuanLian(self, balldata, jiande=1):  # 输入号码序列
        qiandata = balldata[: -jiande]
        houdata = balldata[jiande:]
        for qq, hh in zip(qiandata, houdata):
            for j, k in zip(qq, hh):
                self.transdict[j][k] += 1
        return self.transdict


    # 根据序号确定从何时开始作为历史数据，以及预测用到的数据序列
    def Hietory(self, sign):  #sign不小于1
        if sign >= max(list(self.data['序号'].values)):
            yucedata = self.data[self.data['序号'] == max(list(self.data['序号'].values))]
            return self.data, yucedata
        else:
            newdata = self.data[self.data['序号'] <= sign]
            yucedata = self.data[self.data['序号'] >= sign]  # 因为当期也算做历史数据
            return newdata, yucedata


    # 开始进行获取转移次数、出现次数
    def HuoDe(self, sign):
        # 历史数据、预测数据
        history_data, yuce_data = self.Hietory(sign)
        # 出现字典
        self.chuxiandict = self.TongJICiShu(history_data[self.name].values)
        # 转移字典
        self.transdict = self.GuanLian(history_data[self.name].values)
        # 概率字典
        self.zhuanyidict = self.gailv()


        # 返回编号为键，原始序列和号码序列为值的字典
        xuhaodict = {}

        # 判断是否为预测
        exlist = yuce_data[self.name].values

        bianhaolist = yuce_data['期号'].values

        if len(exlist) == 1:
            #  则返回预测序列
            yucede = self.GetOrder(exlist[0])
            bianhao = bianhaolist[0]
            xuhaodict[bianhao + 1] = ['%s期还没出现' % (bianhao + 1), yucede]
            return xuhaodict

        else:
            for qian, hou, bian in zip(exlist[: -1], exlist[1:], bianhaolist[1:]):
                # 出现字典
                self.chuxiandict = self.TongJICiShu([qian])
                # 转移字典
                self.transdict = self.GuanLian([hou, qian]).copy()
                # 概率字典
                self.zhuanyidict = self.gailv()

                # 预测的
                yucede = self.GetOrder(hou)

                xuhaodict[bian] = [hou, yucede]

            return xuhaodict

    # 定义结果比对的函数
    def Resu_Bdui(self, exlist, count):
        # 判断是否为预测
        if '期' in exlist[0]:
            return '%s期预测结果(前%d位)：%s' % (exlist[0][:7], count, exlist[1][: count])
        else:
            hu = {}
            for jj in range(1, count + 1):
                hu[jj] = {}
                jiaoji = len(list(set(exlist[0]).intersection(set(exlist[1][: jj]))))
                hu[jj][jiaoji] = 1
            return hu

    # 根据字典统计命中球数的概率
    def MingZhong(self, exdict, count):
        # 为每一种结果都获得命中球数的概率
        qiu = {mm: {fu: 0 for fu in range(0, self.redcount + 1)} for mm in range(1, count + 1)}
        # 开始计算
        for hh in exdict:
            ddcit = self.Resu_Bdui(exdict[hh], count)
            if "期" not in ddcit:
                for ghu in ddcit:
                    qiu[ghu][list(ddcit[ghu].keys())[0]] += 1
            else:
                return ddcit
        # 返回概率
        gaidct = {}
        for gg in qiu:
            sunhe = sum(list(qiu[gg].values()))
            gaidct[gg] = {ji: qiu[gg][ji] / sunhe for ji in qiu[gg]}

        # 每种情况按着命中球的个数形成列表
        lidi = {}
        for ut in gaidct:
            lidi[ut] = []
            for jie in range(self.redcount + 1):
                lidi[ut].append(gaidct[ut][jie])
        return lidi

    # 随机选择的理论概率
    def Random_Method(self, n):
        redict = {}
        fu = 0
        for i in range(self.redcount + 1):
            if n >= i:
                tu = comb((len(self.red) - n), (n - i)) * comb(n, i) / comb(len(self.red), n)
                fu += tu
                redict[i] = tu
        # 按命中球的个数返回值
        redu = []
        for j in range(self.redcount + 1):
            if j <= n:
                if j not in redict:
                    redu.append(0)
                else:
                    redu.append(redict[j])
        return redu


#  绘制概率对比

from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号
import matplotlib.pyplot as plt

# 主函数, 输出概率和随机选择概率的对比

if __name__ == "__main__":
    model = MODEL(data.zddd, data.rr, data.rc)


    # 开始统计的条数
    start_tongji = 1339 # 这个值超过所有数据的条数，则为预测下一期的结果
    fu = model.HuoDe(start_tongji)
    # 选择1-9球的结果对比,如果是预测则输出maxcount个候选号码。
    maxcount = 9
    # 概率
    gail = model.MingZhong(fu, maxcount)

    if '期' in gail:  # 预测情况
        print(gail)
    else:
        # 以1-9个球的结果为例
        for ss in range(1, maxcount + 1):
            # 转移
            yizhuan = gail[ss][: ss + 1]
            # 随机理论
            jisui = model.Random_Method(ss)

            plt.figure()

            row_labels = ['本文方法', '理论概率']
            col_labels = ['%d球' % f for f in list(range(min(ss + 1, model.redcount + 1)))]
            table_vals = [['%.5f' % f for f in yizhuan], ['%.5f' % f for f in jisui]]
            row_colors = ['teal', 'plum']
            my_table = plt.table(cellText=table_vals,
                                 cellColours=[['teal'] * len(col_labels), ['plum'] * len(col_labels)], \
                                 rowLoc='center', colLoc='center',
                                 rowLabels=row_labels, colLabels=col_labels, rowColours=row_colors,
                                 loc='bottom')

            plt.plot(list(range(len(yizhuan))), yizhuan, '--', marker='o', lw=2.5, c='teal')

            plt.plot(list(range(len(jisui))), jisui, '-.', marker='p', lw=2.5, c='plum')
            plt.legend(['本文方法(真实数据：统计%d条)' % (max(list(model.data['序号'].values)) - start_tongji + 1), '理论概率'])
            plt.title('SSQ:选择%s个球的命中情况概率对比' % ss)
            plt.xlim(- 0.5, len(col_labels) - 0.5)
            plt.xticks([])
            plt.grid()
            plt.savefig(r'C:\Users\GWT9\Desktop\%s_ssq.jpg' % ss)

        print('运行完毕')




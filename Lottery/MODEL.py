#-*- coding：utf-8 -*-
# &Author  AnFany

# 模型：根据历史数据得到前后同样位置号码之间的转移概率
#      选择最近几期出现的号码对应的概率最大的前几个号码，作为预测号码
#      当前以及之前的所有数据作为计算转移概率的历史数据。
from scipy.special import comb

# 模型的类
class MODEL():
    def __init__(self, data, houxuan, houxuangeshu, name, qishu, sign):
        '''
        data:dataframe格式
        houxuan：号码序列
        houxuangeshu：号码个数
        name：要研究的字段
        qishu：计算前几期号码对应的最大转移概率
        sign：从sign期到最后一期数据作为统计数据,超过最大期数，则为预测
        '''

        self.data = data
        self.houxuan = houxuan
        self.houxuangehsu = houxuangeshu

        # 计算前几期号码对应的最大转移概率
        self.qishu = qishu

        # 从sign期到最后一期数据作为统计数据, 超过最大期数，则为预测
        self.sign = sign


        # 要研究的字段名称
        self.name = name

        # 存储转移次数的字典
        self.transdict = self.InitGai()

        # 存储出现次数的字典
        self.chuxiandict = {h: 0 for h in self.houxuan}

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
        for jj in self.houxuan:
            ecdict[jj] = {}
            for hh in self.houxuan:
                ecdict[jj][hh] = 0
        return ecdict

    # 自定义可以回溯的期数，不止是前一期,将前几期号码合并的函数
    def Hebing(self, exdalsit):
        gu = []
        for j in exdalsit:
            gu += j
        return list(set(gu))

    # 根据转移概率字典，返回前几期号码对应的号码按照概率从大到小的号码序列
    def GetOrder(self, elist):
        exlist = self.Hebing(elist)
        exdict = {i: 0 for i in self.houxuan}
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


    # 根据序号确定从何时开始作为统计数据，要预测的数据序列，以及预测要用到的数据系列
    def Hietory(self):  #sign不小于1
        if self.sign >= max(list(self.data['序号'].values)):
            yucedata = self.data[self.data['序号'] == max(list(self.data['序号'].values))]
            yongdao_yucedata = self.data[self.data['序号'] > max(list(self.data['序号'].values)) - self.qishu]
            return self.data, yucedata, yongdao_yucedata
        else:
            newdata = self.data[self.data['序号'] <= self.sign]  # 因为当期也算做历史数据
            yucedata = self.data[self.data['序号'] >= self.sign]
            yongdao_yucedata = self.data[self.data['序号'] > self.sign - self.qishu]
            return newdata, yucedata, yongdao_yucedata


    # 开始进行获取转移次数、出现次数
    def HuoDe(self):
        # 历史数据、预测数据
        history_data, yuce_data, yongdao_yuce_data = self.Hietory()
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

        yongdao_yu = yongdao_yuce_data[self.name].values

        if len(exlist) == 1:
            #  则返回预测序列
            yucede = self.GetOrder(yongdao_yu)
            bianhao = bianhaolist[0]
            xuhaodict[bianhao + 1] = ['%s期还没出现' % (bianhao + 1), yucede]
            return xuhaodict

        else:
            # 预测用到的数据系列的选取
            biaoshi = 0
            for qian, hou, bian in zip(exlist[: -1], exlist[1:], bianhaolist[1:]):
                # 出现字典
                self.chuxiandict = self.TongJICiShu([qian])
                # 转移字典
                self.transdict = self.GuanLian([hou, qian]).copy()
                # 概率字典
                self.zhuanyidict = self.gailv()

                # 预测的
                yucede = self.GetOrder(yongdao_yu[biaoshi: biaoshi + self.qishu])

                xuhaodict[bian] = [hou, yucede]

                biaoshi += 1

            return xuhaodict

    # 定义结果比对的函数
    def Resu_Bdui(self, exlist, count):
        # 判断是否为预测
        if '期' in exlist[0]:
            return '双色球%s期号码(%s)优选方案：%s' % (exlist[0][:7], self.name, exlist[1][: count])
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
        qiu = {mm: {fu: 0 for fu in range(0, self.houxuangehsu + 1)} for mm in range(1, count + 1)}
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
            for jie in range(self.houxuangehsu + 1):
                lidi[ut].append(gaidct[ut][jie])
        return lidi

    # 随机选择的理论概率
    def Random_Method(self, n):
        redict = {}
        fu = 0
        for i in range(self.houxuangehsu + 1):
            if n >= i:
                tu = comb((len(self.houxuan) - self.houxuangehsu),
                          (n - i)) * comb(self.houxuangehsu, i) / comb(len(self.houxuan), n)
                fu += tu
                redict[i] = tu
        # 按命中球的个数返回值
        redu = []
        for j in range(self.houxuangehsu + 1):
            if j <= n:
                if j not in redict:
                    redu.append(0)
                else:
                    redu.append(redict[j])
        return redu
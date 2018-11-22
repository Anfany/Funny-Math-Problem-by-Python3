# -*- coding：utf-8 -*-
# &Author  AnFany

# 首先更新数据
import DLT_SPYDER as dltdata

# 对存储在文件中的SSQ数据进行处理
import pandas as pd

# 定义处理数据的类
class CP:
    def __init__(self):
        # 基础信息设定
        self.qian = list(range(1, 36))
        self.qc = 5
        self.hou = list(range(1, 13))
        self.hc = 2

        # 数据文件路径
        self.filepath = r'C:\Users\GWT9\Desktop'

        # 没有经过处理的数据
        self.dlt = self.ReadFile('dlt.csv', '前区', '后区')

        # 经过日期分解的数据
        self.dlt_dd = self.ChangeDate(self.dlt)

        # 添加顺序标识的数据
        self.oodata = self.AddOrder(self.dlt_dd)


    # 读取文件的函数
    def ReadFile(self, filename, c1, c2):
        data = pd.read_csv(r'%s\%s' % (self.filepath, filename))
        # 此外需要将存储号码的字符串形式转为列表形式
        data[c1] = [list(map(int, ii[1:-1].split(', '))) for ii in data[c1]]
        data[c2] = [list(map(int, ii[1:-1].split(', '))) for ii in data[c2]]
        return data

    # 将日期变为年份，月份, 日
    def ChangeDate(self, data):
        newdf = data['日期'].str.split('-', expand=True)
        # 更新名字
        newdf = newdf.rename(columns={0: '年份', 1: '月份', 2: '日'})
        # 和原来的合并
        data = data.join(newdf)
        return data

    # 按照日期的先后顺序，添加顺序标识.日期越近，序号越大
    def AddOrder(self, data):
        data.sort_values("日期", inplace=True)
        data['序号'] = list(range(1, len(data) + 1))
        return data

# 首先爬取最新数据
print('爬取DLT最新数据')
dltdata.dc_order()
# 主函数
dlt_data = CP()




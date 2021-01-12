#-*- coding：utf-8 -*-
# &Author  AnFany

# 双色球第一期为03001
import requests  # 这个网页编码方式比较特殊，需打开网页需要用到headers
from bs4 import BeautifulSoup as bs  # 格式化网页源码
import pandas as pd
import datetime


headers = {
       'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
       'Accept-Encoding': 'gizp,defale',
       'Accept-Language': 'zh-CN,zh;q=0.9'
   }

xingqi = {'0': '日', '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六'}

#  函数
def dc_order(start='03001', end='99001', head=headers, xqdict=xingqi):  #end值设置较大，保证可以获取所有的数据

    #  需要存储的数据
    qihao = []  # 存储期号
    riqi = []   # 存储日期
    zhouji = []  # 存储周几
    hongqiu = []  # 存储红球顺序
    lanqiu = []   # 存储蓝球

    response = requests.get('https://datachart.500.com/ssq/history/newinc/outball.php?start=%s&end=%s' % (start, end), headers=head).text

    bsoh = bs(response, "lxml")

    fu = bsoh.find_all('tr', class_='t_tr1')

    for jj in fu:
        ii = jj.get_text().split()[0]   #  数据比较规整：按位选取数据
        qihao.append('20%s' % str(ii[:5]))
        riqi.append(ii[5:15])

        # 根据日期添加星期几
        fu = datetime.datetime.strptime(ii[5:15], '%Y-%m-%d')

        anyday = fu.strftime("%w")

        # 数据中存在日期出现错误的情况，在这里需要更正。
        if anyday not in ['0', '2', '4']:
            # 需要将日期往前算一天
            newday = fu + datetime.timedelta(days=-1)
            # 更改日期
            riqi[-1] = newday
            anyday = newday.strftime('%w')

        zhouji.append('周%s' % xqdict[anyday])

        # 需要转变为列表的形式
        exlist = list(ii[15:27])

        numlist = [int(exlist[i] + exlist[i + 1]) for i in range(0, len(exlist), 2)]

        hongqiu.append(numlist)
        lanqiu.append([int(ii[-2:])])


    data = pd.DataFrame()

    data['期号'] = qihao
    data['日期'] = riqi
    data['星期'] = zhouji
    data['红球'] = hongqiu
    data['蓝球'] = lanqiu

    data.to_csv(r'C:\Users\GWT9\Desktop\ssq.csv', index=False, encoding=u'utf-8')

    return print('爬取的SSQ数据保存完毕,最新期号%s' % qihao[0])

# 主函数
if __name__ == '__main__':
    dc_order()



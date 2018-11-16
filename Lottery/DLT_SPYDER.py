#-*- coding：utf-8 -*-
# &Author  AnFany

# 获取08069至18130期的大乐透开球顺序的信息,08069是第一期有开奖顺序的
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
def dc_order(start='08069', end='99999', head=headers, xqdict=xingqi): # end设置较大数值，可保证获取最新的数据

    #  需要存储的数据
    qihao = []
    riqi = []
    zhouji = []
    qianqu = []
    houqu = []

    response = requests.get('https://datachart.500.com/dlt/history/newinc/outball.php?start=%s&end=%s' %(start, end), headers=head).text

    bsoh = bs(response, "html5lib")

    fu = bsoh.find_all('tr', class_='t_tr1')

    for jj in fu:
        ii = jj.get_text().split()[0]   #  数据比较规整：按位选取数据

        qihao.append('20%s' % str(ii[:5]))
        riqi.append(ii[5:15])
        # 根据日期添加星期几
        fu = datetime.datetime.strptime(ii[5:15], '%Y-%m-%d')

        anyday = fu.strftime("%w")

        zhouji.append('周%s' % xqdict[anyday])

        # 需要转变为列表的形式
        exlist = list(ii[15:25])

        numlist = [int(exlist[i] + exlist[i + 1]) for i in range(0, len(exlist), 2)]

        qianqu.append(numlist)


        exli = list(ii[-4:])

        numl = [int(exli[i] + exli[i + 1]) for i in range(0, len(exli), 2)]

        houqu.append(numl)

    data = pd.DataFrame()

    data['期号'] = qihao
    data['日期'] = riqi
    data['星期'] = zhouji
    data['前区'] = qianqu
    data['后区'] = houqu



    data.to_csv(r'C:\Users\GWT9\Desktop\dlt.csv', index=False, encoding= u'utf-8')

    return print('wanbi')


# 主函数
if __name__ == '__main__':
    dc_order()
# 注意更改路径
import os
os.chdir(r'C:\Users\GWT9\Desktop\queen')  # 设置当前工作目录
import imageio  # 引入合成gif的库

queencount = 8  # 可随意设置，如果设置为大于12的数，程序运行较慢。
# 根据已经选择的坐标点，输出与其冲突的在其斜线方向上的坐标集合
# 为了简化运算，定义一些设置
su = [[i, j] for i in ['+', '-'] for j in ['+', '-']]
sdict = {'+': '<queencount', '-': '> -1'}


# 返回冲突的斜线坐标集合
def simple(zuibiao, sign, sidict=sdict):
    save = []
    hang = zuibiao[0]
    lie = zuibiao[1]
    while eval('hang%s' % sidict[sign[0]]) and eval('lie%s' % sidict[sign[1]]):
        save.append([hang, lie])
        hang = eval('hang %s1' % sign[0])
        lie = eval('lie%s1' % sign[1])
    return save


# 返回与其冲突的全部坐标  斜线方向+同行同列方向
def allno(func, zuibiao, listsi=su, count=queencount):
    alist = []
    # 斜线方向
    for hs in listsi:
        alist += func(zuibiao, hs)  # 斜线方向上的冲突坐标集合
    # 同行同列方向上的冲突坐标集合
    for same in range(0, count):
        alist.append([same, zuibiao[1]])
        alist.append([zuibiao[0], same])
    return alist


# 根据已经选择的坐标，以及冲突的坐标集合，输出摆放第n个皇后的可能的坐标集合
def xikk(newlist, numb=queencount):
    fu = []
    for tu in newlist:
        fu += allno(simple, tu)  # 所有冲突的坐标集合
    slast = []
    if len(newlist) >= numb:
        return slast
    else:
        for jgi in [[len(newlist), j] for j in range(0, numb)]:  # 必须在第n行选取第n个坐标
            if jgi not in fu:
                slast.append(jgi)
        return slast  # 返回可能选择的坐标集合


startdict = {1: 0}  # 表示的是： 下一次添加的是第一行的可行的坐标集合中的第0个元素

# 尾递归优化
import sys
class TailRecurseException(BaseException):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs
def tail_call_optimized(g):
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back and f.f_back.f_back.f_code == f.f_code:
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs

    func.__doc__ = g.__doc__
    return func


# 回溯算法的函数
@tail_call_optimized
def huifu(select, exdict, save, nn=queencount):
    # select:已经选择的摆放皇后的坐标集合列表， exdict:存储第几个皇后的可行列表的第几个元素的字典， save:存储皇后问题的解
    # 判断当前的状况是不是皇后问题的解
    if len(select) == nn:  # 如果是，则添加到save中
        save.append(select)
    # 求出当前对应select的可行性的坐标集合
    fulist = xikk(select)
    if len(fulist) != 0:  # 如果可行性坐标集合不为空
        exdict[len(select) + 1] = 0  # 实时记录下一次选择应该是选择可行性坐标集合中的第几个元素
        return huifu(select + [fulist[exdict[len(select)]]], exdict, save)  # 开始递归
    else:
        # 如果可行性坐标集合为空
        # 开始从后往前计算，找到哪一个可行性坐标集合还有选择的余地
        # 如果都已经没有选择了，则遍历完成
        for jsa in list(range(1, len(select)))[::-1]:  # 从后往前计算
            fuud = xikk(select[0: jsa])
            if exdict[len(select[0: jsa])] < len(fuud) - 1:  # 说明有选择的余地
                # 说明找到一个满足条件的，需要更新字典
                newdict = {}
                for hh in exdict:
                    if hh < jsa + 1:
                        newdict[hh] = exdict[hh]
                fur = exdict[jsa] + 1
                newdict[jsa] = fur
                return huifu(select[0:jsa], newdict, save)  # 开始递归
        return save

sult = []
for jj in [[0, dfu] for dfu in range(0, queencount)]:#遍历第0行的元素，找到每一个位置有皇后时的所有解
    sult = huifu([jj], startdict, sult)#相加
import numpy as np  # 引入numpy数组库
# 通过主对角线对称变换[也就是转置]可以得到的解
def trans(exlist):
    yuannp = np.zeros((len(exlist), len(exlist)))
    for jj in exlist:
        yuannp[jj[0], jj[1]] = 1
    # 获得所有的同质解
    # 获得转置
    trannp = yuannp.T
    # 开始获得值为1 的坐标
    si = []
    for ihang in range(0, len(exlist)):
        for jlie in range(0, len(exlist)):
            if trannp[ihang][jlie] == 1:
                si.append([ihang, jlie])
    return si


# 顺时针每旋转90度产生一个本质一样的解，以及关于主、副对角线对称的解
def sameslover(siglelist):
    yuannp = np.zeros((len(siglelist), len(siglelist)))  # 构建全0数组
    for jj in siglelist:
        yuannp[jj[0], jj[1]] = 1  # 选中的坐标，其值为1
    # 开始旋转3次，因为旋转4次，与开始的重合，所以旋转3次
    xuanzhuan = 0
    # 获得所有的同质解
    tongzhi = []
    while xuanzhuan < 3:
        tongzhi.append(trans(siglelist))  # 添加 主对角线 对称的解
        xuanzhuan += 1
        # 开始向右翻转90度，形成的新数组的规则为：新数组的行从左到右，是旧数组的列从下往上依次组成的
        newnp = []
        for lienu in range(0, len(siglelist)):
            lie = []
            for low_up in range(len(siglelist) - 1, -1, -1):
                lie.append(yuannp[low_up, lienu])
            newnp.append(lie)
        # 开始获得值为1 的坐标
        si = []
        for ihang in range(0, len(siglelist)):
            for jlie in range(0, len(siglelist)):
                if newnp[ihang][jlie] == 1:
                    si.append([ihang, jlie])
        tongzhi.append(si)
        siglelist = si.copy()  # 通过这种变换，来获得关于 副对角线 对称的解
        # 在此基础上继续翻转
        yuannp = np.array(newnp).copy()
    tongzhi.append(trans(siglelist))  # 因为需要四个主对角线，循环里面有3次，因此需要加上最后一次，也就是旋转了270度形成的解 的主对角线 对称的解
    return tongzhi


# print(len(sult))
# 开始去除本质相同的解
for jj in sult:
    for gggg in sameslover(jj):
        if gggg in sult and gggg != jj:  # 不能删除和初始解一样的解
            sult.remove(gggg)
# print(len(sult)

# 开始绘图展示
from pylab import mpl  # 作图显示中文

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 设置中文字体为新宋体
import matplotlib.pyplot as plt

# 下图中以黑色方块代表皇后
scount = 1
for i_so in sult:
    # 开始绘制棋盘
    for i in range(0, len(i_so) + 1):
        plt.axhline(y=i, linewidth=3, color='k')
        plt.axvline(x=i, linewidth=3, color='k')
    plt.axis([0, len(i_so), 0, len(i_so)])
    plt.title('%d皇后问题不同解： 第%s个解' % (queencount, scount))
    # 开始绘制皇后, 黑色方块代表皇后
    for jif in i_so:
        plt.broken_barh([(jif[1], 1)], (len(i_so) - 1 - jif[0], 1), facecolors='k')
    plt.axis('off')  # 关闭坐标轴
    plt.savefig(r"./%s_%s.png" % (queencount, scount))  # 图片保存
    plt.close()
    scount += 1

# 最终的图片合成gif
# 所有的图片name集合
namelist = []
for jjj in range(1, len(sult) + 1):
    namelist += ['%s_%s.png' % (queencount, jjj)] * 8  # 数字8控制动态图中每类图片的显示时间


# 创建gif的函数
def create_gif(image_list, gif_name):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=0.2)  # duration控制动态图中每张图片的显示时间
    return


create_gif(namelist + [namelist[-1]] * 8, 'queen.gif')  # 数字8控制动态图中每类图片的显示时间



# -*- coding：utf-8 -*-
# &Author  AnFany

# 请注意修改文件路径
import os

os.chdir(r'C:\Users\GWT9\Desktop\Hanoi')  # 设置当前路径，也就是存储图片的路径
import imageio  # 引入库

# 解决汉诺塔的程序
# 柱子的名称设置
zhuzi = ['A', 'B', 'C']
# 金片的个数，大于1的整数
panzi = 5
# 利用字典储存每个柱子的金片信息
statusdict = {}
statusdict['A'] = list(range(1, panzi + 1))  # 开始时所有金片在柱子A上
statusdict['B'] = []
statusdict['C'] = []


# 定义更新字典的函数
def updata(startkey, endkey, sdict):  # startkey:开始柱，endkey:目标柱，sdict：存储柱子上金片信息的字典
    if len(sdict[startkey]) == 0:  # 如果开始柱没有金片，则确定不是开始柱，对应规则2
        return False
    if len(sdict[endkey]) != 0:
        if sdict[startkey][0] > sdict[endkey][0]:  # 对应规则3
            return False
    # 开始柱删除金片
    stlist = sdict[startkey].copy()
    forst = stlist[0]  # 要移动的金片
    del (stlist[0])
    sdict[startkey] = stlist.copy()
    # 目标柱增加金片
    endlist = sdict[endkey].copy()
    endlist.insert(0, forst)
    sdict[endkey] = endlist.copy()
    return sdict


# 2个盘子移动的方案
def last(sydict, signnum=0, zhu=zhuzi):  # 移动只和开始柱有关系
    movepath = []  # 存储移动的方案
    movepath.append([zhu[signnum], zhu[(signnum + 1) % 3]])  # 第一步：开始柱===》过渡柱
    sdict = updata(zhu[signnum], zhu[(signnum + 1) % 3], sydict)  # 更新字典
    movepath.append([zhu[signnum], zhu[(signnum + 2) % 3]])  # 第二步：开始柱===》目标柱
    sdict = updata(zhu[signnum], zhu[(signnum + 2) % 3], sdict)  # 更新字典
    movepath.append([zhu[(signnum + 1) % 3], zhu[(signnum + 2) % 3]])  # 第三步：过渡柱===》目标柱
    sdict = updata(zhu[(signnum + 1) % 3], zhu[(signnum + 2) % 3], sdict)  # 更新字典
    return movepath, sdict


# 金片移动=多次[最小的2个盘子的规律移动+其他盘子的规则移动] + 一次[最小的2个盘子的规律移动]
# 最小的盘子的移动靠规律 其他盘子的移动靠规则
def ali(count=panzi, signnum=0, zhu=zhuzi, sdict=statusdict):
    if count == 2:  # 只有2个盘子，直接last函数就可以出结果
        return last(sdict)[0]
    else:
        mode = []  # 存储所有的移动方案
        gu = 2 ** (count - 2) + 1  # 判断循环的次数
        while gu > 2:
            # 最小的两个盘子的规律移动
            result = last(sdict, signnum)
            mode += result[0]
            sdict = result[1]
            # 中间盘子的移动，因为第三步移动完成后，柱子的最上方是最小的，因此这个柱子既不可能是目标柱，也不可能是开始柱子。
            # 所以存在两种情况， 开始柱子 目标柱子：[zhu[signnum],zhu[(signnum + 1) % 3]]
            # 或者[zhu[(signnum + 1) % 3],[zhu[signnum]]
            # 以上情况只会有一个成立。不成立的情况只有2种：要不开始柱没有可移动的盘子，要不就是移动后会出现大的在小的上面
            judge = updata(zhu[signnum], zhu[(signnum + 1) % 3], sdict)
            if judge:  # 没有违背，说明zhu[signnum]为开始柱
                mode += [[zhu[signnum], zhu[(signnum + 1) % 3]]]
                sdict = judge.copy()
            else:  # 违背了
                mode += [[zhu[(signnum + 1) % 3], zhu[signnum]]]
                jjg = updata(zhu[(signnum + 1) % 3], zhu[signnum], sdict)
                sdict = jjg.copy()
            signnum = int((signnum + 2) % 3)  # 更新为下一个开始柱的编号
            gu -= 1
        mode += last(sdict, signnum)[0]  # 最后一个绿色区域的移动
        return mode


from pylab import mpl  # 作图显示中文

mpl.rcParams['font.sans-serif'] = ['FangSong']  # 设置中文字体为新宋体
import matplotlib.pyplot as plt

# 不同大小金片的颜色集合，如果金片多于10种，则随机选择颜色，否则固定
from matplotlib import colors as mcolors

colorname = ['black', 'maroon', 'cyan', 'yellow', 'red', 'blue', 'green', 'tan', 'navy', 'indigo']
colorset = []
import numpy as np

for jcolor in colorname:
    colorset.append(mcolors.cnames[jcolor])
lastcolor = colorset
if panzi > 10:
    lastcolor = np.random.choice(np.array(list(mcolors.cnames.keys())), panzi, replace=False)

# 图片的高度固定为10， 宽度固定为16

# 金片数不大于10，高度固定0.6，否则平均
if panzi <= 10:
    height = 0.6
else:
    height = round(8 / panzi, 1)

# 柱子的高度
if panzi <= 6:
    zhuzihei = panzi + 2
else:
    zhuzihei = 8

# 宽度设置，用列表从小到大表示
widthlist = np.linspace(0.6, 4.2, num=panzi)

# 存储柱子位置的字典
zhuzidict = {'A': [4, 0], 'B': [8, 0], 'C': [12, 0]}


# 根据金片的列表返回相应的path列表的函数
def outfigure(stkey, sidict, hei=height, wid=widthlist, zdi=zhuzidict, zcolo=lastcolor):
    ractlist = []
    ssartpoint = zdi[stkey]  # 起始的绘制点
    for spa in sidict[::-1]:  # 倒着画图，先画大的
        heng = ssartpoint[0] - (wid[spa - 1] / 2)
        zong = ssartpoint[1]
        ractstr = 'plt.Rectangle((%.4f, %.4f), %.4f, %.4f, facecolor="%s")' % (
        heng, zong, wid[spa - 1], hei, zcolo[spa - 1])
        ssartpoint = [ssartpoint[0], ssartpoint[1] + hei + 0.02]  # 更新绘制点
        ractlist.append(ractstr)
    return ractlist  # 返回path的列表


# 绘制柱子状态的函数
def combine(panzizhuangtai, stepnum, zhei=zhuzihei, pco=panzi):
    # 首先绘制柱子，柱子的颜色固定
    rect_a = plt.Rectangle((4, 0), 0.1, zhei, facecolor="#ff0000")
    rect_b = plt.Rectangle((8, 0), 0.1, zhei, facecolor="#00ff00")
    rect_c = plt.Rectangle((12, 0), 0.1, zhei, facecolor="#0000ff")
    fig, ax = plt.subplots()
    ax.add_patch(rect_a)  # 绘制柱子A
    ax.add_patch(rect_b)  # 绘制柱子B
    ax.add_patch(rect_c)  # 绘制柱子C
    # 为了美观，关闭x、y轴
    ax.set_axis_off()
    # 绘制每个柱子的当前盘子状态
    for hzhuzi in panzizhuangtai:
        if len(panzizhuangtai[hzhuzi]) != 0:
            # 开始绘制
            for ftra in outfigure(hzhuzi, panzizhuangtai[hzhuzi]):
                ax.add_patch(eval(ftra))
    # 柱子的设置
    plt.text(3.8, zhei + .2, 'A柱')
    plt.text(7.8, zhei + .2, 'B柱')
    plt.text(11.8, zhei + .2, 'C柱')
    # 图片的设置
    plt.ylim(0, 10)
    plt.xlim(0, 16)
    if stepnum != 2 ** pco - 1:
        plt.title('%d盘三阶汉诺塔  移动%s步后状态' % (pco, stepnum))
    else:
        plt.title('%d盘三阶汉诺塔移动%s步后完成 oh  yes ！！！' % (pco, stepnum))
    plt.savefig(r"./%s.png" % stepnum)  # 保存以便合成gif
    # plt.show()
    plt.close()


# 根据两条线总共选择5个点，前者选择2个，后者3个
def selectpoint(stkey, endkey, stsidict, enddict, zdi=zhuzidict, hei=height):
    # 首先得到起始点
    startpoint = [zdi[stkey][0], len(stsidict) * hei]
    # 再得到终止点
    endpoint = [zdi[endkey][0], len(enddict) * hei]
    # 中间点，纵坐标固定，横坐标为起始点与终止点横坐标和的一半
    middlepoint = [(startpoint[0] + endpoint[0]) / 2, 9]
    # 起始点到中间点的3个点
    sm = []
    for shrng in np.linspace(startpoint[0], middlepoint[0], 3):
        sm.append([shrng,
                   (middlepoint[1] - startpoint[1]) / (middlepoint[0] - startpoint[0]) * (shrng - startpoint[0]) +
                   startpoint[1]])
    # 中间点到结束点的3个点
    for miorng in np.linspace(middlepoint[0], endpoint[0], 3):
        sm.append([miorng,
                   (middlepoint[1] - endpoint[1]) / (middlepoint[0] - endpoint[0]) * (miorng - endpoint[0]) +
                   endpoint[1]])
    return sm[1:]  # 舍去第一个点，剩余5个点


# 绘制中间移动状态的函数
def move(panzizhuangtai, ppiont, stkeynum, s1, s2, stepnum, silenum, zhei=zhuzihei, hei=height, wid=widthlist,
         zcolo=lastcolor, pco=panzi):
    # 首先绘制柱子
    rect_a = plt.Rectangle((4, 0), 0.1, zhei, facecolor="#ff0000")
    rect_b = plt.Rectangle((8, 0), 0.1, zhei, facecolor="#00ff00")
    rect_c = plt.Rectangle((12, 0), 0.1, zhei, facecolor="#0000ff")
    fig, ax = plt.subplots()
    ax.add_patch(rect_a)  # 绘制柱子A
    ax.add_patch(rect_b)  # 绘制柱子B
    ax.add_patch(rect_c)  # 绘制柱子C
    # 为了美观，关闭x、y轴
    ax.set_axis_off()
    # 绘制每个柱子的当前盘子状态
    for hzhuzi in panzizhuangtai:
        if len(panzizhuangtai[hzhuzi]) != 0:
            # 开始绘制
            for ftra in outfigure(hzhuzi, panzizhuangtai[hzhuzi]):
                ax.add_patch(eval(ftra))
    # 绘制移动中的盘子
    rect = plt.Rectangle((ppiont[0] - (wid[stkeynum - 1] / 2), ppiont[1]), wid[stkeynum - 1], hei,
                         facecolor=zcolo[stkeynum - 1])
    ax.add_patch(rect)
    # 柱子的设置
    plt.text(3.8, zhei + .2, 'A柱')
    plt.text(7.8, zhei + .2, 'B柱')
    plt.text(11.8, zhei + .2, 'C柱')
    # 图片的设置
    plt.ylim(0, 10)
    plt.xlim(0, 16)
    plt.title('%d盘三阶汉诺塔  第%s步: %s柱---》%s柱 移动中' % (pco, stepnum, s1, s2))
    plt.savefig(r"./%s_%s.png" % (stepnum, silenum))  # 保存以便合成gif
    plt.close()


# 再重新定义一遍保存初始状态的字典，虽然前面已经定义过
staert = {}
staert['A'] = list(range(1, panzi + 1))
staert['B'] = []
staert['C'] = []

# 先画开始的汉诺塔的状态
step = 0
combine(staert, stepnum=step)
# 开始移动
for hh in ali():
    fir = staert[hh[0]][0]
    jianhao = staert[hh[0]][1:].copy()
    # 获得所有的中间点
    allmiddle = selectpoint(hh[0], hh[1], staert[hh[0]], staert[hh[1]])
    staert[hh[0]] = jianhao.copy()
    # 开始绘制中间过程
    step += 1
    sile = 1
    # 绘制移动过程中的图片
    for mm in allmiddle:
        move(staert, mm, fir, hh[0], hh[1], stepnum=step, silenum=sile)
        sile += 1
    du = staert[hh[1]].copy()
    du.insert(0, fir)
    # 更新字典
    staert[hh[1]] = du.copy()
    # 一个金片移动完成后，绘制状态
    combine(staert, stepnum=step)

# 最终的图片合成gif
# 所有的图片name集合
namelist = ['0.png']  # 开始状态的图片名称
for jjj in range(1, 2 ** panzi):
    for hhgu in range(1, 6):  # 中间移动过程一共选择了5个点
        namelist.append('%s_%s.png' % (jjj, hhgu))
    namelist += ['%s.png' % jjj] * 10


# 创建gif的函数
def create_gif(image_list, gif_name):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=0.1)
    return


# 运行函数
create_gif(namelist + [namelist[-1]] * 10, 'Hanoi.gif')

#引入组合库
import itertools
#算子列表
operator = ['+', '-', '*', '/']
#算子和括号的组合只存在如下五种表达式结构
format = ['((%d%s%d)%s%d)%s%d', \
          '(%d%s%d)%s(%d%s%d)', \
          '(%d%s(%d%s%d))%s%d', \
          '%d%s((%d%s%d)%s%d)', \
          '%d%s(%d%s(%d%s%d))']

#数字和字母穿插
def Chuan(num, letter):
    chuan = []
    for jj in range(len(num)):
        chuan.append(num[jj])
        try:
            chuan.append(letter[jj])
        except IndexError:
            pass
    return chuan

#构建数字和算子的组合
def Combine(numlist, oplist = operator):
    expre = []
    for jj in list(itertools.permutations(numlist, len(numlist))):
        for ii in list(itertools.product(oplist, repeat = 3)):
            expre.append(Chuan(list(jj), list(ii)))
    return expre

#获取全部表达式
def GetExpression(numlist, target, form = format):
    expre = set()
    exall = Combine(numlist)
    for gg in exall:
        for ff in form:
            try:
                ex = str(ff)%tuple(gg)
                if eval(ex) == target:
                    expre.add(ex)
            except ZeroDivisionError:
                pass
    return expre

import re
#提取表达是中数字和算子的函数
def NumOperator(nustr):
    save = []
    start = ''
    for sr in nustr:
        try:
            int(sr)
            start += sr
        except ValueError:
            if start == '':
                save.append(sr)
            else:
                save.append(start)
                save.append(sr)
            start = ''
    if start != '':
        save.append(start)
    return save

#删剪掉相近的表达式函数
def Simple(exprelist):
    simple = []
    last = []
    for ex in exprelist:
        sr = ex
        rema = re.findall("\([^()]+\)", ex)#匹配小括号里的内容
        #将匹配出来的内容进行替换
        for ii in rema:
            ex = ex.replace(ii, str(eval(ii)))
        #提取简化表达式中的数字和算子
        simop = NumOperator(ex)
        if sorted(simop) not in simple:
            simple.append(sorted(simop))
            last.append(sr)
    return last

express = Simple(list(GetExpression([2,5,8,8], 24)))
if len(express) == 0:
    print('无结果')
else:
    print('去掉数学角度上重复的表达式后：')
    for sig in express:
        print('%s = %s'%(sig, eval(sig)))


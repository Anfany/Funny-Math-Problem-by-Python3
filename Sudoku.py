#  引入库
import pandas as pd
import numpy as np
import os
 
# 存储数独题目的Excel文件路径
DataPath = r'C:\Users\AnFany\Desktop\Sudoku'
os.chdir(DataPath)
# 文件名
FileName = 'Sudoku.xlsx'
# 宫数设置，根据题目宫数的不同可选择9,16,25(数字越大，解题速度越慢)
sukoducount = 9
# 读取文件
ReadData = pd.read_excel(r'./%s'%FileName)
# 数独题目
NumData = ReadData.values
# 打印数独题目
print('号称最难的数独题目:\n', NumData)

#  判断数独题目的完整性
while len(NumData) < sukoducount:
    NumData = np.row_stack((NumData, [np.nan] * sukoducount))

#  根据格子的位置，计算该位置可以填写的数字集合
def ProbNumber(hang,lie,data):
    # 行数据
    H = list(data[hang])
    # 列数据
    L = list(data[:, lie])
    # 宫数据
    G = []
    sfang = int(len(data) ** 0.5)
    hh = hang // sfang
    ll = lie // sfang
    for ig in range(sfang):
        for gi in range(sfang):
            G.append(data[hh * sfang + ig, ll * sfang + gi])
    # 行，列，宫已经包含的数字集合  
    lal=list(H)+list(L)+G
    # 该空格可能选择的数字集合
    prob=[ip for ip in list(range(1,len(data)+1)) if ip not in lal]
    return prob


# 为题目中的空格计算填写数字的可能性，输出字典形式
def ForK(data):
    Kdict = {}
    for ik in range(len(data)):
        for ki in range(len(data)):
            if np.isnan(data[ik, ki]): # 判断空格
                # 计算可填写数字的集合
                trans = ProbNumber(ik, ki, data)
                # 转换是为了让所有空格的jieti值中，只有唯一的一个最小值
                jieti = len(trans) * 10000000 + ik * 10000 + ki * 10
                Kdict['%s-%s'%(ik, ki)] = [jieti, len(trans), trans]
    return Kdict


#  选择可能性最小的位置
def SeleM(ddict):
    Small=min(ddict.items(),key=lambda x:(x[1][0]))[0]
    #位置
    weizhi=Small.split('-')
    #hang
    Ha=int(weizhi[0])
    #lie
    Li=int(weizhi[1])
    #集合
    SE=ddict[Small][2]
    return Ha,Li,SE


#初始状态
InitialState={}

InitialState[0]=NumData

#取值字典
NumDict={}

global NU
NU=1

#状态转移
#记录栈中调用函数的次数
minzhai=0
def TransFer(insta,numdi,n=0,c=minzhai):
    #判断是否满足条件
    if len(ForK(insta[n]))==0:
        global NU
        NU=0
        return insta,numdi,n
    #选择最小的
    mmi=SeleM(ForK(insta[n]))
    if c>900:
        return insta,numdi,n

    if len(mmi[2])==0:
        del insta[n]
        c+=1
        return TransFer(insta,numdi,n-1,c)
    else:
        middle=insta[n].copy()
        if n in numdi:
            if numdi[n]+1<len(mmi[2]):
                numdi[n]+=1
                middle[mmi[0],mmi[1]]=mmi[2][numdi[n]]
                n+=1
                insta[n]=middle.copy()
                c+=1
                return TransFer(insta,numdi,n,c)
            else:
                del numdi[n]
                del insta[n]
                c+=1
                return TransFer(insta,numdi,n-1,c)
        else:
            numdi[n]=0
            middle[mmi[0],mmi[1]]=mmi[2][0]
            n+=1
            insta[n]=middle.copy()
            c+=1
            return TransFer(insta,numdi,n,c)

print('Working…')
c_0=TransFer(InitialState,NumDict)

VAR_NAME=locals()

#最终的函数
def Sudoku():
    count=1
    
    while NU!=0:
       VAR_NAME['c_%s'%count]=TransFer(eval('c_%s'%(count-1))[0],eval('c_%s'%(count-1))[1],eval('c_%s'%(count-1))[2])
       count+=1
       print('…')
    print('问题答案:\n',eval('c_%s'%(count-1))[0][eval('c_%s'%(count-1))[2]])

        
import time
start=time.clock()
Sudoku()
print('用时%s秒'%(time.clock() - start))






    
    

    
    
    

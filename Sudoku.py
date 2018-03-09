import pandas as pd
import numpy as np
import os
 
#数据文件路径
DataPath=r'C:\Users\GWT9\Desktop\Pro1 数独Sudoku'
os.chdir(DataPath)
#文件名
FileName='Sudoku.xlsx'
#规格
sukoducount=9
#读取数据
ReadData=pd.read_excel(r'./%s'%FileName)

#数据
NumData=ReadData.values

print('号称最难的数独题目:\n',NumData)

#判断数据行的完整性
while len(NumData)<sukoducount:
    NumData=np.row_stack((NumData,[np.nan]*sukoducount))

#计算可能性
def ProbNumber(hang,lie,data):
    #行数据
    H=list(data[hang])
    #列数据
    L=list(data[:,lie])
    #宫数据
    G=[]
    sfang=int(len(data)**0.5)
    hh=hang//sfang
    ll=lie//sfang
    #宫数据添加
    for ig in range(sfang):
        for gi in range(sfang):
            G.append(data[hh*sfang+ig,ll*sfang+gi])
    #该点的可能性
    lal=list(H)+list(L)+G
    prob=[ip for ip in list(range(1,len(data)+1)) if ip not\
          in lal]
    return prob


#为数据中的空元素选择可能性字典
def ForK(data):
    Kdict={}
    for ik in range(len(data)):
        for ki in range(len(data)):
            if np.isnan(data[ik,ki]):
                #转换，便于字典的最下值是唯一的
                trans=ProbNumber(ik,ki,data)
                jieti=len(trans)*10000000+ik*10000+ki*10
                Kdict['%s-%s'%(ik,ki)]=[jieti,len(trans),trans]
    return Kdict


#选择可能性最小的位置
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




    
    

    
    
    

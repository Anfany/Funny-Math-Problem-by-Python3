#引入库
import numpy as np

#奇数阶
def OddMagic(jieshu):  
    #存储幻方结构
    huanfang=np.zeros((jieshu,jieshu)) 
    #需要填写的数字列表
    listnum=list(range(1,jieshu**2+1))
    #第一行中间填1
    i=0
    j=int(jieshu/2)
    #记录填写的个数
    count=0
    while count<jieshu**2:
        huanfang[i][j]=listnum[count]
        #记录i,j
        cc=i
        dd=j
        #超出了第一行，则填到最底下一行
        if i-1<0:
            i=jieshu-1
        else:
            i-=1
        #超出了最右边一列，则填到最左边一列
        if j+1==jieshu:
            j=0
        else:
            j+=1
        #遇到下一个格子里已经有数字的，就填到当前格子的下方
        if huanfang[i][j]!=0:
            i=cc+1
            j=dd
        #次序加1
        count+=1
    return huanfang

#双偶阶幻方：阶数=2*偶数
def DoubleEvenMagic(jieshu):
    ##存储幻方结构
    huanfang=np.zeros((jieshu,jieshu))
    #需要填写的数字列表
    listnum=list(range(1,jieshu**2+1))
    #第一轮填充,从第一行第一列开始,从左到右,从上到下,从1到jieshu平方,依次填充
    #每四乘四的正方形,画主副对角线。规则是只填充没对角线的,画了对角线格子不写
    #记录个数
    count=0
    for hang in range(len(huanfang)):
        for lie in range(len(huanfang)):
            if (hang%4 in [0,3] and lie%4 in [1,2]) or\
               (hang%4 in [1,2] and lie%4 in [0,3]):#判断对角线
                huanfang[hang][lie]=listnum[count]
    #第二轮填充,从最后一行最后一列开始,从右到左,从下到上,从1到jieshu平方依次填充。
    #规则是只填充画了对角线的，没画对角线的不填
            else:
                huanfang[hang][lie]=listnum[::-1][count]
            count+=1
    return huanfang

#单偶阶幻方：阶数=2*奇数
def SingleEvenMagic(jieshu):
    #幻方结构
    huanfang=np.zeros((jieshu,jieshu))
    #子幻方阶数
    son=int(jieshu/2)
    #A象限幻方
    SAhf=OddMagic(son)
    huanfang[:,0:son][0:son]=SAhf
    #依次填充DBC象限
    huanfang[:,son:][son:]=huanfang[:,0:son][0:son]+son**2
    huanfang[:,son:][0:son]=huanfang[:,son:][son:]+son**2
    huanfang[:,0:son][son:]=huanfang[:,son:][0:son]+son**2
    #计算K值
    k=int((jieshu-2)/4)
    #AC象限互换
    #从A象限的中间行中间列开始为第一格,往右标出K格；标出A象限其他行的左边K列
    #先换AC象限所有行的左边K列
    middle=huanfang[:,0:k][0:son].copy()
    huanfang[:,0:k][0:son]=huanfang[:,0:k][son:]
    huanfang[:,0:k][son:]=middle
    #再换中间行的前2K列
    middle=huanfang[:,0:2*k][int(son/2):(int(son/2)+1)].copy()
    huanfang[:,0:2*k][int(son/2):(int(son/2)+1)]=huanfang[:,0:2*k][int(son/2)+son:(int(son/2)+1+son)]
    huanfang[:,0:2*k][int(son/2)+son:(int(son/2)+1+son)]=middle
    #BD象限互换
    if k-1!=0:
        #从B象限的中间列所有格子开始,向左标出K-1列,与D象限对换
        middle=huanfang[:,son:son+k-1][0:son].copy()
        huanfang[:,son:son+k-1][0:son]=huanfang[:,son:son+k-1][son:]
        huanfang[:,son:son+k-1][son:]=middle
    return huanfang

#最终构建幻方的函数
def Magic(jieshu):
    if jieshu<3:
        return '阶数不应小于3'
    elif jieshu%2==1:
        huanfang=OddMagic(jieshu)
    elif jieshu%4!=0:
        huanfang=SingleEvenMagic(jieshu)
    else:
        huanfang=DoubleEvenMagic(jieshu)
    return huanfang

#验证幻方的函数
def Test(jieshu):
    cc=Magic(jieshu)
    
    sumlist=list(cc.sum(axis=1))+list(cc.sum(axis=0))+[cc.trace()]#所有行、列以及主对角线数字和
    vicediag=0
    for iv in range(jieshu):
        vicediag+=cc[iv][jieshu-iv-1]
    sumlist+=[vicediag]#加上副对角线数字和
    if len(set(sumlist))==1:#判断和相等
        print(cc)
        return '结果正确'
    else:
        print('%s阶程序有bug'%jieshu)
        return False

print(Test(13))


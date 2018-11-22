#-*- coding：utf-8 -*-
# &Author  AnFany

# 预测下一期数据
import MODEL as MM
import SSQ_DATA as data_ssq
import DLT_DATA as data_dlt

# 定义预测SSQ的函数

def Predict_SSQ(outcount=[6, 1], xuhao=999999):
    '''
    :param outcount: 红球、蓝球的输出个数
    :param xuhao: 设置一个大数，则为预测下一期。
    :return: 返回预测的号码
    '''
    # 红球
    model_red = MM.MODEL(data_ssq.ssq_data.oodata, data_ssq.ssq_data.red, data_ssq.ssq_data.rc, '红球', 1, xuhao)
    fu_red = model_red.HuoDe()
    # 确定输出候选号码的个数
    maxcount_red = outcount[0]
    # 输出
    gail_red = model_red.MingZhong(fu_red, maxcount_red)
    print(gail_red)
    # 蓝球
    model_blue = MM.MODEL(data_ssq.ssq_data.oodata, data_ssq.ssq_data.blue, data_ssq.ssq_data.bc, '蓝球', 1, xuhao)
    fu = model_blue.HuoDe()
    # 确定输出候选号码的个数
    maxcount_blue = outcount[1]
    # 输出
    gail_blue = model_blue.MingZhong(fu, maxcount_blue)
    print(gail_blue)
    return print('SSQ预测完毕')


# 定义预测DLT的函数
def Predict_DLT(outcount=[5, 2], xuhao=999999):
    '''
    :param outcount: 前区、后区的输出个数
    :param xuhao: 设置一个大数，则为预测下一期。
    :return: 返回预测的号码
    '''
    # 前区
    model_qian = MM.MODEL(data_dlt.dlt_data.oodata, data_dlt.dlt_data.qian, data_dlt.dlt_data.qc, '前区', 1, xuhao)
    fu_qian = model_qian.HuoDe()
    # 确定输出候选号码的个数
    maxcount_qian = outcount[0]
    # 输出
    gail_qian = model_qian.MingZhong(fu_qian, maxcount_qian)
    print(gail_qian)
    # 后区
    model_hou = MM.MODEL(data_dlt.dlt_data.oodata, data_dlt.dlt_data.hou, data_dlt.dlt_data.hc, '后区', 2, xuhao)
    fu_hou = model_hou.HuoDe()
    # 确定输出候选号码的个数
    maxcount_hou = outcount[1]
    # 输出
    gail_hou = model_hou.MingZhong(fu_hou, maxcount_hou)
    print(gail_hou)
    return print('DLT预测完毕')

# 预测主函数

if __name__ == "__main__":

    Predict_SSQ()
    Predict_DLT()

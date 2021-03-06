# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 15:15:59 2017

@author: zhanghuijfls
"""

import pandas as pd

test = pd.read_csv('D:/SLaughter_code/RawData/bank_detail_test.txt',sep=',',header=None)
test.columns=['id','date','trade_type','trade_num','salary']
test['date'] = (test['date']/86400).astype(int)

loan_time = pd.read_csv('D:/SLaughter_code/RawData/loan_time_test.txt',sep=',',header=None)
loan_time.columns=['id','loan_time']
loan_time['loan_time'] = (loan_time['loan_time']/86400).astype(int)

test = pd.merge(test, loan_time, how='left', on='id')
test['loan'] = test['date']-test['loan_time']

test['type0'] = test['trade_type'].map(lambda x:1 if x==0 else 0)
test['type1'] = test['trade_type'].map(lambda x:1 if x==1 else 0)
test['s0'] = test['salary'].map(lambda x:1 if x==0 else 0)
test['s1'] = test['salary'].map(lambda x:1 if x==1 else 0)

print('---------id---------------')
#id
test2 = test.groupby('id').size().reset_index()
test2.columns = ['id','id_size']

def date_minmax(df):
    if len(df[df>0])==0:
        return 0
    else:
        a = df[df>0]
        return a.max()-a.min()
def cal_unique(df):
    return len(df.unique())
def date_loan_beforenear(df):
    if len(df[df<0])==0:
        return 0
    else:
        return abs(df[df<0].max())
def date_loan_afternear(df):
    if len(df[df>0])==0:
        return 0
    else:
        return df[df>0].min()
        
print('----------------------date---------------------')
#date
#时间跨度， 时间不同的个数，每天记录的最大个数，每天记录平均个数，每天记录最小个数，
#放款前最近的距离，放款后最近的距离，放款前后比例
date_minmax = test.groupby('id')['date'].apply(date_minmax).reset_index()
date_minmax.columns=['id','date_minmax']
date_unique = test.groupby('id')['date'].apply(cal_unique).reset_index()
date_unique.columns=['id','date_unique']
test_date = test.groupby(['id','date']).size().reset_index()
test_date.columns = ['id','date','date_size']
test_date = test_date.groupby('id')['date_size'].agg(['max','mean','min']).reset_index()
test_date.columns = ['id','date_maxsize','date_meansize','date_minsize']

date_loan_beforenear = test.groupby('id')['loan'].apply(date_loan_beforenear).reset_index()
date_loan_beforenear.columns = ['id','date_loan_beforenear']
date_loan_afternear = test.groupby('id')['loan'].apply(date_loan_afternear).reset_index()
date_loan_afternear.columns = ['id','date_loan_afternear']


test2 = pd.merge(test2, date_minmax, on='id')
test2 = pd.merge(test2, date_unique, on='id')
test2 = pd.merge(test2, test_date, on='id')
test2 = pd.merge(test2, date_loan_beforenear, on='id')
test2 = pd.merge(test2, date_loan_afternear, on='id')

test2['date_maxsize_ratio'] = test2['date_maxsize']/test2['id_size']
test2['date_minmax_ratio'] = test2['id_size']/(test2['date_minmax']+1)
test2['date_minmax_ratio_unique'] = test2['id_size']/test2['date_unique']
test2['date_max_min_sizeratio'] = test2['date_minsize']/test2['date_maxsize']
test2['date_maxsize_mean_ratio'] = test2['date_maxsize']/test2['date_meansize']

print('--------------------trade_type--------------------------')
#trade_type
def type1_type0_ratio(df):
    return len(df[df==1])/(len(df[df==0])+1)
def type0_size(df):
    return len(df[df==0])
def type1_size(df):
    return len(df[df==1])
def type1_0_beforeratio(df):
    df = df[df.loan<0]
    return len(df[df.trade_type==1])/(len(df[df.trade_type==0])+1)
def type1_0_afterratio(df):
    df = df[df.loan>0]
    if len(df)==0:
        return 0
    else:
        return len(df[df.trade_type==1])/(len(df[df.trade_type==0])+1)
def type1_beforeratio(df):
    a = df[df.loan<0]
    return len(a[a.trade_type==1])/len(df)
def type1_afterratio(df):
    a = df[df.loan>0]
    return len(a[a.trade_type==1])/len(df)
def type0_beforeratio(df):
    a = df[df.loan<0]
    return len(a[a.trade_type==0])/len(df)
def type0_afterratio(df):
    a = df[df.loan>0]
    return len(a[a.trade_type==1])/len(df)
    
type1_type0_ratio = test.groupby('id')['trade_type'].apply(type1_type0_ratio).reset_index()
type1_type0_ratio.columns = ['id','type1_type0_ratio']
type0_size = test.groupby('id')['trade_type'].apply(type0_size).reset_index()
type0_size.columns = ['id','type0_size']
type1_size = test.groupby('id')['trade_type'].apply(type1_size).reset_index()
type1_size.columns = ['id','type1_size']

type1_type0_beforeratio = test.groupby('id').apply(type1_0_beforeratio).reset_index()
type1_type0_beforeratio.columns=['id','type1_0_beforeratio']
type1_type0_afterratio = test.groupby('id').apply(type1_0_afterratio).reset_index()
type1_type0_afterratio.columns=['id','type1_0_afterratio']

type1_beforeratio = test.groupby('id').apply(type1_beforeratio).reset_index()
type1_beforeratio.columns = ['id','type1_beforeratio']
type1_afterratio = test.groupby('id').apply(type1_afterratio).reset_index()
type1_afterratio.columns = ['id','type1_afterratio']

type0_beforeratio = test.groupby('id').apply(type0_beforeratio).reset_index()
type0_beforeratio.columns = ['id','type0_beforeratio']
type0_afterratio = test.groupby('id').apply(type0_afterratio).reset_index()
type0_afterratio.columns = ['id','type0_afterratio']

test2 = pd.merge(test2, type1_type0_ratio, on='id')
test2 = pd.merge(test2, type0_size, on='id')
test2 = pd.merge(test2, type1_size, on='id')
test2 = pd.merge(test2, type1_type0_beforeratio, on='id')
test2 = pd.merge(test2, type1_type0_afterratio, on='id')
test2 = pd.merge(test2, type1_beforeratio, on='id')
test2 = pd.merge(test2, type1_afterratio, on='id')
test2 = pd.merge(test2, type0_beforeratio, on='id')
test2 = pd.merge(test2, type0_afterratio, on='id')

test2['type1_fre'] = test2['type1_size']/(test2['date_minmax']+1)
test2['type0_fre'] = test2['type0_size']/(test2['date_minmax']+1)
test2['type1_eachday'] = test2['type1_size']/test2['date_unique']
test2['type0_eachday'] = test2['type0_size']/test2['date_unique']
test2['ab_type1_type0_ratio'] = test2['type1_0_afterratio']/(test2['type1_0_beforeratio']+1)
test2['ab_type1_ratio'] = test2['type1_afterratio']/(test2['type1_beforeratio']+1)
test2['ab_type0_ratio'] = test2['type0_afterratio']/(test2['type0_afterratio']+1)


print('----------------------------trade_num----------------------------')
#trade_num  type1_num 支出金额    type0_num 收入金额
#s0_type0_num  非工资收入    s1_type0_num  工资收入
test['type1_num'] = test['type1']*test['trade_num']
test['type0_num'] = test['type0']*test['trade_num']
test['s0_type0_num'] = test['s0']*test['trade_num']
test['s1_type0_num'] = test['s1']*test['type0']*test['trade_num']
type1_num_sum = test.groupby('id')['type1_num'].agg(['sum','max']).reset_index()
type1_num_sum.columns=['id','type1_num_sum','type1_num_max']
type0_num_sum = test.groupby('id')['type0_num'].agg(['sum','max']).reset_index()
type0_num_sum.columns = ['id','type0_num_sum','type0_num_max']

test2 = pd.merge(test2, type1_num_sum, on='id')
test2 = pd.merge(test2, type0_num_sum, on='id')
#平均每笔账单收入，支出金额
test2['type1_num_mean'] = test2['type1_num_sum']/test2['type1_size']
test2['type0_num_mean'] = test2['type0_num_sum']/test2['type0_size']
#平均每天收入，支出金额
test2['date_type0_num'] = test2['type0_num_sum']/(test2['date_minmax']+1)
test2['date_type1_num'] = test2['type1_num_sum']/(test2['date_minmax']+1)

#支付，收入金额之间关系
test2['type1_type0_sum_ratio'] = test2['type1_num_sum']/(test2['type0_num_sum']+1)
test2['type_type0_sum_reduce'] = test2['type0_num_sum']-test2['type1_num_sum']

#工资收入均值，最大值，平均每天工资收入
def s1_type0_num_mean(df):
    df = df[df.s1_type0_num>0]
    if len(df)==0:
        return 0
    else:
        return df.s1_type0_num.mean()
s1_type0_num = test.groupby('id')['s1_type0_num'].agg(['sum','max']).reset_index()
s1_type0_num.columns = ['id','s1_type0_num_sum','s1_type0_num_max']
s1_type0_num_mean = test.groupby('id').apply(s1_type0_num_mean).reset_index()
s1_type0_num_mean.columns = ['id','s1_type0_num_mean']

test2 = pd.merge(test2, s1_type0_num, on='id')
test2 = pd.merge(test2, s1_type0_num_mean, on='id')
test2['s1_type0_eachday'] = test2['s1_type0_num_sum']/test2['date_minmax']

#非工资收入均值，最大值，平均每天非工资收入
def s0_type0_num_mean(df):
    df = df[df.s0_type0_num>0]
    if len(df)==0:
        return 0
    else:
        return df.s0_type0_num.mean()
s0_type0_num = test.groupby('id')['s0_type0_num'].agg(['sum','max']).reset_index()
s0_type0_num.columns = ['id','s0_type0_num_sum','s0_type0_num_max']
s0_type0_num_mean = test.groupby('id').apply(s0_type0_num_mean).reset_index()
s0_type0_num_mean.columns = ['id','s0_type0_num_mean']

test2 = pd.merge(test2, s0_type0_num, on='id')
test2 = pd.merge(test2, s0_type0_num_mean, on='id')
test2['s0_type0_eachday'] = test2['s0_type0_num_sum']/(test2['date_minmax']+1)

#非工资收入占收入之比,放款前后比，以及变化比
def s0_s1_type0(df):
    return df.s0_type0_num.sum()/(df.type0_num.sum()+1)
def before_s0_s1_type0(df):
    df = df[df.loan<0]
    return df.s0_type0_num.sum()/(df.type0_num.sum()+1)
def after_s0_s1_type0(df):
    df = df[df.loan>0]
    return df.s0_type0_num.sum()/(df.type0_num.sum()+1)
s0_s1_type0 = test.groupby('id').apply(s0_s1_type0).reset_index()
s0_s1_type0.columns = ['id','s0_type0_ratio']
before_s0_s1_type0 = test.groupby('id').apply(before_s0_s1_type0).reset_index()
before_s0_s1_type0.columns = ['id','before_s0_type0_ratio']
after_s0_s1_type0 = test.groupby('id').apply(after_s0_s1_type0).reset_index()
after_s0_s1_type0.columns = ['id','after_s0_type0_ratio']

test2 = pd.merge(test2, s0_s1_type0, on='id')
test2 = pd.merge(test2, before_s0_s1_type0, on='id')
test2 = pd.merge(test2, after_s0_s1_type0, on='id')
test2['ab_s0_type0_ratio'] = test2['after_s0_type0_ratio']/(test2['before_s0_type0_ratio']+1)

#平均每天支出，收入金额,和最大值
id_date_type1 = test.groupby(['id','date'])['type1_num'].sum().reset_index()
id_date_type1.columns = ['id','date','type1_num']
id_date_type1_mean = id_date_type1.groupby('id')['type1_num'].agg(['mean','max']).reset_index()
id_date_type1_mean.columns = ['id','id_date_type1_mean','id_date_type1_max']

id_date_type0 = test.groupby(['id','date'])['type0_num'].sum().reset_index()
id_date_type0.columns = ['id','date','type0_num']
id_date_type0_mean = id_date_type0.groupby('id')['type0_num'].agg(['mean','max']).reset_index()
id_date_type0_mean.columns = ['id','id_date_type0_mean','id_date_type0_max']

test2 = pd.merge(test2, id_date_type1_mean, on='id')
test2 = pd.merge(test2, id_date_type0_mean, on='id')


#放款前后个数
def before_date_loan(df):
    return len(df[df<0])
def after_date_loan(df):
    return len(df[df>0])
before_date_loan = test.groupby('id')['loan'].apply(before_date_loan).reset_index()
before_date_loan.columns = ['id','before_date_loan']
after_date_loan = test.groupby('id')['loan'].apply(after_date_loan).reset_index()
after_date_loan.columns = ['id','after_date_loan']

test2 = pd.merge(test2, before_date_loan, on='id')
test2 = pd.merge(test2, after_date_loan, on='id')
test2['ab_date_loan'] = test2['after_date_loan']/(test2['before_date_loan']+1)



test2.to_csv('D:/SLaughter_code/python_feature/bank_test.csv',index=None)











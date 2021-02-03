from typing import List
import pandas as pd
import sys, numpy as np
from datetime import datetime
from pyecharts.charts import Bar, Line
from pyecharts.charts import Pie
from pyecharts import options as opts

## 전처리데이터 불러오기
Rawdata = pd.read_excel('./Rawdata.xlsx')

## 공통
# x축, 출원연도list
출원연도list = []
for year in range(20):
    years = year + (datetime.today().year - 19)
    출원연도list.append(years)
# DataFrame 생성 시 열 만들고 데이터 입력
출원연도list = pd.DataFrame(data={'출원연도' : 출원연도list})
# 동적 변수 할당 mod
mod = sys.modules[__name__]
# 주요국(중국제외), For문
주요국 = ['KR', 'JP', 'US', 'EP']

## 첫번째(A), 전체 출원동향(연도별 출원건수 및 누적건수)
# 1-1, 데이터 정리
A출원연도counts = pd.DataFrame(Rawdata['출원연도'].value_counts())
A그래프data = A출원연도counts.reset_index()
A그래프data.rename(columns={'index' : '출원연도', '출원연도' : '출원건수'}, inplace = True)
A그래프data = A그래프data.sort_values(by='출원연도', ascending = True)
A그래프data['누적건수'] = np.cumsum(A그래프data['출원건수'])
# 1-2, Bar그래프
Abar = (Bar()
    .add_xaxis(list(A그래프data['출원연도']))
    .add_yaxis('출원건수', list(A그래프data['출원건수']))
    # 보조축 생성, 간격 1000건
    .extend_axis(yaxis=opts.AxisOpts(interval = 1000))
    # 레이블 삭제
    #.set_series_opts(label_opts=opts.LabelOpts(is_show=False)
    #.add_yaxis('범례', 값)
    #.add_xaxis / .add_yaxis 추가함으로써 막대 추가 가능
    #.set_global_opts(title_opts=opts.TitleOpts(title='제목', subtitle='소제목))
)
# 1-3, Line그래프
Aline = (Line()
    # list_str = map(str, list_int)
    .add_xaxis(xaxis_data = map(str,A그래프data['출원연도']))
    # 레이블 삭제 / 보조축 인덱스
    .add_yaxis("누적건수", y_axis = list(A그래프data['누적건수']),label_opts=opts.LabelOpts(is_show=False), yaxis_index = 1, is_smooth=True)
)
# 1-4, 최종 그래프 저장
Abar.overlap(Aline).render("전체 출원동향.html")


## 두번째(B), 주요국 연도별 출원동향 및 점유율
# 2-1, 데이터 정리1
B주요국counts = Rawdata['출원국가코드'].value_counts()
B그래프data1 = B주요국counts.reset_index()
B그래프data1.rename(columns={'index' : '출원국가코드', '출원국가코드' : '출원건수'}, inplace = True)
# 2-1, Pie그래프
Bpie = (Pie()
        .add('', data_pair = [list(a) for a in zip(B그래프data1['출원국가코드'], B그래프data1['출원건수'])]
            , center = ['80%', '25%']
            , radius = ('40'))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b} : {d}%"))
       )
# 2-2, 데이터 정리2
B국가연도data = Rawdata[['출원국가코드', '출원연도']]
for country in 주요국:
    Bconditoin = (B국가연도data['출원국가코드'] == country)
    B주요국data = B국가연도data[Bconditoin] # 출원국가 필터링
    B출원연도counts = B주요국data['출원연도'].value_counts()
    B그래프data2 = B출원연도counts.reset_index()
    B그래프data2.rename(columns={'index' : '출원연도', '출원연도' : '출원건수'}, inplace = True)
    B그래프data2 = B그래프data2.sort_values(by='출원연도', ascending = True)
    B그래프data21 = pd.merge(출원연도list, B그래프data2, on='출원연도', how='left')
    B그래프data22 = B그래프data21.replace(np.nan, 0, regex=True)
    B그래프data23 = B그래프data22.astype({'출원건수' : np.int64})
    # 동적 변수 할당
    setattr(mod, 'Blinedata{}'.format(country), B그래프data23)
# 2-3, Bar그래프
Bbar = (Bar()
    .add_xaxis(list(출원연도list['출원연도']))
    )
# 2-4, Line그래프
Bline = (Line()
    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
    .add_yaxis('KR' ,y_axis = list(getattr(mod, 'Blinedata{}'.format('KR'))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
    .add_yaxis('US' ,y_axis = list(getattr(mod, 'Blinedata{}'.format('US'))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
    .add_yaxis('JP' ,y_axis = list(getattr(mod, 'Blinedata{}'.format('JP'))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
    .add_yaxis('EP' ,y_axis = list(getattr(mod, 'Blinedata{}'.format('EP'))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    )
    
Bbar.overlap(Bline)
Bbar.overlap(Bpie).render('주요국 출원동향.html')

## 세번째(C), 주요국 내 상위 다출원국가 연도별 출원동향 및 점유율
# 3-1, 데이터 정리1
for country1 in 주요국:
    Ccondition1 = (Rawdata['출원국가코드'] == country1) 
    C출원국가data = Rawdata[Ccondition1] # 출원국가 필터링
    C출원국가코드counts = C출원국가data['출원인국가코드'].value_counts()
    C그래프data1 = C출원국가코드counts.reset_index()
    C그래프data1.rename(columns={'index' : '출원인국가코드', '출원인국가코드' : '출원건수'}, inplace = True)
    C그래프data1 = C그래프data1.sort_values(by='출원건수', ascending = False).head(4)
 # 3-2, Pie그래프
    Cpie = (Pie()
        .add('',[list(a) for a in zip(C그래프data1['출원인국가코드'], C그래프data1['출원건수'])]
            , center = ['80%', '25%']
            , radius = '40')
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b} : {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}")) {c}는 건수
        # .set_global_opts(title_opts=opts.TitleOpts(title='제목'))
        # .render("국가별 출원건수 - {} 내 상위 다출원국가 - 점유율 .html".format(ccodea))
    )

# 3-3, 데이터 정리2
    C국가코드list = list(C그래프data1['출원인국가코드'][0:])
    for country2 in C국가코드list:
        Ccondition2 = (C출원국가data['출원인국가코드'] == country2)
        C출원인국가data = C출원국가data[Ccondition2] # 출원인국가 필터링
        C출원인국가data = C출원인국가data[['출원연도','출원인국가코드']]
        C출원연도counts = C출원인국가data['출원연도'].value_counts()
        C그래프data2 = C출원연도counts.reset_index()
        C그래프data2.rename(columns={'index' : '출원연도', '출원연도' : '출원건수'}, inplace = True)
        C그래프data2 = C그래프data2.sort_values(by='출원연도', ascending = True)
        C그래프data21 = pd.merge(출원연도list, C그래프data2, on='출원연도', how='left')
        C그래프data22 = C그래프data21.replace(np.nan, 0, regex=True)
        C그래프data23 = C그래프data22.astype({'출원건수' : np.int64})     
        # 동적 변수 할당 setattr
        setattr(mod, 'Clinedata{}'.format(country2), C그래프data23)

    Cbar = (Bar()
    .add_xaxis(list(출원연도list['출원연도']))
    )
    
    Cline = (Line()
    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
    .add_yaxis('{}'.format(C그래프data1['출원인국가코드'][0])
               ,y_axis = list(getattr(mod, 'Clinedata{}'.format(C그래프data1['출원인국가코드'][0]))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
    .add_yaxis('{}'.format(C그래프data1['출원인국가코드'][1]),
               y_axis = list(getattr(mod, 'Clinedata{}'.format(C그래프data1['출원인국가코드'][1]))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
    .add_yaxis('{}'.format(C그래프data1['출원인국가코드'][2])
               ,y_axis = list(getattr(mod, 'Clinedata{}'.format(C그래프data1['출원인국가코드'][2]))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
    .add_yaxis('{}'.format(C그래프data1['출원인국가코드'][3])
               ,y_axis = list(getattr(mod, 'Clinedata{}'.format(C그래프data1['출원인국가코드'][3]))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    )
    
    Cbar.overlap(Cline)
    Cbar.overlap(Cpie).render('{}.html'.format(country1))
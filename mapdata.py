import pandas as pd
import sys, numpy as np
from datetime import datetime
from pyecharts.charts import Bar, Line
from pyecharts.charts import Pie
from pyecharts import options as opts

# preprocessina 엑셀파일 또는 새로 생성하여야 함 (출원연도)
rawdata = pd.read_excel('./preprocessinga.xlsx')

# 2002 ~ 2021 출원연도 리스트
predatabyearlist = []
for year in range(20):
    year = year + (datetime.today().year - 19)
    predatabyearlist.append(year)
    year = 0
# DataFrame 생성 시 칼럼 기초값
predatabyearlist = pd.DataFrame(data={'출원연도' : predatabyearlist})
# 동적 변수 할당 mod
mod = sys.modules[__name__]
# KR, JP, US, EP / For문 List
krjpusep = ['KR', 'JP', 'US', 'EP']

# 첫번째, 전체 출원연도별 출원건수 - Bar/Line그래프
agraph = pd.DataFrame(rawdata['출원연도'].value_counts())
agraph = agraph.reset_index()
agraph.rename(columns={'index' : '출원연도', '출원연도' : '출원건수'}, inplace = True)
agraph = agraph.sort_values(by='출원연도', ascending = True)
agraph['누적건수'] = np.cumsum(agraph['출원건수'])
# Bar그래프 작성
abar = (Bar()
    .add_xaxis(list(agraph['출원연도']))
    .add_yaxis('출원건수', list(agraph['출원건수']))
    # 보조축 생성, 간격 1000건
    .extend_axis(yaxis=opts.AxisOpts(interval = 1000))
    # 레이블 삭제
    #.set_series_opts(label_opts=opts.LabelOpts(is_show=False)

    #.add_yaxis('범례', 값)
    #.add_xaxis / .add_yaxis 추가함으로써 막대 추가 가능

    #.set_global_opts(title_opts=opts.TitleOpts(title='제목', subtitle='소제목))
)
# Line그래프 작성 / str list로 변환하여야 함 # list_str = map(str, list_int) 사용
aline = (Line()
    .add_xaxis(xaxis_data = map(str,agraph['출원연도']))
    # 레이블 삭제 / 보조축 인덱스
    .add_yaxis("누적건수", y_axis = list(agraph['누적건수']),label_opts=opts.LabelOpts(is_show=False), yaxis_index = 1, is_smooth=True)
)
# 첫번째, 최종 Bar + Line
abar.overlap(aline).render("전체 출원동향.html")


# 두번째, KR, JP, US, EP 출원
bgraphdataa = rawdata['출원국가'].value_counts()
bgraphdataa = bgraphdataa.reset_index()
bgraphdataa.rename(columns={'index' : '출원국가', '출원국가' : '출원건수'}, inplace = True)
# 2-1, pie 그래프 작성
bpie = (Pie()
        .add('', data_pair = [list(a) for a in zip(bgraphdataa['출원국가'], bgraphdataa['출원건수'])]
            , center = ['80%', '25%']
            , radius = ('40'))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b} : {d}%"))
       )

# 2-2, line 그래프 작성
bgraphdatab = rawdata[['출원국가', '출원연도']]
for bcodeb in krjpusep:
    bconditionb = (bgraphdatab['출원국가'] == bcodeb)
    bpredatab = bgraphdatab[bconditionb] # 출원국가 필터링
    bconditionb = (bgraphdatab['출원국가'] == bcodeb)
    bpredatab = bgraphdatab[bconditionb]
    bpredatab = bpredatab['출원연도'].value_counts()
    bpredatab = bpredatab.reset_index()
    bpredatab.rename(columns={'index' : '출원연도', '출원연도' : '출원건수'}, inplace = True)
    bpredatab = bpredatab.sort_values(by='출원연도', ascending = True)
    bpredatabyeara = pd.merge(predatabyearlist, bpredatab, on='출원연도', how='left')
    bpredatabyearb = bpredatabyeara.replace(np.nan, 0, regex=True)
    bpredatabyearc = bpredatabyearb.astype({'출원건수' : np.int64})
    # 동적 변수 할당
    setattr(mod, 'blinedata{}'.format(bcodeb), bpredatabyearc)

bbar = (Bar()
    .add_xaxis(list(predatabyearlist['출원연도']))
    )
    
bline = (Line()
    .add_xaxis(xaxis_data = map(str,list(predatabyearlist['출원연도'])))
    .add_yaxis('KR' ,y_axis = list(getattr(mod, 'blinedata{}'.format('KR'))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    .add_xaxis(xaxis_data = map(str,list(predatabyearlist['출원연도'])))
    .add_yaxis('JP' ,y_axis = list(getattr(mod, 'blinedata{}'.format('JP'))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    .add_xaxis(xaxis_data = map(str,list(predatabyearlist['출원연도'])))
    .add_yaxis('US' ,y_axis = list(getattr(mod, 'blinedata{}'.format('US'))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    .add_xaxis(xaxis_data = map(str,list(predatabyearlist['출원연도'])))
    .add_yaxis('EP' ,y_axis = list(getattr(mod, 'blinedata{}'.format('EP'))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    )
    
bbar.overlap(bline)
bbar.overlap(bpie).render('국가별 출원동향.html')

# 세번째
# 3-1, 국가별 출원건수 - Pie그래프 (점유율)
for ccodea in krjpusep:
    cconditiona = (rawdata['출원국가'] == ccodea) 
    cgraphdata = rawdata[cconditiona] # 출원국가 필터링
    cpredataa = cgraphdata['국가코드'].value_counts()
    cpredataa = cpredataa.reset_index()
    cpredataa.rename(columns={'index' : '국가코드', '국가코드' : '출원건수'}, inplace = True)
    cpredataa = cpredataa.sort_values(by='출원건수', ascending = False).head(4)
    # Pie그래프 작성
    cpie = (Pie()
        .add('',[list(a) for a in zip(cpredataa['국가코드'], cpredataa['출원건수'])]
            , center = ['80%', '25%']
            , radius = '40')
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b} : {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}")) {c}는 건수
        # .set_global_opts(title_opts=opts.TitleOpts(title='제목'))
        # .render("국가별 출원건수 - {} 내 상위 다출원국가 - 점유율 .html".format(ccodea))
    )

    # 3-2. 국가별 출원건수 - line그래프 (연도별 출원동향)
    cgraphcodeb = list(cpredataa['국가코드'][0:])
    for ccodeb in cgraphcodeb:
        ccondtionb = (cgraphdata['국가코드'] == ccodeb)
        cpredatab = cgraphdata[ccondtionb]        
        cpredatab = cpredatab[['출원연도','국가코드']]
        cpredatab = cpredatab['출원연도'].value_counts()
        cpredatab = cpredatab.reset_index()
        cpredatab.rename(columns={'index' : '출원연도', '출원연도' : '출원건수'}, inplace = True)
        cpredatab = cpredatab.sort_values(by='출원연도', ascending = True)
        cpredatabyeara = pd.merge(predatabyearlist, cpredatab, on='출원연도', how='left')
        cpredatabyearb = cpredatabyeara.replace(np.nan, 0, regex=True)
        cpredatabyearc = cpredatabyearb.astype({'출원건수' : np.int64})
        
        # 동적 변수 할당 setattr
        setattr(mod, 'data{}'.format(ccodeb), cpredatabyearc)

    cbar = (Bar()
    .add_xaxis(list(predatabyearlist['출원연도']))
    )
    
    cline = (Line()
    .add_xaxis(xaxis_data = map(str,list(predatabyearlist['출원연도'])))
    .add_yaxis('{}'.format(cpredataa['국가코드'][0])
               ,y_axis = list(getattr(mod, 'data{}'.format(cpredataa['국가코드'][0]))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    .add_xaxis(xaxis_data = map(str,list(predatabyearlist['출원연도'])))
    .add_yaxis('{}'.format(cpredataa['국가코드'][1]),
               y_axis = list(getattr(mod, 'data{}'.format(cpredataa['국가코드'][1]))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    .add_xaxis(xaxis_data = map(str,list(predatabyearlist['출원연도'])))
    .add_yaxis('{}'.format(cpredataa['국가코드'][2])
               ,y_axis = list(getattr(mod, 'data{}'.format(cpredataa['국가코드'][2]))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    .add_xaxis(xaxis_data = map(str,list(predatabyearlist['출원연도'])))
    .add_yaxis('{}'.format(cpredataa['국가코드'][3])
               ,y_axis = list(getattr(mod, 'data{}'.format(cpredataa['국가코드'][3]))['출원건수'])
               ,label_opts=opts.LabelOpts(is_show=False)
               ,is_smooth=True)
    )
    
    cbar.overlap(cline)
    cbar.overlap(cpie).render('{}.html'.format(ccodea))
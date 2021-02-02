import pandas as pd
import sys, numpy as np
from datetime import datetime
from pyecharts.charts import Bar, Line
from pyecharts.charts import Pie
from pyecharts import options as opts

# preprocessina 엑셀파일 또는 새로 생성하여야 함 (출원연도)
rawdata = pd.read_excel('./preprocessing.xlsx')

# 전체 출원연도별 출원건수 - Bar/Line그래프
agraph = pd.DataFrame(rawdata['출원연도'].value_counts())
agraph = agraph.reset_index()
agraph.rename(columns={'index' : '출원연도', '출원연도' : '출원건수'}, inplace = True)
agraph = agraph.sort_values(by='출원연도', ascending = True)
agraph['누적건수'] = np.cumsum(agraph['출원건수'])
# Bar그래프 작성
abar = (Bar()
    .add_xaxis(list(agraph['출원연도']))
    .add_yaxis('출원건수', list(agraph['출원건수']))
    # .add_yaxis('범례', 값)
    # .add_xaxis / .add_yaxis 추가함으로써 막대 추가 가능
    # .set_global_opts(title_opts=opts.TitleOpts(title='제목', subtitle='소제목))
    # .render('연도별 출원건수 그래프(bar).html')
)
# Line그래프 작성 / str list로 변환하여야 함
# list_str = map(str, list_int) 사용
aline = (Line()
    .add_xaxis(xaxis_data = map(str,agraph['출원연도']))
    .add_yaxis("누적건수", y_axis = list(agraph['누적건수']))
    # .render("누적건수 그래프(line).html")
)

# Bar + Line
abar.overlap(aline).render("전체 출원동향.html")


# 국가별 출원건수 - Pie그래프, 상위 4개 국가코드 및 출원건수
bgraphcodea = ['KR', 'JP', 'US', 'EP']
for bcodea in bgraphcodea:
    bcondition = (rawdata['출원국가'] == bcodea) 
    bgraphdata = rawdata[bcondition] # 출원국가 필터링
    bpredataa = bgraphdata['국가코드'].value_counts()
    bpredataa = bpredataa.reset_index()
    bpredataa.rename(columns={'index' : '국가코드', '국가코드' : '출원건수'}, inplace = True)
    bpredataa = bpredataa.sort_values(by='출원건수', ascending = False).head(4)
    # Pie그래프 작성
    (Pie()
        .add('',[list(a) for a in zip(bpredataa['국가코드'],bpredataa['출원건수'])])
        # ,radius=["60%", "20%"] 도넛으로 만듬
        # ,center=["35%, "50%] 위치 조정

        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}")) {c}는 건수
        # .set_global_opts(title_opts=opts.TitleOpts(title='제목'))

        .render("{} 출원건수(상위 4개국) .html".format(bcodea))
    )

    # 2002 ~ 2021
    bpredatabyear = []
    for year in range(20):
        year = year + (datetime.today().year - 19)
        bpredatabyear.append(year)
        year = 0

    # DataFrame 생성 시 칼럼 기초값
    bpredatabyear = pd.DataFrame(data={'출원연도' : bpredatabyear})


    # 국가별 출원건수 - line그래프
    bgraphcodeb = list(bpredataa['국가코드'][0:])
    for bcodeb in bgraphcodeb:
        bcondtionb = (bgraphdata['국가코드'] == bcodeb)
        bpredatab = bgraphdata[bcondtionb]        
        bpredatab = bgraphdata[['출원연도','국가코드']]
        bpredatab = bpredatab['출원연도'].value_counts()
        bpredatab = bpredatab.reset_index()
        bpredatab.rename(columns={'index' : '출원연도', '출원연도' : '출원건수'}, inplace = True)
        bpredatab = bpredatab.sort_values(by='출원연도', ascending = True)

        #bpredatabyeara = pd.merge(bpredatabyear, bpredatab, on='출원연도', how='left')
        #bpredatabyearb = bpredatabyeara.replace(np.nan, 0, regex=True)
        #bpredatabyearc = bpredatabyearb.astype({'출원건수' : np.int64})

        mod = sys.modules[__name__]
        setattr(mod, 'data{}'.format(bcodeb), bpredatab)

        # 동적 변수 할당
        #mod = sys.modules[__name__]
        #setattr(mod, 'data{}'.format(bcodeb), bpredatabyearc)

        #기본 Bar 그래프
        basicxaxis = list(range(datetime.today().year - 20, datetime.today().year + 1))
        basicbargraph = (Bar()
                    .add_xaxis(basicxaxis)
                    .set_global_opts(xaxis_opts=opts.AxisOpts(interval = 1))
                    )
        #Line 그래프
        bline = (Line()
                .add_xaxis(xaxis_data = map(str, getattr(mod, 'data{}'.format(bpredataa['국가코드'][0]))['출원연도']))
                 .add_yaxis('',y_axis = list(getattr(mod, 'data{}'.format(bpredataa['국가코드'][0]))['출원건수']))
                 # .add_xaxis(xaxis_data = map(str, getattr(mod, 'data{}'.format(bpredataa['국가코드'][1]))['출원연도']))
                 .add_yaxis('',y_axis = list(getattr(mod, 'data{}'.format(bpredataa['국가코드'][1]))['출원건수']))
                 # .add_xaxis(xaxis_data = map(str, getattr(mod, 'data{}'.format(bpredataa['국가코드'][2]))['출원연도']))
                 .add_yaxis('',y_axis = list(getattr(mod, 'data{}'.format(bpredataa['국가코드'][2]))['출원건수']))
                 # .add_xaxis(xaxis_data = map(str, getattr(mod, 'data{}'.format(bpredataa['국가코드'][3]))['출원연도']))
                 .add_yaxis('',y_axis = list(getattr(mod, 'data{}'.format(bpredataa['국가코드'][3]))['출원건수']))
                # .add_xaxis(xaxis_data = map(str,bdataaa))
                # .add_yaxis('',y_axis = list(bdataab))
                # .add_xaxis(xaxis_data = map(str,('data{}'.format(bpredataa['국가코드'][0]))['출원연도']))
                # .add_yaxis('', y_axis = list(('data{}'.format(bpredataa['국가코드'][0]))['출원건수']))
                )

            #bline.render('test.html')
            #basicbargraph.overlap(bline).render('test.html')




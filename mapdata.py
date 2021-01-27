import pandas as pd
import numpy as np
from pyecharts.charts import Bar, Line
from pyecharts.charts import Pie
from pyecharts import options as opts

mapdata = pd.read_excel('./preprocessing.xlsx')

# 전체 출원연도별 출원건수 - Bar/Line그래프
grapha = pd.DataFrame(mapdata['출원연도'].value_counts())
grapha = grapha.reset_index()
grapha.rename(columns={'index' : '출원연도', '출원연도' : '출원건수'}, inplace = True)
grapha = grapha.sort_values(by='출원연도', ascending = True)
grapha['누적건수'] = np.cumsum(grapha['출원건수'])
# Bar그래프 작성
(Bar()
    .add_xaxis(list(grapha['출원연도']))
    .add_yaxis('', list(grapha['출원건수']))
    # .add_yaxis('범례', 값)
    # .add_xaxis / .add_yaxis 추가함으로써 막대 추가 가능
    # .set_global_opts(title_opts=opts.TitleOpts(title='제목', subtitle='소제목))
    # .render('연도별 출원건수 그래프(bar).html')
)
# Line그래프 작성 / str list로 변환하여야 함
# list_str = map(str, list_int) 사용
(Line()
    .add_xaxis(xaxis_data = list(grapha['출원연도']))
    .add_yaxis("", y_axis = list(grapha['누적건수']))
    # .render("누적건수 그래프(line).html")
)

# Bar + Line


# 국가별 출원건수 - Pie그래프, 상위 4개 국가코드 및 출원건수
graphbcode = ['KR', 'JP', 'US', 'EP']
for code in graphbcode:
    condition = (mapdata['출원국가'] == code)
    graphb = mapdata[condition]
    pregraphb = graphb['국가코드'].value_counts()
    pregraphb = pregraphb.reset_index()
    pregraphb.rename(columns={'index' : '국가코드', '국가코드' : '출원건수'}, inplace = True)
    pregraphb = pregraphb.sort_values(by='출원건수', ascending = False).head(4)
    # Pie그래프 작성
    (Pie()
        .add('',[list(a) for a in zip(pregraphb['국가코드'],pregraphb['출원건수'])])
        # .set_global_opts(title_opts=opts.TitleOpts(title='제목'))
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}")) 이건 뭔지 모르겠음.
        .render("{} 출원건수(상위 4개국) .html".format(code))
    )


# 국가별 출원건수 - 막대그래프
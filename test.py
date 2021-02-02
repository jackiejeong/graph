import pandas as pd
import sys, numpy as np
from datetime import datetime
from pyecharts.charts import Bar, Line
from pyecharts.charts import Pie
from pyecharts import options as opts


# 2번 그래프 2002 ~ 2021
bpredatabyear = []
for year in range(20):
    year = year + (datetime.today().year - 19)
    bpredatabyear.append(year)
    year = 0


# line 그래프 기본 x축 생성
basicxaxis = list(range(datetime.today().year - 20, datetime.today().year + 1))
basicbargraph = (Bar()
                        .add_xaxis(basicxaxis))


# DataFrame 생성 시 칼럼 기초값
pd.DataFrame(data={'출원연도' : bpredatabyear})
# DataFrame 왼쪽 데이터 기준으로 병합/ 값 없을 경우 Nan
pd.merge(bpredatabyear, bpredatab, on='출원연도', how='left')
# Nan을 0으로
bpredatabyear.replace(np.nan, 0, regex=True)
# float을 int로 변환
bpredatabyear = bpredatabyear.astype({'출원건수' : np.int64})
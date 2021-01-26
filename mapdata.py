import pandas as pd
import numpy as np

mapdata = pd.read_excel('./preprocessing.xlsx')

# 전체 출원연도별 출원건수 - 막대그래프
grapha = pd.DataFrame(mapdata['출원년도'].value_counts())
grapha = grapha.reset_index()
grapha.rename(columns={'index' : '출원년도', '출원년도' : '출원건수'}, inplace = True)
grapha = grapha.sort_values(by='출원년도', ascending = False)
# 막대그래프 작성

# 국가별 출원건수 - 도넛그래프, 상위 4개 국가코드 및 출원건수
graphbcode = ['KR', 'JP', 'US', 'EP']
for code in graphbcode:
    condition = (mapdata['출원국가'] == code)
    graphb = mapdata[condition]
    pregraphb = graphb['국가코드'].value_counts()
    pregraphb = pregraphb.reset_index()
    pregraphb.rename(columns={'index' : '국가코드', '국가코드' : '출원건수'}, inplace = True)
    pregraphb = pregraphb.sort_values(by='출원건수', ascending = False).head(4)
    # 도넛그래프 작성 후 저장

# 국가별 출원건수 - 막대그래프
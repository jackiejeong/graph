import pandas as pd
import numpy as np
from datetime import datetime

Rawdata = pd.read_excel('./excel.xlsx', header = 4)

Rawdata = Rawdata[['번호', '명칭', '요약', '출원인', '출원인주소', '출원인국가', '출원번호', '출원일',
'공개번호', '공개일', '등록번호', '등록일', '권리 현황', '최종 상태', '자국인용횟수', '자국피인용횟수', 'INPADOC패밀리수']]

# 출원일 필터
# condition = (Rawdata['출원일'] >= '2001')
condition = (Rawdata['출원일'] >= str(datetime.today().year - 19))

Rawdata = Rawdata[condition]

# 출원연도 추출
출원연도list = []
for date in Rawdata['출원일']:
    year = date[0:4]
    출원연도list.append(year)

# 출원연도 컬럼 추가
Rawdata.insert(7,'출원연도',출원연도list)

# NaN을 빈 칸으로 바꾸고 데이터 교체
Rawdata = Rawdata.replace(np.nan, '', regex=True)

# 자국인용횟수, 자국피인용횟수, INPACOD패밀리수 0을 빈칸으로 교체
#Rawdata.loc[Rawdata['자국인용횟수'] == 0, '자국인용횟수'] = ''
#Rawdata.loc[Rawdata['자국피인용횟수'] == 0, '자국피인용횟수'] = ''
#Rawdata.loc[Rawdata['INPADOC패밀리수'] == 0, 'INPADOC패밀리수'] = ''

# 출원국가 추출
출원국가codelist = []
for number in Rawdata['번호']:
    출원국가code = number[0:2]
    출원국가codelist.append(출원국가code)

# 컬럼 추가(순서, 컬럼이름, 값)
Rawdata.insert(0,'출원국가코드',출원국가codelist)
Rawdata.insert(0,'기술분류','')

# 출원인국가 추출
출원인국가codelist = []
for country in Rawdata['출원인국가']:
    if country:
        countries = country[0:2]
    else:
        countries = ""
    출원인국가codelist.append(countries)

# 컬럼 추가
Rawdata.insert(7,'출원인국가코드', 출원인국가codelist)
Rawdata.insert(6, '대표명화', '')
Rawdata.insert(6, '출원인정리', '')

Rawdata.to_excel('./Rawdata.xlsx')
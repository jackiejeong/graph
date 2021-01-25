import pandas as pd
import numpy as np

pre = pd.read_excel('./excel.xlsx', header = 4)

pre = pre[['번호', '명칭', '요약', '출원인', '출원인주소', '출원인국가', '출원번호', '출원일',
'공개번호', '공개일', '등록번호', '등록일', '권리 현황', '최종 상태', '자국인용횟수', '자국피인용횟수', 'INPADOC패밀리수']]

# 출원일 필터
condition = pre['출원일'] >= '2001'
pre = pre[condition]

# NaN을 빈 칸으로 바꾸고 데이터 교체
pre = pre.replace(np.nan, '', regex=True)

# 출원국가 추출
countrylist = []
for cc in pre['번호']:
    ccl = cc[0:2]
    countrylist.append(ccl)

# 컬럼 추가(순서, 컬럼이름, 값)
pre.insert(0,'출원국가',countrylist)
pre.insert(0,'기술분류','')

# 국가코드 추출
codelist = []
for cd in pre['출원인국가']:
    if cd:
        cdl = cd[0:2]
    else:
        cdl = ""
    codelist.append(cdl)

# 국가코드 컬럼 추가
pre.insert(7,'국가코드', codelist)
pre.insert(6, '대표명화', '')

pre.to_excel('./preprocessing.xlsx')
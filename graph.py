from numpy.lib.npyio import save
import pandas as pd
import sys, numpy as np
from datetime import datetime
from pyecharts.charts import Bar, Line
from pyecharts.charts import Pie
from pyecharts import options as opts
from tkinter import filedialog
from time import sleep

def Graph():
    loadpath = filedialog.askopenfilename(initialdir="/", title="엑셀 파일 선택",
                                          filetypes=(("Excel files","*.xlsx"),
                                          ("all files", "*.*")))


    savepath = filedialog.asksaveasfilename(initialdir="/", title="그래프 저장 위치 선택",
                                          filetypes=(("html files","*.html"),
                                          ("all files", "*.*")))

                                    
    ## 전처리데이터 불러오기
    Rawdata = pd.read_excel(loadpath)
    
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
    A그래프data.columns = ['출원연도', '출원건수']
    # A그래프data.rename(columns={'index' : '출원연도', '출원연도' : '출원건수'}, inplace = True)
    A그래프data = A그래프data.sort_values(by='출원연도', ascending = True)
    A그래프data['누적건수'] = np.cumsum(A그래프data['출원건수'])
    
    # 1-2, Bar 그래프
    Abar = (Bar()
            .add_xaxis(list(A그래프data['출원연도']))
            .add_yaxis('출원건수', list(A그래프data['출원건수']))
            # 보조축 생성, 간격 1000건
            .extend_axis(yaxis=opts.AxisOpts(interval = 100))
            # 레이블 삭제
            #.set_series_opts(label_opts=opts.LabelOpts(is_show=False)
            #.add_yaxis('범례', 값)
            #.add_xaxis / .add_yaxis 추가함으로써 막대 추가 가능
            #.set_global_opts(title_opts=opts.TitleOpts(title='제목', subtitle='소제목))
            )
            
    # 1-3, Line 그래프
    Aline = (Line()
            # list_str = map(str, list_int)
            .add_xaxis(xaxis_data = map(str,A그래프data['출원연도']))
            # 레이블 삭제 / 보조축 인덱스
            .add_yaxis("누적건수", y_axis = list(A그래프data['누적건수']),label_opts=opts.LabelOpts(is_show=False), yaxis_index = 1, is_smooth=True)
            )
            
    # 1-4, 최종 그래프 저장
    Abar.overlap(Aline).render('{}_전체 출원동향.html'.format(savepath))


    ## 두번째(B), 주요국 연도별 출원동향 및 점유율
    # 2-1, 데이터 정리1
    B주요국counts = Rawdata['출원국가코드'].value_counts()
    B그래프data1 = B주요국counts.reset_index()
    B그래프data1.columns = ['출원국가코드', '출원건수']
    # B그래프data1.rename(columns={'index' : '출원국가코드', '출원국가코드' : '출원건수'}, inplace = True)
    
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
        B그래프data2.columns = ['출원연도', '출원건수']
        # B그래프data2.rename(columns={'index' : '출원연도', '출원연도' : '출원건수'}, inplace = True)
        B그래프data2 = B그래프data2.sort_values(by='출원연도', ascending = True)
        B그래프data21 = pd.merge(출원연도list, B그래프data2, on='출원연도', how='left')
        B그래프data22 = B그래프data21.replace(np.nan, 0, regex=True)
        B그래프data23 = B그래프data22.astype({'출원건수' : np.int64})
        # 동적 변수 할당
        setattr(mod, 'Blinedata{}'.format(country), B그래프data23)
        
    # 2-3, Bar 그래프
    Bbar = (Bar()
            .add_xaxis(list(출원연도list['출원연도']))
            )
            
    # 2-4, Line 그래프
    Bline = (Line()
            .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
            .add_yaxis('KR' ,y_axis = list(getattr(mod, 'Blinedata{}'.format('KR'))['출원건수'])
                        , label_opts=opts.LabelOpts(is_show=False)
                        , is_smooth=True)
            .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
            .add_yaxis('US' ,y_axis = list(getattr(mod, 'Blinedata{}'.format('US'))['출원건수'])
                        , label_opts=opts.LabelOpts(is_show=False)
                        , is_smooth=True)
            .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
            .add_yaxis('JP' ,y_axis = list(getattr(mod, 'Blinedata{}'.format('JP'))['출원건수'])
                        , label_opts=opts.LabelOpts(is_show=False)
                        , is_smooth=True)
            .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
            .add_yaxis('EP' ,y_axis = list(getattr(mod, 'Blinedata{}'.format('EP'))['출원건수'])
                        , label_opts=opts.LabelOpts(is_show=False)
                        , is_smooth=True)
            )
    
    # 2-5, 그래프 출력
    Bbar.overlap(Bline)
    Bbar.overlap(Bpie).render('{}_주요국 출원동향.html'.format(savepath))
    
    
    ## 세번째(C), 주요국 내 상위 다출원국가 연도별 출원동향 및 점유율(상위 4개의 국가만 포함되므로, 출원건수 차이남)
    # 3-1, 데이터 정리1
    for country1 in 주요국:
        Ccondition1 = (Rawdata['출원국가코드'] == country1) 
        C출원국가data = Rawdata[Ccondition1] # 출원국가 필터링
        C출원국가코드counts = C출원국가data['출원인국가코드'].value_counts()
        C그래프data1 = C출원국가코드counts.reset_index()
        C그래프data1.columns = ['출원인국가코드', '출원건수']
        # C그래프data1.rename(columns={'index' : '출원인국가코드', '출원인국가코드' : '출원건수'}, inplace = True)
        C그래프data1 = C그래프data1.sort_values(by='출원건수', ascending = False).head(4)
        
    # 3-2, Pie 그래프
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
            C그래프data2.columns = ['출원연도','출원건수']
            # C그래프data2.rename(columns={'index' : '출원연도', '출원연도' : '출원건수'}, inplace = True)
            C그래프data2 = C그래프data2.sort_values(by='출원연도', ascending = True)
            C그래프data21 = pd.merge(출원연도list, C그래프data2, on='출원연도', how='left')
            C그래프data22 = C그래프data21.replace(np.nan, 0, regex=True)
            C그래프data23 = C그래프data22.astype({'출원건수' : np.int64})     
            # 동적 변수 할당 setattr
            setattr(mod, 'Clinedata{}'.format(country2), C그래프data23)
            
    # 3-4, Bar 그래프
        Cbar = (Bar()
                .add_xaxis(list(출원연도list['출원연도']))
                )
                
    # 3-5, Line 그래프
        Cline = (Line()
                .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                .add_yaxis('{}'.format(C그래프data1['출원인국가코드'][0])
                        , y_axis = list(getattr(mod, 'Clinedata{}'.format(C그래프data1['출원인국가코드'][0]))['출원건수'])
                        , label_opts=opts.LabelOpts(is_show=False)
                        , is_smooth=True)
                .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                .add_yaxis('{}'.format(C그래프data1['출원인국가코드'][1])
                        , y_axis = list(getattr(mod, 'Clinedata{}'.format(C그래프data1['출원인국가코드'][1]))['출원건수'])
                        , label_opts=opts.LabelOpts(is_show=False)
                        , is_smooth=True)
                .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                .add_yaxis('{}'.format(C그래프data1['출원인국가코드'][2])
                        , y_axis = list(getattr(mod, 'Clinedata{}'.format(C그래프data1['출원인국가코드'][2]))['출원건수'])
                        , label_opts=opts.LabelOpts(is_show=False)
                        , is_smooth=True)
                .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                .add_yaxis('{}'.format(C그래프data1['출원인국가코드'][3])
                        , y_axis = list(getattr(mod, 'Clinedata{}'.format(C그래프data1['출원인국가코드'][3]))['출원건수'])
                        , label_opts=opts.LabelOpts(is_show=False)
                        , is_smooth=True)
                )
    # 3-6, 그래프 출력
        Cbar.overlap(Cline)
        Cbar.overlap(Cpie).render('{}_{} 내 상위 다출원국가.html'.format(savepath, country1))
    
    
    ## 네번째(D), 기술분류별 출원동향 및 점유율
    # 4-1, 기술분류 두 개 이상일 경우 진행
    D기술분류list = list(Rawdata['기술분류'])
    D기술분류list중복제거 = set(D기술분류list)
    if len(D기술분류list중복제거) >= 2:
    # 4-1, 데이터 정리1 (Rawdata 기술분류 되어있어야 함)
        D기술분류counts = Rawdata['기술분류'].value_counts()
        D그래프data1 = D기술분류counts.reset_index()
        D그래프data1.columns = ['기술분류','출원건수']
        # D기술분류data.rename(columns={'index' : '기술분류', '기술분류' : '출원건수'}, inplace=True)

    # 4-2, Pie 그래프
        Dpie = (Pie()
                .add('',[list(a) for a in zip(D그래프data1['기술분류'], D그래프data1['출원건수'])]
                    , center = ['80%', '25%']
                    , radius = '40')
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b} : {d}%"))
                )

    # 4-3, 데이터 정리 2
        for classification in D그래프data1['기술분류']:
            Dcondition = (Rawdata['기술분류'] == classification)
            D분류data = Rawdata[Dcondition]
            D출원연도counts = D분류data['출원연도'].value_counts()
            D출원연도data = D출원연도counts.reset_index()
            D출원연도data.columns = ['출원연도', '출원건수']
            # D출원연도data.rename(columns={'index' : '출원연도', '출원연도' : '출원건수'}, inplace=True)
            D출원연도data = pd.merge(출원연도list, D출원연도data, on='출원연도', how='left')
            D출원연도data = D출원연도data.replace(np.nan, 0, regex=True)
            D그래프data2 = D출원연도data.astype({'출원건수' : np.int64})
            setattr(mod, 'Dlinedata{}'.format(classification), D그래프data2)

    # 4-3-1, Bar 그래프
        Dbar = (Bar()
                .add_xaxis(list(출원연도list['출원연도']))
                )

    # 4-3-2, 기술분류가 2개일 경우
        if len(D기술분류list중복제거) == 2:
            Dline = (Line()
                    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                    .add_yaxis('{}'.format(D그래프data1['기술분류'][0])
                        , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][0]))['출원건수'])
                        , label_opts=opts.LabelOpts(is_show=False)
                        , is_smooth=True)
                    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                    .add_yaxis('{}'.format(D그래프data1['기술분류'][1])
                        , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][1]))['출원건수'])
                        , label_opts=opts.LabelOpts(is_show=False)
                        , is_smooth=True)
                    )
            Dbar.overlap(Dline)

    # 4-3-3, 기술분류가 3개일 경우
        elif len(D기술분류list중복제거) == 3:
            Dline = (Line()
                    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                    .add_yaxis('{}'.format(D그래프data1['기술분류'][0])
                        , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][0]))['출원건수'])
                        , label_opts=opts.LabelOpts(is_show=False)
                        , is_smooth=True)
                    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                    .add_yaxis('{}'.format(D그래프data1['기술분류'][1])
                        , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][1]))['출원건수'])
                        , label_opts=opts.LabelOpts(is_show=False)
                        , is_smooth=True)
                    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                    .add_yaxis('{}'.format(D그래프data1['기술분류'][2])
                        , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][2]))['출원건수'])
                        , label_opts=opts.LabelOpts(is_show=False)
                    , is_smooth=True)
                    )
            Dbar.overlap(Dline)

    # 4-3-4, 기술분류가 4개일 경우
        elif len(D기술분류list중복제거) == 4:
            Dline = (Line()
                    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                    .add_yaxis('{}'.format(D그래프data1['기술분류'][0])
                            , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][0]))['출원건수'])
                            , label_opts=opts.LabelOpts(is_show=False)
                            , is_smooth=True)
                .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                .add_yaxis('{}'.format(D그래프data1['기술분류'][1])
                            , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][1]))['출원건수'])
                            , label_opts=opts.LabelOpts(is_show=False)
                            , is_smooth=True)
                .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                .add_yaxis('{}'.format(D그래프data1['기술분류'][2])
                            , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][2]))['출원건수'])
                            , label_opts=opts.LabelOpts(is_show=False)
                            , is_smooth=True)
                .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                .add_yaxis('{}'.format(D그래프data1['기술분류'][3])
                            , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][3]))['출원건수'])
                            , label_opts=opts.LabelOpts(is_show=False)
                            , is_smooth=True)
                    )
            Dbar.overlap(Dline)

    # 4-3-5, 기술분류가 5개일 경우
        elif len(D기술분류list중복제거) == 5:
            Dline = (Line()
                    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                    .add_yaxis('{}'.format(D그래프data1['기술분류'][0])
                            , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][0]))['출원건수'])
                            , label_opts=opts.LabelOpts(is_show=False)
                            , is_smooth=True)
                    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                    .add_yaxis('{}'.format(D그래프data1['기술분류'][1])
                            , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][1]))['출원건수'])
                            , label_opts=opts.LabelOpts(is_show=False)
                            , is_smooth=True)
                    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                    .add_yaxis('{}'.format(D그래프data1['기술분류'][2])
                            , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][2]))['출원건수'])
                            , label_opts=opts.LabelOpts(is_show=False)
                            , is_smooth=True)
                    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                        .add_yaxis('{}'.format(D그래프data1['기술분류'][3])
                            , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][3]))['출원건수'])
                            , label_opts=opts.LabelOpts(is_show=False)
                            , is_smooth=True)
                    .add_xaxis(xaxis_data = map(str,list(출원연도list['출원연도'])))
                    .add_yaxis('{}'.format(D그래프data1['기술분류'][4])
                            , y_axis = list(getattr(mod, 'Dlinedata{}'.format(D그래프data1['기술분류'][4]))['출원건수'])
                            , label_opts=opts.LabelOpts(is_show=False)
                            , is_smooth=True)
                    )
            Dbar.overlap(Dline)

    # 4-2-6, 그래프 출력
        Dbar.overlap(Dpie).render('{}_기술분류별 출원동향 및 점유율.html'.format(savepath))
    
    # 값이 아예 없을 경우, 에러메세지 
    else:
        pass


    ## 다섯번째(E), 주요국 내/외국인 출원건수 점유율
    # 5-1, 데이터 정리
    for country in 주요국:
        Econdition = (Rawdata['출원국가코드'] == country)
        E주요국data = Rawdata[Econdition]
        E내외국인data = E주요국data['출원인국가코드']
        E내외국인data = E내외국인data.reset_index()
        if country == 'EP':
            EP국가 = ['GR', 'NL', 'DK', 'DE', 'LV', 'RO', 'LU', 'LT', 'BE', 'BG', 'CY', 'SE', 'ES', 'SK', 'SI', 'IE', 'EE', 'GB', 'AT', 'IT', 'CZ', 'PT', 'PL', 'FR', 'FI', 'HU']
            for EP수정 in EP국가:    
                E내외국인data['출원인국가코드'] = np.where(E내외국인data['출원인국가코드'] == EP수정, 'EP', '외국인') # 다 외국인으로 수정되는 문제 발생!
            E그래프data = E내외국인data['출원인국가코드'].value_counts()
            E그래프data = E그래프data.reset_index()
            E그래프data.columns = ['내외국인','출원건수']
            setattr(mod, 'EpiedataEP', E그래프data)
        else:
            E내외국인data['출원인국가코드'] = np.where(E내외국인data['출원인국가코드'] == country, '{}'.format(country), '외국인')
            E그래프data = E내외국인data['출원인국가코드'].value_counts()
            E그래프data = E그래프data.reset_index()
            E그래프data.columns = ['내외국인','출원건수']
            setattr(mod, 'Epiedata{}'.format(country), E그래프data)

    # 5-2, Pie 그래프
    Dpie = (Pie()
            .add("한국",[list(z) for z in zip(getattr(mod, 'Epiedata{}'.format(주요국[0]))['내외국인'], getattr(mod, 'Epiedata{}'.format(주요국[0]))['출원건수'])]
                , center = ["30%", "45%"]
                , radius = '70')
            .add("일본",[list(z) for z in zip(getattr(mod, 'Epiedata{}'.format(주요국[1]))['내외국인'], getattr(mod, 'Epiedata{}'.format(주요국[1]))['출원건수'])]
                , center = ["60%", "45%"]
                , radius = '70')
            # 범례 삭제
            .set_global_opts(legend_opts=opts.LegendOpts(is_show = False))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b} : {d}%")) # 소수점 제거하던지 글씨크기를 줄이던지
            )
    Dpie.render('{}_주요국 내외국인 출원점유율_1.html'.format(savepath))

    # 5-3, Pie 그래프
    Dpie = (Pie()
            .add("미국",[list(z) for z in zip(getattr(mod, 'Epiedata{}'.format(주요국[2]))['내외국인'], getattr(mod, 'Epiedata{}'.format(주요국[2]))['출원건수'])]
                , center = ["30%", "45%"]
                , radius = '70')
            .add("유럽",[list(z) for z in zip(getattr(mod, 'Epiedata{}'.format(주요국[3]))['내외국인'], getattr(mod, 'Epiedata{}'.format(주요국[3]))['출원건수'])] # EP에 해당하는 국가 찾아서 
                , center = ["60%", "45%"]
                , radius = '70')
            # 범례 삭제
            .set_global_opts(legend_opts=opts.LegendOpts(is_show = False))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b} : {d}%")) # 소수점 제거하던지 글씨크기를 줄이던지
            )

    Dpie.render('{}_주요국 내외국인 출원점유율_2.html'.format(savepath))
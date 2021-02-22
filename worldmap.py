import json
import folium
import pandas as pd

# json 파일 불러오기
worldmap_json = json.load(open('./WorldCountries.json', encoding = 'utf-8'))

# worldmap_json['features'][0]['properties'] # {'PLACENAME': 'Svalbard'} key 확인용

# map 초기값, 중앙점, 지도유형, 줌 크기
세계지도 = folium.Map(location = [32.3468904,6.1352215], tiles = 'CartoDB dark_matter', zoom_start = 2)

# 정량분석 데이터 가져오기
정량data = pd.read_excel('./Rawdata.xlsx')
출원인국가코드counts = 정량data['출원인국가코드'].value_counts()
출원인국가코드counts = 출원인국가코드counts.reset_index()
출원인국가코드counts.columns = ['출원인국가코드', '출원건수']

# 정리된 국가코드 파일 불러오기
출원인국가코드data = pd.read_excel('./출원인국가코드.xlsx')

# 출원인국가코드 + 국가코드data
세계지도data = pd.merge(출원인국가코드counts, 출원인국가코드data, how = 'left', on = '출원인국가코드')

# 세계지도 그리기
folium.Choropleth(
    geo_data = worldmap_json,
    data = 세계지도data,
    columns = ['영문명', '출원건수'],
    fill_color = 'YlGn',
    fill_opacity = 0.7,
    line_opacity = 0.5,
    key_on = 'properties.PLACENAME').add_to(세계지도)

# 지도 경계선 그리기
def style_function(feature):
    return {
        'opacity' : 0.7,
        'weight' : 0.5, # 선 굵기
        'color' : 'white',
        'fillOpacity' : 0, # 경계선 내 색상
        'dashArray' : '5,5'
    }
folium.GeoJson(worldmap_json, style_function = style_function).add_to(세계지도)

# 세계지도 저장
세계지도.save('./세계지도.html')
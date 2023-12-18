from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import numpy as np

import pandas as pd

driver = webdriver.Chrome()
# 크롤링 결과 저장할 변수
data = pd.DataFrame(columns=['장소명', '순번', '리뷰내용'])

# visitor는 방문자리뷰, ugc(User Generated Contents)는 블로그 리뷰
# place 뒤애 있는 숫자가 네이버맵 장소 고유 번호임
place_nums = {'임랑해수욕장': 13491880, '태종대': 12079965,
              '휜여울문화마을': 37418047, '국립해양박물관': 16752569}
for place, num in zip(place_nums.keys(), place_nums.values()):
    print(place)
    url = f"https://pcmap.place.naver.com/place/{num}/review/visitor?from=map&fromPanelNum=1&x=129.26324797715085&y=35.317111761983&timestamp=202312131904&type=photoView"

    driver.get(url)
    time.sleep(1)

    # 더보기 버튼 누르기
    # 한번에 10개씩 로딩 됨
    max_iter = 200
    for i in range(max_iter):
        time.sleep(np.random.uniform(3, 5))
        try:
            driver.find_element(By.CLASS_NAME, "fvwqf").click()
        except:
            break

    html = driver.page_source

    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')

    # Find all links with the class 'j0LvW'
    reviews = soup.select('.YeINN')

    i = 1
    # 데이터 저장하는거로 바꾸기
    for review in reviews:
        if review.select_one('.zPfVt'):
            print(i, "번째 리뷰 :", review.select_one('.zPfVt').text)
            rev = review.select_one('.zPfVt').text
            data.loc[len(data)] = [place, i, rev]
            i += 1
        else:
            print(i, "번째 리뷰 :", "텍스트 리뷰 없음")

data.to_csv('Crawl_data_1214.csv')

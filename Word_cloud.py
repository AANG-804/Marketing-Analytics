from konlpy.tag import Okt
import pandas as pd

import matplotlib.pyplot as plt
from wordcloud import WordCloud

import matplotlib.font_manager as fm


# Initialize the Korean text processor
okt = Okt()

# Load data
data = pd.read_csv('./data/Crawl_data_1214.csv')
font_path = './PretendardVariable.ttf'

# 폰트 이름 가져오기
font_name = fm.FontProperties(fname=font_path).get_name()

# 폰트 설정
plt.rc('font', family=font_name)


def extract_words(text):
    # Function to extract nouns and adjectives from text
    tagged = okt.pos(text, norm=True, stem=True)
    nouns = [n for n, tag in tagged if tag in [
        'Noun'] and n not in ['굿', '굳', '좋다', '날', '태종대', '곳', '부산']]
    adjectives = [a for a, tag in tagged if tag in [
        'Adjective'] and a not in ['굿', '굳', '좋다', '있다', '없다', '그렇다']]
    return nouns, adjectives


# Group data by location
grouped_data = data.groupby('장소명')['리뷰내용'].apply(' '.join)

# Prepare word clouds for each location
word_clouds = {}

for location, reviews in grouped_data.items():
    nouns, adjectives = extract_words(reviews)
    print(location)
    # Create word clouds
    word_cloud_nouns = WordCloud(font_path=font_path,
                                 background_color='white').generate(' '.join(nouns))
    word_cloud_adjectives = WordCloud(font_path=font_path,
                                      background_color='white').generate(' '.join(adjectives))

    word_clouds[location] = (word_cloud_nouns, word_cloud_adjectives)

    plt.rc('font', family='Malgun Gothic')
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(word_cloud_nouns, interpolation='bilinear')
    plt.title(f'{location} - Nouns')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(word_cloud_adjectives, interpolation='bilinear')
    plt.title(f'{location} - Adjectives')
    plt.axis('off')

    plt.savefig(f'Wordclouds/{location}_Wordcloud.png', dpi=300)
    plt.clf()

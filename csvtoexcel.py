import pandas as pd

df = pd.read_csv('data/Crawl_data_1214.csv', index_col=0)
df.to_excel('data/크롤링결과_엑셀.xlsx')

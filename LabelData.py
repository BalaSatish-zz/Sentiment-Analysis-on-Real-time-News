import requests
import csv
import pandas as pd
import numpy as np
np.set_printoptions(threshold=np.inf)


location = ("/home/bunny/NewsAnalysisCode/uci-news-aggregator.csv")

# with open(location,mode='r')as file:
#     reader = csv.DictReader(file)
#     line_count = 0
#     for row in reader:
#         if line_count == 0:
#             print(f'column names are {", ".join(row)}')
#             line_count +=1
#         line_count +=1
#     print(f'Processed {line_count} lines.')




# pd.set_option('display.expand_frame_repr', True)
# pd.set_option('display.max_rows', 1700000)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_colwidth', -1)
# df = pd.read_csv(location, usecols=[1], names=['TITLE'])
# #print(df)
# with open('mycsv.csv','w',newline='') as f:
#     thewriter = csv.writer(f)
#     thewriter.writerow(['TITLE', 'VALUE'])
#     for i in df:
#         print (df['TITLE'])
#         thewriter.writerow([''+df['TITLE'], '0'])
para=""
response = requests.post('http://text-processing.com/api/sentiment/', data={"text":""+para})
sentiment = response.json()
print (sentiment['label'])
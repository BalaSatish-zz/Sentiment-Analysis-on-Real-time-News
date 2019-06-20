import xlrd
import csv
import pandas as pd
import numpy as np
np.set_printoptions(threshold=np.inf)


location = ("/home/bunny/NewsAnalysisCode/TwitterData.csv")

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
# df = pd.read_csv(location, usecols=[5], names=['Tweets'], header=None, encoding='latin-1')
# with open('mycsv.csv','w',newline='') as f:
#     thewriter = csv.writer(f)
#     thewriter.writerow(['Tweets', 'Values'])
#     for i in df:
#         print (df['Tweets'])
#         thewriter.writerow([''+df['Tweets'], 'NA'])
#

with open('Result.csv', 'a', newline='') as csvfile:
    fieldnames = ['Name','Link','Title','Info','Value','Sentiment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow({'Name':'thehindhu', 'Link':'URL','Title':'URL','Info':'URL','Value':'URL','Sentiment':'URL'})
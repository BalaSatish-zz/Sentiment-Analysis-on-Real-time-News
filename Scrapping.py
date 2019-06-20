import webbrowser

from bs4 import BeautifulSoup
import Process
import requests
import json
import xlrd
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import webbrowser, os

#'http://www.thehindu.com/news/national/karnataka/womens-padayatra-halted-on-way-to-vidhana-soudha/article26132653.ece'
# url ='http://www.thehindu.com/news/national/karnataka/womens-padayatra-halted-on-way-to-vidhana-soudha/article26132653.ece'
# # url = input("URL:")
# url = url.replace(" ","")
# articleid = url.replace('/','.').split('.')[-2].split('e')[1]
#
# source = requests.get(url).text
# soup = BeautifulSoup(source,'lxml')
# title = soup.find('h1',class_='title')
# intro = soup.find('h2',class_='intro')
#
# print(title.text)
# print(intro.text)
# content = soup.find('div',id="content-body-14269002-"+articleid)
# para = content.text
# para = para.replace("\n","")
# print(para)

# url2 ='https://www.deccanchronicle.com/nation/current-affairs/140219/on-last-day-of-lok-sabha-pm-modi-misses-earthquake.html'
#
# source = requests.get(url2).text
# soup = BeautifulSoup(source,'lxml')
#
# title = soup.find('h1',class_='headline')
# content = soup.find('div',id='storyBody')
# ptags = soup.find_all('p',class_='')
# finalcontent =""
# for ptag in ptags:
#     finalcontent = finalcontent + ptag.text.replace('\n','')
# print(title.text)
# print(finalcontent)
#
# url3 = 'https://economictimes.indiatimes.com/news/elections/lok-sabha/west-bengal/how-mamata-is-planning-to-checkmate-bjp-in-bengal/articleshow/68403502.cms'
# source = requests.get(url3).text
# soup = BeautifulSoup(source,'lxml')
# title = soup.find('h1',class_='clearfix title')
# para = soup.find('div',class_='Normal')
# finalcontent = para.text
# print(title.text)
# print(finalcontent)e
######################################################

loc = ("/home/bunny/NewsAnalysisCode/NewLinks.xlsx")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

sheet.cell_value(0, 0)
x = Process
for i in range(1,sheet.nrows):
    print(i)
    print(sheet.cell_value(i, 1))
    print(sheet.cell_value(i, 2))
    print(sheet.cell_value(i, 3))
    url1 = sheet.cell_value(i, 1)
    url2 = sheet.cell_value(i, 2)
    url3 = sheet.cell_value(i, 3)
    p = Process
    p.read_urls(url1,url2,url3)
    x=p
p=x
#url1='https://www.thehindu.com/news/national/kerala/two-women-under-50-enter-sabarimala-temple/article25887406.ece'
#url2='https://www.deccanchronicle.com/nation/current-affairs/241218/protesters-prevail-2-women-of-menstruating-age-turned-back-at-sabarim.html'
#url3='https://economictimes.indiatimes.com/news/politics-and-nation/two-women-below-50-claim-they-entered-keralas-sabarimala-temple/articleshow/67343872.cms'
#p = Process
#p.read_urls(url1,url2,url3)

paperslistapi,paperslist,topicslist = p.get_papers_list()
#paperslistapi = {'The Hindhu': {'probability': {'neg': 0.193145208414218, 'neutral': 0.9039921023275364, 'pos': 0.806854791585782}, 'label': 'neutral'}, 'Deccan Chronicle': {'probability': {'neg': 0.5620083759742753, 'neutral': 0.9036868682398352, 'pos': 0.43799162402572467}, 'label': 'neutral'}, 'Economic Times': {'probability': {'neg': 0.28909042097406035, 'neutral': 0.9025352409016457, 'pos': 0.7109095790259397}, 'label': 'neutral'}}
#paperslist = {'The Hindhu': {'probability': {'neg': 0.2631578947368421, 'neutral': 0.8680555555555556, 'pos': 0.7368421052631579}, 'label': 'neutral'}, 'Deccan Chronicle': {'probability': {'neg': 0.4117647058823529, 'neutral': 0.8759124087591241, 'pos': 0.5882352941176471}, 'label': 'neutral'}, 'Economic Times': {'probability': {'neg': 0.2777777777777778, 'neutral': 0.8758620689655172, 'pos': 0.7222222222222222}, 'label': 'neutral'}}
print(paperslistapi)
print(paperslist)

apiprobs=[]
papernames=[]
for papername in paperslistapi:
    papernames.append(papername)

for paper in paperslistapi:
    sentiment = paperslistapi[paper]
    probability = sentiment['probability']
    for keys in probability:
        apiprobs.append(probability[keys])

myprobs=[]

for paper in paperslist:
    sentiment = paperslist[paper]
    probability = sentiment['probability']
    for keys in probability:
        myprobs.append(probability[keys])
keyslist=['neg','pos','neutral']
AP=[]
MP=[]
for i in range(len(apiprobs)):
    AP.append(float("%.3f " %apiprobs[i]))
    MP.append(float("%.3f " %myprobs[i]))
print(AP)
print(MP)
x=[1,2,3,4,5,6,7,8,9]
plt.plot(x,AP,label="AS")
plt.plot(x,MP,label="PS")
plt.title('API-Sentiment(AS) vs Predicted-Sentiment(PS) graph')
plt.legend()
plt.savefig('/home/bunny/NewsAnalysisCode/Results/Graphs/APIvsPredicted.png')
#plt.show()
plt.close()

neglist=[]
neulist=[]
poslist=[]
for i in range(len(MP)):
    if i in [0,3,6]:
        neglist.append(MP[i])
        continue
    if i in [1,4,7]:
        neulist.append(MP[i])
        continue
    if i in [2,5,8]:
        poslist.append(MP[i])

tick_label=papernames
index = np.arange(len(neglist))
plt.bar(index,neglist,tick_label=tick_label,width=0.4,color=['grey','brown'])
plt.xlabel('Newspapers')
# naming the y-axis
plt.ylabel('Negative Probability')
# plot title
plt.title('Negative Sentiments of Newspapers')
plt.savefig('/home/bunny/NewsAnalysisCode/Results/Graphs/NegativeComparison.png')
#plt.show()
plt.close()

index = np.arange(len(poslist))
plt.bar(index,poslist,tick_label=tick_label,width=0.4,color=['grey','brown'])
plt.xlabel('Newspapers')
# naming the y-axis
plt.ylabel('Positive Probability')
# plot title
plt.title('Positive Sentiments of Newspapers')
plt.savefig('/home/bunny/NewsAnalysisCode/Results/Graphs/PositiveComparison.png')
#plt.show()
plt.close()

index = np.arange(len(neulist))
plt.bar(index,neulist,tick_label=tick_label,width=0.4,color=['grey','brown'])
plt.xlabel('Newspapers')
# naming the y-axis
plt.ylabel('Neutral Probability')
# plot title
plt.title('Neutral Sentiments of Newspapers')
plt.savefig('/home/bunny/NewsAnalysisCode/Results/Graphs/NeutralComparison.png')
#plt.show()
plt.close()
webbrowser.open('file://' + os.path.realpath('/home/bunny/NewsAnalysisCode/Results/Graphs/Graphs.html'))
# json_string = json.dumps(paperslist)
# json_string = json_string.replace()
# json_string = json_string.replace('"my_sentiment"','XXXXXXX')
# print(len(json_string))
# for string in json_string:
#     if string[0]=='p':
#         print(string)
# print(json_string)
import requests
from bs4 import BeautifulSoup
import csv

import newlda
from Classifier import Classify


class Process:
    url1=""
    url2=""
    url3=""
    paperslistapi = {}
    paperslist={}
    paralist=[]
    topicslist=[]
    sentimentList=[]
    @staticmethod
    def removeNonAscii(s):
        return "".join(i for i in s if ord(i) < 128)
    @staticmethod
    def get_papers_list():
        return Process.paperslist
    @staticmethod
    def classify_urls(URL):
        if "www.thehindu.com" in URL:
            print("The Hindu\n")
            Process.scrap_hindu(URL)
            return
        if "www.deccanchronicle.com" in URL:
            print("Deccan Chronicle\n")
            Process.scrap_deccan(URL)
            return

        if "economictimes.indiatimes.com" in URL:
            print("Economic Times\n")
            Process.scrap_economic(URL)
            return
        print("None of them")

    @staticmethod
    def html_text(p):
        soup = BeautifulSoup(p.content, 'html.parser')
        content = soup.select('h2.intro + div p, div.article-topics-container + div p')
        content_text = [tag.get_text() for tag in content]
        return "".join(content_text)

    @staticmethod
    def scrap_hindu(url):
        paper="The Hindhu"
        link=url
        title=""
        url = url.replace(" ", "")
        # articleid = url.replace('/', '.').split('.')[-2].split('e')[1]
        # source = requests.get(url).text
        # soup = BeautifulSoup(source,'lxml')
        # #titletag = soup.find('h1',class_='title')
        # intro = soup.find('h2',class_='intro')
        # #title = titletag.text
        # #print(titletag.text)
        # #print(intro.text)
        # #content = soup.find('div',id="content-body-14269002-"+articleid)
        # content = soup.find('div',class_='article-block-multiple-live-snippet')
        # para = content.text
        # Process.paralist.append(para)

        # # print(seed)
        # print("Links =" + str(len(links)))
        text = ""
        link = 'https://www.thehindu.com/news/international/new-zealand-mosque-shooting/article26541269.ece'

        page = requests.get(link)

        if (page.status_code == 200):
            text=text+(Process.html_text(page))
        else:
            text.append("404 Empty")
            print("Found 404 Error")
        para = pre_process_data(text)
        analyse_sentiment(paper,link,title,para)
        #pre_process_data(url,title,para)

    @staticmethod
    def scrap_deccan(url):
        paper="Deccan Chronicle"
        link=url
        title=""
        url = url.replace(" ", "")
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        titletag = soup.find('h1', class_='headline')
        content = soup.find('div', id='storyBody')
        ptags = soup.find_all('p', class_='')
        finalcontent = ""
        for ptag in ptags:
            finalcontent = finalcontent + ptag.text.replace('\n', '')
        title = titletag.text
        Process.paralist.append(finalcontent)
        finalcontent = pre_process_data(finalcontent)
        print(titletag.text)
        print(finalcontent)
        finalcontent = pre_process_data(finalcontent)
        analyse_sentiment(paper,link,title,finalcontent)

    @staticmethod
    def scrap_economic(url):
        paper = "Economic Times"
        link = url
        url = url.replace(" ","")
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        titletag = soup.find('h1', class_='clearfix title')
        title = titletag.text
        para = soup.find('div', class_='Normal')
        finalcontent = para.text
        Process.paralist.append(finalcontent)
        finalcontent = pre_process_data(finalcontent)
        print(title)
        print(finalcontent)
        analyse_sentiment(paper, link, title, finalcontent)

def read_urls(a,b,c):
    Process.paperslist.clear()
    Process.paperslistapi.clear()
    Process.paralist.clear()
    Process.topicslist.clear()
    Process.sentimentList.clear()

    Process.url1 = a
    Process.classify_urls(Process.url1)
    Process.url2 = b
    Process.classify_urls(Process.url2)
    Process.url3 = c
    Process.classify_urls(Process.url3)
    Process.topicslist = newlda.lda(Process.paralist)
    file = open('/home/bunny/NewsAnalysisCode/Results/Graphs/Topics.txt','w')
    for topic in Process.topicslist:
        file.write(str(""+topic+", "))
    file.close()
    with open('Results/Result.csv', 'a', newline='') as csvfile:
        fieldnameslist = ['Topics']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnameslist)
        writer.writerow({'Topics': Process.topicslist})
    with open('Results/TopicsList.csv', 'a', newline='') as csvfile:
        fieldnameslist = ['Topics', 'Sentiment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnameslist)
        writer.writerow(
            {'Topics': Process.topicslist, 'Sentiment': Process.sentimentList})

    return

def pre_process_data(para):
    para = para.lower()
    para = para.replace(u'\xa0', ' ')
    para = para.replace("\n"," ")
    para = para.replace("\t"," ")
    para = para.replace("\n", " ")
    para = para.replace("/", " ")
    para = para.replace("\\", " ")
    newsdata=""
    para = Process.removeNonAscii(para)
    for x in para:
        if x.isalpha():
            newsdata = newsdata+x
        elif x.isspace():
            newsdata = newsdata+x
        elif x=="-":
            newsdata = newsdata + " "
        elif x == "_":
            newsdata = newsdata + " "
        elif x == "–":
            newsdata = newsdata + " "
    data = newsdata
    return (data)

def analyse_sentiment(paper, link, title, para):
    response = requests.post('http://text-processing.com/api/sentiment/', data={"text": "" + para})
    sentiment0 = response.json()
    label = sentiment0['label']
    print(sentiment0)
    newtitle =""
    for x in title:
        if(x.isspace):
            newtitle = newtitle +x
        if(x.isalpha):
            newtitle = newtitle + x
    C = Classify()
    sentiment1,wholedata = C.getSentiment(para,paper)
    print(sentiment1)
    Process.paperslistapi[paper] = sentiment0
    Process.paperslist[paper]=sentiment1
    #file.write(paper)
    #print(Process.paperslist)
    sentiment = sentiment1
    with open('Results/Result.csv', 'a', newline='') as csvfile:
        fieldnameslist = ['Name', 'Link', 'Title', 'Info', 'Positive', 'Negative', 'Neutral', 'Sentiment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnameslist)
        writer.writerow(
            {'Name': paper, 'Link': link, 'Title': newtitle, 'Info': para, 'Positive': sentiment['probability']['pos'],
             'Negative': sentiment['probability']['neg'], 'Neutral': sentiment['probability']['neutral'],
             'Sentiment': sentiment['label']})
        Process.sentimentList.append(sentiment)


def get_papers_list():
    papersList = Process.paperslist
    papersListapi = Process.paperslistapi
    topicslist = Process.topicslist
    return papersListapi,papersList,topicslist
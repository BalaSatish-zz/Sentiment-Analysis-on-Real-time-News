import csv
import ast
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import webbrowser, os
csv.register_dialect('myDialect',
delimiter = ',',
skipinitialspace=True)
TopicsRows = []
SentimentsRows = []
sentimentslist=[]
with open('TopicsList.csv') as csvfile:
    readCSV = csv.reader(csvfile, dialect='myDialect')
    for row in readCSV:
        row[0] = row[0].replace('[','')
        row[0] = row[0].replace(']', '')
        row[0] = row[0].replace("'",'')
        row0 = row[0].split(',')
        TopicsRows.append(row0)
        row[1] = row[1].replace('[','')
        row[1] = row[1].replace(']', '')
        tup1 = ()
        tup1 = ast.literal_eval(row[1])
        sentimentslist.append(tup1)
    #print(sentimentslist)

    # print(Topics)
    # print(Sentiments)
TopicsList = []
TopicSentimentsList = []
for i in range(0,len(TopicsRows)):
    # print(TopicsRows[i])
    for x in TopicsRows[i]:
        TopicsList.append(x.replace(" ",''))
        TopicSentimentsList.append(sentimentslist[i])
print(len(TopicsList))
print(len(TopicSentimentsList))
#################################################Getting Unique Sentiments
UniqueTopicsList=[]
UniqueSentimentList=[]
repeatedTopics = []
for i in range(0,len(TopicsList)):
    if TopicsList[i] not in UniqueTopicsList:
        UniqueTopicsList.append(TopicsList[i])
        UniqueSentimentList.append(TopicSentimentsList[i])
    elif TopicsList[i] in UniqueTopicsList:
        repeatedTopics.append({TopicsList[i]:TopicSentimentsList[i]})
print(len(UniqueTopicsList))
print(len(UniqueSentimentList))
print(len(repeatedTopics))
count=0
rdict={}
for repeatedTopic in repeatedTopics:
    for topic in repeatedTopic:
        key = topic
        count = 0
        for repeatedTopic1 in repeatedTopics:
            # print(type(repeatedTopic1))
            for x in repeatedTopic1:
                if x==key:
                    count = count+1
            #print(repeatedTopic1)
        rdict[key]=count

for key in rdict:
    count = rdict[key]
    counter = 0
    dposprob = 0
    dnegprob = 0
    dneutralprob = 0
    eposprob = 0
    enegprob = 0
    eneutralprob = 0
    hposprob = 0
    hnegprob = 0
    hneutralprob = 0
    # print(key,count)
    sentimenttuplelist = []
    for repeatedTopic in repeatedTopics:
        for topic in repeatedTopic:
            if(key==topic):
                sentimenttuplelist.append(repeatedTopic[topic])
    #print(key,sentimenttuplelist)
    passcount = 0
    for sentimenttuple in sentimenttuplelist:
        # print(key,sentimenttuple)
        for sentiments in sentimenttuple:
            # print(key,sentiments['probability'],type(sentiments['probability']))
            singleprob = sentiments['probability']
            # print(singleprob['neg'])
            # print(singleprob['pos'])
            # print(singleprob['neutral'])
            print("/////////////////////////////////", passcount+1)
            if counter == count * passcount:
                dnegprob = dnegprob+singleprob['neg']
                dposprob = dposprob+singleprob['pos']
                dneutralprob = dneutralprob+singleprob['neutral']
            elif counter == (count * passcount)+1:
                enegprob = enegprob+singleprob['neg']
                eposprob = eposprob+singleprob['pos']
                eneutralprob = eneutralprob+singleprob['neutral']
            elif counter == (count * passcount)+2:
                hnegprob = hnegprob+singleprob['neg']
                hposprob = hposprob+singleprob['pos']
                hneutralprob = hneutralprob+singleprob['neutral']
            counter=counter+1
        passcount = passcount + 1
        print("SingleDone")
            #negprob = negprob + singleprob['neg']
        if counter == (count * 3):
            for index in range(0,len(UniqueTopicsList)):
                if(key==UniqueTopicsList[index]):
                    sentimenttuple1 =UniqueSentimentList[index]
                    # print(sentimenttuple1,type(sentimenttuple1))
                    flag = 0
                    for sentiments1 in sentimenttuple1:
                        # print(key,sentiments['probability'],type(sentiments['probability']))
                        singleprob1 = sentiments1['probability']
                        # print(singleprob['neg'])
                        # print(singleprob['pos'])
                        # print(singleprob['neutral'])
                        print("/////////////////////////////////", passcount + 1)
                        if flag == 0:
                            dnegprob = dnegprob + singleprob1['neg']
                            dposprob = dposprob + singleprob1['pos']
                            dneutralprob = dneutralprob + singleprob1['neutral']
                        elif flag == 1:
                            enegprob = enegprob + singleprob1['neg']
                            eposprob = eposprob + singleprob1['pos']
                            eneutralprob = eneutralprob + singleprob1['neutral']
                        elif flag == 2:
                            hnegprob = hnegprob + singleprob1['neg']
                            hposprob = hposprob + singleprob1['pos']
                            hneutralprob = hneutralprob + singleprob1['neutral']
                        flag=flag+1
                        #########################
                        label1 ="neg"
                        greatest = dnegprob
                        if greatest<dposprob:
                            greatest = dposprob
                            label1 = "pos"
                        if greatest<dneutralprob:
                            greatest = dneutralprob
                            label1 = "neutral"
                        ########################
                        label2 = "neg"
                        greatest = enegprob
                        if greatest < eposprob:
                            greatest = eposprob
                            label2 = "pos"
                        if greatest < eneutralprob:
                            greatest = eneutralprob
                            label2 = "neutral"
                        ########################
                        label3 = "neg"
                        greatest = hnegprob
                        if greatest < hposprob:
                            greatest = hposprob
                            label3 = "pos"
                        if greatest < hneutralprob:
                            greatest = hneutralprob
                            label3 = "neutral"
                        ########################
                        sentituple = ({'probability':{'neg':dnegprob/(count+1),'neutral':dneutralprob/(count+1),'pos':dposprob/(count+1)},'label':label1},
                                     {'probability':{'neg':enegprob/(count+1),'neutral':eneutralprob/(count+1),'pos':eposprob/(count+1)},'label':label2},
                                     {'probability':{'neg':hnegprob/(count+1),'neutral':hneutralprob/(count+1),'pos':hposprob/(count+1)},'label':label3})
                        # print(sentituple,count)
                        UniqueSentimentList[index] = sentituple
            print("Total Deccan Chronicle: ", dnegprob/(count+1), dposprob/(count+1), dneutralprob/(count+1))
            print("Total Econimic Times: ", enegprob/(count+1), eposprob/(count+1), eneutralprob/(count+1))
            print("Total The Hindu: ", hnegprob/(count+1), hposprob/(count+1), hneutralprob/(count+1))
        #print(negprob/counter,negprob,counter)
    posprob = 0
    negprob = 0
    neutralprob = 0
    passcount=0
    # counter=0
    # print("Deccan Chronicle: ", dnegprob, dposprob, dneutralprob)
    # print("Econimic Times: ", enegprob, eposprob, eneutralprob)
    # print("The Hindu: ", hnegprob, hposprob, hneutralprob)
    print("TotalDone")
print("/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
print(len(UniqueTopicsList))
print(len(UniqueSentimentList))
#######################################################################################################################################
###################### Plot Graph #################################

def plotgraph(key):
    TopicName = UniqueTopicsList[key]
    TopicSentimentsTuple = UniqueSentimentList[key]
    print(TopicName,TopicSentimentsTuple,type(TopicSentimentsTuple))
    neglist = []
    neulist = []
    poslist = []
    file = open('/home/bunny/NewsAnalysisCode/Results/TopicGraphs/Topics.txt', 'w')
    file.write(str(""+TopicName))
    file.close()
    papernames=['Deccan Chronicle','Economic Times','The Hindu']
    for papersentiment in TopicSentimentsTuple:
        paperprob = papersentiment['probability']
        print(paperprob,type(paperprob))
        for prob in paperprob:
            if prob=="neg":
                neglist.append(paperprob[prob])
            if prob=="pos":
                poslist.append(paperprob[prob])
            if prob=="neutral":
                neulist.append(paperprob[prob])
    tick_label = papernames
    index = np.arange(len(neglist))
    plt.bar(index, neglist, tick_label=tick_label, width=0.4, color=['grey', 'brown'])
    plt.xlabel('Newspapers')
    # naming the y-axis
    plt.ylabel('Negative Probability')
    # plot title
    plt.title('Negative Sentiments of Newspapers')
    plt.savefig('/home/bunny/NewsAnalysisCode/Results/TopicGraphs/NegativeComparison.png')
    # plt.show()
    plt.close()

    index = np.arange(len(poslist))
    plt.bar(index, poslist, tick_label=tick_label, width=0.4, color=['grey', 'brown'])
    plt.xlabel('Newspapers')
    # naming the y-axis
    plt.ylabel('Positive Probability')
    # plot title
    plt.title('Positive Sentiments of Newspapers')
    plt.savefig('/home/bunny/NewsAnalysisCode/Results/TopicGraphs/PositiveComparison.png')
    # plt.show()
    plt.close()

    index = np.arange(len(neulist))
    plt.bar(index, neulist, tick_label=tick_label, width=0.4, color=['grey', 'brown'])
    plt.xlabel('Newspapers')
    # naming the y-axis
    plt.ylabel('Neutral Probability')
    # plot title
    plt.title('Neutral Sentiments of Newspapers')
    plt.savefig('/home/bunny/NewsAnalysisCode/Results/TopicGraphs/NeutralComparison.png')
    # plt.show()
    plt.close()
    webbrowser.open('file://' + os.path.realpath('/home/bunny/NewsAnalysisCode/Results/TopicGraphs/TopicGraphs.html'))

while True:
    for x in range(0,len(UniqueTopicsList)):
        print(x,UniqueTopicsList[x])
    key = int(input("Select one of the Topic for Sentiment"))
    plotgraph(key)



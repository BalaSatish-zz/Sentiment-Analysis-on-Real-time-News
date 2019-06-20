import csv
import pandas as pd
import numpy as np
from nltk.corpus import stopwords

class Classify:
    def getSentiment(self,newsarticledata,paper):
        stop_words = set(stopwords.words('english'))

        np.set_printoptions(threshold=np.inf)
        path = ("/home/bunny/NewsAnalysisCode/Words/")

        Alphabets = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        print("Loading dataset")
        dataset={}
        for alphabet in Alphabets:
            file=open(""+path+"Positive/"+alphabet,"r")
            dataset["P"+alphabet] = (file.read()).lower()

        for alphabet in Alphabets:
            file=open(""+path+"Negative/"+alphabet,"r")
            dataset["N"+alphabet] = (file.read()).lower()

        #print(dataset)
        print("dataset loaded...")
        data=newsarticledata
        print("preprocessing...")
        data = data.replace("  "," ")
        data = data.replace("\n"," ")
        data = data.replace("\r", " ")
        data = data.lower()
        newdata=""
        for x in data:
            if x.isalpha():
                newdata = newdata+x
            if x.isspace():
                newdata = newdata+x
        #print(newdata)
        newsList=newdata.split(" ")
        uniqueNewsWords=[]
        for x in newsList:
            if x not in stop_words and len(x)>2 and x not in uniqueNewsWords :
                uniqueNewsWords.append(x)
        #print(uniqueNewsWords)
        print("done pre-processing...")
        print("started sentiment analysis...")
        classifiedAsP=[]
        classifiedAsN=[]
        Neutral=[]
        for x in uniqueNewsWords:
            alphabet=x[0].upper()
            positvewordslist = (dataset['P'+alphabet]).split(",")
            negativewordslist = (dataset['N'+alphabet]).split(",")
            if x in positvewordslist:
                classifiedAsP.append(x)
                continue
            if x in negativewordslist:
                classifiedAsN.append(x)
                continue
            lastchar = x[-1]
            x = x[:-1]
            if x in positvewordslist:
                classifiedAsP.append(x)
                continue
            if x in negativewordslist:
                classifiedAsN.append(x)
                continue
            Neutral.append(x+lastchar)
        paper = paper.replace(' ','')
        file = open("/home/bunny/NewsAnalysisCode/Results/NewClassifiedDetails/"+paper+".txt",'w')
        file.write(paper)
        file.write(':\n')
        file.write('Classified as Positive Words:')
        file.write(str(len(classifiedAsP)))
        file.write('\n\t')
        n=0
        for word in classifiedAsP:
            if n<10:
                file.write(word)
                file.write(',')
                n=n+1
            else:
                file.write('\n\t')
                n=0
        file.write('.\n\n\n\n')

        file.write('Classified as Negative Words:')
        file.write(str(len(classifiedAsN)))
        file.write('\n\t')
        n=0
        for word in classifiedAsN:
            if n<10:
                file.write(word)
                file.write(',')
                n=n+1
            else:
                file.write('\n\t')
                n=0
        file.write('.\n\n\n\n')


        file.write('Classified as Neutral Words:')
        file.write(str(len(Neutral)))
        file.write('\n\t')
        n=0
        for word in Neutral:
            if n<10:
                file.write(word)
                file.write(',')
                n=n+1
            else:
                file.write('\n\t')
                n=0
        file.write('.\n\n\n\n')
        file.close()
        print("analysis completed...")
        print("Classified as Positive Words:",len(classifiedAsP),classifiedAsP)
        print("Classified as Negative Words:",len(classifiedAsN),classifiedAsN)
        print("Classified as Neutral Words:",len(Neutral),Neutral)
        wholedata = "Classified as Positive Words:",len(classifiedAsP),classifiedAsP,"\n","Classified as Negative Words:",len(classifiedAsN),classifiedAsN,"\n","Classified as Neutral Words:",len(Neutral),Neutral
        poswords=len(classifiedAsP)
        negwords=len(classifiedAsN)
        neuwords=len(Neutral)
        totalposneg = poswords+negwords
        posprob = poswords/totalposneg
        negprob = negwords/totalposneg
        totalwords=poswords+negwords+neuwords
        neuprob= neuwords/totalwords
        print("Positive: ",posprob)
        print("Negaitive: ",negprob)
        print("Neutral: ",neuprob)
        sentimentlist ={}
        sentimentlist['neg']=(negprob)
        sentimentlist['neutral']=(neuprob)
        sentimentlist['pos']=(posprob)
        key = 0
        keyname=""
        for x,y in sentimentlist.items():
            if y > key:
                key = y
                keyname = x
        sentiment={
            'probability':{'neg':negprob,
                           'neutral':neuprob,
                           'pos':posprob},
            'label':keyname
        }
        return sentiment,wholedata
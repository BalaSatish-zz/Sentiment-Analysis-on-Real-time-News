import csv
import pandas as pd
import numpy as np



np.set_printoptions(threshold=np.inf)
path = ("/home/bunny/NewsAnalysisCode/")

Alphabets = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

for filename in Alphabets:
    textLocation = path+"Words/Positive/"+filename+""
    csvLocation = path+"WordsCSV/Positive/"+filename+".csv"
    with open(textLocation,'r') as textfile:
        data = textfile.read()
        wordsList = data.split(",")
        with open(csvLocation,'w',newline='')as f:
            thewriter = csv.writer(f)
            thewriter.writerow(['Words', 'Value','Occurrences'])
            for word in wordsList:
                thewriter.writerow([''+word, '4','0'])
        print(filename+": Successful")


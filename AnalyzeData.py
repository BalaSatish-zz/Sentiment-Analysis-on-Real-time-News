import csv
import pandas
import numpy


NewsData = input("Input the String Data:")

def preProcessData(Data):
    print("\n\n\nCleaning Data....\n")
    for x in Data:
        if(x.isalpha() or x.isspace()):
            Data
        else:
            Data = Data.replace(x,'')
    Data = Data.lower()
    return Data

NewsData = preProcessData(NewsData)
WordsList = NewsData.split(" ")
print(WordsList)
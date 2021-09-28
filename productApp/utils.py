import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import  cosine_similarity
from sklearn.feature_extraction.text import  CountVectorizer



    

def createDataset(data):
    columns =[]
    for p in data:
        row = []
        for key in p:
            row.append(p[key])
    columns.append(row)

    dataset = pd.DataFrame(columns,columns=list(data[0].keys()))
    dataset.to_csv('products.csv')

def addProduct(data):
    try:
        dataset = pd.read_csv('products.csv')
        dataset[dataset.size[0]] = data
        dataset.to_csv('products.csv')
    except FileNotFoundError:
        dataToCreate = []
        dataToCreate.append(data)
        createDataset(dataToCreate)
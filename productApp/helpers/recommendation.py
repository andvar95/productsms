import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import  cosine_similarity
from sklearn.feature_extraction.text import  CountVectorizer
from django.forms.models import model_to_dict




def getDict(data):
    try:
        data = model_to_dict(data)
    except AttributeError:
        data = data
    return data


def getRow(data):
    row = []
    p =getDict(data)
    for key in p:
        row.append(p[key])
    return row    

def createDataset(data):
    columns =[]
    for p in data:
        row = getRow(getDict(p))
        columns.append(row)
    dataset = pd.DataFrame(columns,columns=list(getDict(data[0]).keys()))
    dataset.to_csv('products.csv',index=False)
    get_important_features()

def addProduct(data):
    data = getDict(data)
    try:
        dataset = pd.read_csv('products.csv')
        dataset.loc[dataset.shape[0]] = getRow(data)
        dataset.to_csv('products.csv',index=False)
        get_important_features()
    except FileNotFoundError:
        dataToCreate = []
        dataToCreate.append(data)
        createDataset(dataToCreate)

def get_important_features():
    dataset = pd.read_csv('products.csv')
    columns = ['name','price','category','in_stock']
    important_features = []
    #print(dataset)
    for i in range(0,dataset.shape[0]):
        data = ""
        for col in columns:
            data += str(dataset[col][i])+" "
        important_features.append(data[:len(data)-1])
    #print(important_features)
    generateSimilarityMatrix(important_features)


def generateSimilarityMatrix(data):
    cm = CountVectorizer().fit_transform(data)
    cs = cosine_similarity(cm)
    print(cs)
    np.savetxt('cs.txt',cs)
  

def modifySimilarityMatrix(name):
    cs = np.loadtxt('cs.txt')
    dataset = pd.read_csv('products.csv')
    productId = dataset[dataset.name == name].index[0]
    #print(productId)
    scores = list(enumerate(cs[productId]))
    sorted_scores = sorted(scores, key = lambda x:x[1],reverse=True)
    j= 0
    id = []
    for item in sorted_scores:
        name = dataset.loc[item[0]]['name']
        id.append(dataset.loc[item[0]]['id'])
        #print("{}-{}".format(j,name))
        j +=1
        if j==5:
            break
    
    return id
  
    



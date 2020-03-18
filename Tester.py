import random
import time
import json
import os
import glob
import pprint
import pandas as pd
from random import sample
from random import randint
from random import randrange
from ArticleNode import ArticleNode
from GetArticles import GetArticles
from MultiwayTree import multiwayTree

class Tester:
    def __init__ (self,n):
         self.numberOfNodes = n
         keywords= pd.read_csv("adhoc_wordlist.csv")
         df = pd.DataFrame(keywords)
         keywordList = df[["KEYWORDS"]].values.tolist()
         keywordList = [j[0] for j in keywordList]
         keywordList = [x.lower() for x in keywordList]
         keywordList = [x.strip() for x in keywordList]
         self.keywordList = keywordList

         self.maxReferencesPerNode = 35

    def assignDummyKeyWords(self,node):   
        # Dummy nodes need Keywords
        numberOfKeywords = random.randint(1,len(self.keywordList))
        for i in range(numberOfKeywords):
            node.keywordList.append(random.choice(self.keywordList))
        node.keywordList= list(set(node.keywordList))

    def assignDummyReferences(self,node):
        numberOfReferences =  randrange(self.maxReferencesPerNode)
        for i in range(numberOfReferences):
            node.references.append(random.randint(1,self.numberOfNodes))

    def generateDummyNodes(self):
        nodeList = []
        for i in range(1,(self.numberOfNodes+1)):
            newNode = ArticleNode(i,"a")
            nodeList.append(newNode)
            self.assignDummyKeyWords(newNode)
            self.assignDummyReferences(newNode)
        return nodeList

    def realNodeSearchTest(self,numberOfSearches):
        # #Initialize and preprocess data from GetArticles.py
        print("Processing Articles:")
        generator = GetArticles()
        articles = generator.getArticles()
        nodeList = list(articles.values())
        count = 0
        for node in nodeList:
            node.articleID = int(node.articleID)
            node.references = [int(article) for article in node.cited]
            node.keywordList = list(node.keywordDict.values())


        #Initialize DataStructure
        tree = multiwayTree(nodeList)

        #Search parameters
        numberOfTestSearches = 3
        count = 0
        successfulSearches=[]
        for i in range(numberOfTestSearches):
            
            #numberOfKeywords = random.randint(1,len(tree.keywords))
            numberOfKeywords = 3
            #searchList = sample(tree.keywords,numberOfKeywords)
            searchList = ['social','media','social media','social-media']
            searchResults = tree.keyWordSearch(searchList)
            startTime = time.time()
            tree.keyWordSearch(searchList)
            # print("Search time: %s seconds" % (time.time() - startTime))
            # print("SearchList: ",searchList)
            # print("Search Qualified Articles :", len(searchResults))
            # print("Articles in keywords:-")
            # for keyword in searchList:
            #     print(keyword,": ", len(tree.nodeDictionary[keyword].successors))
            if(len(searchResults)>0) : 
                count+=1
                successfulSearches.append(searchList)
            print (searchResults)

        categorizedArticles= 0
        for keyword in tree.keywords:
            categorizedArticles+=len(tree.nodeDictionary[keyword].successors)
        unnecessary = tree.subcategories + tree.categories
        identifiedKeywords = set(tree.keywords) - set(unnecessary)
        #print("All keywords identified: \n", set(identifiedKeywords))
        print("Number of Categorized Articles = ",categorizedArticles,"/",len(nodeList))
        print("Number of Successful Searches: ", count)


    def keywordExistanceCheck(self):
        def intersection (list1,list2):
            return list(set(list1) & set(list2))
        #Convert keywords in adhoc_wordlist.csv into lowercase list of keywords
        # access abstracts of each of the downloaded .json files and check for keywords
        path = '/Users/AgNI/Documents/Capstone/2018-10-25'
        count = 0 
        dead_abstracts = 0
        search = ['social','media','social-media', 'social media']
        for filename in glob.glob(os.path.join(path, '*.json')): #only process .JSON files in folder.      
            with open(filename, encoding='utf-8', mode='r') as currentFile:
                data=currentFile.read().replace('\n', '')
                words = json.loads(data)["abstract"]
                words = words.split()
                words = [x.strip() for x in words]
                words = [x.lower() for x in words]
                words = set(words)
                match = len(intersection(words,set(search)))
                if len(words) == 0:
                    dead_abstracts+=1
                if match>0 :
                    count+=1
        print(count)
            #print(list(intersection(words,keywordList)))
    def keywrodCSVCheck(self):
        df = pd.read_csv("keywords.csv")
        print(df['article_count'].sum())
        
    def dummyNodeSearchTest(self,numberOfSearchTerms):

        # Generate Dummy Nodes
        #startTime = time.time()
        nodeList = self.generateDummyNodes()

        #Initialize multiway Tree
        tree = multiwayTree(nodeList)

        #Conduct search and print metrics
        numberOfSearchTerms = random.randint(1,len(self.keywordList))
        searchList = sample(self.keywordList,numberOfSearchTerms)

        #startTime = time.time()
        searchResults = tree.keyWordSearch(searchList)    
        return searchResults
        
tester = Tester(10000)
output = tester.dummyNodeSearchTest(5)
print (output)
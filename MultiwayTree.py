from ArticleNode import ArticleNode
from DummyNode import DummyNode
import random
from collections import deque
import time
from random import randrange
from random import sample
import pandas as pd

class multiwayTree:
    def __init__ (self,nodeList):
        self.root = ArticleNode(0,"Root")
        
        self.nodeDictionary = {
            0:self.root
        } 
        self.authorDictionary = {

        }    
        self.numberOfSubtrees = 0       
        self.categoryDict,self.categories,self.subcategories = self.createCategoryDict()
        self.keywords = self.categories + self.subcategories
        self.nodeList = nodeList
        
        self.addCategoryNodes()
        self.addSubcategoryNodes()
        self.initializeNodeDictionary()
        self.assignSubTrees()
        self.establishNodeRelationships()

    def intersection(self,list1, list2):
        return set(list1).intersection(set(list2))

    def createCategoryDict(self):
        dataFrame = pd.read_csv("scimago_categories_then_areas.csv")
        dataFrame = dataFrame.drop(columns= ['Code'])
        dataFrame = dataFrame.drop(index =[0,1])
        dataFrame = dataFrame.reset_index()
        dataFrame = dataFrame.drop(columns = ['index'])
        dataFrame.columns = ['Subcategory', 'Category']
        dataFrame = dataFrame[['Category', 'Subcategory']]
        prev = dataFrame.iloc[0]
        current = dataFrame.iloc[0]
        subcategories = []
        categoryDict = {}

        for i in range(len(dataFrame)):
            current = dataFrame.iloc[i]
            if (prev['Category'] == current['Category']):
                subcategories.append(current['Subcategory'])
            else:
                categoryDict[prev['Category']] = subcategories
                subcategories = []
                subcategories.append(current['Subcategory'])
            prev = current
        
        categoryDict[prev['Category']] = subcategories
        categories =list(categoryDict.keys())
        subcategories = []
        for key in categoryDict:
            for category in categoryDict[key]:
                subcategories.append(category.lower())
        

        return categoryDict,categories,subcategories
    
    def addCategoryNodes(self):
        for category in self.categories:
            self.nodeDictionary[category] = ArticleNode(aid = -self.numberOfSubtrees,name = category)
            self.nodeDictionary[category].predecessors = self.root
            self.root.successors.append(self.nodeDictionary[category]) 
            self.numberOfSubtrees += 1
        

    def addSubcategoryNodes(self):
        for subcategory in self.subcategories:
            self.nodeDictionary[subcategory] = ArticleNode(-self.numberOfSubtrees,subcategory)
            self.nodeDictionary[subcategory].predecessors = self.root
            self.root.successors.append(self.nodeDictionary[subcategory]) 
            self.numberOfSubtrees+=1
        
        
    
    def initializeNodeDictionary(self):
        
        #Create Category and subCategory Nodes

        for node in self.nodeList:          
            self.nodeDictionary[node.articleID] = node 

            #Authors Initialized in self.authorDictionary
            for author in node.authorList:
                node.authorList = node.authorList.lower()
            authors = node.authorList
            # no need to check if author already exists or not because dict[a] is created if not already present.
            for author in authors:
                self.nodeDictionary[author].append(node)
        
            for keyword in node.keywordList:

                if (keyword not in self.keywords):
                    self.numberOfSubtrees = self.numberOfSubtrees + 1
                    self.keywords.append(keyword)
                    self.nodeDictionary[keyword] = ArticleNode(-self.numberOfSubtrees,keyword)
                    self.nodeDictionary[keyword].predecessors = self.root
                    self.root.successors.append(self.nodeDictionary[keyword])            
    
    def assignSubTrees(self):
        for i in range(1,len(self.nodeList)):
            for keyword in self.nodeDictionary[i].keywordList:
                self.nodeDictionary[keyword].successors.append(self.nodeDictionary[i])
                self.nodeDictionary[i].subTreePredecessors.append(self.nodeDictionary[keyword]) 
    
    def establishNodeRelationships(self):
        for i in range(1,len(self.nodeDictionary)-self.numberOfSubtrees):
            for reference in self.nodeDictionary[i].references:
                if(reference <= (len(self.nodeDictionary)-self.numberOfSubtrees)):
                    self.nodeDictionary[i].successors.append(self.nodeDictionary[reference])
                    self.nodeDictionary[reference].predecessors.append(self.nodeDictionary[i])

    def printRelations(self):
        print ("Successors: ")
        count = 1
        for i in range(1,len(self.nodeDictionary)-self.numberOfSubtrees):
            print ("element ",count, ": ", end = '')
            count+=1
            for successor in self.nodeDictionary[i].successors:
                print(successor.articleID,end = ' ')
            print()

        count = 1
        print ("\n\nPredecessors:")
        for i in range(1,len(self.nodeDictionary)-self.numberOfSubtrees):
            print ("element ",count, ": ", end = '')
            count+=1
            for predecessor in self.nodeDictionary[i].predecessors:
                print(predecessor.articleID,end = ' ')
            print()   
    
    def keyWordSearch(self,searchList):
        min = len(self.nodeDictionary)
        searchTree = None

        #find the smallest subTree
        for keyword in searchList:
            if(len(self.nodeDictionary[keyword].successors)<min):
                min = len(self.nodeDictionary[keyword].successors)
                searchTree = self.nodeDictionary[keyword]

        #remove subtree from searchlist
        searchList.remove(searchTree.name)  
        searchOutput = []
        for successor in searchTree.successors:
            if(set(searchList).issubset(set(successor.keywordList))):
                searchOutput.append(successor.articleID)
        
        categoryCountDict={}
        searchArticlesInCurrentCategory=[]
        for category in self.categories:
            searchArticlesInCurrentCategory = self.intersection(self.nodeDictionary[category].successors,searchOutput)
            categoryCountDict[category] = list(searchArticlesInCurrentCategory)
            searchArticlesInCurrentCategory = []
        return categoryCountDict

    def subCategorizer(self,aidList):
        subcategory_dict={}
        searchArticlesInCurrentCategory = []
        for subcategory in self.subcategories:
            searchArticlesInCurrentCategory = self.intersection(self.nodeDictionary[subcategory].successors,aidList)
            subcategory_dict[subcategory] = list(searchArticlesInCurrentCategory)
            searchArticlesInCurrentCategory = []
        return subcategory_dict

    
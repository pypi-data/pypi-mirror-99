#!/usr/bin/env python

__author__ = "Tom Zastrow"
__copyright__ = "Copyright 2020, Tom Zastrow"
__credits__ = ["Tom Zastrow"]
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "Tom Zastrow"
__email__ = "thomas.zastrow@mpcdf.mpg.de"
__status__ = "Development"

import os

class Token(object):
    def __init__(self, token, lemma, pos, dep, shape, isAlpha, isStop):
        self.token = token
        self.lemma = lemma
        self.pos = pos
        self.dep = dep
        self.shape = shape
        self.isAlpha = isAlpha
        self.isStop = isStop
    
    def display(self):
        print(self.token, self.lemma, self.pos, self.dep, self.shape, self.isAlpha, self.isStop)

class Sentence(object):
    def __init__(self):
        self.tokens =  []

    def display(self):
        for t in self.tokens:
            t.display()

    def displayAsTokens(self):
        for t in self.tokens:
            print(t.token, end=" ")
        print()

    def toString(self, annotation):
        temp = ""

        if annotation == "token":
            for t in self.tokens:
                temp = temp + t.token + " "

        if annotation == "lemma":
            for t in self.tokens:
                temp = temp + t.lemma + " "

        if annotation == "pos":
            for t in self.tokens:
                temp = temp + t.pos + " "

        temp = temp[:-1]
        return temp


class Article(object):
    def __init__(self, id, url, title):
        self.id = id
        self.url = url
        self.title = title
        self.sentences = []

    def display(self):
        print("ID: ", str(self.id))
        print("Title: ", str(self.title))
        print("URL: ", str(self.url))
        print()
        for s in self.sentences:
            s.display()


class Subcorpus(object):
    def __init__(self):
        self.articles = []  
        self.statistics = {}  

    def read (self, infile):
        f = open(infile, "r")
        lines = f.readlines()
        f.close()

        for line in lines:
            if line.startswith("<doc id=\""):
                rec = line.split("\" ")
                id = int(rec[0].replace("<doc id=\"", ""))
                url = rec[1].replace("url=\"", "")
                title = rec[2].replace("title=\"", "").replace("\">", "").strip()
                a = Article(id, url, title) 
            elif line.startswith("</doc>"):
                self.articles.append(a)
              
            elif line.startswith("<s>"):
                s = Sentence()
            elif line.startswith("</s>"):
                a.sentences.append(s)
            else:
                rec = line.strip().split("\t")
                if len(rec) != 7:
                    print("PASST nicht:", line)
                else:
                    t = Token(rec[0],rec[1],rec[2],rec[3],rec[4],rec[5],rec[6])
                    s.tokens.append(t)
        
        self.statistics["articles"] = len(self.articles)
        self.statistics["sentences"] = 0
        self.statistics["tokens"] = 0
        for a in self.articles:
            self.statistics["sentences"] = self.statistics["sentences"] + len(a.sentences)
            for s in a.sentences:
                self.statistics["tokens"] = self.statistics["tokens"] + len(s.tokens)


class Corpus(object):
    def __init__(self, basePath):
        self.basePath = basePath

    def getSubcorpora(self):   
        liste = []
        for root, dirs, files in os.walk(self.basePath):
                path = root.split('/')
                for file in files:
                    liste.append(os.path.join(root, file))
        return liste

    def getSubcorporaSlices(self, n):
        liste = self.getSubcorpora()
        n = max(1, n)
        return (liste[i:i+n] for i in range(0, len(liste), n))

    def getFolders(self):
        return [d for d in os.listdir(self.basePath) if os.path.isdir(os.path.join(self.basePath, d))]



    def getFolderPartitions(self, n):
        folders = self.getFolders()
        n = int(len(self.getFolders()) / n)
        n = max(1, n)
        return (folders[i:i+n] for i in range(0, len(folders), n))


if __name__ == "__main__":
    print("These are the objects for the wp-toolbox, call them from your own applications!")


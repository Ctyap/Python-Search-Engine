from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import RegexpTokenizer
import re
from nltk.stem.snowball import PorterStemmer
from collections import Counter
from urllib.request import urlopen
import requests

words = dict()

class Document:
    def __init__(self, json):
        self.content = json['content']
        self.encoding = json['encoding']
        self.url = json['url']
        self.stem = PorterStemmer()
        self.wordCount = 0
        
        self.body = list()
        self.headers1 = list()
        self.headers2 = list()
        self.headers3 = list()
        self.bold = list()
        #self.titles = list()

        
    def getURL(self):
        return self.url
    
    def extractData(self):
        html_content = self.content      
        
        soup = BeautifulSoup(html_content,"html.parser")
                
        tokenizer = RegexpTokenizer(r'\w+')

        #Text between the body tags
        bodyText = soup.find_all("body")
        
        #print(str(bodyText))
        
        #Text in bold (b, strong) are important
        boldText = soup.find_all("b") + soup.find_all("strong")
        
        #Text in headings (h1) are important
        headerText1 = soup.find_all("h1")
        
        #Text in headings (h2) are important
        headerText2 = soup.find_all("h2")
        
        #Text in headings (h3) are important
        headerText3 = soup.find_all("h3")
        
        #title = soup.find_all("title")


        
        
        
        for line in bodyText:
            for term in tokenizer.tokenize(line.text):
                if term.isalnum() and self.isEnglish(term):
                    self.wordCount +=1
                    self.body.append((self.stem.stem(term.lower())))
                    

                     
        for line in boldText:
            for term in tokenizer.tokenize(line.text):
                if term.isalnum() and self.isEnglish(term):
                    self.wordCount +=1
                    self.bold.append((self.stem.stem(term.lower())))

        
        for line in headerText1:
            for term in tokenizer.tokenize(line.text):
                if term.isalnum() and self.isEnglish(term):
                    self.wordCount +=1                    
                    self.headers1.append((self.stem.stem(term.lower())))

        for line in headerText2:
            for term in tokenizer.tokenize(line.text):
                if term.isalnum() and self.isEnglish(term):
                    self.wordCount +=1                   
                    self.headers2.append((self.stem.stem(term.lower())))


        for line in headerText3:
            for term in tokenizer.tokenize(line.text):
                if term.isalnum() and self.isEnglish(term):
                    self.wordCount +=1                   
                    self.headers3.append((self.stem.stem(term.lower())))
                    
        """
        for line in title:
            for term in tokenizer.tokenize(line.text):
                if term.isalnum() and self.isEnglish(term):
                    self.wordCount +=1                   
                    self.titles.append((self.stem.stem(term.lower())))
        """
    
    def extractTermFreq(self):
        #Converts each list into dictionary: term as key and how many times it appeared in the list as value.
            
        bodyCount = Counter(self.body)
        
        headerCount1 = Counter(self.headers1)
        headerCount2 = Counter(self.headers2)
        headerCount3 = Counter(self.headers3)

        boldCount = Counter(self.bold)
        
        #titleCount = Counter(self.titles)
        
        
        
        return (bodyCount, headerCount1, headerCount2, headerCount3, boldCount, self.wordCount)
    
    
    def isEnglish(self, term):
        try:
            term.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True
        
        
        
        
     
        
        
        
        

        






    

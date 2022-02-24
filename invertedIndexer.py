import os
from bs4 import BeautifulSoup
from collections import Counter
import Document
import nltk
import json
from Posting import Posting
from nltk.tokenize import RegexpTokenizer
import pickleIndex
import validators
from urllib.parse import urldefrag



def create_index(dev_folder):
    urls = set()
    
    #Create dictionary that stores postings
    index = dict()
    
    #Iterate through directory
    count = 0

    for (root, dirs, files) in os.walk(dev_folder):
        
        #name -> 906c24a2203dd5d6cce210c733c48b336ef58293212218808cf8fb88edcecc3b.json
        for name in files:
            
            #Create doc that is accessible to create soup object
            #A path-like object representing a file system path.
            doc = os.path.join(root, name)

            with open(doc) as j:
                
                #The json.load() is used to read the JSON document from file and The json.loads() is used to convert the JSON String document into the Python dictionary.
                data = json.load(j)
                
                url = data['url']
                
                pure_url, frag = urldefrag(url)

                #Check for broken html links and removes duplicates

                if pure_url not in urls and validators.url(pure_url):
                    
                    urls.add(pure_url)
                    
                    document = Document.Document(data)
                    
                    document.extractData()
                    
                    docURL = document.getURL()
                    
                    bodyCount, headerCount1, headerCount2, headerCount3, boldCount, docWordCount = document.extractTermFreq()
                    
                    index_tokens(docURL, doc, index, bodyCount, headerCount1, headerCount2, headerCount3, boldCount, docWordCount, count)
                else:
                    continue
                
                
                #index.update(updated_index)
                """
                for k,v in index.items():
                    for post in v:
                        print("Term[ {} ]: {}".format(k,post))
    
                """
            count+=1
            print("Completed Doc {}".format(count))
            # sortedList = sorted(index.items(), key=lambda x: (x[0]))
            # for i in sortedList[0:10]:
            #     print(i)

    return index, count
                    

                
def index_tokens(URL, doc, index, bodyCount, headerCount1, headerCount2, headerCount3, boldCount, docWordCount, count):
    
    iterateDicCounts(URL, doc, index, bodyCount, 1, docWordCount, count)#1
    iterateDicCounts(URL, doc, index, headerCount1,4, docWordCount, count)#4
    iterateDicCounts(URL, doc, index, headerCount2,3, docWordCount, count)#3
    iterateDicCounts(URL, doc, index, headerCount3, 2, docWordCount, count)#2
    iterateDicCounts(URL, doc, index, boldCount, 1.5, docWordCount, count)#5
    #iterateDicCounts(URL, doc, index, titleCount, 5, docWordCount, count)

    



def iterateDicCounts(URL, doc, index, count_dict, importance, docWordCount, count):
    
    for token, freq in count_dict.items():
        
        new_posting = Posting(doc, count, URL)
        
        new_posting.termFreq = freq
        new_posting.wordCount = docWordCount
        new_posting.calc_TF()
        
        if importance == 1:
            new_posting.important = 1
        elif importance == 4:
            new_posting.important = 4
        elif importance == 3:
            new_posting.important = 3
        elif importance == 2:
            new_posting.important = 2
        else:
            new_posting.important = 1.5
            #new_posting.important = 5
        
        
        if token not in index:
            index[token] = set()
            
            index[token].add(new_posting)

        else:

            index_copy = index[token].copy()
             
            if len(index_copy) == 0:
                index[token].add(new_posting)
            else:

                if any(post.docID == new_posting.docID for post in index_copy):
                    for post in index_copy:
                        if post.docID == new_posting.docID:
                            post.termFreq = new_posting.termFreq + post.termFreq
                            post.important += new_posting.important
                            post.calc_TF()
    
    
                else:
                    index[token].add(new_posting)


    

def pickleIt(index, saved_folder, filename):
    return pickleIndex.pickleIndex(index, saved_folder, filename)
     
def createReport(index, count):
    saved_path = "C:\\Users\\coope\\OneDrive\\Desktop\\invertedIndex\\report.txt"
    
    with open(saved_path, 'wb') as file:
        print("Total Docs: {}\n".format(count))
        #file.write("Total Docs: {}\n".format(count))
        print("Number of unique tokens: {}\n".format(len(index)))
        #file.write("Number of unique tokens: {}\n".format(len(index)))
        #file.write("TABLE:")
        print("TABLE: ")
        #file.write("TERM   |   DOCUMENT FREQUENCY   | (doc-ID, Term Frequency) ")
        print("TERM   |   DOCUMENT FREQUENCY   | (doc-ID, Term Frequency) ")
        for token, set_of_postings in index.items():
            postings = [(post.docID, post.termFreq) for post in set_of_postings]
            no_postings = len(postings)

            table = token + ' ' + str(no_postings) + ': ' + str(postings) + '\n'
            
            file.write(table.encode('utf-8'))
    


if __name__ == '__main__':
    #C:\Users\coope\OneDrive\Desktop\DEV
    #C:\Users\coope\OneDrive\Desktop\DEV2

    saved_folder= "C:\\Users\\coope\\OneDrive\\Desktop\\invertedIndex"
    # assignment3\DEV
    filename = 'assignment3'
    
    while True:
        dev_folder = input("Enter name of directory: ")
         
        if not os.path.exists(dev_folder):
            print("{} does not exist.".format(dev_folder))
        else:
            index, count = create_index(dev_folder)
            
            """
            for i,v in sorted(index.items(), key=lambda item: (item[0])):
                for post in v:
                    print("Term[ {} ]: {}".format(i,post))
            """
            
            pickleIt(index, saved_folder, filename)
            #createReport(index, count)

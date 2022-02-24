"""unpickle, read, search"""
import math
import pickle
import nltk
from nltk.stem.snowball import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import words
from collections import defaultdict
import sys
import re
from regex.regex import search
from time import perf_counter

#List that includes all English stop words to be skipped when tokenizer -- refers to Question 3.
stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as",
             "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't",
             "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
             "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
             "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
             "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
             "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of",
             "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
             "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than",
             "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
             "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under",
             "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
             "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's",
             "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
             "yourself", "yourselves"]





# def unpickleIndex(index, full_path, filename):
def unpickleIndex(full_path, userInput):
    #print("Entered pickled")
    
    filename = "assignment3.pickle"
    
    dict = defaultdict(set)

    
    for token in userInput:
        updatedFilename = token[0] + filename

        final_full_path = full_path + '\\' + updatedFilename
        
        
        with open(final_full_path, 'rb') as pickle_file:
            try:
                while True:
                    index = pickle.load(pickle_file)
                
                    for word, setPostings in index.items():
                        if token == word:
                            dict[token] = setPostings
                            break
                    break
        
            except EOFError:
                print("{} doesn't exist.".format(token))
                pass


    #print("Successsfully pickled")
    
    '''
    for k, v in dict.items():
        print(k)
        for post in v:
            print(post.URL)
    '''
    
    return dict
    

def buffer(path, fileName):
    # this dummy dict is for testing purposes; mocks the pickle file of dictionaries
    # dictionary with the token as the key and a set of posting objects where that key was found
    dummy_dict = {
                'token1': {"set", "of", "posting", "1"}, 'token2': {"set", "of", "posting", "2"},
                'token3': {"set", "of", "posting", "3"}, 'token4': {"set", "of", "posting", "4"},
                'token5': {"set", "of", "posting", "5"}, 'token6': {"set", "of", "posting", "6"},
                'token7': {"set", "of", "posting", "7"}, 'token8': {"set", "of", "posting", "8"},
                'token9': {"set", "of", "posting", "9"}, 'token10': {"set", "of", "posting", "10"},
                'token11': {"set", "of", "posting", "11"}, 'token12': {"set", "of", "posting", "12"}
    }

    """UNCOMMENT THESE TWO LINES BELOW WHEN NOT TESTING"""
    fullPath = path + "\\" + fileName
    realPickleFile = open(fullPath, 'rb')

    # """create a file to read from"""
    # dummyPickleFile = open('dummyTextFile', 'w')

    # for k, v in dummy_dict.items():
    #     dummyPickleFile.write(str(v))
    # dummyPickleFile.close()
    #
    # """open the file to read"""
    # dummyPickleFile = open('dummyTextFile', 'r')


    buf = []
    while True:
        # To find the size of a dictionary in bytes we can use the getsizeof() function of the sys module.
        # total_size_dummy_dict = sys.getsizeof(dummy_dict)
        # print(total_size_dummy_dict)
        # for k, v in dummy_dict.items():
        #     print("size of " + k + "'s set: " + str(sys.getsizeof(k)) + ": " + str(sys.getsizeof(dummy_dict[k])))

        # bytes_to_read = sys.getsizeof(1024)
        print(sys.getsizeof(realPickleFile))
        line = realPickleFile.readline(100) # INSERT HOW MANY BYTES YOU WANT TO READ HERE i.e the size of the next n sets to read)
        print(line)
        # break
        if not line:
            break
        buf.append(line)
        # if line.endswith('.\n'):
        #     print
        #     'Decoding', buf
        #     print
        #     pickle.loads(''.join(buf)) # <-- this line joins the list, then loads it, why?
        # """do something here after it is loaded?"""
        #     buf = [] # <-- this line resets the buffer, but only if the line ends with a newline character
    print(buf)
    # dummyPickleFile.close()

def calculateDF(userInputTokens: list, index: dict):
    #print("Enters calculate DF")

    '''
    for word in userInputTokens:
        print(word)
    '''
         
    uniquePages = 55393
    # key is token
    # value is tf idf
    ranking = {}
    
    search_results = defaultdict(int)
        
    for token in userInputTokens:
        try:
            if token in stop_words:
                continue
            else:
                for postingObject in index[token]:
                    # IDF is inverse data frequency
                    IDF = math.log(uniquePages / len(index[token]))
                    # TF is term frequency
                    TF_IDF = postingObject.TF * IDF
                    TF_IDF += postingObject.important
    
                    if token not in ranking:
                        ranking[token] = [(postingObject, TF_IDF)]
                    else:
                        ranking[token].append((postingObject, TF_IDF))                
        except Exception as e:
            print("Word doesn't exist.")
            print(e)
            break
        
    for token, post in ranking.items():
        for posting, score in post:
            if posting.URL not in search_results:
                search_results[posting.URL] = score
            else:
                
                search_results[posting.URL] += score + 100
    return search_results


            

# tf - idf: tf-idf(t, d) = tf(t, d) * log(N/(df + 1))
# idf(t) = N/df
# tf-idf(t, d) = tf * idf

# tf_idf = {}
# for i in range(N):
#     tokens = processed_text[i]
#     counter = Counter(tokens + processed_title[i])
#     for token in np.unique(tokens):
#         tf = counter[token]/words_count
#         df = doc_freq(token)
#         idf = np.log(N/(df+1))
#         tf_idf[doc, token] = tf*idf

if __name__ == "__main__":


    """UNCOMMENT THESE LINES BELOW WHEN NOT TESTING"""
    directory = "C:\\Users\\coope\\OneDrive\\Desktop\\invertedIndex"

    filename = "assignment3.pickle"
    # buffer(directory, filename)
    


    # # take userinput, need to stem too
    promptUser = input("Do you want to search or not (y or n)? \n")
        
    while promptUser.lower() != 'n':
        
        userInput = input("\nEnter your query (q to quit): \n")
        
        if userInput.lower() == 'q':
            break
    
        userInput = userInput.lower()
        
        if "and" in userInput:
            userInput = userInput.replace("and", "")
            
        userInput = userInput.split()
        
        userInputTokens = [PorterStemmer().stem(token) for token in userInput]
        
        index = unpickleIndex(directory, userInputTokens)
        
        """
        for word, setposting in index.items():
            for post in setposting:
                print(word, post.URL)
        """
        """dont uncomment this?"""
        
        start = perf_counter()
        search_results = calculateDF(userInputTokens, index)
        end = perf_counter() 
        execution_time = (end - start)
        print (execution_time)
        print(type(search_results))
        if search_results == {}:
            print("Word does not exist.")
        else:
            for url, score in  sorted(search_results.items(), key=lambda item: (-item[1]))[:5]:
                print("URL:", url)
            
    print("Thanks for searching!")

  




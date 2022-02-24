class Posting():
    def __init__(self, docName, docID, URL):
        self.docID = docID
        self.docName = docName
        self.termFreq = 0
        self.important = 0
        self.wordCount = 0
        self.TF = 0
        self.URL = URL
    
    
    def calc_TF(self):
        self.TF = self.termFreq/self.wordCount
        
    
    def __str__(self):
        return str(self.docID) + " freq: " + str(self.termFreq) + " importance: " + str(self.important) + "tf-score: " + str(self.TF)

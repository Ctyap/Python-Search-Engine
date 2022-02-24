import pickle

def extract_index(file_path): 
    with open(file_path, 'rb') as file:
        index = pickle.load(file)
        #file.close()
        return index


if __name__ == "__main__":
    saved_folder= "C:\\Users\\coope\\OneDrive\\Desktop\\invertedIndex\\sassignment3.pickle"
    
    a_index = extract_index(saved_folder)
    
    for i,v in a_index.items():
        print(i, list(v)[0].URL)
    

import pickle

def pickleIndex(index, full_path, filename):
    # full_path = full_path + '\\' + filename + '.pickle'
    alphabet = ["a", "b",  "c", 'd' ,'e' ,'f'
                ,'g' ,'h', 'i', 'j', 'k', 'l','m'
                ,'n','o' ,'p', 'q' ,'r' ,'s' ,'t',
                'u','v', 'w', 'x', 'y', 'z',
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    pickleDict = {}



    for letter in alphabet:
        for i, v in sorted(index.items(), key= lambda x: (x[0])):
            # print(i)
            if i.startswith(letter):
                print(i)
                pickleDict[i] = v
        
        # makes a new pickle file for each letter in alphabet and digits 0-9 ... i.e there'll be 36 pickle files
        # we will use these 36 pickle files for searching efficiently
        full_path = full_path + "\\" + letter  + filename + ".pickle"
        # a_saved_folder\\assignment3.pickle

        pickle_out = open(full_path, "wb")
        pickle.dump(pickleDict, pickle_out)
        pickle_out.close()
        pickleDict.clear()
        
        full_path = "C:\\Users\\coope\\OneDrive\\Desktop\\invertedIndex"

from collections import defaultdict
import re
import glob


def create_n_grams(lang, num, k): #returns top k n-grams according to frequency
    words = re.sub('['+string.punctuation+']', '', lang) #  punctuation removed
    #words = words.lower()
    words = re.sub('\s+', ' ', words).strip() # replaces multiple spaces, newline tabs with a single space
    #words = words.replace(' ','_')# so that we can visualise spaces easily
    grams = {}
    #print (words)
    for i in range(len(words)-num):
        temp = words[i:i+num]
        if temp in grams:
            grams[temp] += 1
        else:
            grams[temp] = 1
    sum_freq = len(words) - num + 1
    for key in grams.keys():
        red = 1 # reduction factor equal 1 if no '_' is present
        if '_' in key: red = 2
        #grams[key] = round(math.log(grams[key] / (red * sum_freq)), 3) #normalizing by dividing by total no of n-grams for that corpus and taking log     
        #grams[key] = sum_freq
    grams = sorted(grams.items(), key= lambda x : x[1], reverse = True) 
    
    return grams



def create_lang_profile(lang, k):


    # find all files relating to language
    all_files = []
    for file in glob.glob(lang + "/*.txt"):
        all_files.append(file)
    print("{0} files found".format(len(all_files)))
    
    # read them in, and store in big list
    sentences = []
    for file in all_files:
        with open (file, 'r', encoding='utf-8') as fname:
            for row in fname:
                sentences.append(row)
    print("{0} sentences loaded".format(len(sentences)))
    
    # merge for function compliance
    train_corpora = '\n'.join(sentences)
    
    # generate n-grams
    uni_grams = create_n_grams(train_corpora, 1, k)
    bi_grams = create_n_grams(train_corpora, 2, k)
    tri_grams = create_n_grams(train_corpora, 3, k)
    
    # create dictionaries
    ngrams = dict(uni_grams)
    ngrams.update(bi_grams)
    ngrams.update(tri_grams)
    
    
    # save as a larger dictionary in the style of langdetect
    profile = {"freq" : ngrams, "n_words" : [1969690,2210879,1502429] , "name" : lang}
    
    # dump to profile file
    with open("profiles/{0}".format(lang), "w+", encoding="utf8") as f:
        json.dump(profile, f, ensure_ascii=False)
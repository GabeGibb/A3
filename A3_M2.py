import json
from nltk.stem import PorterStemmer
import math

def load_index():
    with open('index.json', 'r') as file:
        index = json.load(file)
    return index

def get_query():
    print()
    query = input("Search Bar: ").split()
    stemmer = PorterStemmer()
    stemmed_query = []
    for word in query:
        stemmed_query.append(stemmer.stem(word.lower()))
    # CHANGE: For loop used to remove invalid (non-alphanumeric) terms
    # CHANGE: For loop to make sure terms do not contain foreign characters
    query = stemmed_query
    for word in query[:]:
        valid_char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                      'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                      'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6',
                      '7', '8', '9']
        for char in word:
            if char not in valid_char:
                query.remove(word)
                break
    return query

def get_intersection_of_urls(index, query):
    urls_set = None
    for word in query:
        try:
            result = index[word]
        except:
            # In case word does not exist in index
            # CHANGE: Removed "print("No results found.")" because of repetition
            return
        if urls_set is None:
            urls_set = set(result.keys())
        else:
            # Where the AND operation happens
            urls_set = urls_set.intersection(set(result.keys()))
    return urls_set

def get_scores_for_urls(index, urls_set, query):
    urls_set = list(urls_set)

    # CHANGE: # Relevancy score involves frequency (tf)
    tf = []
    for url in urls_set:
        relevancy_score = 0
        for word in query:
            # Makes sure word and url are valid
            if word in index and url in index[word]:
                relevancy_score += index[word][url]
        relevancy_score = math.log(relevancy_score, 10) + 1
        tf.append((url, relevancy_score))
    
    # CHANGE: Relevancy score involves rarity (idf)
    total_docs = 0 # N
    for url in urls_set:
        for word in query:
            total_docs += len(index[word])

    df = []
    for url in urls_set:
        relevancy_score = 0
        for word in query:
            # Makes sure word and url are valid
            if word in index and url in index[word]:
                relevancy_score += len(index[word])
        df.append((url, relevancy_score))

    idf = []
    for frequency in df:
        idf.append((frequency[0], math.log((total_docs/frequency[1]), 10)))

    urls_with_scores = []
    for i in range(len(tf)):
        urls_with_scores.append((tf[i][0], (tf[i][1] * idf[i][1])))
    
    return urls_with_scores

# Searching query
def search_index(index):
    query = get_query()

    # Implicitly uses AND operation on query with multiple words
    urls_set = get_intersection_of_urls(index, query)
    # In case words do not share any URLs
    if urls_set is None:
        print("No results found.") # CHANGE: elif len(urls_set) and if None
        return
    elif len(urls_set) == 0:
        print("No results found.")
        return
    
    # Calculates each URL's relevancy score
    urls_with_scores = get_scores_for_urls(index, urls_set, query)

    # Final top 5 URLs
    top_5 = sorted(urls_with_scores, key=lambda x: x[1], reverse=True)[:5]

    print('TOP URLS:')
    for top in top_5:
        print(top)


if __name__ == "__main__":
    index = load_index()
    search_index(index)
    search_index(index)
    search_index(index)
    search_index(index)

import json
from nltk.stem import PorterStemmer
import math

# h, q, z
def load_index(letter):
    letter = letter.lower()
    file_letter = ''
    if letter <= 'h':
        with open('indices/merged_index_a.json', 'r') as file:
            index = json.load(file)
            file_letter = 'a'
    elif letter <= 'q':
        with open('indices/merged_index_b.json', 'r') as file:
            index = json.load(file)
            file_letter = 'b'
    else:
        with open('indices/merged_index_c.json', 'r') as file:
            index = json.load(file)
            file_letter = 'c'
    return index, file_letter

def calculate_file_letter(letter):
    letter = letter.lower()
    if letter <= 'h':
        return 'a'
    elif letter <= 'q':
        return 'b'
    return 'c'

def get_query():
    print()
    query = input("Search Bar: ").split()
    stemmer = PorterStemmer()
    stemmed_query = []

    # Combine stemming and filtering non-alphanumeric characters in one step
    stemmed_query = [stemmer.stem(word.lower()) for word in query if word.isalnum()]

    return stemmed_query

def get_intersection_of_urls(query):
    urls_set = None
    small_index = {}
    index = {}
    index_letter = ''
    for word in sorted(query):
        if index_letter != calculate_file_letter(word) or index == {}:
            index, index_letter = load_index(word[0])
        try:
            result = index[word]
            small_index[word] = result
        except:
            # In case word does not exist in index
            return
        if urls_set is None:
            urls_set = set(result.keys())
        else:
            # Where the AND operation happens
            urls_set = urls_set.intersection(set(result.keys()))
    return urls_set, small_index

def get_scores_for_urls(index, urls_set, query):
    urls_set = list(urls_set)

    # CHANGE: # Relevancy score involves frequency (tf)
    tf = []
    for url in urls_set:
        relevancy_score = 0
        for word in query:
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
def search_index():
    query = get_query()

    # Implicitly uses AND operation on query with multiple words
    urls_set, small_index = get_intersection_of_urls(query)
    # In case words do not share any URLs
    if urls_set is None or len(urls_set) == 0:
        print("No results found.")
        return
    
    # Calculates each URL's relevancy score (tf-idf)
    urls_with_scores = get_scores_for_urls(small_index, urls_set, query)

    # Final top 5 URLs
    top_5 = sorted(urls_with_scores, key=lambda x: x[1], reverse=True)[:5]

    print('TOP URLS:')
    for top in top_5:
        print(top)


if __name__ == "__main__":
    search_index()
    # search_index(index)
    # search_index(index)
    # search_index(index)

import json

def load_index():
    with open('index.json', 'r') as file:
        index = json.load(file)
    return index

def get_query():
    print()
    query = input("Search Bar: ").split()
    for i in range(len(query)):
        # Lowercasing the query
        query[i] = query[i].lower()
    return query

def get_intersection_of_urls(index, query):
    urls_set = None
    for word in query:
        try:
            result = index[word]
        except:
            # In case word does not exist in index
            print("No results found.")
            return
        if urls_set is None:
            urls_set = set(result.keys())
        else:
            # Where the AND operation happens
            urls_set = urls_set.intersection(set(result.keys()))
    return urls_set

def get_scores_for_urls(index, urls_set, query):
    urls_with_scores = []
    for url in urls_set:
        relevancy_score = 0
        for word in query:
            # Makes sure word and url are valid
            if word in index and url in index[word]:
                # Relevancy score correlates with frequency
                relevancy_score += index[word][url]
        urls_with_scores.append((url, relevancy_score))
    return urls_with_scores

# Searching query
def search_index(index):
    query = get_query()

    # Implicitly uses AND operation on query with multiple words
    urls_set = get_intersection_of_urls(index, query)
    # In case words do not share any URLs
    if len(urls_set) == 0:
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

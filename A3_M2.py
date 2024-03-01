import json

def load_index():
    with open('index.json', 'r') as file:
        index = json.load(file)
    return index

# Searching query
def search_index(index):
    print()
    query = input("Search Bar: ").split()
    for i in range(len(query)):
        # Lowercasing the query
        query[i] = query[i].lower()

    # Implicitly uses AND operation on query with multiple words
    top_5 = None
    for word in query:
        try:
            result = index[word]
        except:
            # In case word does not exist in index
            print("No results found.")
            return
        if top_5 is None:
            top_5 = set(result.keys())
        else:
            # Where the AND operation happens
            top_5 = top_5.intersection(set(result.keys()))

    # Finding top 5 URLs
    if len(top_5) == 0:
        # In case words do not share any URLs
        print("No results found.")
        return
    # Calculates each URL's relevancy score
    top_5_with_scores = []
    for url in top_5:
        relevancy_score = 0
        for word in query:
            # Makes sure word and url are valid
            if word in index and url in index[word]:
                # Relevancy score correlates with frequency
                relevancy_score += index[word][url]
        top_5_with_scores.append((url, relevancy_score))
    top_5 = top_5_with_scores
    # Final top 5 URLs
    top_5 = sorted(top_5, key=lambda x: x[1], reverse=True)[:5]

    print('TOP URLS:')
    for top in top_5:
        print(top[0])


if __name__ == "__main__":
    index = load_index()
    search_index(index)
    search_index(index)
    search_index(index)
    search_index(index)

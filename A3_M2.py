import json

def load_index():
    with open('index.json', 'r') as file:
        index = json.load(file)
    return index

# Searching Query
def search_index(index):
    print()
    query = input("Search Bar: ").split()
    # try:
    relevancy_dict = {}
    for word in query:
        if word not in index: # if word not in index, skip it
            print(word, "not found in index")
            continue
        
        result = sorted(index[word].items(), key=lambda x: x[1], reverse=True)[:20] #changed to 20 values to be a little more accurate
        for pair in result:
            if pair[0] not in relevancy_dict:
                relevancy_dict[pair[0]] = pair[1]
            else:
                relevancy_dict[pair[0]] += pair[1]

    top_5 = sorted(relevancy_dict.items(), key=lambda x: x[1], reverse=True)[:5]
    # print(top_5)
    print('TOP URLS:')
    for top in top_5:
        print(top[0])
    print()


if __name__ == "__main__":
    search_index(load_index())

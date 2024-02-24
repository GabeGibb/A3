import json

def load_index():
    with open('index.json', 'r') as file:
        index = json.load(file)
    return index

# Searching Query
def search_index(index):
    print()
    query = input("Search Bar: ").split(" ")
    try:
        relevancy_dict = {}
        for word in query:
            result = sorted(index[word].items(), key=lambda x: x[1], reverse=True)[:5]
            for pair in result:
                if pair[0] not in relevancy_dict:
                    relevancy_dict[pair[0]] = pair[1]
                else:
                    relevancy_dict[pair[0]] += pair[1]

        top_5 = sorted(relevancy_dict.items(), key=lambda x: x[1], reverse=True)[:5]
        print(top_5)
    except:
        print("Error")

if __name__ == "__main__":
    search_index(load_index())

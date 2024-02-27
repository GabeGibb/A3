import json

def load_index():
    with open('index.json', 'r') as file:
        index = json.load(file)
    return index

# Searching Query
def search_index(index):
    print()
    query = input("Search Bar: ").split()
    for i in range(len(query)):
        # Lowercasing the query
        if query[i] != "AND":
            query[i] = query[i].lower()
        # Differentiating normal words from AND operations in query
        elif i != 0 and i != len(query)-1 and len(query) > 2:
            continue
        else:
            query[i] = query[i].lower()

    # Collects the indices of the words the AND operations are combining
    positions_of_interest = []
    for word in query:
        if word == "AND":
            positions_of_interest.append(query.index(word)-1)
    # Combines the operands of the AND operations
    for position in positions_of_interest:
        query[position] = query[position] + " AND " + query[position + 2]
        query[position + 1] = ""
        query[position + 2] = ""
    for word in query[:]:
        if word == "":
            query.remove(word)
    relevancy_dict = {}
    relevancy_dict1 = {}
    relevancy_dict2 = {}
    for i in range(len(query)):
        # For AND operations in query
        if len(query[i].split(" AND ")) == 2:
            first = query[i].split(" AND ")[0]
            second = query[i].split(" AND ")[1]
            if first not in index or second not in index: # if word not in index, skip it
                print(first + " AND " + second + " not found in index")
                continue
            result = sorted(index[first].items(), key=lambda x: x[1], reverse=True)[:20] #changed to 20 values to be a little more accurate
            for pair in result:
                if pair[0] not in relevancy_dict1:
                    relevancy_dict1[pair[0]] = pair[1]
                else:
                    relevancy_dict1[pair[0]] += pair[1]
            result = sorted(index[second].items(), key=lambda x: x[1], reverse=True)[:20] #changed to 20 values to be a little more accurate
            for pair in result:
                if pair[0] not in relevancy_dict2:
                    relevancy_dict2[pair[0]] = pair[1]
                else:
                    relevancy_dict2[pair[0]] += pair[1]
            # Combines relevancy dicts
            for key in relevancy_dict1:
                if key in relevancy_dict2:
                    relevancy_dict[key] = relevancy_dict1[key] + relevancy_dict2[key]

        # For normal words in query
        else:
            if query[i] not in index: # if word not in index, skip it
                print(word, "not found in index")
                continue
            result = sorted(index[query[i]].items(), key=lambda x: x[1], reverse=True)[:20] #changed to 20 values to be a little more accurate
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


if __name__ == "__main__":
    index = load_index()
    search_index(index)
    search_index(index)
    search_index(index)
    search_index(index)

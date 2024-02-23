import json
import os
from bs4 import BeautifulSoup

class InvertedIndex:
    def __init__(self):
        self.index = {}

    def tokenize(self, text):
        tokens = []
        current_token = ""
        for char in text.lower():
            if char.isalnum():
                current_token += char
            elif current_token != "":
                tokens.append(current_token)
                current_token = ""
        return tokens

    def add_posting(self, token, dicti):
        if token not in self.index: # string, list<pair<string, int>>
            self.index[token] = [(dicti["url"], dicti["content"].count(token))]
        # doc name/id & frequency in doc
        self.index[token].append((dicti["url"], dicti["content"].count(token)))



def index_folder(folder):
    # Example Test 1:
    index = InvertedIndex()

    # Walk through all directories and files recursively
    for root, dirs, files in os.walk(folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r') as file:
                # Process the contents of the file
                for line in file: # url, content, encoding
                    dicti = json.loads(line)
                    content = dicti["content"]
                    soup = BeautifulSoup(content, "html.parser")
                    text = soup.get_text()
                    tokens_list = index.tokenize(text)

                    for token in tokens_list:
                        index.add_posting(token, dicti)

    indexed = set()
    for key in index.index:
        indexed.add(index.index[key][0])

    # Serialize index to JSON file
    with open('index.json', 'w') as file:
        json.dump(index.index, file)

    # Get size the file in bytes
    file_size_bytes = os.path.getsize('index.json')
    # Convert bytes to kilobytes
    file_size_kb = file_size_bytes / 1024

    # For the report
    unique_words = len(index.index)
    indexed_documents = len(indexed)

    print("Directory: analyst")
    print("Number of Unique Words: " + str(indexed_documents))
    print("Number of Indexed Documents: " + str(unique_words))
    print("Total Size of Index on Disk in KB: " + str(file_size_kb))

    # Remove the temporary file
    # os.remove('index.json')
    # print()


# This is a test folder I made with only a subset of the data
index_folder("test")
# index_folder("developer")


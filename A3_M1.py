import json
import os
from bs4 import BeautifulSoup
import re

class InvertedIndex:
    def __init__(self):
        self.index = {}

    def tokenize(self, text):
        # More efficient way to tokenize
        lower_text = text.lower()
        alphaNumText = re.sub(r'[^a-zA-Z0-9 ]', '', lower_text)

        return alphaNumText.split()

    def add_posting(self, token, dicti):
        # print(self.index)
        if token not in self.index: # string, list<pair<string, int>>
            self.index[token] = {dicti["url"]: 1}
        # doc name/id & frequency in doc
        else:
            if dicti["url"] not in self.index[token]:
                self.index[token][dicti["url"]] = 1
            else:
                self.index[token][dicti["url"]] += 1



def index_folder(folder):
    # Example Test 1:
    index = InvertedIndex()

    num_files = 0
    # Walk through all directories and files recursively
    for root, _, files in os.walk(folder):
        num_files += len(files)
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r') as file:
                # Process the contents of the file
                plain_text = file.read()
                dicti = json.loads(plain_text)
                content = dicti["content"]
                soup = BeautifulSoup(content, "html.parser")
                text = soup.get_text()
                tokens_list = index.tokenize(text)

                for token in tokens_list:
                    index.add_posting(token, dicti)



    # Serialize index to JSON file
    with open('index.json', 'w') as file:
        json.dump(index.index, file)

    # Get size the file in bytes
    file_size_bytes = os.path.getsize('index.json')
    # Convert bytes to kilobytes
    file_size_kb = file_size_bytes / 1024

    # For the report
    unique_words = len(index.index)

    print("Directory: " + folder)
    print("Number of Unique Words: " + str(unique_words))
    print("Number of Indexed Documents: " + str(num_files))
    print("Total Size of Index on Disk in KB: " + str(file_size_kb))

    # Remove the temporary file
    # os.remove('index.json')
    # print()


# This is a test folder I made with only a subset of the data
index_folder("test")
# index_folder("developer")


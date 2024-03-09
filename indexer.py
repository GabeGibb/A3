import json
import os
import sys
import shutil
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer

class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.index_counter = 1
        self.stemmer = PorterStemmer()

    def tokenize(self, text):
        # More efficient way to tokenize
        lower_text = text.lower()
        alphaNumText = re.sub(r'[^a-zA-Z0-9 ]', '', lower_text)

        return alphaNumText.split()

    def add_posting(self, token, dicti):
        token = self.stemmer.stem(token.lower())

        # print(self.index)
        if token not in self.index: # string, list<pair<string, int>>
            self.index[token] = {dicti["url"]: 1}
        # doc name/id & frequency in doc
        else:
            if dicti["url"] not in self.index[token]:
                self.index[token][dicti["url"]] = 1
            else:
                self.index[token][dicti["url"]] += 1

    def offload_index_if_needed(self, force=False):
        # If size too big offload to file
        size_in_bytes = sys.getsizeof(self.index)
        if size_in_bytes > 10000000 or force:
            with open(f'temp_indices/index_{self.index_counter}.json', 'w') as file:
                json.dump(self.index, file)
            self.index = {}
            self.index_counter += 1

    def merge_indices(self):
        # Merge all indices into three separate merged indexes alphabetically
        merged_index = {}

        for root, _, files in os.walk("temp_indices"):
            for file_name in files:
                with open(os.path.join(root, file_name), 'r') as file:
                    index = json.load(file)
                    for key in index:
                        if key not in merged_index:
                            merged_index[key] = index[key]
                        else:
                            # Merge into dict by adding the two dictionaries together
                            merged_index[key].update(index[key])

        # If it doesn't exist, create it
        dir_name = "indices"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # merge indices into a file for the word
        for key, value in merged_index.items():
            if len(key) > 0 and len(key) < 20:
                try:
                    with open(f'indices/{key}.json', 'w') as file:
                        json.dump(value, file)
                except:
                    print(f"Error: {key}")


def extract_important_words(content):
    important_words = []
    soup = BeautifulSoup(content, 'html.parser')
    # shortened, you can find all in one statement
    tags = soup.find_all(['h1', 'h2', 'h3', 'b', 'strong', 'title'])
    for tag in tags:
        for word in tag.get_text().split():
            important_words.append(word)

    return important_words



def index_folder(folder):
    # Create a folder to store offloaded indices if it doesnt exist
    dir_name = "temp_indices"
    if not os.path.exists(dir_name):
        # If it doesn't exist, create it
        os.makedirs(dir_name)

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
                for line in file:
                    dicti = json.loads(line)
                    content = dicti["content"]
                    soup = BeautifulSoup(content, "html.parser")
                    text = soup.get_text()
                    tokens_list = index.tokenize(text)
                    
                    important_words = extract_important_words(content)
                    for token in tokens_list:
                        # Increases important words' frequencies by 2
                        if token in important_words:
                            index.add_posting(token, dicti)
                        # Adding lowercased version of tokens
                        index.add_posting(token, dicti)
            index.offload_index_if_needed()
    
    # Offload the last index
    index.offload_index_if_needed(True)

    # Merge the indexes into 3 indices and delete the temp indices
    index.merge_indices()
    try:
        shutil.rmtree(dir_name)
    except OSError as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    # This is a test folder I made with only a subset of the data
    # index_folder("test")
    # index_folder("analyst")
    index_folder("developer")

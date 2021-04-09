# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 21:03:15 2021

@author: Adam
"""

#import pytest
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from task import AutoCompleteIndex, IncrementalAutoCompleteSearch
import pandas as pd
import random
import string



CSV_FILE_NAME = "Aword.csv"

class AutocompleteBruteForce:
    def __init__(self, auto_complete_index, max_recommendations):
        self.autocomplete = auto_complete_index
        self.buffer = ""
        self.max_recommendations = max_recommendations
        
    def get_predictions(self, prefix):
        predictions = []
        options = self.autocomplete.options
        for word, count in options.items():
            if word.startswith(prefix):
                predictions.append((word, count))
        
        predictions = sorted(predictions, key = lambda x: x[1], reverse=True)
        return [x[0] for x in predictions[0: self.max_recommendations]]


def get_list_options(csvFilename, start_idx, stop_idx):
    df_options = pd.read_csv(csvFilename, header=None)
    # Create a list of tuples for Dataframe rows using list comprehension
    list_of_tuples = [tuple(row) for row in df_options[start_idx: stop_idx].to_numpy()]
    #print("get_list_options created following list: %s" % str(list_of_tuples))
    return list_of_tuples

def get_random_words_from_options(options, num_words):
    num_options = len(options)
    res = []
    for i in range(num_words):
        res.append(options[random.randint(0, num_options)][0])
    return res

def generate_random_words(num_words, max_word_len):
    res = []
    letters = string.ascii_lowercase
    for i in range(num_words):
        res.append(''.join(random.choice(letters) for i in range(random.randint(0,max_word_len))))
    return res
    

def compare_autocompletesearch_against_brute_force_for_word(ac_search, ac_brute, word):
    for i in range(len(word)):
        ac_search_res = ac_search.type_character(word[i])
        brute_force_res = ac_brute.get_predictions(word[:i+1])
        # print("ac_search_res when calling type_character(%s): %s" % (word[i], str(ac_search_res)))
        # print("brute_force_res on prefix %s: %s\n" % (word[:i+1], str(brute_force_res)))
        assert ac_search_res == brute_force_res
    ac_search.set_buffer("")
    

def test_autocompletesearch_against_bruteforce(csvFilename, start_idx, stop_idx, num_existing_words, num_random_words, max_random_word_len,  max_predictions):
    #1. Add long list of options to model
    options = get_list_options(csvFilename, start_idx, stop_idx)
    auto_complete_index = AutoCompleteIndex(options)
    ac_search = IncrementalAutoCompleteSearch(auto_complete_index, max_predictions)
    ac_brute = AutocompleteBruteForce(auto_complete_index, max_predictions)
    
    #2. Create random list of words to test
    words = get_random_words_from_options(options, num_existing_words)
    words.extend(generate_random_words(num_random_words, max_random_word_len))
    print("test_autocompletesearch_against_bruteforce created following words to test against: %s" % str(words))
    
    #3. Write function that receives word, and compares brute force with regular model
    for word in words:
        compare_autocompletesearch_against_brute_force_for_word(ac_search, ac_brute, word)

    print("EVERYTHING WORKED!")

if __name__=="__main__":
    test_autocompletesearch_against_bruteforce(CSV_FILE_NAME, 0, 500, 10, 10, 5, 10)

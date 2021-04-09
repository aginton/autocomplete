# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 20:13:18 2021

@author: Adam
"""


import requests
URL_BASE = "http://localhost:5000/"
JSON_VALID_OPTIONS = {"options": [{"word": "aaa", "count": 3}, {"word": "aa", "count": 10}, {"word": "azz", "count": 4}]}
EXISTING_WORD = "aaa"
NON_EXISTING_WORD ="pz"
PREFIX = "aba"
ADD_OPTION = ("cat", 10)
TYPE_CHAR = "a"



def test_auto_complete_index_get_predictions_status_code_equals_200(word = None):
    url = URL_BASE+"auto_complete_index/get"
    if word is not None:
        url += "/" + word
        
    response = requests.get(url)
    assert response.status_code == 200
    print("test_auto_complete_index_get_predictions_status_code_equals_200 with argument %s passed. " % word)



def test_auto_complete_index_post_status_code_equals_200(options_to_add = None):
    if options_to_add is not None:
        response = requests.post(URL_BASE+"auto_complete_index/post", json = options_to_add)
        assert response.status_code == 200
    print("test_auto_complete_index_put_status_code_equals_200 with argument %s passed" % str(options_to_add))



def test_auto_complete_search_get_status_code_equals_200(prefix = None):
    url = URL_BASE+"auto_complete_search/get"
    if prefix is not None:
        url += "/" + prefix
    response = requests.get(url)
    assert response.status_code == 200
    print("test_auto_complete_search_get_status_code_equals_200 with argument %s passed" % str(prefix))


def test_auto_complete_search_put_status_code_equals_200(char = None):
    if char is not None:
        response = requests.put(URL_BASE+"auto_complete_search/put/" + char)
        assert response.status_code == 200
    print("test_auto_complete_search_get_status_code_equals_200 with argument %s passed" % str(char))


def test_auto_complete_search_remove_status_code_equals_200():
     response = requests.delete(URL_BASE+"auto_complete_search/remove")
     assert response.status_code == 200
     print("test_auto_complete_search_remove_status_code_equals_200 passed")


if __name__ == "__main__":
    test_auto_complete_index_get_predictions_status_code_equals_200()
    test_auto_complete_index_get_predictions_status_code_equals_200(EXISTING_WORD)
    test_auto_complete_index_get_predictions_status_code_equals_200(NON_EXISTING_WORD)
    test_auto_complete_index_post_status_code_equals_200()
    test_auto_complete_index_post_status_code_equals_200(JSON_VALID_OPTIONS)
    test_auto_complete_search_get_status_code_equals_200(PREFIX)
    test_auto_complete_search_put_status_code_equals_200(TYPE_CHAR)
    test_auto_complete_search_put_status_code_equals_200()
    print("ALL TESTS PASSED!!!")
    
    
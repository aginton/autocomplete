# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 23:13:23 2021

@author: Adam
"""

from flask import Flask, url_for, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse, abort
from markupsafe import escape
from task import AutoCompleteIndex, IncrementalAutoCompleteSearch

app = Flask(__name__)
api = Api(app)

options = [('aaa', 3), ('aa', 10), ('azz', 4)]
auto_complete_index = AutoCompleteIndex(options)
auto_complete_search = IncrementalAutoCompleteSearch(auto_complete_index, max_recommendations=2)




@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return "exception", 500



@app.route('/auto_complete_index/post', methods=['POST'])
def add_options():
      data = request.json
      if 'options' not in data:
          return "missing options!"
      options = [(x['word'], x['count']) for x in data['options']]
      auto_complete_index.add_options(options)
      return auto_complete_index.map_prefixes_to_options



@app.route('/auto_complete_index/get/<string:word>', methods=['GET'])
def get_count(word):
        if word in auto_complete_index.options:
            return str(auto_complete_index.options[word])
        else:
            return {"error_message": "{} is not a valid word.".format(word)}
        
@app.route('/auto_complete_index/get', methods=['GET'])
def get_all_options():
    return auto_complete_index.options




# The following methods are used to represent a particular search query. 
@app.route('/auto_complete_search/get/<string:word>', methods=['GET'])
def get_predictions(word):
        if word in auto_complete_index.map_prefixes_to_options:
            return str(auto_complete_index.map_prefixes_to_options[word])
        else:
            return {"error_message": "No words found with {} as prefix.".format(word)}
        
        
@app.route('/auto_complete_search/put/<string:char>', methods=["PUT"])
def type_character(char):
    return str(auto_complete_search.type_character(char))
    

@app.route('/auto_complete_search/remove', methods=["DELETE"])
def delete_character():
    return str(auto_complete_search.delete_character())
    

@app.route('/auto_complete_search/get', methods=["GET"])
def get_prefix():
    return auto_complete_search.buffer



if __name__ == '__main__':    
    app.run(debug=True)  # run our Flask app

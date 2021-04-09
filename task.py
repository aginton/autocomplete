"""
In this task we ask to implement a solution for incremental text Auto-Complete. To do so we want to create 2 classes:

1. The AutoCompleteIndex class - this class will get as input an iterator of all optional auto-complete results with there counts.
    It is expected to handle a large amount of options (100,000+).

2. The IncrementalAutoCompleteSearch class. - this class will get as input an instance of the AutoCompleteIndex class;
    It should enable typing in char by char (i.e. incremental) and get a list of top k recommended strings sorted by count
    after each character addition/deletion. The run time expectations is: O(1) for these methods.


For example:
>> options = [('aaa', 3), ('aa', 10), ('azz', 4)]
>> auto_complete_index = AutoCompleteIndex(options)
>> auto_complete_search = IncrementalAutoCompleteSearch(auto_complete_index, max_recommendations=2)
>> auto_complete_search.type_character('a')
['aa', 'azz']
>> auto_complete_search.type_character('a')
['aa', 'aaa']
>> auto_complete_search.delete_character()
['aa', 'azz']
>> auto_complete_search.type_character('z')
['azz']
>> auto_complete_search.type_character('p')
[]
"""




class AutoCompleteIndex(object):
    def __init__(self, options):
        """
        :param options: an iterator of (<string>, <count>) tuples. i.e. [('aaa', 3), ('aa', 10), ('azz', 4)]
        """
        self.root = {}
        self.map_prefixes_to_options = {}
        self.options = {}
        self.add_options(options)


    def add_options(self, options):
        """
        :param options: an iterator of (<string>, <count>) tuples. i.e. [('aaa', 3), ('aa', 10), ('azz', 4)]
        """
        for option in options:
            self.add_option(option)
    
    
    def add_option(self, option):
        word = option[0]
        if len(word) < 1:
            return
        if option in self.options:
            return
        self.options[option[0]] = option[1]
        cur = self.root
        
        for i in range(len(word)):
            prefix = word[:(i+1)]
            if prefix not in self.map_prefixes_to_options:
                self.map_prefixes_to_options[prefix] = []
            
            self.map_prefixes_to_options[prefix].append(option)
            
            self.map_prefixes_to_options[prefix] = sorted(self.map_prefixes_to_options[prefix], key=lambda x: x[1], reverse=True)
            
    
    
    def printPrefixPredictions(self):
        for key, value in self.map_prefixes_to_options.items():
            print(key, ':', value)
        print()
        
        


class IncrementalAutoCompleteSearch(object):

    def __init__(self, auto_complete_index, max_recommendations):
        self.autocomplete = auto_complete_index
        self.buffer = ""
        self.max_recommendations = max_recommendations
        

    def getTopK(self, prefix):
        if len(prefix) == 0:
            return []
        if prefix not in self.autocomplete.map_prefixes_to_options:
            return []
        
        predictions = self.autocomplete.map_prefixes_to_options[prefix]
        num_predictions_to_return = min(self.max_recommendations, len(predictions))
        res = []
        for i in range(num_predictions_to_return):
            res.append(predictions[i][0])
        return res
    
    def type_character(self, c):
        """
        Takes a character `c` as input, adds it to the current prefix and returns a sorted list of 'top' recommendations for this prefix.
        The run time expectations is: O(1)
        :param c: a character.
        :return: a list sorted by count of strings of 'top' recommendations.
        """        
        self.buffer = self.buffer + c
        return self.getTopK(self.buffer)
        

    def delete_character(self):
        """
        Deletes the last character from the current prefix and returns a sorted list of 'top' recommendations for this prefix.
        The run time expectations is: O(1)
        :return: a list sorted by count of strings of 'top' recommendations.
        """
        
        if len(self.buffer) <= 1:
            self.buffer = ""
        else:
            self.buffer = self.buffer[:len(self.buffer)-1]
        
        return self.getTopK(self.buffer)
    
    def set_buffer(self, newBuffer):
        self.buffer = newBuffer
    
    

if __name__ == "__main__":
    options = [('aaa', 3), ('aa', 10), ('azz', 4)]
    auto_complete_index = AutoCompleteIndex(options)
    auto_complete_search = IncrementalAutoCompleteSearch(auto_complete_index, max_recommendations=2)
    print(auto_complete_search.type_character('a'))  # --> ['aa', 'azz']
    print(auto_complete_search.type_character('a'))  # --> ['aa', 'aaa']
    print(auto_complete_search.delete_character())  # --> ['aa', 'azz']
    print(auto_complete_search.type_character('z'))  # --> ['azz']
    print(auto_complete_search.type_character('p'))  # --> []
    
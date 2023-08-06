#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 14:33:25 2019

@author: psakicki
"""

#from geodezyx import *                   # Import the GeodeZYX modules
#from geodezyx.externlib import *         # Import the external modules
#from geodezyx.megalib.megalib import *   # Import the legacy modules names

def dicts_merge(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.

    WARN : first values will be erased if the same key is present in following dicts !!!

    http://stackoverflow.com/questions/38987/how-can-i-merge-two-python-dictionaries-in-a-single-expression
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def dicts_of_list_merge_mono(dol1, dol2):
    """
    https://stackoverflow.com/questions/1495510/combining-dictionaries-of-lists-in-python
    """
    keys = set(dol1).union(dol2)
    no = []
    return dict((k, dol1.get(k, no) + dol2.get(k, no)) for k in keys)


def dicts_of_list_merge(*dict_args):
    result = dict()
    for dictionary in dict_args:
        result = dicts_of_list_merge_mono(result,dictionary)
    return result


def dic_key_for_vals_list_finder(dic_in , value_in):
    """
    dic_in is a dict like :
        dic_in[key1] = [val1a , val1b]
        dic_in[key2] = [val2a , val2b , val2c]
        
    E.g. if value_in = val2b then the function returns key2
    
    NB : the function returns the first value found, then
         dic_in has to be injective !!
    """
    for k , v in dic_in.items():
        if value_in in v:
            return k
    
    print("WARN : no key found for value",value_in,"... None returned")
    return None

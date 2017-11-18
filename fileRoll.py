# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 22:23:21 2017

@author: Connor
"""

import pandas as pd
from os import walk

fileDirectory = r'D:\old desktop\Development\scrapeWMATA\fileDownload'

def file_walk(directory):
    file_name_list = []
    for (dirpath, dirnames, filenames) in walk(directory):
        file_name_list.extend(filenames)
        break
    return(file_name_list)
    
useFiles = file_walk(fileDirectory)
#pdb.set_trace()
for file in useFiles:
    
    df = pd.read_csv(fileDirectory + '\\' + file)
    if file == useFiles[0]:
        dfResults = df
    else:
        dfTwo = [dfResults, df]
        dfResults = pd.concat(dfTwo, ignore_index = True)
dfResults.to_csv('results.csv')

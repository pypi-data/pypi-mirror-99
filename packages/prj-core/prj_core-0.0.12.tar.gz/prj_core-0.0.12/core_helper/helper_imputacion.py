# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 14:52:15 2021

@author: User
"""

import numpy as np
import pandas as pd

def agregar_na_cl_list(df,cl_list):
    
    for c_name in cl_list:
        new_c = 'NA_'+c_name 
        df[new_c] = np.where((df[c_name].isna()) , 1 , 0 )
        
    return df


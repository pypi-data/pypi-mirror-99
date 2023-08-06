# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 14:52:15 2021

@author: User
"""

import numpy as np
import pandas as pd

def agregar_na_cls(df,cl_list):
    
    for c_name in cl_list:
        new_c = 'NA_'+c_name 
        df[new_c] = np.where((df[c_name].isna()) , 1 , 0 )
        
    return df


def fill_nan_with_nan_category_in_cls(df,cl_list):
    
    for c_name in cl_list:
        df[c_name].replace(np.nan, "NAN_CATEGORY" ,inplace=True)        
    return df

def fill_nan_with_mean_in_cl(df,cl_name,cls_group):
    df[cl_name] = df.groupby([cls_group])[cl_name].apply(lambda x: x.fillna(x.mean()))
    return df
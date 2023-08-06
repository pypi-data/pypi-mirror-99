# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 12:21:41 2021

@author: User
"""

import numpy as np
import pandas as pd
from functools import reduce
from core_helper import helper_acces_db as hadb
from core_helper import helper_dataframe as hdf



def generar_kpis_historicos(df,anio_df=None,anio_right=None,cls_json=None,t_anios=0,modalidad="EBR"):
    
    if(t_anios<=1):            
        print("ERROR: El numero minimo de t_anios debe ser = ",2)        
        return False
    
    ultimo_anio =anio_right- t_anios
    
    if(ultimo_anio<2014):            
        print("ERROR: Se pretende consultar hasta el anio ",ultimo_anio,", solo se tiene data hasta el 2014")        
        return False    
    
    
    if(anio_right>anio_df):            
        print("ERROR: El parametro anio_right no puede ser mayor al parametro anio_right ")        
        return False    
    
    cls_list = []
    for key, value in cls_json.items():
        cls_list.append(key)  
        
    if 'ID_PERSONA' not in cls_list :
        cls_list.append('ID_PERSONA')
        
    print(' '.join(cls_list)) 
    


    ID_PERSONA_SERIES = df['ID_PERSONA']
    

    num = anio_df-anio_right
    list_df_m_tras = []

    
    kpi_final_dic = {}
    print()
    for anio in range(anio_right,ultimo_anio,-1):
        if(anio<=2013):
            break

        
        df_m_t = pd.merge(ID_PERSONA_SERIES, hadb.get_siagie_por_anio(anio,modalidad=modalidad,columns_n=cls_list),left_on="ID_PERSONA",
                          right_on="ID_PERSONA", how='left')
        
        for key, values in cls_json.items():
            if  isinstance(values, list):
                print("category")   
                for val in values:
                    if num ==0:
                        cl_pf = val+"_T"               
                    else:
                        cl_pf = val+"_T_MENOS_{}".format(num)                        
                    df_m_t[cl_pf] = np.where((df_m_t[key]==val),1,0)
                    print(key," - ",cl_pf)
                    if  (val in kpi_final_dic) ==False:
                        kpi_final_dic[val]=[]                    
                    kpi_final_dic[val].append(cl_pf)
                df_m_t.drop([key], axis = 1,inplace=True) 
            elif values=="dummy":      
                print("dummy")
                if num ==0:
                    cl_pf = key+"_T"              
                else:
                    cl_pf = key+"_T_MENOS_{}".format(num)                
                df_m_t[cl_pf] = np.where((df_m_t[key]==1),1,0)
                print(key," - ",cl_pf)
                
                if  (key in kpi_final_dic) ==False:
                    kpi_final_dic[key]=[]                    
                kpi_final_dic[key].append(cl_pf)
                df_m_t.drop([key], axis = 1,inplace=True) 
                
            elif values=="numero":    
                print("numero")                
                if num ==0:
                    cl_pf = key+"_T"              
                else:
                    cl_pf = key+"_T_MENOS_{}".format(num)                
                df_m_t[cl_pf] = df_m_t[key]  
                
                if  (key in kpi_final_dic) ==False:
                    kpi_final_dic[key]=[]                    
                kpi_final_dic[key].append(cl_pf)
                df_m_t.drop([key], axis = 1,inplace=True) 

        list_df_m_tras.append(df_m_t)
        num+=1

    df_final = reduce(lambda left,right: pd.merge(left,right,on='ID_PERSONA'), list_df_m_tras)


    kpi_list = []
    for key, cls_anios in kpi_final_dic.items():
        kpi_list.append(key)   
        df_final = set_generic_kpis(df_final,key,cls_anios)
        #df_final.drop(cls_anios, axis = 1,inplace=True) 
        
    print(' '.join(kpi_list))   

    return df_final


def set_generic_kpis(df,cl_name=None,cl_list=[],set_nan=False):

    if(set_nan==False):
        df['TOTAL_'+cl_name] = df[cl_list].sum(axis=1)
        df['MEAN_'+cl_name] = df[cl_list].mean(axis=1)
        if(len(cl_list)>2):
            df['STD_'+cl_name] = df[cl_list].std(axis=1)
        df['MIN_'+cl_name] = df[cl_list].min(axis=1)
        df['MAX_'+cl_name] = df[cl_list].max(axis=1)
    else:
        df['TOTAL_'+cl_name] = np.nan
        df['MEAN_'+cl_name] = np.nan
        df['STD_'+cl_name] = np.nan
    return df


#df_2017 = hadb.get_siagie_por_anio(anio=2017,id_grado=9)

#cls_json = {}
#cls_json['SITUACION_FINAL']=["APROBADO"]
#cls_json['SITUACION_FINAL']=[["APROBADO","DESAPROBADO"],"APROBADO"]
#cls_json['JUNTOS']="dummy"
#df_h = generar_kpis_historicos(df_2017,2017,2015,cls_json,5,"EBR")


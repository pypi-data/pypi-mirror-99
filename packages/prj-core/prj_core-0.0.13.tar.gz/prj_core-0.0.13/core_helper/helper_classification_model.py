# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 15:44:39 2021

@author: User
"""
import json
import os
import math
import sys
import numpy as np
import pandas as pd
import shap
import time
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix, roc_auc_score, classification_report,average_precision_score , f1_score
from sklearn.metrics import roc_curve, precision_recall_curve, auc,recall_score,precision_score
from helper_transformers import CatTransformer
from helper_functions import reduce_mem_usage
from sklearn.model_selection import train_test_split
from scipy.stats import randint as sp_randint
from scipy.stats import uniform as sp_uniform
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV, StratifiedKFold
from imblearn.under_sampling import RandomUnderSampler
import seaborn as sns

import scikitplot as skplt
import lightgbm as lgb 
import pickle

def get_macro_region(macro):
    if(macro=="lima"):
        return ['DRE LIMA METROPOLITANA','DRE LIMA PROVINCIAS','DRE CALLAO']
    elif(macro=="norte"):
        return ['DRE ANCASH','DRE CAJAMARCA','DRE LA LIBERTAD','DRE LAMBAYEQUE','DRE PIURA','DRE TUMBES']
    elif(macro=="sur"):
        return ['DRE AREQUIPA','DRE CUSCO','DRE MADRE DE DIOS','DRE MOQUEGUA','DRE PUNO','DRE TACNA']   
    elif(macro=="centro"):
        return ["DRE APURIMAC","DRE AYACUCHO","DRE HUANCAVELICA",'DRE HUANUCO','DRE JUNIN','DRE PASCO','DRE ICA']
    elif(macro=="oriente"):
        return ['DRE AMAZONAS','DRE LORETO','DRE SAN MARTIN','DRE UCAYALI']


def get_default_params():
    params = {}
    params['metric']="None" 
    params['first_metric_only']=True 
    params['importance_type']="gain"
    params['use_missing']=True 
    params['zero_as_missing']=False 
    params['n_estimators']=10000
    params['objective']="binary" 
    params['random_state']=1
    params['num_leaves']=15 
    params['feature_fraction']=0.7
    params['bagging_fraction']=0.7
    params['bagging_freq']=1
    params['n_jobs']=4
    return params


def get_fit_params(X_train,y_train,X_test, y_test,fn_eval):
 
    fit_params={"early_stopping_rounds":800, 
                "eval_metric" : fn_eval, 
                "eval_set" : [(X_train,y_train),(X_test,y_test)],
                'eval_names': ['train','test'],
                'verbose': 200,
                'feature_name': 'auto', # that's actually the default
                'categorical_feature': 'auto' # that's actually the default
               }    
    return fit_params


def f1_eval_metric(y_true, y_pred):

    eval_result = f1_score(y_true, y_pred.round())
    return ("f1", eval_result, True)

def precision_eval_metric(y_true, y_pred):

    eval_result = precision_score(y_true, y_pred.round())
    return ("precision", eval_result, True)

def recall_eval_metric(y_true, y_pred):

    eval_result = recall_score(y_true, y_pred.round())
    return ("recall", eval_result, True)

def average_precision_eval_metric(y_true, y_pred):

    eval_result = average_precision_score(y_true, y_pred)
    return ("average_precision", eval_result, True)

def roc_auc_eval_metric(y_true, y_pred):

    eval_result = roc_auc_score(y_true, y_pred)
    return ("roc_auc", eval_result, True)

def get_fn_eval(score_rs):     
    if(score_rs=="f1"):
        fn_eval=f1_eval_metric
    elif(score_rs=="precision"):
        fn_eval=precision_eval_metric
    elif(score_rs=="recall"):
        fn_eval=recall_eval_metric
    elif(score_rs=="average_precision"):
        fn_eval=average_precision_eval_metric  
    elif(score_rs=="roc_auc"):
        fn_eval=roc_auc_eval_metric
    #else:
    #    fn_eval=custom_eval_metric
        
    return fn_eval

#def neg_bagging_fraction_pipeline_model(X_train,y_train,X_test,y_test,X_t,X_t_mas_1,url):
def neg_bagging_fraction_pipeline_model(X_train,y_train,X_test,y_test,url):
    start = time.time()

    N_p = y_train[y_train==1].count()
    N_n = y_train[y_train==0].count()

    alpha = (10000-N_p)/N_n
    params = get_default_params()
    params['pos_bagging_fraction'] = 1
    params['neg_bagging_fraction'] = alpha
    params['scale_pos_weight'] = (alpha*N_n)/N_p

    ###################################################

    model = lgb_model(X_train,y_train,X_test,y_test,params=params)
    save_model(model,url)
    
    predicted_probas = model.predict_proba(X_test) 
    
    
    #predicted_probas_t = model.predict_proba(X_t)
    #y_prob_uno_t = predicted_probas_t[:,1]
        
    #predicted_probas_t_mas_1 = model.predict_proba(X_t_mas_1)
    #y_prob_uno_t_mas_1 = predicted_probas_t_mas_1[:,1]
     
    kpis = print_kpis_rendimiento_modelo(y_test,predicted_probas,url)   
    print_shap_plot(model,X_test,url)
    print("Time elapsed: ", time.time() - start)
    #get_summary_evaluation2(X_test,predicted_probas,y_test,url)
  
    #return kpis , predicted_probas , y_prob_uno_t, y_prob_uno_t_mas_1
    return kpis , predicted_probas 

def print_shap_plot(model,X_test,url_dir):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    #shap.summary_plot(shap_values, X_test)    
    #print(shap_values[0].shape)
    if url_dir is None:
        #shap_values[1] hace referencia a los valores shap de la class 1
        shap.summary_plot(shap_values[1], X_test)
    else:
        fig = shap.summary_plot(shap_values[1], X_test,show=False )
        plt.savefig(url_dir+'/importancia_variables.png', bbox_inches='tight')
        plt.close(fig)      
 
    
def lgb_model(X_train,y_train,X_test,y_test,score_rs='average_precision',params=None):

    fn_eval = get_fn_eval(score_rs)
    fit_params = get_fit_params(X_train,y_train,X_test,y_test,fn_eval)
  
                       
    model = lgb.LGBMClassifier(**params)
    print('---------- definicion del modelo ----------------')
    print(model)
    print('-------------------------------------------------')
    
    model.fit(X_train,y_train,**fit_params)
   
    return model

def lgb_model_rscv(X_train, y_train, X_test, y_test,score_rs='average_precision', params=None,n_iter=None,n_jobs = 4):
    
    print("++++++++++++++++++++++++ INICIO - ESTIMAR MODELO ++++++++++++++++++++++++")   
    fn_eval = get_fn_eval(score_rs)
    fit_params = get_fit_params(X_train,y_train,X_test,y_test,fn_eval)          

    cv_ = get_kfold()          
           
           
    print('RandomizedSearchCV -> Multiples Hyperparametros')
    grid_obj = RandomizedSearchCV(estimator=lgb.LGBMClassifier(),
                                  param_distributions=params,
                                  cv=cv_,
                                  n_iter=n_iter,
                                  refit=True,
                                  return_train_score=False,
                                  scoring = score_rs,
                                  n_jobs = n_jobs,
                                  verbose= True,          
                                  random_state=375)

    grid_obj.fit(X_train, y_train,**fit_params)

    estimator = grid_obj.best_estimator_
    results = pd.DataFrame(grid_obj.cv_results_)
    best_params = grid_obj.best_params_  
    
    print('------------mejores hyperparametros-------------')
    print(best_params)
    print('------------------------------------------------')
    
    return results, estimator , best_params


def custom_bagging_model(X_train,y_train,X_test,y_test,score_rs='average_precision',params=None,alpha=None, 
                         n_iter_rscv=None,K = 1):
    
    
    MIN_N_TRAIN = 10000 #numero minimo de registros para que lgb no sobre ajuste

    N_p = y_train[y_train==1].count()
    N_n = y_train[y_train==0].count()
    
    fn_eval = get_fn_eval(score_rs)
    fit_params = get_fit_params(X_train,y_train,X_test,y_test,fn_eval)
        
    alpha=(MIN_N_TRAIN-N_p)/(N_n) 
    N_n_res = int(round(alpha*N_n,0))
    
    list_model = []
    if(alpha>1):
        print("No existen suficientes registros para realizar el entrenamiento. El número minimo es de ",MIN_N_TRAIN)
        return
    else:
        print("alpha: ",alpha)
    lambda_ = N_p/N_n

    #T = int(round(math.log(0.05)/math.log(1-K*alpha)))
    T,K = get_T_reducido(K,alpha)
    print("T: ",T,"k:",K)

    for i in range(T):
        print("model :",i)

        rus = RandomUnderSampler(random_state=i,sampling_strategy={1:N_p ,0: N_n_res},replacement=False) #majority
        X_res, y_res = rus.fit_resample(X_train, y_train)
        print("total: ",len(y_res),", Class_1: ",y_res[y_res==1].count(),", Class_0: ",y_res[y_res==0].count())
       

        if n_iter_rscv is None:
            if params is None:
                params = get_default_params()   
                
            params['pos_bagging_fraction']=1
            params['neg_bagging_fraction']=1
            params['scale_pos_weight']=(K*alpha*N_n)/N_p
            
            model = lgb_model(X_res,y_res,X_test,y_test,score_rs=score_rs,params=params)  
        else:
            results, model = lgb_model_rscv(X_res, y_res, X_test, y_test,score_rs=score_rs, n_iter=n_iter_rscv)   

        list_model.append(model)
  
    return list_model

def get_T_reducido(K,alpha):
    T = get_T(K,alpha)   
    
    if(T>20):
        K = K +1
        T = get_T(K,alpha)
        
        if(T>20):
            K = K +1
            T = get_T(K,alpha)
            
            if(T>20):
                K = K +1
                T = get_T(K,alpha)
        
        return T, K 
    else:
        return T, K

def get_T(K,alpha):
    T = int(round(math.log(0.05)/math.log(1-K*alpha)))
    return T


def get_kfold():
    n_splits = 10
    kfold = StratifiedKFold(n_splits=n_splits, shuffle=True,random_state=2)
    return kfold

def print_kpis_rendimiento_modelo(y_test,predicted_probas,url_dir):   
    
    y_prob_uno = predicted_probas[:,1]
    y_pred = np.round(y_prob_uno, 0)
    
    #y_pred = np.round(y_prob_uno, 0) se estaba repitiendo
    precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred,average="binary",pos_label=1)
    print(classification_report(y_test, y_pred))
    average_precision = average_precision_score(y_test, y_pred)
    print("average_precision", average_precision)
    
    roc_auc = roc_auc_score(y_test, y_prob_uno)    
    skplt.metrics.plot_roc(y_test, predicted_probas)    
    if url_dir is None:
        plt.show()
    else:
        plt.savefig(url_dir+'/roc_curve.png', bbox_inches='tight')
        plt.close()
    
    return precision, recall, f1 , average_precision , roc_auc




def save_model(model,url_dir):
    filename = url_dir+'/model.sav'    
    if url_dir is None:
        print("")
    else:
        pickle.dump(model, open(filename, 'wb'))   
    
def load_save_model(url_dir):
    filename = url_dir+'/model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model


def get_summary_evaluation2(X,predicted_probas,y,url_dir,modalidad="EBR"):
    y_prob_uno = predicted_probas[:,1]
    y_pred = np.round(y_prob_uno, 0)
    

    X_eval = X.copy()
    #X_eval['PREDICT_PROBA'] = estimator_random.predict_proba(X)[:,1]
    #X_eval['PREDICT'] = estimator_random.predict(X)
    
    X_eval['PREDICT_PROBA'] = y_prob_uno
    X_eval['PREDICT'] = list(y_pred)
    
    

    X_eval['REAL'] =  y

    criteria = [X_eval['PREDICT_PROBA'].between(0,0.1),
                X_eval['PREDICT_PROBA'].between(0.1, 0.2), 
                X_eval['PREDICT_PROBA'].between(0.2, 0.3),
                X_eval['PREDICT_PROBA'].between(0.3, 0.4),
                X_eval['PREDICT_PROBA'].between(0.4, 0.5),
                X_eval['PREDICT_PROBA'].between(0.5, 0.6),
                X_eval['PREDICT_PROBA'].between(0.6, 0.7),
                X_eval['PREDICT_PROBA'].between(0.7, 0.8),
                X_eval['PREDICT_PROBA'].between(0.8, 0.9),
                X_eval['PREDICT_PROBA'].between(0.9,0.95),
                X_eval['PREDICT_PROBA'].between(0.95, 1)
               ]

    values = ['0% - 10%', '10% - 20%', '20% - 30%','30% - 40%',
              '40% - 50%','50% - 60%','60% - 70%','70% - 80%','80% - 90%','90% - 95%','95% - 100%']

    values_index = [1, 2,3,4,5,6,7,8,9,10,11]
    
    ###################################################################
    
    criteria2 = [X_eval['PREDICT_PROBA'].between(0.0, 0.5),
                X_eval['PREDICT_PROBA'].between(0.5, 1),             
               ]

    values2 = ['0% - 50%', '50% - 100%']

    values_index2 = [1, 2]
    
    #####################################################
 
    X_eval['PREDICT_CATEGORY'] = np.select(criteria, values, 0)
    X_eval['PREDICT_CATEGORY_INDEX'] = np.select(criteria, values_index, 0)

    X_eval['PREDICT_CATEGORY2'] = np.select(criteria2, values2, 0)
    X_eval['PREDICT_CATEGORY_INDEX2'] = np.select(criteria2, values_index2, 0)

    X_eval['TOTAL'] = 1     

    
    X_eval['ACIERTO(VP)'] = np.where( (X_eval['REAL']==1) & (X_eval['PREDICT']==1), 1 ,0)
    X_eval['FP'] = np.where( (X_eval['REAL']==0) & (X_eval['PREDICT']==1), 1 ,0)    

    X_eval_gb = X_eval.groupby(['PREDICT_CATEGORY_INDEX','PREDICT_CATEGORY']).agg({'TOTAL':'count','REAL':'sum'}).reset_index()
    X_eval_gb.sort_values(by='PREDICT_CATEGORY_INDEX', ascending=False,inplace=True)
    X_eval_gb.rename(columns={'REAL': 'DESERTORES TEST','TOTAL': 'TOTAL TEST','PREDICT_CATEGORY':'RANGO'}, inplace=True)
    del X_eval_gb['PREDICT_CATEGORY_INDEX']
    X_eval_gb.reset_index(drop=True,inplace=True)

    X_eval_gb['TOTAL TEST %']=round(X_eval_gb['TOTAL TEST']/X_eval_gb['TOTAL TEST'].sum(),3)
    X_eval_gb['COBERTURA %']=round(X_eval_gb['DESERTORES TEST']/X_eval_gb['DESERTORES TEST'].sum(),3)


    X_eval_gb['PRECISION RANGO %']=round(X_eval_gb['DESERTORES TEST']/X_eval_gb['TOTAL TEST'],3)

    
    X_eval_gb['TOTAL TEST %'] = X_eval_gb['TOTAL TEST %']*100 
    X_eval_gb['PRECISION RANGO %'] = X_eval_gb['PRECISION RANGO %']*100 
    X_eval_gb['COBERTURA %'] = X_eval_gb['COBERTURA %']*100 
    
    #X_eval_gb.index.name = 'N'


    # Set colormap equal to seaborns light green color palette


    if url_dir is None:
        cm = sns.light_palette("red", as_cmap=True)
        return (X_eval_gb.style
                        .background_gradient(cmap=cm, subset=['PRECISION RANGO %'])
                        #.format({'TOTAL TEST %': "{:.1%}"})  
                        #.format({'PRECISION RANGO %': "{:.1%}"})
                        #.format({'COBERTURA %': "{:.1%}"})
                       )
    else:
        if(modalidad=="EBR"):
            X_eval_gb.to_excel(url_dir+"/df_agg_t.xlsx", encoding="utf-8")    
            get_min_prob_df(predicted_probas,y,url_dir)
        else:
            X_eval_gb.to_excel(url_dir+"/df_agg_t_{}.xlsx".format(modalidad), encoding="utf-8")  
            
   
'''            
def split_x_y(ID_GRADO,macro_region,modalidad="EBR"):

    lista_regiones = get_macro_region(macro_region)
    list_join_n=[]
    list_join_n_mas_1=[]
    for region in lista_regiones:

        url_dir = "{}/{}/".format(region,ID_GRADO)
        print(url_dir)
        try:
            df_join_n , df_join_n_mas_1 = get_saved_join_data(url_dir,modalidad=modalidad)
        except:
            continue
        
        #df_join_n , df_join_n_mas_1 = get_saved_join_data(url_dir,modalidad=modalidad)
        df_join_n['REGION']= region
        df_join_n_mas_1['REGION']= region
        
        ############tempEEE#######
        df_join_n['D_REGION']= region
        df_join_n_mas_1['D_REGION']= region
        ########################
        
        
        print(region)
        print(df_join_n.DESERCION.value_counts())
        list_join_n.append(df_join_n)
        list_join_n_mas_1.append(df_join_n_mas_1)

    df_join_n = pd.concat(list_join_n)
    df_join_n_mas_1 = pd.concat(list_join_n_mas_1)

    fe_df(df_join_n,df_join_n_mas_1)

    X_train, X_test, y_train, y_test , X_t, X_t_eval, y_eval , ID_P_T,ID_P_T_MAS_1, y = tranform_data(df_join_n,df_join_n_mas_1,False)
    

    return X_train, X_test, y_train, y_test , X_t, X_t_eval, y_eval ,  ID_P_T,ID_P_T_MAS_1 , y
'''    

def get_saved_join_data(url_dir,sub_dir="data",modalidad="EBR"):
    
    if not url_dir:
        url_dir="../02.PreparacionDatos/03.Fusion/reporte_modelo/"+sub_dir+"/"
    else:
        url_dir = '{}/{}'.format("../02.PreparacionDatos/03.Fusion/reporte_modelo/"+sub_dir,url_dir)
        if not os.path.exists(url_dir):
            os.makedirs(url_dir)
        print("reporte generado en : "+url_dir)
    
    if (modalidad=="EBR"):
        specific_url = url_dir+"data.csv"
        specific_url_eval = url_dir+"data_eval.csv"
    else:
        specific_url = url_dir+"data_{}.csv".format(modalidad)
        specific_url_eval = url_dir+"data_eval_{}.csv".format(modalidad)        
    
    dt = {'COD_MOD':str,'COD_MOD_T':str,'ANEXO':int,'ANEXO_T':int,'EDAD':int,
          'N_DOC':str,'COD_MOD_T_MENOS_1':str,
          'ANEXO_T_MENOS_1':int,'NUMERO_DOCUMENTO_APOD':str,'ID_PERSONA':int}

    df=pd.read_csv(specific_url,dtype=dt, encoding="utf-8") 
    df_eval=pd.read_csv(specific_url_eval,dtype=dt, encoding="utf-8") 
    
    return df,df_eval

            
def get_min_prob_df(predicted_probas,y_test,url_dir):

    y_prob_uno = predicted_probas[:,1]
    y_pred = np.round(y_prob_uno, 0)

    df = pd.DataFrame()
    df['y_prob_uno']  = y_prob_uno
    df['y_pred']  = y_pred
    df['y_test']  = list(y_test)  
    df.sort_values(by=['y_prob_uno'],ascending=False,inplace=True)
    #print(df.head(20))
    total_deser = np.sum(y_test)  


    list_y_true = []
    list_y_pred = []
    list_precision = []
    prob_min = 0
    t_test_min = 0
    prec = 0 
    for index, row in df.iterrows(): 
        list_y_true.append(row['y_test'])
        list_y_pred.append(row['y_pred'])
        pr = precision_score(list_y_true, list_y_pred, average='binary')
        list_precision.append(pr)
        if(pr<1):
            break
        else:
            prob_min = row['y_prob_uno']
            t_test_min = len(list_y_true)
            prec = pr


    df_min = pd.DataFrame()
    df_min['PROB MIN']  = [prob_min]
    df_min['TOTAL DESERTORES TEST RANGO']  = [t_test_min]
    df_min['TOTAL DESERTORES TEST']  = [int(total_deser)]
    df_min['PRECISION RANGO %']  = [int(prec*100)]
    #return df_min
    
    df_min.to_excel(url_dir+"/df_agg_t_min.xlsx", encoding="utf-8")
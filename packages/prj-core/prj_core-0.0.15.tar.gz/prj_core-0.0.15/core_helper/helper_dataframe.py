import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets

def reduce_mem_usage(df,category=False):
    """ iterate through all the columns of a dataframe and modify the data type
        to reduce memory usage.        
    """
    start_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            if category:
                df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    
    return df


def heatmap_nan(X=None):
    plt.figure(figsize = (16,5))
    sns.heatmap(X.isnull(), cbar=False)

def two_d(array):    
    np_array = np.array(array)    
    if(np_array.ndim==1):
        np_array=np_array.reshape(len(np_array),1)
    return np_array

            
def show_na(df):
    total = len(df)
    lista_nan_column = []
    for column in df.columns:
        total_na = df[column].isna().sum()
        per = total_na/total
        if(total_na>0):
            print(column+" : "+str(total_na)+ ", frac: "+str(total_na)+"/"+str(total) +" , per: "+str(per))
            lista_nan_column.append(column)
    return lista_nan_column

def get_cat_columns(X):    
    _cols = X.columns
    _num_cols = X._get_numeric_data().columns
    _categorical_columns_name = list(set(_cols) - set(_num_cols))
    return _categorical_columns_name


# Generate dataset with 1000 samples, 100 features and 2 classes
def generate_dataset(n_samples=10000, n_features=100, n_classes=2, random_state=42,df=True):  
    X, y = datasets.make_classification(
        n_features=n_features,
        n_samples=n_samples,  
        n_informative=int(0.6 * n_features),    # the number of informative features
        n_redundant=int(0.0 * n_features),      # the number of redundant features
        n_repeated=int(0.0 * n_features), # the number of repeated features
        n_classes=n_classes, 
        random_state=random_state)
    
    if(df==True):
        df=pd.DataFrame(data=X[0:,0:],  index=[i for i in range(X.shape[0])],
                columns=['f'+str(i) for i in range(X.shape[1])])
        return (df, y)
    else:
        return (X, y)   
    
import numpy as np
import pandas as pd
import os
from sklearn.metrics import mean_absolute_error

class Data:
    '''
    General data class for ML analysis of dengue fever.
    Note, all functions are in-place. To create a new copy
    of a class instance, use deepcopy(class_instance).
    
    Functions that begin with an underscore are internal
    functions, and are typically designed to be called by other
    class functions, not by the runtime user.
    '''
    def __init__(s,directory=None):
        if type(directory) == type(None):
            s.read_data('../data')
        else:
            s.read_data(directory)
        s.cities = ['sj','iq']
        s.loaded_to_array = 0
        
        # For keeping track of applied transformations.
        s._internal_trans_list  = []
        s._internal_kwargs_list = []
        
        s._pred_reverse_trans_list  = []
        s._pred_reverse_kwargs_list = []
        
        return
    
    def read_data(s,directory):
        '''
        s._df_valid is not the same as s.df_valid
        The leading underscore indicates that this is a 
        temporary, internal variable. The one to access is
        s.df_valid, which is a dictionary of frames created
        by split_data, which separates out the two cities.
        '''
        
        s.df      = pd.read_csv(os.path.join(directory,'dengue_features_train.csv'))
        s.y_tr    = pd.read_csv(os.path.join(directory,'dengue_labels_train.csv'))
        s._df_valid = pd.read_csv(os.path.join(directory,'dengue_features_test.csv'))
        
        s.df['total_cases'] = s.y_tr['total_cases'] / 1
        del(s.y_tr)
        
        s.df['time'] = s.df.index
        s.df.loc[(s.df['city']=='iq'), 'time'] -= s.df[s.df['city']=='iq'].index.min()
        
        s.df['cat_cases'] = 0
        s.df.loc[(s.df['total_cases']>10),'cat_cases']=1
        s.df.loc[(s.df['total_cases']>40),'cat_cases']=2
        
        s.df = s.df.fillna(method='ffill')
        
        s.df_original = s.df.copy()
        return
    
    def split_data(s, tr_frac=0.7, randomise=False, seed=None):
        train_cut = int(len(s.df)*tr_frac)
        
        if randomise:
            pass
        
        s.df_train = {}
        s.df_testt = {}
        s.df_valid = {}
        
        for city in s.cities:
            s.df_train[city] = s.df[s.df['city']==city][:train_cut]
            s.df_testt[city] = s.df[s.df['city']==city][:train_cut]
            s.df_valid[city] = s.df[s.df['city']==city]
        return 
    
    def unsplit(s):
        s.df = pd.concat([
            df_train['sj'],
            df_train['iq'],
            df_testt['sj'],
            df_testt['iq']
        ])
        return
        
    def transform(s, trans_list, kwargs_list={}, direction='for', reversible_preds=0):
        '''
        The recommended way to use this function is with no arguments.
        This will automatically undo all applied functions in reverse order,
        then flush the transformations list.
        
        If you mix manual and automatic transformation reversal then the automatic
        reversal may not work, and you will be left with an incorrectly transformed
        dataframe.
        '''
        if type(trans_list)==type(None) and direction=='inv':
            trans_list  = s._internal_trans_list
            kwargs_list = s._internal_kwargs_list
            s.transform(trans_list[::-1], kwargs_list[::-1], direction='inv')
            s._internal_trans_list  = []
            s._internal_kwargs_list = []
        
        if type(trans_list)!=type([]):
            trans_list = [trans_list]
        if type(kwargs_list)!=type([]):
            kwargs_list = [kwargs_list]
        
        if reversible_preds==0:
            s._internal_trans_list.extend(trans_list)
            s._internal_kwargs_list.extend(kwargs_list)
        else:
            s._pred_reverse_trans_list.extend(trans_list)
            s._pred_reverse_kwargs_list.extend(kwargs_list)
            
        if type(kwargs_list)!=type(None) and len(kwargs_list)!=len(trans_list):
            print('Error in options list')
            raise 
            
        for trans,kwargs in zip(trans_list,kwargs_list):
            trans(s,direction,**kwargs)
        return 
    
    def df_to_arr(s):
        '''
        To avoid having 2 copies of every array for the two cities,
        I have made all relevant arrays into dicts of two arrays.
        e.g. s.X_train_full['sj'] is the full train matrix for SJ, and
        s.X_train_full['iq'] is for IQ.
        '''
        s.cities = ['sj','iq']
        
        s.arr_X_train = {}
        s.arr_y_train = {}
        
        s.arr_X_testt = {}
        s.arr_y_testt = {}
        
        s.arr_X_valid = {}
        
        # Concatenation of train and testt, for testing on all available
        # data before estimating valid.
        s.arr_X_train_full = {}
        s.arr_y_train_full = {}
        
        for city in s.cities:
            X_cols = [c for c in s.df_train[city].columns if c not in ['total_cases', 'week_start_date', 'city'] ]
            
            s.arr_X_train[city] = s.df_train[city][X_cols].values
            s.arr_y_train[city] = s.df_train[city]['total_cases'].values

            s.arr_X_testt[city]  = s.df_testt[city][X_cols].values
            s.arr_y_testt[city]  = s.df_testt[city]['total_cases'].values

            s.arr_X_valid[city] = s.df_train[city][X_cols].values
            
            s.arr_X_train_full[city] = np.concatenate([s.arr_X_train[city],s.arr_X_testt[city]],0)
            s.arr_y_train_full[city] = np.concatenate([s.arr_y_train[city],s.arr_y_testt[city]],0)
        
        s.loaded_to_array = 1
        return

class Modelplus:
    def init_parent(s):
        # This checks that the child class has set up the models correctly
        if type(s.models)==type(None) or not ('sj' in s.models.keys() and 'iq' in s.models.keys()):
            print('''
            Overwrite this function with the child class. Or, 
            call Modelplus with an argument of a model.
            Child class's __init__ must create an attribute 
            called s.models, typically by calling an 
            sklearn or keras model. However, these may also be 
            custom-defined. s.models = {s.model_sj, s.model_iq}.
            ''')
        s.cities = ['sj','iq']
        
        s.mae_train_cities = {}
        s.mae_testt_cities = {}
        
        s.mae_train_total = 0
        s.mae_testt_total = 0
        
        s.preds_train = {}
        s.preds_testt = {}
        s.preds_valid = {}
        return
    
    def _check_loaded(s,data):
        if data.loaded_to_array == 0:
            data.df_to_arr()
        return
    
    def fit(s,data,mode='sub'):
        '''
        Mode here can be "sub" to train on the train set, for testing on testt, 
        or "full", to train on train+testt, to test on valid.
        '''
        s._check_loaded(data)
        
        for city in s.cities:
            if mode.lower() in ['sub','s']:
                s.models[city].fit(data.arr_X_train[city] , data.arr_y_train[city])
            elif mode.lower() in ['full','f']:
                s.models[city].fit(data.arr_X_train_full[city] , data.arr_y_train_full[city])
        return
    
    def undo_pred_transforms(s,data,preds):
        _temp_preds = preds.copy()
        for trans,kwargs in zip(data._pred_reverse_trans_list[::-1],data._pred_reverse_kwargs_list[::-1]):
            _temp_preds = trans(data=data,directions='pr',preds=_temp_preds,**kwargs)
        return _temp_preds
    
    def predict(s,data,mode='test'):
        s._check_loaded(data)
        for city in s.cities:
            if mode.lower() in ['test','testt','t']:
                s.preds_testt[city] = s.models[city].predict(data.arr_X_testt[city])
                s.preds_testt[city] = s.undo_pred_transforms(data,s.preds_testt[city])
                s.mae_testt_cities[city] = mean_absolute_error(data.arr_y_testt[city], s.preds_testt[city])
            elif mode.lower() in ['val','valid','v']:
                s.preds_valid[city] = s.models[city].predict(data.arr_X_valid[city])
                s.preds_valid[city] = s.undo_pred_transforms(data,s.preds_valid[city])
            else:
                print('Error')
                return
            
        if mode.lower() in ['test','testt','t']:
            s._l_sj = len(data.arr_X_testt['sj'])
            s._l_iq = len(data.arr_X_testt['iq'])
            
            s.mae_testt_total = (
                s._l_sj*s.mae_testt_cities['sj'] + 
                s._l_iq*s.mae_testt_cities['iq']
            ) / (s._l_sj + s._l_iq)
            return s.preds_testt
        
        elif mode.lower() in ['val','valid','v']:
            return s.preds_valid
    
    def valid_to_file(s,data):
        s._check_loaded(data)
        pass
    
    def plotting_funcs(s,data):
        s._check_loaded(data)
        pass
    
def ensemble_fit(data,model_list):
    pass

def hyperparam_fit(data,model_list):
    pass

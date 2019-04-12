import numpy as np

def logdist_labels(data,direction='for',preds=None):
    if direction in ['f', 'for', 'forward']:
        for city in data.cities:
            data.df_train[city]['total_cases'] = np.log(data.df_train[city]['total_cases']+1)
            data.df_testt[city]['total_cases'] = np.log(data.df_testt[city]['total_cases']+1)
        return
    if direction in ['i', 'inv', 'inverse']:
        for city in data.cities:
            data.df_train[city]['total_cases'] = np.exp(data.df_train[city]['total_cases'])-1
            data.df_testt[city]['total_cases'] = np.exp(data.df_testt[city]['total_cases'])-1        
        return 
    if direction in ['p','pr','preds','predreverse','pred_reverse']:
        outs = preds.copy()
        for city in data.cities:
            for i in range(len(outs)):
                outs[i] = np.exp(outs[i])-1
        return outs
                

def remove_avg(data,direction='for',preds=None):
    '''
    Each label is transformed to be the difference of that label's value about the average.
    '''
    if direction in ['f', 'for', 'forward']:
        data._remove_avg_averages = {}
        for city in data.cities:
            data._remove_avg_averages[city] = data.df_train[city].groupby('weekofyear').agg({'total_cases':np.mean}).to_dict()['total_cases']
            for i in range(len(data.df_train[city])):
                data.df_train[city].loc[i,'total_cases'] -= data._remove_avg_averages[city][data.df_train[city].loc[i,'weekofyear']]
            for i in range(len(data.df_testt[city])):
                data.df_testt[city].loc[i,'total_cases'] -= data._remove_avg_averages[city][data.df_testt[city].loc[i,'weekofyear']]
        return
    if direction in ['i', 'inv', 'inverse']:
        for city in data.cities:
            for i in range(len(data.df_train[city])):
                data.df_train[city].loc[i,'total_cases'] += data._remove_avg_averages[city][data.df_train[city].loc[i,'weekofyear']]
            for i in range(len(data.df_testt[city])):
                data.df_testt[city].loc[i,'total_cases'] += data._remove_avg_averages[city][data.df_testt[city].loc[i,'weekofyear']]
        return 
    if direction in ['p','pr','preds','predreverse','pred_reverse']:
        outs = preds.copy()
        for city in data.cities:
            for i in range(len(outs)):
                outs[i] += data._remove_avg_averages[city][data.df_valid[city].loc[i,'weekofyear']]
        return outs
                
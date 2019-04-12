def logdist_labels(data,direction='for',preds=None):
    pass

def remove_avg(data,direction='for',preds=None):
    '''
    Each label is transformed to be the difference of that label's value about the average.
    '''
    if direction in ['f', 'for', 'forward']:
        data._remove_avg_averages = {}
        for city in data.cities:
            data._remove_avg_averages[city] = data.df_train['sj'].groupby('weekofyear').agg({'total_cases':sum}).to_dict()['total_cases']
            for i in range(len(data.df_train[city])):
                data.df_train[city].loc[i,'total_cases'] /= data._remove_avg_averages[city][data.df_train[city].loc[i,'weekofyear']]
            for i in range(len(data.df_testt[city])):
                data.df_testt[city].loc[i,'total_cases'] /= data._remove_avg_averages[city][data.df_testt[city].loc[i,'weekofyear']]
    return
    if direction in ['i', 'inv', 'inverse']:
        for city in data.cities:
            for i in range(len(data.df_train[city])):
                data.df_train[city].loc[i,'total_cases'] *= data._remove_avg_averages[city][data.df_train[city].loc[i,'weekofyear']]
            for i in range(len(data.df_testt[city])):
                data.df_testt[city].loc[i,'total_cases'] *= data._remove_avg_averages[city][data.df_testt[city].loc[i,'weekofyear']]
    return 
    if direction in ['p','pr','preds','predreverse','pred_reverse']:
        outs = {
            'sj':preds['sj'].copy(),
            'iq':preds['iq'].copy(),
        }
        for city in data.cities:
            for i in range(len(data.df_valid[city])):
                outs[i] *= data._remove_avg_averages[city][data.df_valid[city].loc[i,'weekofyear']]
        return outs
                
def trans_divk(data,direction='for',k=40,col='station_max_temp_c'):
    if direction.lower() in ['f', 'for', 'forward']:
        for city in data.cities:
            data.df_train[city].loc[:,col] /= k
            data.df_testt[city].loc[:,col] /= k
            data.df_valid[city].loc[:,col] /= k
            
    elif direction.lower() in ['i', 'inv', 'inverse']:
        for city in data.cities:
            data.df_train[city].loc[:,col] *= k
            data.df_testt[city].loc[:,col] *= k
            data.df_valid[city].loc[:,col] *= k

def sqrtdist_labels(data,direction='for',preds=None):
    
    frwrd = ['f', 'for', 'forward']
    invrs =  ['i', 'inv', 'inverse']
    prds = ['p','pr','preds','predreverse','pred_reverse']
    
    if direction not in [frwrd + invrse + prds]:
        print("Invalid direction,")
    
    if direction in frwrd:
        for city in data.cities:  
            data.df_train[city]['total_cases'] = np.sqrt(data.df_train[city]['total_cases'])
            data.df_testt[city]['total_cases'] = np.sqrt(data.df_testt[city]['total_cases'])     
            data.df_train[city].rename(columns = {'total_cases':'sqrt_total_cases'}, inplace = True)
            data.df_testt[city].rename(columns = {'total_cases':'sqrt_total_cases'}, inplace = True)
        return
    
    if direction in invrs:
        for city in data.cities:
            data.df_train[city]['sqrt_total_cases'] = np.square(data.df_train[city]['sqrt_total_cases'])
            data.df_testt[city]['sqrt_total_cases'] = np.square(data.df_testt[city]['sqrt_total_cases'])            
            data.df_train[city].rename(columns = {'sqrt_total_cases':'total_cases'}, inplace = True)
            data.df_testt[city].rename(columns = {'sqrt_total_cases':'total_cases'}, inplace = True)
        return 
    
    if direction in prds:
        outs = preds.copy()
        for city in data.cities:
            for i in range(len(outs)):
                outs[i] = np.square(outs[i])
        return outs    

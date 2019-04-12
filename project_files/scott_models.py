from general_funcs import Modelplus
        
class MP_NN(Modelplus):
    def __init__(s,kwargs_sj={},kwargs_iq={}):
        from sklearn.neural_network import MLPRegressor
        s.models = {}
        s.models['sj'] = MLPRegressor(**kwargs_sj)
        s.models['iq'] = MLPRegressor(**kwargs_iq)
        
        s.init_parent() # All model classes must include this line
        return
    
class MP_RF(Modelplus):
    def __init__(s,kwargs_sj={},kwargs_iq={}):
        from sklearn.ensemble import RandomForestRegressor
        s.models = {}
        s.models['sj'] = RandomForestRegressor(**kwargs_sj)
        s.models['iq'] = RandomForestRegressor(**kwargs_iq)
        
        s.init_parent() # All model classes must include this line
        return
        
class MP_CatBoost(Modelplus):
    def __init__(s,kwargs_sj={},kwargs_iq={}):
        from catboost import CatBoostRegressor
        s.models = {}
        s.models['sj'] = CatBoostRegressor(**kwargs_sj)
        s.models['iq'] = CatBoostRegressor(**kwargs_iq)
        
        s.init_parent() # All model classes must include this line
        return
    
class MP_VAR(Modelplus):
    def __init__(s,kwargs_sj={},kwargs_iq={}):
        pass
    
        s.init_parent() # All model classes must include this line
        return
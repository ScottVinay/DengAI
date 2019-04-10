from general_funcs import Modelplus
        
class MP_NN(Modelplus):
    def __init__(s,kwargs_sj={},kwargs_iq={}):
        from sklearn.neural_network import MLPRegressor
        s.models = {}
        s.models['sj'] = MLPRegressor(**kwargs_sj)
        s.models['iq'] = MLPRegressor(**kwargs_iq)
        
        s.init_parent() # All model classes must include this line
        
        return
        
    
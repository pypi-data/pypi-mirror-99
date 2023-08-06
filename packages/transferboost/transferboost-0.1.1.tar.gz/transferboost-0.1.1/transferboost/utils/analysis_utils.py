import numpy as np
from functools import reduce

def plot_proba_evol(X,y,model, max_n_trees=500):
    arrays = list()
    for ix in range(1,max_n_trees+1):
        try:
            pred_ix = model.predict_proba(X, num_iteration=ix)[:,1]
        except:
            pred_ix = model.predict_proba(X, ntree_limit=ix)[:,1]
        arrays.append(pred_ix)
    return np.transpose(reduce(lambda x,y: np.vstack((x,y)),arrays))        
        
    
def find_pred_trend(X,y,model, max_n_trees = 500):
    
    proba_trees = plot_proba_evol(X,y,model, max_n_trees=max_n_trees)
    
#     return proba_trees
    
    mean_y_0 = proba_trees[y.values==0].mean(axis=0)
    std_y_0 = proba_trees[y.values==0].std(axis=0)

    mean_y_1 = proba_trees[y.values==1].mean(axis=0)
    std_y_1 = proba_trees[y.values==1].std(axis=0)
    
    return mean_y_0, std_y_0, mean_y_1, std_y_1
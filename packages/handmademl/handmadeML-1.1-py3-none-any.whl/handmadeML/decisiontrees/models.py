'''This module contains decision trees models'''

#import numpy as np
import pandas as pd

from .utils import node_construction, node_navigation
#from ..common.utils import compute_metric
#from ..optimizers.adam import AdamOptimizer

class DecisionTreeClassifier ():
    '''equivalent to sklearn with limited options:
    handles numerical data only
    criterion : gini only
    splitter  : best only
    max_depth : None only (nodes are expanded until
         all leaves are pure or until all leaves
         contain less than min_samples_split samples
    min_samples_split : integers only
         (fraction of n_samples not supported)
    min_samples_leaf : 1 only
         (only the min_samples_splits criterions
         stops the growth of the tree)
    min_weight_fraction_leaf : 0 only
    max_features :None only (all features)
    max_leaf_nodes : None only (unlimited)
    min_impurity_decrease : 0 only
    min_impurity_split : 0 only
    '''
    def __init__(self, max_depth=10000, min_samples_split=2):
        self.max_depth=max_depth
        self.min_samples_split=min_samples_split
        self.tree={'level':0,
                   'type':'root',
                   'gini':None,
                   'samples_count':None,
                   'feature':None,
                   'threshold':None,
                   'left':None,
                   'right':None,
                   }

    def fit(self, X_train, y_train):
        '''y_train : pd.Series. If DataFrame, the 1st column will be used as target
           X_train : DataFrame or 2D array'''
        if isinstance(y_train,pd.core.frame.DataFrame):
            y_train=y_train.iloc[:,0]
        X_train=pd.DataFrame(X_train)
        self.tree['gini']=1-((y_train.groupby(y_train).count()/y_train.count())**2).sum()
        self.tree['samples_count']=y_train.count()

        node_construction(self.tree, X_train, y_train,
                          max_depth=self.max_depth,
                          min_samples_split=self.min_samples_split)

    def predict(self, X_test):
        X_test=pd.DataFrame(X_test)
        return X_test.apply(lambda x: node_navigation(self.tree, x), axis=1)

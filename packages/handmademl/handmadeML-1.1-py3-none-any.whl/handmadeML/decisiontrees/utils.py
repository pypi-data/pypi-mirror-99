'''This module contains all functions needed for
the decision trees'''

#import pandas as pd
import numpy as np

## Functions

def node_construction(subtree,subX,suby,max_depth,min_samples_split):
    '''This recursive function is called by the fit method of
    dicision tree classifier

    Function for building the building the next left and right
    subnodes/leafs (and the associated subsplits of the dataset,
    depending of the current node and the associated dataset'''
    splits={}
    for index,col in subX.iteritems():
        splits[index]=np.sort(col.sample(1000,replace=True).unique())
        splits[index]=((splits[index][1:]+splits[index][:-1])/2).tolist()
    splits=[[(key,threshold) for threshold in value] for key,value in splits.items()]
    splits=[y for x in splits for y in x]

    ginis=[]
    ginis_left=[]
    ginis_right=[]
    counts_left=[]
    counts_right=[]
    for split in splits:
        mask=subX[split[0]]<split[1]
        y_left=suby[mask]
        y_right=suby[-mask]
        count_left=y_left.count()
        counts_left.append(count_left)
        count_right=y_right.count()
        counts_right.append(count_right)
        gini_left =1-((y_left.groupby( y_left).count()/ count_left)**2 ).sum()
        ginis_left.append(gini_left)
        gini_right=1-((y_right.groupby(y_right).count()/count_right)**2).sum()
        ginis_right.append(gini_right)
        gini_weighted= (y_left.count()*gini_left + y_right.count()*gini_right)/subtree['samples_count']
        ginis.append(gini_weighted)
    print(splits)
    print(ginis)

    best_split_index=ginis.index(min(ginis))
    best_split=splits[best_split_index]
    subtree['feature']=best_split[0]
    subtree['threshold']=best_split[1]
    left_gini  =ginis_left  [best_split_index]
    right_gini =ginis_right [best_split_index]
    left_count =counts_left [best_split_index]
    right_count=counts_right[best_split_index]
    mask=subX[best_split[0]]<best_split[1]
    y_left=suby[mask]
    y_right=suby[-mask]

    if left_gini < subtree['gini'] and\
      left_count >= min_samples_split and\
      subtree['level'] < max_depth and\
      left_gini > 0:
        X_left=subX[mask]
        subtree['left'] = {'level':subtree['level']+1,
                           'type':'node',
                           'gini':left_gini,
                           'samples_count':left_count,
                           'feature':None,
                           'threshold':None,
                           'left':None,
                           'right':None,
                           }
        node_construction(subtree['left'], X_left, y_left,     #recursion
                       max_depth=max_depth,
                       min_samples_split=min_samples_split)
    else:
        subtree['left'] = {'level':subtree['level']+1,
                           'type':'leaf',
                           'gini':left_gini,
                           'samples_count':left_count,
                           'category':y_left.mode()}

    if right_gini < subtree['gini'] and\
      right_count >= min_samples_split and\
      subtree['level'] < max_depth and\
      right_gini > 0:
        X_right=subX[-mask]
        subtree['right'] = {'level':subtree['level']+1,
                           'type':'node',
                           'gini':right_gini,
                           'samples_count':right_count,
                           'feature':None,
                           'threshold':None,
                           'left':None,
                           'right':None,
                           }
        node_construction(subtree['right'], X_right, y_right,   #recursion
                       max_depth=max_depth,
                       min_samples_split=min_samples_split)
    else:
        subtree['right'] = {'level':subtree['level']+1,
                           'type':'leaf',
                           'gini':right_gini,
                           'samples_count':right_count,
                           'category':y_right.mode()[0]}

def node_navigation(subtree, X_sample):
    '''This recursive function is called by the decision tree
    predict method
    X_sample : pd series (one single sample) with features as index'''
    if subtree['type']=='leaf':
        return subtree['category']
    feature=subtree['feature']
    if feature not in X_sample.index:
        raise ValueError(f'tree grown using feature {feature},\
which is not found in the columns of X')
    if X_sample[feature]>subtree['threshold']:
        return node_navigation(subtree['right'], X_sample)   #recursion
    return node_navigation(subtree['left'], X_sample)        #recursion

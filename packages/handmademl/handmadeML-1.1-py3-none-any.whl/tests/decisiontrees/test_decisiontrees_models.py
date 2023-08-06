import unittest

#import sys
#sys.path.append('../')
import pandas as pd


from handmadeML.decisiontrees.models import *


#---------------------------------------------------------------------------
## ttests for method predict
#---------------------------------------------------------------------------
class Test_predict(unittest.TestCase):

  def test_predict_method_behaviour(self):
    dtc=DecisionTreeClassifier(min_samples_split=10)
    dtc.tree={'level': 0,
             'type': 'root',
             'feature': 'aa',
             'threshold': 0.5,
             'left': None,
             'right': None}
    dtc.tree['left']={'level': 1,
                 'type': 'root',
                 'feature': 'bb',
                 'threshold': 0.5,
                 'left': {'level':2,'type':'leaf','category':1},
                 'right': {'level':2,'type':'leaf','category':0}}
    dtc.tree['right']={'level':1,
                  'type':'leaf',
                  'category':1}
    X_test=pd.DataFrame({'aa':[0.1,0.2,0.7],'bb':[1,0,1],'cc':[1,1,0]})
    prediction = dtc.predict(X_test)
    self.assertTrue((prediction==pd.Series([0,1,1])).all(),\
        f"uncorrect predict method. returned {prediction}, expected [0,1,1]")

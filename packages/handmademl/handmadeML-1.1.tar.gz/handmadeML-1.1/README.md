# handmadeML
This package is created to merge to sub-projects : handmade-neural-network and handmade-machine-learning
The components and logics from both projects should converge

# Objective
This is a personal challenge : re-code all the components of machine learning and deep learning algos

## The code is inspired by the logic of sklaern and keras, but is much simpler:
  - common terminology and workflow (model instanciation, model.fit, model.predict etc..) but simplified (no .compile method for instance)
  - less features implemented
  - less checks, exceptions, tricky cases allowed, etc.
  - probably much less computionaly efficient

## Implemented so far:
### linear classifier :
  - loss options : hinge, squared_hinge (for SVC) and logit (for Logistic regression)
  - penalty options : l1,l2
  - kernel : only linear

### decision trees
  - decion tree classifier

### neuralnets
  - dense networks only
  - 5 activation functions:
    - relu, tanh (mostly for hidden layers)
    - linear (for regression output)
    - sigmoid, softmax (for classifiction outputs)
  - 4 loss functions:
    - mse, mae (for regression tasks)
    - binary crossentropy (for binary classification tasks)
    - multiclass crossentropy (for multiclassification)
  - gradient descent with back-propagation
  - simple GrandientDescent optimizer only
    - stochastic or mini-batch
    - adjustable learning rate
    - without momentum
  - metric computation at the end of each batch/epoch for monitoring during training
    - only loss functions
  - weights and bias initializers : zeros, ones and glorot_uniform only

  - a pedagogical notebook in the notebooks folder contains a guided implementation, step by step, of a simple neural network, equivalent to the Tensorflow Playgroung

## To be coded later :
### linear classifier :
  - kernel trick with simple kernels : polynomials, rbf
  - create a pedagogical tutorial notebook about linear SVC

### decision trees :
  - regression trees

### ensemble methods and other optmization methods :
  - bagging
  - boosting
  - cross validation
  - grid search
  - randomized search

### neuralnets :
  - regularization:
     - l1, l2, elasticnet
     - on kernels (weights)

  - early stopping on validation data
  - training history tracking
  - momentum for SGD optimizer
  - other metrics (accuracy, roc_auc, etc.)
  - other optimizers
    - adam

## To be coded much later :
### linear models :
  - more for svm :
    - Linear SV regressors
    - more hinge options
    - more kernels
 - regressors with ridge/lasso/elasticnet

### neuralnets :
  - dropout
  - regularization on biais and activity of the neurons
  - other optimizers
    - rmsprop

### usupervised models :
  - k-mean
  - pca


## To be probably never coded :
### neuralnets :
  - padding
  - CNN specifics:
    - conv2D layers
    - kernels
    - max pooling layers
    - flatting layer
  - RNN specifics:
    - simple RNN layer
    - masking layer
    - LSTM layer


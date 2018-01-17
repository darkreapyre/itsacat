# Necessay Libraries
import numpy as np
import datetime
import matplotlib.pyplot as plt
import h5py
import scipy
import json
from json import dumps, loads
from boto3 import client, resource, Session
import botocore

# Global Variables
rgn = None
s3_client = client('s3', region_name=rgn) # S3 access
s3_resource = resource('s3')

def load_data():
    test_dataset = h5py.File('datasets/test_catvnoncat.h5', "r")
    test_set_x_orig = np.array(test_dataset["test_set_x"][:]) # your test set features
    test_set_y_orig = np.array(test_dataset["test_set_y"][:]) # your test set labels
    classes = np.array(test_dataset["list_classes"][:]) # the list of classes
    test_set_y_orig = test_set_y_orig.reshape((1, test_set_y_orig.shape[0]))
    
    return test_set_x_orig, test_set_y_orig, classes

def sigmoid(z):
    """
    Computes the sigmoid of z

    Arguments:
    z -- A scalar or numpy array of any size

    Return:
    sigmoid(z)
    """
    return 1. / (1. + np.exp(-z))

def relu(z):
    """
    Implement the ReLU function.

    Arguments:
    z -- Output of the linear layer, of any shape

    Returns:
    a -- Post-activation parameter, of the same shape as z
    """
    a = np.maximum(0, z)
    # Debug statement
    #assert(a.shape == z.shape)
    return a

def forward_prop(input, params, layers, activations):
    """
    Executes the Forward Propogation step.
    
    Arguments:
    input -- Input data of shape (No. features, No. training examples)
    params -- Trained Weights and Bias
    layers -- Numer of hidden layers in the trained neural network
    activations -- Activation function for each layer
    """
    A_prev = input
    results = []
    for l in range(1, layers+1):
        W = params['W'+str(l)]
        b = params['b'+str(l)]
        Z = np.dot(W, A_prev) + b
        if activations['layer'+str(l)] == 'relu':
            A_prev = realu(Z)
        if activations['layer'+str(l)] == 'sigmoid':
            A_prev = sigmoid(Z)
        results.append('A': A_prev)
    output = results[-1]['A']
    return output

def predict(X, NN_parameters, trained_parameters):
    """
    Applies the Forward Propogation step with optmized paramters to the input data.
    Compares the output to the labeled data to determine classification with a
    threshold of 0.5.
    
    Arguments:
    X -- Input data of any shape
    Y -- Labels of shape (1, no.examples)
    
    Returns:
    Y_pred -- The predicted label
    """
    # Run Forward Propagation on the input data
    layers = NN_parameters['layers']
    activations = NN_parameters['activations']
    output = forward_prop(X, trained_parameters, layers, activations)
    decision_boundry = np.vectorize(lambda x: 1 if x > 0.5 else 0)
    Y_pred = decision_boundary(output)
    return Y_pred

def print_mislabeled_images(classes, X, y, p):
    """
    Plots images where predictions and truth were different.
    X -- dataset
    y -- true labels
    p -- predictions
    """
    a = p + y
    mislabeled_indices = np.asarray(np.where(a == 1))
    plt.rcParams['figure.figsize'] = (40.0, 40.0) # set default size of plots
    num_images = len(mislabeled_indices[0])
    for i in range(num_images):
        index = mislabeled_indices[1][i]
        
        plt.subplot(2, num_images, i + 1)
        plt.imshow(X[:,index].reshape(64,64,3), interpolation='nearest')
        plt.axis('off')
        plt.title("Prediction: " + classes[int(p[0,index])].decode("utf-8") + " \n Class: " + classes[y[0,index]].decode("utf-8"))
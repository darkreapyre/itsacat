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

def forward_prop(X, parameters):

def predict(X, Y, NN_parameters, trained_parameters):
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
    A = forward_prop(X, NN_parameters, trained_parameters)

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
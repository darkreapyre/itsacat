import numpy as np
def sigmoid(z):
    return 1. / (1.+np.exp(-z))

def relu(Z):
    A = np.maximum(0,Z)
    return A

class DNN():
    def __init__(self, layers_dims, activations):
        self.layers_dim = layers_dim
        self.__num_layers = len(layers_dims)
        self.activations = activations
        self.input_size = layers_dims[0]
        """
        Note: Change this!
        self.parameters = self.__parameters_initializer(layers_dims)
        """
        self.output_size = layers_dims[-1]
"""
    def __parameters_initializer(self, layers_dims):
        # special initialzer with np.sqrt(layers_dims[l-1])
        L = len(layers_dim)
        parameters = {}
        for l in range(1, L):
            parameters['W'+str(l)] = np.random.randn(layers_dim[l], layers_dim[l-1]) / np.sqrt(layers_dim[l-1])
            parameters['b'+str(l)] = np.zeros((layers_dim[l], 1))
        return parameters
"""

    def __one_layer_forward(self, A_prev, W, b, activation):
        Z = np.dot(W, A_prev) + b
        if activation == 'sigmoid':
            A = sigmoid(Z)
        if activation == 'relu':
            A = relu(Z)
        if activation == 'leaky_relu':
            A = leaky_relu(Z)
        cache = {'Z': Z, 'A': A}
        return A, cache

    def __forward_propagation(self, X):
        caches = []
        A_prev = X
        caches.append({'A': A_prev})
        # forward propagation by laryer
        for l in range(1, len(self.layers_dim)):
            W, b = self.parameters['W'+str(l)], self.parameters['b'+str(l)]
            A_prev, cache = self.__one_layer_forward(A_prev, W, b, self.activations[l-1])
            caches.append(cache)
        AL = caches[-1]['A']
        return AL, caches

    def __compute_cost(self, AL, Y):
        """
        Origional Code from TrainerLambda:
        m = Y.shape[1]
        
        # Compute loss from aL and y.
        cost = (1./m) * (-np.dot(Y,np.log(AL).T) - np.dot(1-Y, np.log(1-AL).T))
        cost = np.squeeze(cost)      # To make sure your cost's shape is what we expect (e.g. this turns [[17]] into 17).
        assert(cost.shape == ())
        """
        m = Y.shape[1]
        cost = -np.sum(Y*np.log(AL) + (1-Y)*np.log(1-AL)) / m
        return cost

    def cost_function(self, X, Y):
        # use the result from forward propagation and the label Y to compute cost
        assert (self.input_size == X.shape[0])
        AL, _ = self.__forward_propagation(X)
        return self.__compute_cost(AL, Y)

    def sigmoid_backward(self, dA, Z):
        s = sigmoid(Z)
        dZ = dA * s*(1-s)
        return dZ

    def relu_backward(self, dA, Z):
        dZ = np.array(dA, copy=True)
        dZ[Z <= 0] = 0
        return dZ

    def __linear_backward(self, dZ, A_prev, W):
        m = A_prev.shape[1]
        dW = np.dot(dZ, A_prev.T) / m
        db = np.sum(dZ, axis=1, keepdims=True) / m
        dA_prev = np.dot(W.T, dZ)
        return dA_prev, dW, db

    def __activation_backward(self, dA, Z, activation):
        assert (dA.shape == Z.shape)
        if activation == 'sigmoid':
            dZ = self.sigmoid_backward(dA, Z)
        if activation == 'relu':
            dZ = self.relu_backward(dA, Z)
        if activation == 'leaky_relu':
            dZ = self.leaky_relu_backward(dA, Z)
        if activation == 'tanh':
            dZ = self.tanh_backward(dA, Z)
        return dZ

    def __backward_propagation(self, caches, Y):
        m = Y.shape[1]
        L = self.__num_layers
        grads = {}
        # backward propagate last layer
        AL, A_prev = caches[L-1]['A'], caches[L-2]['A']
        grads['dZ'+str(L-1)] = AL - Y
        grads['dA'+str(L-2)], \
        grads['dW'+str(L-1)], \
        grads['db'+str(L-1)] = self.__linear_backward(grads['dZ'+str(L-1)],
                                                      A_prev, self.parameters['W'+str(L-1)])
        # backward propagate by layer
        for l in reversed(range(1, L-1)):
            grads['dZ'+str(l)] = self.__activation_backward(grads['dA'+str(l)],
                                                            caches[l]['Z'],
                                                            self.activations[l-1])
            A_prev = caches[l-1]['A']
            grads['dA'+str(l-1)], \
            grads['dW'+str(l)], \
            grads['db'+str(l)] = self.__linear_backward(grads['dZ'+str(l)], A_prev, self.parameters['W'+str(l)])
        return grads

    def __update_parameters(self, grads, learning_rate):
        for l in range(1, self.__num_layers):
            self.parameters['W'+str(l)] -= learning_rate * grads['dW'+str(l)]
            self.parameters['b'+str(l)] -= learning_rate * grads['db'+str(l)]

    def fit(self, X, Y, num_iterations, learning_rate, print_cost=False, print_num=100):
        for i in range(num_iterations):
            # forward propagation
            AL, caches = self.__forward_propagation(X)
            # compute cost
            cost = self.__compute_cost(AL, Y)
            # backward propagation
            grads = self.__backward_propagation(caches, Y)
            # update parameters
            self.__update_parameters(grads, learning_rate)
            # print cost
            if i % print_num == 0 and print_cost:
                    print ("Cost after iteration %i: %f" %(i, cost))
        return self

    def predict_prob(self, X):
        A, _ = self.__forward_propagation(X)
        return A

    def predict(self, X, threshold=0.5):
        pred_prob = self.predict_prob(X)
        threshold_func = np.vectorize(lambda x: 1 if x > threshold else 0)
        Y_prediction = threshold_func(pred_prob)
        return Y_prediction

    def accuracy_score(self, X, Y):
        pred = self.predict(X)
        return len(Y[pred == Y]) / Y.shape[1]
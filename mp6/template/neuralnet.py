# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
"""
This is the main entry point for MP6. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch
import torch.nn as nn


class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network

        @param lrate: The learning rate for the model.
        @param loss_fn: A loss function defined in the following way:
            @param yhat - an (N,out_size) tensor
            @param y - an (N,) tensor
            @return l(x,y) an () tensor that is the mean loss
        @param in_size: Dimension of input
        @param out_size: Dimension of output

        For Part 1 the network should have the following architecture (in terms of hidden units):

        in_size -> 32 ->  out_size

        """
        lrate = .001
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        self.model = nn.Sequential(
            nn.Linear(in_size, 60),
            nn.LeakyReLU(),
            nn.Linear(60, 30),
            nn.LeakyReLU(),
            nn.Linear(30, out_size),
            nn.LeakyReLU(),
            nn.Sigmoid()
        )
        self.optimizer = torch.optim.SGD(self.model.parameters(), lrate, weight_decay = .43)



    def set_parameters(self, params):
        """ Set the parameters of your network
        @param params: a list of tensors containing all parameters of the network
        """
        pass

    def get_parameters(self):
        """ Get the parameters of your network
        @return params: a list of tensors containing all parameters of the network
        """
        return self.model.parameters()


    def forward(self, x):
        """ A forward pass of your neural net (evaluates f(x)).

        @param x: an (N, in_size) torch tensor

        @return y: an (N, out_size) torch tensor of output from the network
        """
        
        return self.model(x)

    def step(self, x, y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        self.optimizer.zero_grad()
        output = self.model(x)
        loss = self.loss_fn(output, y)
        loss.backward()
        self.optimizer.step()
        return loss


def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Make NeuralNet object 'net' and use net.step() to train a neural net
    and net(x) to evaluate the neural net.

    @param train_set: an (N, in_size) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M,) torch tensor
    @param n_iter: int, the number of epochs of training
    @param batch_size: The size of each batch to train on. (default 100)

    # return all of these:

    @return losses: Array of total loss at the beginning and after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: A NeuralNet object

    # NOTE: This must work for arbitrary M and N
    """
    batch_size = 150
    lrate = 0.0001
    nnet = NeuralNet(lrate, nn.CrossEntropyLoss(), len(train_set[0]), 2)
    dataset = torch.utils.data.TensorDataset(train_set, train_labels) 
    dataloader = torch.utils.data.DataLoader(dataset, batch_size)
    loss = []
    for epoch in range (n_iter):
        x = 0
        for batch in dataloader:
            x += nnet.step(batch[0], batch[1])
        loss.append(x.item())

    retval = np.zeros(len(dev_set))

    # dev_set
    x = nnet.forward(dev_set)
    for index, pair in enumerate(x):
        if pair[0] < pair[1]:
            retval[index] = 1

    return loss,retval,nnet

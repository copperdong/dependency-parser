import torch
import json
import copy
import os
import MST
import numpy as np
import torch.nn as nn
import torch.autograd as autograd
import torch.optim as optim
from gensim.models import Word2Vec
from torch.autograd import Variable

# class MLP(torch.nn.Module):
#     def __init__(self, input_dimension, hidden_dimension, output_dimension):
#         """
#         In the constructor we instantiate two nn.Linear modules and assign them as
#         member variables.
#         """
#         super(MLP, self).__init__()
#         self.linear1 = torch.nn.Linear(input_dimension, hidden_dimension)
#         self.linear2 = torch.nn.Linear(hidden_dimension, output_dimension)
#
#     def forward(self, x):
#         """
#         In the forward function we accept a Variable of input data and we must return
#         a Variable of output data. We can use Modules defined in the constructor as
#         well as arbitrary operators on Variables.
#         """
#         h = self.linear1(torch.sigmoid(x)).clamp(min=0)
#         y_pred = self.linear2(h)
#         return y_pred

class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.U = nn.Parameter(torch.randn(3, 5))
        self.MLP_layer_1 = torch.nn.Linear(3, 4)
        self.MLP_layer_2 = torch.nn.Linear(4,3)

    def MLP(self, input):
        hidden = self.MLP_layer_1(torch.sigmoid(input)).clamp(min=0)
        output = self.MLP_layer_2(hidden)
        return output

    def forward(self, inp):
        step1 = torch.t(3 + torch.mm(self.U, inp))
        output = self.MLP(step1)
        return output

def mse_loss(input, target):
    return torch.sum((input - target) ** 2)

network = Network()

network_params_1 = copy.deepcopy(list(network.parameters()))
# print(network_params_1)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(network.parameters(), lr=0.1)

inputs = Variable(torch.randn(5,1))
targets = Variable(torch.randn(3,1), requires_grad = False)

outputs = network(inputs)
loss = mse_loss(outputs, torch.t(targets))
# print(loss)
loss.backward()
optimizer.step()

network_params_2 = copy.deepcopy(list(network.parameters()))

print (np.array_equal(network_params_1, network_params_2))

# if np.array_equal(network_params_1, network_params_2):
#     print("theyrethesame")
# else:
#     print("updates!")

for i in range(len(network_params_1)):
    print(i,"th parameter")
    if np.array_equal(network_params_1[i], network_params_2[i]):
        print("they're the same")
    else:
        print("they've changed. woohoo!")

# print(network_params_1[0])
# print(network_params_2[0])

#
#
# mat = torch.randn(3,5)
# vec = torch.randn(5,1)
# print(torch.mm(mat, vec))

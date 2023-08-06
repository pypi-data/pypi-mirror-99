import torch
import torch.nn as nn
import torch.nn.functional as F

class FPOMDPNet(nn.Module):
    def __init__(self, input_size_a, input_size_b, hidden_size, output_size, qnet_type):
        super(FPOMDPNet, self).__init__()

        self.subnet = qnet_type(input_size_a+input_size_b, hidden_size, output_size)

    def forward(self, x_a, x_b):
        x = self.subnet(torch.cat([x_a, x_b], dim=-1))
        return x

    def predict(self, x_a, x_b):
        y = self.forward(x_a, x_b)
        return torch.argmax(y, 1)
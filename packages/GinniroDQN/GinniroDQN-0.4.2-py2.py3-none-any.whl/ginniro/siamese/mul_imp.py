import torch
import torch.nn as nn
import torch.nn.functional as F

class MulNet(nn.Module):
    def __init__(self, input_size_a, input_size_b, hidden_size, output_size, qnet_type):
        super(MulNet, self).__init__()

        self.subnet_a = qnet_type(input_size_a, hidden_size, output_size)
        self.subnet_b = qnet_type(input_size_b, hidden_size, output_size)

        self.linear_i2h = nn.Linear(output_size*2, hidden_size)
        self.linear_h2w = nn.Linear(hidden_size, 1)

    def forward(self, x_a, x_b):
        y_a = self.subnet_a(x_a)
        y_b = self.subnet_b(x_b)

        y = F.tanh(self.linear_i2h(torch.cat([y_a, y_b])))
        y = self.linear_h2o(y)

        return y

    def predict(self, x_a, x_b):
        y = self.forward(x_a, x_b)
        return torch.argmax(y, 1)
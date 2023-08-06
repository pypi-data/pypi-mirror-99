import torch
import torch.nn as nn
import torch.nn.functional as F

class SiameseNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, qnet_type):
        super(SiameseNet, self).__init__()

        self.subnet_a = qnet_type(input_size, hidden_size, output_size)
        self.subnet_b = qnet_type(input_size, hidden_size, output_size)

    def forward(self, x):
        x_a = self.subnet_a(x)
        x_b = self.subnet_b(x)
        return x_a, x_b

    def predict(self, x):
        y_a, y_b = self.forward(x)
        return torch.argmax(y_a+y_b, 1)
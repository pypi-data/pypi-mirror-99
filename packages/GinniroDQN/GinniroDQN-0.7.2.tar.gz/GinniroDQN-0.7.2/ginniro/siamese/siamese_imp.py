import torch
import torch.nn as nn
import torch.nn.functional as F

class SiameseNet(nn.Module):
    def __init__(self, input_size_a, input_size_b, hidden_size, output_size, qnet_type):
        super(SiameseNet, self).__init__()

        self.subnet_a = qnet_type(input_size_a, hidden_size, output_size)
        self.subnet_b = qnet_type(input_size_b, hidden_size, output_size)

    def forward(self, x_a, x_b):
        x_a = self.subnet_a(x_a) * 0.5
        x_b = self.subnet_b(x_b) * 0.5
        return x_a + x_b

    def predict(self, x_a, x_b):
        y = self.forward(x_a, x_b)
        return torch.argmax(y, 1)
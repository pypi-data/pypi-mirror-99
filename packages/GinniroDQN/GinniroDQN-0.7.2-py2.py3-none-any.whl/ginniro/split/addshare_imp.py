import torch
import torch.nn as nn
import torch.nn.functional as F

class SplitAddShareNet(nn.Module):
    def __init__(self, input_size_a, input_size_b, hidden_size, output_size, qnet_type):
        super(SplitAddShareNet, self).__init__()

        input_size = input_size_a + input_size_b

        self.subnet_a = qnet_type(input_size, hidden_size, output_size)
        self.subnet_b = qnet_type(input_size, hidden_size, output_size)

    def forward(self, x_a, x_b):
        x = torch.cat([x_a, x_b], dim=-1)

        y_a = self.subnet_a(x)
        y_b = self.subnet_b(x)

        return y_a, y_b

    def predict(self, x_a, x_b):
        y_a, y_b = self.forward(x_a, x_b)
        return torch.argmax(y_a+y_b, 1)
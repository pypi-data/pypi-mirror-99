import torch
import torch.nn as nn
import torch.nn.functional as F

class SplitMixNet(nn.Module):
    def __init__(self, input_size_a, input_size_b, hidden_size, output_size, qnet_type):
        super(SplitMixNet, self).__init__()

        self.subnet_a = qnet_type(input_size_a, hidden_size, output_size)
        self.subnet_b = qnet_type(input_size_b, hidden_size, output_size)

        self.linear_i2h = nn.Linear(input_size_a + input_size_b, hidden_size)
        self.linear_h2w = nn.Linear(hidden_size, 1)

    def forward(self, x_a, x_b):
        w = F.tanh(self.linear_i2h(torch.cat([x_a, x_b], dim=-1)))
        w = F.sigmoid(self.linear_h2w(w))

        y_a = self.subnet_a(x_a) * w
        y_b = self.subnet_b(x_b) * (1 - w)

        return y_a, y_b

    def predict(self, x_a, x_b):
        y_a, y_b = self.forward(x_a, x_b)
        return torch.argmax(y_a+y_b, 1)
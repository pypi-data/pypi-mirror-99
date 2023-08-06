import torch
import torch.nn as nn
import torch.nn.functional as F

class SplitShareNet(nn.Module):
    def __init__(self, input_size_a, input_size_b, hidden_size, output_size, qnet_type):
        super(SplitShareNet, self).__init__()

        input_size = input_size_a + input_size_b

        self.subnet_a = qnet_type(input_size, hidden_size, output_size)
        self.subnet_b = qnet_type(input_size, hidden_size, output_size)

        self.linear_i2h = nn.Linear(input_size, hidden_size)
        self.linear_h2w = nn.Linear(hidden_size, 1)

    def forward(self, x_a, x_b):
        x = torch.cat([x_a, x_b], dim=-1)
        w = F.tanh(self.linear_i2h(x))
        w = F.sigmoid(self.linear_h2w(w))

        y_a = self.subnet_a(x) * w
        y_b = self.subnet_b(x) * (1 - w)

        return y_a, y_b

    def predict(self, x_a, x_b):
        y_a, y_b = self.forward(x_a, x_b)
        return torch.argmax(y_a+y_b, 1)
import torch
import torch.nn as nn
import torch.nn.functional as F

class MixNet(nn.Module):
    def __init__(self, input_size_a, input_size_b, hidden_size, output_size, qnet_type):
        super(MixNet, self).__init__()

        self.subnet_a = qnet_type(input_size_a, hidden_size, output_size)
        self.subnet_b = qnet_type(input_size_b, hidden_size, output_size)

        self.linear_i2h = nn.Linear(input_size_a + input_size_b, hidden_size)
        self.linear_h2w = nn.Linear(hidden_size, 2)

    def forward(self, x_a, x_b):
        x_a = self.subnet_a(x_a)
        x_b = self.subnet_b(x_b)

        x_w = F.tanh(self.linear_i2h(torch.cat([x_a, x_b], dim=-1)))
        x_w = F.sigmoid(self.linear_h2w(x_w))

        # x_a => batch_size * output_size
        # x_b => batch_size * output_size
        # x_w => batch_size * 2
        x_w_a, x_w_b = x_w.split(1, dim=-1)
        x_w_a = x_w_a.expand(dim=-1)
        x_a = torch.mm(x_a, x_w_a)
        x_w_b = x_w_b.expand(dim=-1)
        x_b = torch.mm(x_b, x_w_b)

        return x_a + x_b

    def predict(self, x_a, x_b):
        # y_a, y_b = self.forward(x)
        y = self.forward(x_a, x_b)
        return torch.argmax(y, 1)
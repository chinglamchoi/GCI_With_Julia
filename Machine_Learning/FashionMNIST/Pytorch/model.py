import torch
import torch.nn as nn
import torch.nn.functional as F

class ConvNet(nn.Module):

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)

        self.fc1 = nn.Linear(576, 72)
        self.output = nn.Linear(72, 10)

    def forward(self, x):
        out = F.relu(self.conv1(x))
        out = F.max_pool2d(out, kernel_size=2, stride=2)

        out = F.relu(self.conv2(out))
        out = F.max_pool2d(out, kernel_size=2, stride=2)

        out = F.relu(self.conv3(out))
        out = F.max_pool2d(out, kernel_size=2, stride=2)
        
        out = out.view(out.size(0), -1)
        out = F.relu(self.fc1(out))
        #out = F.relu(self.fc2(out))
        out = F.relu(self.output(out))
        return out

def run_cnn():
    return ConvNet()
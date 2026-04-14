import sys
sys.path.append("/home/ljj/3-biaffine-taketurn/src+mamba")
from mymamba import MambaBlock,MambaModel
import torch
import torch.nn as nn
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

dim,layer_num = 512,3

x = torch.randn(22, 10, dim).to(device)
i = 0
mymambablock = MambaModel('mamba_' + str(i), dim=dim, layer_num=layer_num).to(device)

print(mymambablock.name)
y_mamba = mymambablock(x).to(device)

print(mymambablock)
print(y_mamba.shape, y_mamba)
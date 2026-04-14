import os
import sys
sys.path.append("/home/ljj/3-biaffine-taketurn/srcmamba")
import torch
from torch import nn, optim
from mamba_simple import Mamba, Block
from torch.utils.data import Dataset, DataLoader
import numpy as np

# 设置固定的随机种子
torch.manual_seed(1046546544)
np.random.seed(1046546544)

"""构建模型"""
# 定义一个使用 Mamba 作为 Mixer 的 Block 类
# class MambaBlock(Block):
#     def __init__(self, dim, **kwargs):
#         # 使用 Mamba 作为 mixer_cls 初始化 Block
#         super().__init__(dim, mixer_cls=Mamba, **kwargs)

class MambaBlock(Block):
    def __init__(self, dim, **kwargs):
        # 移除不在 Mamba 类中定义的参数
        super().__init__(dim, mixer_cls=Mamba, norm_cls=nn.LayerNorm, fused_add_norm=True, residual_in_fp32=True, **kwargs)

# 定义一个包含三层 MambaBlock 的模型
class MambaModel(nn.Module):
    def __init__(self, dim, layer_num, **kwargs):
        super().__init__()
        # 添加三个 MambaBlock 层
        self.blocks = nn.ModuleList([
            MambaBlock(dim, **kwargs) for _ in range(layer_num)
        ])
        
    def forward(self, x):
        #初始化残差，因为一开始没有
        residual = None
        #print(residual)
        for block in self.blocks:
            x,residual = block(x, residual)
            #print(residual)
        return x


# 模型参数
# batch, length, dim = 5, 64, 16
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
layer_num = 3  # 你可以根据需要修改这个值来设置层的数量
# 实例化模型
model = MambaModel(dim=16, layer_num=layer_num).to(device)
print(model)

# 定义数据集和数据加载器
class RandomDataset(Dataset):
    def __init__(self, batch_size, num_features, num_classes, length):
        self.batch_size = batch_size
        self.num_features = num_features
        self.num_classes = num_classes
        self.length = length
    
    def __len__(self):
        return self.batch_size
    
    def __getitem__(self, idx):
        # 生成随机输入特征
        x = torch.randn(self.length, self.num_features)
        # 生成随机类别索引作为真实标签
        y = torch.randint(0, self.num_classes, (self.num_features,))
        return x, y

# 数据集参数
batch_size = 10
num_features = 16
num_classes = 3
length = 64

# 实例化数据集和数据加载器
random_dataset = RandomDataset(batch_size, num_features, num_classes, length)
data_loader = DataLoader(dataset=random_dataset, batch_size=batch_size, shuffle=True)

# 定义损失函数和优化器
cross_entropy = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 训练模型
num_epochs = 10
best_loss = float('inf')
best_epoch = 0
model_folder = '/home/ljj/mamba/mamba_ssm/savemodel'
for epoch in range(num_epochs):
    model.train()  # 设置模型为训练模式
    total_loss = 0
    model_filename = f"mymodel_{epoch+1}.pth"
    model_path = os.path.join(model_folder, model_filename)
    for x, y in data_loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()  # 清除之前的梯度
        y_pred = model(x)  # 前向传递
        print(type(y),type(y_pred))
        print("y:",y.shape)
        print("y_p:",y_pred.shape)
        loss = cross_entropy(y_pred, y)  # 计算损失
        loss.backward()  # 后向传播
        optimizer.step()  # 更新权重
        total_loss += loss.item()
    # 保存最好的模型
    if total_loss / len(data_loader) < best_loss:
        best_epoch = epoch + 1
        bestmodel_filename = f"mymodel_{best_epoch}.pth"
        bestmodel_path = os.path.join(model_folder, model_filename)
        if os.path.exists(bestmodel_path):  # 删除之前的模型
            os.remove(bestmodel_path)
        best_loss = total_loss / len(data_loader)
        torch.save(model.state_dict(), model_path)  # 保存模型参数
        
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {total_loss / len(data_loader)}")

# 评估模型
def evaluate_model(model, data_loader):
    if os.path.exists(bestmodel_path):
            # 如果文件存在，加载模型
            model.load_state_dict(torch.load(bestmodel_path))
            print("Model loaded from", bestmodel_path)
    else:
            # 如果文件不存在，初始化一个新的模型
            print("No model found. Initializing a new model.")
            
    model.eval()  # 设置模型为评估模式
    total_loss = 0
    with torch.no_grad():
        for x, y in data_loader:
            x, y = x.to(device), y.to(device)
            y_pred = model(x)
            loss = cross_entropy(y_pred, y)
            total_loss += loss.item()
    return total_loss / len(data_loader)

eval_loss = evaluate_model(model, data_loader)
print(f"评估损失: {eval_loss}")
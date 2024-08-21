import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.multiprocessing as mp
import time
from torch.utils.data import DataLoader, TensorDataset

# Define the model
class SimpleFFNN(nn.Module):
    def __init__(self):
        super(SimpleFFNN, self).__init__()
        self.fc1 = nn.Linear(20, 10)
        self.fc2 = nn.Linear(10, 1)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

# Create synthetic dataset
def get_data_loaders(batch_size):
    X = torch.randn(1000, 20)
    y = (torch.sum(X, dim=1) > 0).float().unsqueeze(1)
    dataset = TensorDataset(X, y)
    train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return train_loader

# Training function for each process
def train_model(rank, models, epochs, batch_size):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_loader = get_data_loaders(batch_size)
    
    model = models[rank].to(device)
    optimizer = torch.optim.Adam(model.parameters())
    criterion = nn.BCELoss()
    
    model.train()
    start_time = time.time()
    print(f"Model {rank} started training at {time.strftime('%X')}.")

    for epoch in range(epochs):
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
        print(f'Process {rank} | Epoch {epoch+1}, Loss: {loss.item():.4f}')

    end_time = time.time()
    print(f"Model {rank} finished training at {time.strftime('%X')}. Time taken: {end_time - start_time:.2f} seconds.")

# Function to train multiple models with timing
def train_multiple_models(num_models, epochs, batch_size):
    models = [SimpleFFNN() for _ in range(num_models)]
    
    spawn_start_time = time.time()
    print(f"Spawning models at {time.strftime('%X')}.")

    # Use mp.spawn to start processes
    mp.spawn(train_model, args=(models, epochs, batch_size), nprocs=num_models, join=True)
    
    spawn_end_time = time.time()
    print(f"All models finished training at {time.strftime('%X')}. Total time taken: {spawn_end_time - spawn_start_time:.2f} seconds.")

if __name__ == '__main__':
    num_models = 4
    epochs = 5
    batch_size = 64
    
    train_multiple_models(num_models, epochs, batch_size)

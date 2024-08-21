import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim
from util import util
import os
import pandas as pd
import numpy as np
from functools import reduce


def map_angle_to_int(angle):
    """
    Map angles as values between 1 -4 based on X type direction
    """
    if (0 <= angle <= 45) or (316 <= angle <= 360):
        return 1
    elif 46 <= angle <= 135:
        return 2
    elif 136 <= angle <= 225:
        return 3
    elif 226 <= angle <= 315:
        return 4
    else:
        raise ValueError(f"Angle {angle} out of range (0-360)")

def get_disp_rot(curr, prev=None, offset=0, degrees=False, neg_pi=True):
    """
    Get the rotation angle of a body from its current and or previous position
    Agrs:
        curr (list, np.ndarray): current position of agent
        prev (list, np.ndarray): previous position of agent
        offset float: radian value to offset computed rotation
        degrees (bool): flag to return rotation as degrees
        neg_pi (bool): treat radians as values between -pi to pi 
    
    Returns:
        rot (float): computed rotation value
    """
    disp = np.array(curr)
    if prev is not None:
        disp = np.array(curr) - np.array(prev)
    
    rot = np.arctan2(disp[1], disp[0])
    disp = np.linalg.norm(disp)
    #rot = rot % (2*math.pi) if not neg_pi else rot
    rot = rot + offset
    if degrees:
        return disp, radians_to_degrees(rot, neg_pi=neg_pi)
    return disp, rot

def radians_to_degrees(radians, z_axis= 1, neg_pi=True):
    """
    Takes in the radians value and a neg_pi value
    We bot environment specifies radians as 0 - pi and encode direction as z-axis
    If neg_pi is true, values are converted from -pi to pi to 0 to 2pi
    """
    import math
    
    radians = radians*z_axis
    radians = radians % (2*math.pi) if neg_pi else radians
    degrees = round(math.degrees(radians))
    degrees = degrees % 360  # Ensure degrees stay within 0-359 range
    if degrees < 0:
        degrees += 360  # Add 360 to negative degrees to bring them into positive range
    
    # Force values of 360 to 0
    if degrees == 360: degrees = 0
    return degrees

class NextStateModelFC(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dims=128, num_layers=3, dropout_rate=0.2, activation='relu'):
        super(NextStateModelFC, self).__init__()

        assert num_layers >= 2, 'Number of layers must be at least 2'
        
        self.activation = getattr(torch.nn.functional, activation)

        self.input_layer = nn.Linear(input_dim, hidden_dims)
        self.bn_input = nn.BatchNorm1d(hidden_dims)
        self.dropout_input = nn.Dropout(dropout_rate)

        self.layers = nn.ModuleList()
        for _ in range(num_layers-2):
            self.layers.append(nn.Linear(hidden_dims, hidden_dims))
            self.layers.append(nn.BatchNorm1d(hidden_dims))
            self.layers.append(nn.Dropout(dropout_rate))

        self.output_layer = nn.Linear(hidden_dims, output_dim)

    def forward(self, x):
        x = self.dropout_input(self.activation(self.bn_input(self.input_layer(x))))
        
        for i in range(0, len(self.layers), 3):
            x = self.layers[i+2](self.activation(self.layers[i+1](self.layers[i](x))))
        
        next_state = self.output_layer(x)
        return next_state

class BaseWorld():
    def __init__(self, dataset_path=None, env=None, ) -> None:
        self.dataset_path = dataset_path
        self.env = env
        self.path = None

    
    def prepare_dataset(self,):
        if self.dataset_path is None and self.env is None:
            util.verbose(f"No dataset/ env specified", decorator="error")
            return
        
        if self.env is not None:
            temp = [attr for attr in dir(util) if f"{self.env}_world" in attr]
            self.path = getattr(util, temp[0])
            self.path = os.path.join(self.path, "world_pos_dict.pickle")
        self.path = self.dataset_path if self.dataset_path else self.path

        if not os.path.isfile(self.path):
            util.verbose("Dataset path not found!", decorator="error")
            return
        
        dataset = util.unpickle_file(self.path, verbose=True)
        self.names = dataset.get("names")
        self.points = dataset.get("points")
        self.df = pd.DataFrame(self.points, columns=self.names)


    def compute_actions(self):
        pass

    def preprocess_data(self,):
        pass
    
    def load_dataset(self):
        pass


class BaseDataset(Dataset):
    def __init__(self, df):
        self.df = df

    def __getitem__(self, idx):
        temp = self.df.iloc[idx]
        data = torch.tensor(temp["data"], dtype=torch.float32)
        target = torch.tensor(temp["target"], dtype=torch.float32)
        return data, target
    
    def __len__(self):
        return len(self.df)


class MPEWorld(BaseWorld):
    def __init__(self, dataset_path=None, env="mpe", n_agent=3, n_landmarks=3, step=0.001, n_actions=5) -> None:
        super().__init__(dataset_path, env)
        self.n_agents = n_agent
        self.n_landmarks = n_landmarks
        self.step = step
        self.n_actions = n_actions
        self.angle_act_map = {}

        self.prepare_dataset()

    def preprocess_data(self):
        self.datapoints = []
        for (id, row), (nx_id, nx_row) in zip(
            self.df.iterrows(), self.df.shift(-1).iterrows()):
            # Exit if we are at the end of the df
            if nx_row.isnull().values.any():
                break
            if row['episode'] == nx_row['episode']:
                # Remove the episode columns
                curr = reduce(lambda x, y: x+y, row.drop('episode').tolist())
                next = reduce(lambda x, y: x+y, nx_row.drop('episode').tolist())
                # Compute action
                action_list = []
                for i in range(self.n_agents):
                    name = f"agents_{i}"
                    disp, angle = get_disp_rot(nx_row[name], row[name], 
                                         degrees=True)
                    if disp < self.step:
                        action_list.append(0)
                    else:
                        action_list.append(map_angle_to_int(angle))
                # convert action list to one hot before adding
                action_list = [util.one_hot_encode(act, self.n_actions)
                               for act in action_list]
                action_list = reduce(lambda x, y: x+y, action_list)
                curr.extend(action_list)    # Add action to data
                self.datapoints.append([curr, next])
        
        self.data = pd.DataFrame(self.datapoints, 
                                 columns=["data", "target"])
        # TODO: Implement MPEDataset
        self.dataset = BaseDataset(self.data)
        aaa = self.data
        return
    

    def load_dataset(self, test_size=0.15, val_size=0.15, batch_size=32):
        
        self.batch_size = batch_size
        size = self.dataset.__len__()
        test_amount, val_amount = int(size * test_size), int(size * val_size)

        # this function will automatically randomly split your dataset but you could also implement the split yourself
        train_set, val_set, test_set = torch.utils.data.random_split(self.dataset, [
                    (size - (test_amount + val_amount)), 
                    test_amount, 
                    val_amount])

        self.train_set = DataLoader(
            train_set, batch_size=self.batch_size, shuffle=True)
        self.val_set = DataLoader(
            val_set, batch_size=self.batch_size, shuffle=True)
        self.test_set = DataLoader(
            test_set, batch_size=self.batch_size, shuffle=True)
    

    def train(self, num_epochs=50, val_epoch=20):

        # Model, loss function, and optimizer
        # Determine input dimension from the dataset
        input_dim = self.dataset[0][0].shape[0]
        output_dim = self.dataset[0][1].shape[0]

        self.model = NextStateModelFC(input_dim=input_dim, output_dim=output_dim)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)

        for epoch in range(num_epochs):
            self.model.train()
            running_loss = 0.0
            
            for inputs, targets in self.train_set:
                optimizer.zero_grad()
                
                outputs = self.model(inputs)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()
                
                running_loss += loss.item() * inputs.size(0)
            
            epoch_loss = running_loss / len(self.train_set.dataset)
            if epoch%10 == 0:
                print(f"Epoch {epoch+1}/{num_epochs}, Training Loss: {epoch_loss:.4f}")

            # Evaluate on validation set
            if epoch > 0 and epoch%val_epoch == 0:
                val_loss = self.evaluate(self.model, self.val_set, criterion)
                print(f"Epoch {epoch+1}/{num_epochs}, Validation Loss: {val_loss:.4f}")

        # Evaluate on test set
        test_loss = self.evaluate(self.model, self.test_set, criterion)
        print(f"Epoch {epoch+1}/{num_epochs}, Test Loss: {test_loss:.4f}")


    def evaluate(self, model, data_loader, criterion):
        model.eval()
        running_loss = 0.0
        with torch.no_grad():
            for inputs, targets in data_loader:
                outputs = model(inputs)
                print(inputs[0], targets[0], outputs[0])
                loss = criterion(outputs, targets)
                running_loss += loss.item() * inputs.size(0)
        
        epoch_loss = running_loss / len(data_loader.dataset)
        return epoch_loss




world = MPEWorld()
world.preprocess_data()
world.load_dataset()
world.train(num_epochs=500, val_epoch=50)
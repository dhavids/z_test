from util.util import *
import yaml

base= "/home/ayomide/OneDrive/MARL_git/z_tester/test"
name = get_file_name(base, "temp", ext=".png")

info = (name, "py")

test = " ".join(info)
print(test)

path = "/home/ayomide/OneDrive/MARL_git/configs/mpe/mappo/train.yaml"
with open(path, 'r') as f:
    train_config = yaml.safe_load(f)

print(recursive_update(train_config['agg'], train_config['default']))
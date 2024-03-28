from util.util import *

base= "/home/ayomide/OneDrive/MARL_git/z_tester/test"
name = get_file_name(base, "temp", ext=".png")

info = (name, "py")

test = " ".join(info)
print(test)
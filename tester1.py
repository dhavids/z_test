temp = {}
with open("file.txt", "r") as f:
    for line in f.readlines():
        t = line.split()
        temp[t[0]] = t[1]

message = []
with open("t.txt", "r") as f:
    for line in f.readlines():
        message.append(temp[line.split()[-1]])


print(" ".join(message))

def stair_case(message_keys):
    temp = sorted([int(i) for i in message_keys])
    subsets = []
    start = 0
    end = 1

    while end <= len(temp):
        subsets.append(temp[start:end])
        start = end
        end = end + len(subsets) + 1 # 1 is added to imitate step variable
    
    print(subsets)
    return subsets

def decode(message_file):
    temp = {}   # temp dict to hold decoder k:v pairs
    with open(message_file, "r") as f:
        for line in f.readlines():
            t = line.split()
            temp[int(t[0])] = t[1] 
    
    stairs = stair_case(list(temp.keys()))
    message = [temp[i[-1]] for i in stairs]    # message list    
    return " ".join(message)

print(decode("coding_qual_input.txt"))
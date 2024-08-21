import multiprocessing as mp
import time

def helper(args):
    id, start = args
    local_start = time.time()
    print(f"Process {id} sleeping {local_start - start} seconds  after global start.")
    time.sleep(10)
    print(f"Process {id} awake after {time.time() - local_start} seconds")


# Create a pool of worker processes
ctx = mp.get_context('spawn')
start = time.time()

args_list = [(i, start) for i in range(3)]
with mp.Pool(3) as p:
    p.map(helper, args_list)

end = time.time() - start
print(f"\nProgram ended after {end} seconds")
    

from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = 256000

# --- Step 1: root generates data ---
if rank == 0:
    data = np.random.uniform(0.0, 1.0, N)
else:
    data = None

# --- Step 2: scatter data ---
local_n = N // size
local_data = np.zeros(local_n)

comm.Scatter(data, local_data, root=0)

# --- Step 3: compute local sums ---
local_sum = np.sum(local_data)
local_sq_sum = np.sum(local_data**2)

# --- Step 4: reduce to global sums ---
total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)
total_sq_sum = comm.reduce(local_sq_sum, op=MPI.SUM, root=0)

# --- Step 5: compute mean and std on root ---
if rank == 0:
    mean = total_sum / N
    variance = (total_sq_sum / N) - mean**2
    std = np.sqrt(variance)

    print(f"Mean = {mean}")
    print(f"Std  = {std}")

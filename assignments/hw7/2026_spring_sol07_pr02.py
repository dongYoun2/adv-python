
from mpi4py import MPI
import numpy as np
from math import exp, factorial

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Problem settings
M = 1000.0          # finite integration range [0, M]
n_local = 1000      # increments per partition
k_max = 15          # compute J1, J2, ..., J15

# Domain decomposition
# Total domain [0, M] is split into `size` partitions
local_width = M / size
h = local_width / n_local

a_local = rank * local_width
b_local = a_local + local_width

# Local contribution for J1 ... J15
local_J = np.zeros(k_max, dtype=np.float64)

# Midpoint rule on this rank's subinterval
for j in range(n_local):
    x = a_local + (j + 0.5) * h
    fx = exp(-x)

    # x shape: scalar
    # fx shape: scalar
    # local_J shape: (15,)
    x_pow = x
    for k in range(1, k_max + 1):
        local_J[k - 1] += x_pow * fx * h
        x_pow *= x

# Reduce all local partial integrals to root
global_J = np.zeros(k_max, dtype=np.float64)
comm.Reduce(local_J, global_J, op=MPI.SUM, root=0)

if rank == 0:
    print(f"Computed moments J_k (from 0 to {M:.0f})")
    print(f"Processes = {size}, partitions = {size}, increments/partition = {n_local}")
    print()

    for k in range(1, k_max + 1):
        exact = factorial(k)   # I_k == k!
        approx = global_J[k - 1]
        rel_err = abs(approx - exact) / exact
        print(f"J_{k:2d} = {approx: .10e}   exact = {exact: .10e}   rel.err = {rel_err: .3e}")

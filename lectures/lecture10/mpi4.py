#####
# Sending a message to a process and receiving a message back
#####

import numpy
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

randNum = numpy.zeros(1) 

if rank == 1:
        randNum = numpy.random.rand(1)
        print("Process", rank, "drew the number", randNum[0])
        comm.Send(randNum, dest=0)
        comm.Recv(randNum, source=0)
        print("Process", rank, "received the number", randNum[0], "from process 0")
        
if rank == 0:
        print("Process", rank, "before receiving has the number", randNum[0])
        comm.Recv(randNum, source=1)
        print("Process", rank, "received the number", randNum[0], "from process 1")
        randNum *= 20
        comm.Send(randNum, dest=1) 

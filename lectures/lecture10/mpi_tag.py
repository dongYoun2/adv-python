from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank() 

data1 = None
data2 = None

if rank == 0:
    data1 = ('a','b', 'c', 'd')
    data2 = (1, 2, 3, 4)
    
    comm.send(data1, dest=1, tag=0)    
    comm.send(data2, dest=1, tag=1)
    
    

elif rank == 1:
    print('On Process',rank,'before recv: data1 = ', data1)
    print('On Process',rank,'before recv: data2 = ', data2)
    
    data1 = comm.recv(source=0, tag=0)  
    data2 = comm.recv(source=0, tag=1)
    
    print('On Process',rank,'after  recv: data1 = ', data1)
    print('On Process',rank,'after  recv: data2 = ', data2)
    

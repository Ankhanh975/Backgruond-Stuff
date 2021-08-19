from multiprocessing import 
import array
import time
import os

#os.system("C:/src/Python/Share_RAM/shared_memory2.py ")

shm_a = shared_memory.SharedMemory(create=True, size=10) #10 btye
print(shm_a.name)
shm_a.buf[:10] = b'0000000000'

shm_a.close()
shm_a.unlink()



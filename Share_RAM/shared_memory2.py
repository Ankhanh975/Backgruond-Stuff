from multiprocessing import shared_memory
import array
import time

time.sleep(0.5)
shm_b = shared_memory.SharedMemory(name="aaaa 00000000")

print('b')
while True:
    print("b: "+str(bytes(shm_b.buf[:10])))
    time.sleep(1/60)
    
time.sleep(5)
shm_b.close()

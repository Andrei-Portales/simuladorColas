import random
import simpy

# creacion de funciones
def numeroAlazar(interval):
    return int(random.expovariate(1 / 10))

# variables dinamicas
numProcesos = 3
numRam = 100



# variables de simulador
events = []
env = simpy.Environment()
RAM = simpy.Container(env, init=numRam, capacity=numRam)
CPU = simpy.Resource(env,capacity = numProcesos)

def process():
    print("")




import simpy
import random

for n in range(5):
    print(int(random.expovariate(1.0 / 10)))

print(random.seed(2))

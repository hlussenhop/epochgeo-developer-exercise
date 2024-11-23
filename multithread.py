import os
from multiprocessing import cpu_count

# Number of CPU cores
print("os.cpu_count():", os.cpu_count())
print("multiprocessing.cpu_count():", cpu_count())
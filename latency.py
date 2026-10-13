import time
from contextlib import contextmanager
@contextmanager
def measure_latency(logs,key):
    s=time.perf_counter(); yield; logs[key]=round((time.perf_counter()-s)*1000,2)

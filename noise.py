import numpy as np

def add_noise(sig,sr,noise_type='hospital',snr=5.0):
    n=np.random.randn(len(sig))*(0.5 if noise_type=='hospital' else 0.2)
    k=(np.mean(sig**2)/(np.mean(n**2)*10**(snr/10)))**0.5
    return sig+k*n

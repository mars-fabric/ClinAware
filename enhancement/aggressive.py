import librosa, numpy as np
from scipy.signal import medfilt

def enhance(sig,sr):
    S=librosa.stft(sig); mag,ph=np.abs(S),np.angle(S)
    mag=medfilt(mag,(1,9)); return librosa.istft(np.maximum(mag-mag.mean(),0)*np.exp(1j*ph))

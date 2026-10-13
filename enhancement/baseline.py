import librosa, numpy as np

def enhance(sig,sr):
    S=librosa.stft(sig); mag,ph=np.abs(S),np.angle(S)
    nf=mag[:,:5].mean(axis=1,keepdims=True)
    return librosa.istft(np.maximum(mag-nf,0)*np.exp(1j*ph))

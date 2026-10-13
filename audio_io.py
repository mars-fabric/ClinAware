import librosa
def load_audio(p,sr=16000): 
    return librosa.load(p,sr=sr,mono=True)

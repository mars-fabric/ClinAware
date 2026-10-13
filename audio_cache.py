import soundfile as sf, os, uuid
CACHE_DIR = 'audio_cache'
os.makedirs(CACHE_DIR, exist_ok=True)

def create_session(): return str(uuid.uuid4())

def save_audio(sid, name, sig, sr):
    p=f"{CACHE_DIR}/{sid}_{name}.wav"; sf.write(p,sig,sr); return p

def load_audio_path(sid,name):
    p=f"{CACHE_DIR}/{sid}_{name}.wav"; return p if os.path.exists(p) else None

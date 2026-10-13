from fastapi import FastAPI,UploadFile,File,Form
from fastapi.responses import FileResponse,HTMLResponse,JSONResponse
from audio_io import load_audio
from noise import add_noise
from biomarkers import extract_biomarkers
from risk_model import risk_score
from viz import spec
from latency import measure_latency
from enhancement import baseline,aggressive,demucs_model
from audio_cache import create_session,save_audio,load_audio_path
import tempfile,os
app=FastAPI()
ENHANCERS={
    'baseline':baseline.enhance,
    'aggressive':aggressive.enhance,
    'demucs':demucs_model.enhance
    }


@app.get('/')
def ui(): return HTMLResponse(open('static/index.html',encoding='utf-8').read())

@app.post('/analyze')
async def analyze(file:UploadFile=File(...),enhancer:str='baseline',add_noise_flag:bool=Form(True,alias='add_noise')):
    latency={}
    sid=create_session()
    p=tempfile.NamedTemporaryFile(delete=False).name; open(p,'wb').write(await file.read())
    with measure_latency(latency,'load'): sig,sr=load_audio(p); os.remove(p)
    noisy=add_noise(sig,sr) if add_noise_flag else sig
    results = {}

    # Biomarkers BEFORE enhancement (same noisy input for all)
    bm_noisy = extract_biomarkers(noisy, sr)
    risk_noisy = risk_score(bm_noisy)

    for name, enhancer_fn in ENHANCERS.items():
        with measure_latency(latency, f"enhance_{name}"):
            enhanced = enhancer_fn(noisy, sr)

        bm_enh = extract_biomarkers(enhanced, sr)
        risk_enh = risk_score(bm_enh)

        results[name] = {
            "audio": {
                "enhanced": f"/audio/{sid}_{name}/enhanced"
            },
            "spectrograms": {
                "enhanced": spec(enhanced, sr, f"{name.title()} Enhanced")
            },
            "biomarkers": {
                "before": bm_noisy,
                "after": bm_enh
            },
            "risk": {
                "before": risk_noisy,
                "after": risk_enh
            }
        }

        save_audio(sid + "_" + name, "enhanced", enhanced, sr)

    save_audio(sid, "clean", sig, sr)
    save_audio(sid, "noisy", noisy, sr)

    spectrograms = {
        "clean": spec(sig, sr, "Clean"),
        "noisy": spec(noisy, sr, "Noisy"),
        "enhanced": spec(enhanced, sr, "Enhanced")
    }
    
    return JSONResponse({
    "session_id": sid,
    "common": {
        "spectrograms": {
            "clean": spec(sig, sr, "Clean"),
            "noisy": spec(noisy, sr, "Noisy")
        },
        "audio": {
            "clean": f"/audio/{sid}/clean",
            "noisy": f"/audio/{sid}/noisy"
        },
        "biomarkers_noisy": bm_noisy,
        "risk_noisy": risk_noisy,
        "add_noise_applied": add_noise_flag
    },
    "enhancers": results,
    "latency_ms": latency
    })


@app.get('/audio/{sid}/{v}')
def audio(sid,v): return FileResponse(load_audio_path(sid,v))

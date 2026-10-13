# ClinAware: Speech Enhancement Needs Clinical Awareness

Kachare, P.H., Amancharla, C. (2026) ClinAware: Speech Enhancement Needs Clinical Awareness. Proc. Interspeech 2026, 4473-4474 [paper](https://www.isca-archive.org/interspeech_2026/kachare26_interspeech.pdf)

Clinical-awareness speech enhancement demo (Interspeech 2026 Show & Tell). A FastAPI backend serves
multiple speech enhancement strategies (baseline, aggressive, Demucs) and extracts clinical biomarkers
and risk scores from the enhanced audio, with a lightweight web UI for interactive testing.

## Structure

- `app.py` — FastAPI app and `/analyze` endpoint
- `audio_io.py`, `audio_cache.py`, `noise.py`, `latency.py`, `viz.py` — audio I/O, caching, noise injection, timing, spectrogram viz
- `biomarkers.py`, `risk_model.py` — clinical biomarker extraction and risk scoring
- `enhancement/` — enhancement strategies (`baseline`, `aggressive`, `demucs_model`)
- `static/index.html` — web UI

## Running locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open `http://localhost:8000`.

## Notes

- `audio_cache/` is used at runtime to store per-session intermediate audio and is not checked into
  version control.
- No sample/patient audio, PDFs, or other binary assets are included in this repository — only source
  code needed to run the app.

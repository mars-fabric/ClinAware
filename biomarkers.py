import librosa, numpy as np

def extract_biomarkers(sig,sr):
    e=librosa.feature.rms(y=sig)[0]
    f0=librosa.yin(sig,fmin=75,fmax=300,sr=sr)
    f0=f0[~np.isnan(f0)]
    sc=librosa.feature.spectral_centroid(y=sig,sr=sr)[0]

    # Jitter proxy: cycle-to-cycle variation of F0 (relative mean abs diff)
    if len(f0)>1 and f0.mean()>0:
        jitter=float(np.abs(np.diff(f0)).mean()/f0.mean())
    else:
        jitter=0.0

    # Shimmer proxy: cycle-to-cycle variation of amplitude (relative mean abs diff of RMS)
    if len(e)>1 and e.mean()>0:
        shimmer=float(np.abs(np.diff(e)).mean()/e.mean())
    else:
        shimmer=0.0

    # Speaking rate proxy: syllable nuclei per second via RMS-envelope peak picking
    duration=len(sig)/sr if sr>0 else 0.0
    if duration>0 and len(e)>0:
        env=e/(e.max()+1e-9)
        hop=512
        peaks=librosa.util.peak_pick(env,pre_max=3,post_max=3,pre_avg=3,
                                      post_avg=5,delta=0.1,wait=3)
        speaking_rate=float(len(peaks)/duration)
    else:
        speaking_rate=0.0

    return {
        'pause_ratio':float(1-(e>np.percentile(e,40)).mean()),
        'f0_mean':float(f0.mean()) if len(f0)>0 else 0.0,
        'f0_std':float(f0.std()) if len(f0)>0 else 0.0,
        'spectral_centroid_mean':float(sc.mean()),
        'spectral_centroid_std':float(sc.std()),
        'jitter':jitter,
        'shimmer':shimmer,
        'speaking_rate':speaking_rate
    }

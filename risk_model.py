import numpy as np

def clamp(x, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, x)))

def risk_score(b):
    """
    Lightweight, interpretable risk indicator.
    This is NOT a diagnostic model.

    Biomarkers used:
      - pause_ratio
      - f0_mean (Hz)
      - f0_std (Hz)
      - spectral_centroid_std
      - jitter         (cycle-to-cycle F0 variation)
      - shimmer        (cycle-to-cycle amplitude variation)
      - speaking_rate  (syllables/sec)
    """

    # --- Normalization (conservative, heuristic ranges) ---

    # Speech activity balance
    pause_ratio = clamp(b["pause_ratio"])            # already in [0,1]

    # Pitch biomarkers
    f0_mean_norm = clamp(b["f0_mean"] / 200.0)       # typical range ~80–250 Hz
    f0_std_norm  = clamp(b["f0_std"] / 80.0)         # variability scale

    # Spectral stability
    spec_std_norm = clamp(b["spectral_centroid_std"] / 3000.0)

    # Voice quality (perturbation) biomarkers
    jitter_norm  = clamp(b.get("jitter", 0.0) / 0.05)    # relative F0 perturbation
    shimmer_norm = clamp(b.get("shimmer", 0.0) / 0.15)   # relative amplitude perturbation

    # Articulation rate: slowed speech raises risk; normal ~4 syll/s
    speaking_rate = b.get("speaking_rate", 4.0)
    slow_rate_norm = clamp((4.0 - speaking_rate) / 4.0)

    # --- Weighted linear combination ---
    # Weights chosen for interpretability, not clinical calibration (sum to 1.0)

    score = (
        0.22 * pause_ratio +             # pauses / reduced speech activity
        0.08 * f0_mean_norm +            # pitch shift
        0.20 * f0_std_norm +             # prosodic instability
        0.12 * spec_std_norm +           # spectral instability
        0.18 * jitter_norm +             # frequency perturbation (hoarseness)
        0.12 * shimmer_norm +            # amplitude perturbation (breathiness)
        0.08 * slow_rate_norm            # slowed articulation rate
    )

    return clamp(score)

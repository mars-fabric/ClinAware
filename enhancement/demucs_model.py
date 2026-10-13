import torch
from demucs.pretrained import get_model
from demucs.apply import apply_model
_model=None

def enhance(sig,sr):
    global _model
    if _model is None: _model=get_model('htdemucs').cpu().eval()
    w=torch.tensor(sig).float()[None]
    if w.shape[0]==1: w=w.repeat(2,1)
    w=w[None]
    with torch.no_grad():
        out=apply_model(_model,w,device='cpu')[0]
        return out[0].flatten().numpy() if out.shape[0]>1 else out.flatten().numpy()

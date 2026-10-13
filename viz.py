import matplotlib.pyplot as plt, librosa, librosa.display, io, base64, numpy as np

def spec(sig,sr,t):
    fig,ax=plt.subplots(figsize=(3,1.5),dpi=300)
    S=librosa.amplitude_to_db(abs(librosa.stft(sig)),ref=np.max)
    librosa.display.specshow(S,sr=sr,ax=ax,x_axis='s',y_axis='linear')
    yticks = ax.get_yticks()
    ax.set_yticklabels([f"{yt/1000:.1f}" for yt in yticks],fontsize=5)
    ax.set_ylabel("Freq. (kHz)",fontsize=6)
    ax.set_xlabel("Time (s)",fontsize=6)
    ax.tick_params(axis='x',labelsize=5)
    buf=io.BytesIO()
    plt.savefig(buf,format='png',bbox_inches='tight',pad_inches=0.05,dpi=300)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()

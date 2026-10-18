# descriptive fits of |phi_v| (five-grid Romberg extrapolant) on U=1, v in [45,108]:  (a) single power A(1+v)^-q,  (b) A0 (1+v)^-(k+1) + C exp(-g v)
# residuals are relative (ln-ratio); amplitude ratio = A0 / (k B r+/r-)
import json, numpy as np, analyze, warnings
from scipy.optimize import least_squares
warnings.filterwarnings('ignore')
kp=0.048969; rr=9.897927/1.057475
for fn,k in [('gen_B0.03_k0.5_A0_U1_w0.3_v110.json',.5),('gen_B0.03_k1.5_A0_U1_w0.3_v110.json',1.5),('gen_B0.03_k2.5_A0.02_U1_w0.3_v110.json',2.5)]:
    D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq'])
    y=np.abs(analyze.extrap([np.array(D['data'][h]['PV'][2]) for h in hs])[-1][0])
    m=(vq>=45)&(vq<=108); v=vq[m]; y=y[m]; amp=k*0.03*rr
    fa=lambda p,v: np.exp(p[0])*(1+v)**(-p[1])
    fb=lambda p,v: np.exp(p[0])*(1+v)**(-(k+1))+np.exp(p[1])*np.exp(-p[2]*v)
    best=None
    for p0 in ([-3,2],[0,3],[3,4]):
        r=least_squares(lambda p: np.log(fa(p,v))-np.log(y),p0)
        if best is None or r.cost<best.cost: best=r
    ra=best; best=None
    for p0 in ([-4,-1,0.05],[0,-4,0.05],[-1,-2,0.03],[2,-4,0.06]):
        try: r=least_squares(lambda p: np.log(np.abs(fb(p,v)))-np.log(y),p0)
        except Exception: continue
        if best is None or r.cost<best.cost: best=r
    rb=best
    print('%s k=%g: single power  exponent %.2f  rms %.2f%% max %.2f%% | tail+exp  gamma %.4f (kappa_+=%.4f)  A0/transported %.2f  rms %.2f%% max %.2f%%'%(fn[4:30],k,ra.x[1],100*np.sqrt(np.mean(ra.fun**2)),100*np.abs(ra.fun).max(),rb.x[2],kp,np.exp(rb.x[0])/amp,100*np.sqrt(np.mean(rb.fun**2)),100*np.abs(rb.fun).max()))

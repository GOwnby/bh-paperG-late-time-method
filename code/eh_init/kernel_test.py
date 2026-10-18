# Linear-response test: phi_v(U,v) = int_0^v K(v-v') f(v') dv',  f = d phi_H/dv.
# K is measured from a compact H+ pulse (Gaussian flux, width 2, area -B, B=0.003 so that the background is static to 1e-3) and applied to the power-law tail (B=0.03, k=3/2).
import json, numpy as np, analyze, warnings
warnings.filterwarnings('ignore')
def get(fn,n):
    D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq'])
    return vq,analyze.extrap([np.array(D['data'][h]['PV'][n]) for h in hs])[-1][0],D
Bp=0.003; B=0.03; k=1.5
f=lambda v: -k*B*(1+v)**(-k-1)
for n in (0,2):
    vt,Pt,_=get('gen_B0.03_k1.5_A0_U1_w0.3_v110.json',n)
    Ks={}
    for vs,fn in ((10,'gen_B0.003_k1.5_A0_U1_w0.3_v110_P10_2.json'),(3,'gen_B0.003_k1.5_A0_U1_w0.3_v110_P3_2.json')):
        vq,R,D=get(fn,n); tau=vq-vs; K=R/(-Bp); Ks[vs]=(tau,K)
    print('ray U=%s'%[0.3,0.6,1.0,1.2][n])
    for vs,(tau,K) in Ks.items():
        ok=tau>=10 if vs==10 else tau>=17
        rates=[-(np.log(abs(K[int(t-tau[0]+3)]))-np.log(abs(K[int(t-tau[0]-3)])))/6 for t in (40,60,80,90)]
        print('  pulse v_s=%d: K(tau=30,40,60,80,95)='%vs,['%.3e'%K[int(t-tau[0])] for t in (30,40,60,80,95)],' local decay rate of K at tau=40,60,80,90:',np.round(rates,4))
        for V in (40,60,80,100):
            vp=np.linspace(0,V,40001); Kint=np.interp(V-vp,tau[ok],K[ok],left=0.0)
            pred=np.trapezoid(Kint*f(vp),vp); print('     predict tail-only v=%d: ratio pred/measured = %.3f'%(V,pred/Pt[int(V-vt[0])]))

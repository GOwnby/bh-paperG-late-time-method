# E11: kernel of the static interior with the accumulated mass parameter mu_f (f = 1 - 2(mu_f + M_N(r))/r) and the resulting flux compared with the PDE.
# usage: MU_F=9.9555e-3 python3 kernel_mu.py gen3_B0.03_k1.5_v300.json
import os,sys,json,numpy as np,warnings
warnings.filterwarnings('ignore')
fn=sys.argv[1]; sys.argv=[sys.argv[0]]
import transfer_vec_mu as TV, analyze
kp=TV.kp; km=TV.km; rp=TV.rp; rm=TV.rm; T0=(1+(rp/rm)**2)/2
print('MU_F=%s: r-=%.6f r+=%.6f kappa-=%.6f kappa+=%.6f T0=%.4f'%(os.environ.get('MU_F','0'),rm,rp,km,kp,T0))
dw=0.004; ws=np.arange(dw/2,6.0,dw); T,_=TV.Tvec(ws,ds=0.002); sig2=0.5
tau=np.arange(-12,200.5,0.5); Kt=(1/np.pi)*np.real((np.exp(-1j*np.outer(tau,ws))*(T*np.exp(-ws**2*sig2/2))).sum(1))*dw
tc=60.0*0.05/kp; m=(tau>=tc)&(tau<=2*tc); y=Kt[m]*np.exp(kp*tau[m]); X=np.vstack([np.ones(m.sum()),np.exp(-kp*tau[m]),np.exp(-2*kp*tau[m])]).T
(R1,c1,c2),*_=np.linalg.lstsq(X,y,rcond=None); print('R1=%.5f c1=%.3f c2=%.3f'%(R1,c1,c2))
def Kf(t):
    t=np.asarray(t,float); out=np.interp(t,tau,Kt,left=0.0); tail=np.exp(-kp*t)*(R1+c1*np.exp(-kp*t)+c2*np.exp(-2*kp*t)); return np.where(t>2*tc,tail,out)
D=json.load(open(fn)); k=D['k']; B=D['B']; hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq'])
P=analyze.extrap([np.array(D['data'][h]['PV'][2]) for h in hs])[-1][0]
def pred(v):
    vp=np.concatenate([np.linspace(0,min(v,60),24001),np.linspace(min(v,60),v+12,100001)[1:]])
    return np.trapezoid(Kf(v-vp)*(-k*B*(1+vp)**(-k-1)),vp)
print('k=%g B=%g: PDE phi_v / kernel(mu_f) phi_v at v ='%(k,B))
print('  '+'  '.join('%d: %.5f'%(v,P[int(v-vq[0])]/pred(float(v))) for v in (100,150,200,250,280,290)))

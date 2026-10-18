# Analytic kernel for any fixed-l Hayward mass m_N (a_N=2 m_N, l=1) and comparison with a tail-only PDE run.  usage: python3 kernel_general.py <mN> <json>
import sys, json, numpy as np, warnings
mN=sys.argv[1]; fn=sys.argv[2]; sys.argv=[sys.argv[0],mN]
warnings.filterwarnings('ignore')
import transfer_vec as TV, analyze
kp=TV.kp; km=TV.km; T0=(1+(TV.rp/TV.rm)**2)/2
dw=0.004; ws=np.arange(dw/2,6.0,dw); T,_=TV.Tvec(ws,ds=0.002); sig2=0.5
tau=np.arange(-12,200.5,0.5); Kt=(1/np.pi)*np.real((np.exp(-1j*np.outer(tau,ws))*(T*np.exp(-ws**2*sig2/2))).sum(1))*dw
tc=40.0/ (kp/0.05) if False else 60.0*0.05/kp   # fit window scaled with 1/kappa_+: tau in [tc, 2 tc]
m=(tau>=tc)&(tau<=2*tc); y=Kt[m]*np.exp(kp*tau[m]); X=np.vstack([np.ones(m.sum()),np.exp(-kp*tau[m]),np.exp(-2*kp*tau[m])]).T
(R1,c1,c2),*_=np.linalg.lstsq(X,y,rcond=None)
print('m_N=%s: T0=%.4f  R1=%.5f  (K e^{kp tau} = R1 + c1 e^{-kp tau} + c2 e^{-2kp tau}, c1=%.3f c2=%.3f)'%(mN,T0,R1,c1,c2))
def Kf(t):
    t=np.asarray(t,float); out=np.interp(t,tau,Kt,left=0.0); tail=np.exp(-kp*t)*(R1+c1*np.exp(-kp*t)+c2*np.exp(-2*kp*t)); return np.where(t>2*tc,tail,out)
D=json.load(open(fn)); k=D['k']; B=D['B']; km_f=D['km']; hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq'])
n=2
P=analyze.extrap([np.array(D['data'][h]['PV'][n]) for h in hs])[-1][0]; S=np.abs(analyze.extrap([np.array(D['data'][h]['sV'][n]) for h in hs])[-1][0])
def pred(v):
    vp=np.concatenate([np.linspace(0,min(v,60),24001),np.linspace(min(v,60),v+12,100001)[1:]])
    return np.trapezoid(Kf(v-vp)*(-k*B*(1+vp)**(-k-1)),vp)
lam=S+2*np.gradient(np.log(np.abs(P)),vq)
print('k=%.1f B=%g U=%.1f  kappa-(mu_f)=%.5f kappa+=%.5f  kappa- - 2 kappa+ = %+.5f'%(k,B,D['Uq'][n],km_f,kp,km_f-2*kp))
print('   v    phi_v meas      pred       ratio    p_meas   lambda=|sV|+2dln|phi_v|/dv    kappa-(mu_f)-2kappa+')
for v in (40,60,80,100,120,150,180,210,240):
    if v>=vq[-1]-5: continue
    i=int(v-vq[0]); pm=-(np.log(abs(P[i+3]))-np.log(abs(P[i-3])))/(np.log(vq[i+3]+1)-np.log(vq[i-3]+1))
    print('  %4d  %.4e  %.4e  %.4f   %.2f   %+.4f   (|sV|-km = %+.1e)'%(v,P[i],pred(v),P[i]/pred(v),pm,lam[i],S[i]-km_f))
print('early windows (analytic kernel only): v, phi_v, lambda_pred=kappa_-(mu_f)+2 dln|phi_v|/dv (|sigma_v|~kappa_-)')
for v in (5,10,15,20,25,30,40,60):
    h=0.5; lp=km_f+2*(np.log(abs(pred(v+h)))-np.log(abs(pred(v-h))))/(2*h); print('  %3d  %.3e  %+.4f'%(v,pred(v),lp))

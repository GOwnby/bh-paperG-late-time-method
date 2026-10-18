# K(tau) from the ODE transfer function (Gaussian-smoothed like the measured pulse) vs PDE kernel; plus long-run comparison with the analytic kernel.
import json, numpy as np, analyze, warnings, transfer_vec as TV
warnings.filterwarnings('ignore')
kp=TV.kp
dw=0.004; ws=np.arange(dw/2,6.0,dw)
T,_=TV.Tvec(ws,ds=0.002)
np.save('T_mN5.npy',np.vstack([ws,T.real,T.imag]))
def Ksm(tau,sig2):   # smoothed with Gaussian of variance sig2: factor exp(-w^2 sig2/2)
    ph=np.exp(-1j*np.outer(tau,ws))
    return (1/np.pi)*np.real((ph*(T*np.exp(-ws**2*sig2/2))).sum(1))*dw
D=json.load(open('gen_B0.003_k1.5_A0_U1_w0.3_v150_P60_2.json')); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq'])
R=analyze.extrap([np.array(D['data'][h]['PV'][2]) for h in hs])[-1][0]; tau=vq-60; Kp=R/(-0.003)
Ka=Ksm(tau,2.0)
print('tau   K_PDE      K_ODE(smoothed)   ratio')
for t in (-4,-2,0,2,5,10,20,30,40,50,60,70,80,88):
    i=int(np.where(tau==t)[0][0]); print('%4d  %.4e  %.4e  %.4f'%(t,Kp[i],Ka[i],Kp[i]/Ka[i] if Ka[i]!=0 else np.nan))
# R1 from the (nearly unsmoothed) tail: K e^{kp tau} at large tau
tt=np.array([30.,40,60,80,100,150,200]); Ku=Ksm(tt,0.25)
print('K_ODE(tau) e^{kappa+ tau} (sigma^2=0.25):',np.round(Ku*np.exp(kp*tt),4))

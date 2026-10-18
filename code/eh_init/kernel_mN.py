# Kernel at smaller masses (E5): PDE pulse response (v_s=40, B=0.003, U=1) vs the ODE transfer function.  usage: python3 kernel_mN.py <mN> <json>
import sys, json, numpy as np, warnings
mN=sys.argv[1]; fn=sys.argv[2]; VS=float(sys.argv[3]) if len(sys.argv)>3 else 40.0; sys.argv=[sys.argv[0],mN]
warnings.filterwarnings('ignore')
import transfer_vec as TV, analyze
kp=TV.kp; km=TV.km; T0=(1+(TV.rp/TV.rm)**2)/2
dw=0.004; ws=np.arange(dw/2,6.0,dw); T,_=TV.Tvec(ws,ds=0.002)
D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq'])
R=analyze.extrap([np.array(D['data'][h]['PV'][2]) for h in hs])[-1][0]; tau=vq-VS; Kp=R/(-D['B'])
Ka=(1/np.pi)*np.real((np.exp(-1j*np.outer(tau,ws))*(T*np.exp(-ws**2))).sum(1))*dw
print('m_N=%s  r-=%.5f r+=%.5f kappa-=%.5f kappa+=%.5f  kappa-/kappa+=%.3f   T(0)=(1+(r+/r-)^2)/2=%.3f'%(mN,TV.rm,TV.rp,km,kp,km/kp,T0))
for t in (-2,0,5,10,20,30,40,60,80,100):
    if t>tau[-1]: print('  tau=%4d  beyond the run (tau_max=%d)'%(t,tau[-1])); continue
    i=int(np.where(tau==t)[0][0]); print('  tau=%4d  K_PDE %.4e  K_ODE %.4e  ratio %.4f'%(t,Kp[i],Ka[i],Kp[i]/Ka[i]))
rate=lambda K,t:-(np.log(abs(K[int(t-tau[0])+3]))-np.log(abs(K[int(t-tau[0])-3])))/6
tr=[t for t in (60,80,100) if t+3<=tau[-1]]
print('  local decay rate of K_PDE at tau=%s: %s   (kappa_+ = %.4f)'%(tr,' '.join('%.4f'%rate(Kp,t) for t in tr),kp))
iw=np.argmin(abs(ws-0.0)); print('  int K_PDE (all tau, trapezoid, tail e^{-kp}) = %.3f vs T0 %.3f'%(np.trapezoid(np.concatenate([Kp,Kp[-1]*np.exp(-kp*np.arange(1,3000))]),dx=1.0),T0))

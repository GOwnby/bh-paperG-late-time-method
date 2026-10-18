# Kernel from the ODE transfer function (m_N=5): K(tau) for tau<=TAU1 by Fourier inversion (Gaussian-smoothed, variance 0.5), beyond by R1 e^{-kp tau}(1 + a e^{-kp tau} + b e^{-2 kp tau}) fitted on [60,120].
# Then: (i) convolution with the tail f vs the v=300 runs; (ii) crossover table with the analytic kernel.
import json, numpy as np, analyze, warnings, transfer_vec as TV
warnings.filterwarnings('ignore')
kp=TV.kp; R1=0.64423; T0=(1+(TV.rp/TV.rm)**2)/2
dw=0.004; ws=np.arange(dw/2,6.0,dw); T,_=TV.Tvec(ws,ds=0.002)
sig2=0.5
tau=np.arange(-12,160.5,0.5); ph=np.exp(-1j*np.outer(tau,ws))
Kt=(1/np.pi)*np.real((ph*(T*np.exp(-ws**2*sig2/2))).sum(1))*dw
m=(tau>=60)&(tau<=120); y=Kt[m]*np.exp(kp*tau[m])/R1-1; X=np.vstack([np.exp(-kp*tau[m]),np.exp(-2*kp*tau[m])]).T
(a,b),*_=np.linalg.lstsq(X,y,rcond=None); res=np.abs(X@np.array([a,b])-y).max()
print('fit tail: a=%.3f b=%.3f  max resid of K e^{kp tau}/R1: %.1e ; int K (to 120, + tail) vs T0=%.3f'%(a,b,res,T0))
def Kf(t):
    t=np.asarray(t,float); out=np.interp(t,tau,Kt,left=0.0)
    tail=R1*np.exp(-kp*t)*(1+a*np.exp(-kp*t)+b*np.exp(-2*kp*t))
    return np.where(t>120,tail,out)
tt=np.arange(-12,5000,0.05); KK=Kf(tt); print('int K = %.3f'%np.trapezoid(KK,tt))
Bp=0.003
def pred(v,k):   # f(v')=0 for v'<0; kernel (smoothed, slightly acausal) integrated over v' in [0, v+12]
    vp=np.concatenate([np.linspace(0,min(v,60),24001),np.linspace(min(v,60),v+12,100001)[1:]])
    return np.trapezoid(Kf(v-vp)*(-k*Bp*(1+vp)**(-k-1)),vp)
for k,fn in ((0.5,'gen_B0.003_k0.5_A0_U1_w0.3_v300.json'),(1.5,'gen_B0.003_k1.5_A0_U1_w0.3_v300.json')):
    L=json.load(open(fn)); hl=sorted(L['data'],key=float,reverse=True); vl=np.array(L['vq'])
    P=analyze.extrap([np.array(L['data'][h]['PV'][2]) for h in hl])[-1][0]
    print('k=%.1f   v: measured, predicted(analytic kernel), ratio; p measured / predicted'%k)
    for v in (60,100,140,180,220,260,290):
        i=int(v-vl[0]); meas=P[i]; pr=pred(v,k)
        pm=-(np.log(abs(P[i+4]))-np.log(abs(P[i-4])))/(np.log(vl[i+4]+1)-np.log(vl[i-4]+1))
        pp=-(np.log(abs(pred(v+4,k)))-np.log(abs(pred(v-4,k))))/(np.log(v+5)-np.log(v-3))
        print('  %4d  %.4e  %.4e  %.4f   %.2f / %.2f'%(v,meas,pr,meas/pr,pm,pp))
print('crossover with analytic kernel (first v with phi_v within 10%% of T0 f(v)):')
for k in (0.5,1.5,2.0,3.0):
    vv=np.arange(60,6000,10.0); rat=np.array([pred(v,k)/(T0*(-k*Bp*(1+v)**(-k-1))) for v in vv]); ok=np.where(abs(rat-1)<0.1)[0]
    print('  k=%.1f  v_c=%s   ratio at v=100: %.2f'%(k,vv[ok[0]] if len(ok) else '>6000',rat[int((100-60)/10)]))
np.save('K_analytic_tau.npy',np.vstack([tau,Kt]))

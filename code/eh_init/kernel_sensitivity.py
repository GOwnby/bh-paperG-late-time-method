"""Sensitivity of the kernel prediction of phi_v (Section 4.3(b) of Paper G) to the two numerical choices made in kernel_analytic.py:
the variance sig2 of the Gaussian smoothing (baseline 0.5) and the window [t0,t1] on which the pole-tail coefficients a, b are fitted
(baseline [60,120]; the kernel is continued by R_1 e^{-kappa_+ tau}(1+a e^{-kappa_+ tau}+b e^{-2 kappa_+ tau}) beyond tau=t1).
Prints, for the B=0.003, U=1 tail-only runs (v1=300), the ratio measured/predicted phi_v at v=60,100,290 for k=1/2 and k=3/2.
usage: python3 kernel_sensitivity.py   (needs gen_B0.003_k{0.5,1.5}_A0_U1_w0.3_v300.json; output: results_kernel_sensitivity.txt)"""
import json, numpy as np, analyze, warnings, transfer_vec as TV, sys
warnings.filterwarnings('ignore')
kp=TV.kp; R1=0.64423
dw=0.004; ws=np.arange(dw/2,6.0,dw); T,_=TV.Tvec(ws,ds=0.002)
Bp=0.003
print('measured/predicted phi_v (Romberg, B=0.003, U=1); baseline sig2=0.5, fit window [60,120]')
meas={}
for k,fn in ((0.5,'gen_B0.003_k0.5_A0_U1_w0.3_v300.json'),(1.5,'gen_B0.003_k1.5_A0_U1_w0.3_v300.json')):
    L=json.load(open(fn)); hl=sorted(L['data'],key=float,reverse=True); vl=np.array(L['vq'])
    meas[k]=(vl,analyze.extrap([np.array(L['data'][h]['PV'][2]) for h in hl])[-1][0])
# last two rows: the higher terms of the pole expansion dropped (b = 0; a = b = 0), Sec. 4.2 'dropping its higher terms'
for sig2,win,drop in ((0.5,(60,120),0),(0.25,(60,120),0),(1.0,(60,120),0),(0.5,(80,140),0),(0.5,(50,110),0),(0.5,(60,120),1),(0.5,(60,120),2)):
    tau=np.arange(-12,200.5,0.5); ph=np.exp(-1j*np.outer(tau,ws))
    Kt=(1/np.pi)*np.real((ph*(T*np.exp(-ws**2*sig2/2))).sum(1))*dw
    m=(tau>=win[0])&(tau<=win[1]); y=Kt[m]*np.exp(kp*tau[m])/R1-1; X=np.vstack([np.exp(-kp*tau[m]),np.exp(-2*kp*tau[m])]).T
    (a,b),*_=np.linalg.lstsq(X,y,rcond=None)
    if drop >= 1: b = 0.0
    if drop == 2: a = 0.0
    def Kf(t):
        t=np.asarray(t,float); out=np.interp(t,tau,Kt,left=0.0)
        tail=R1*np.exp(-kp*t)*(1+a*np.exp(-kp*t)+b*np.exp(-2*kp*t)); return np.where(t>win[1],tail,out)
    def pred(v,k):
        vp=np.concatenate([np.linspace(0,min(v,60),24001),np.linspace(min(v,60),v+12,100001)[1:]])
        return np.trapezoid(Kf(v-vp)*(-k*Bp*(1+vp)**(-k-1)),vp)
    row=[]
    for k in (0.5,1.5):
        vl,P=meas[k]
        for v in (60,100,290): row.append(P[int(v-vl[0])]/pred(v,k))
    print('sig2=%.2f fit window [%d,%d]%s  a=%7.3f b=%7.3f | k=1/2: v=60,100,290: %.4f %.4f %.4f | k=3/2: v=60,100,290: %.4f %.4f %.4f'%(sig2,win[0],win[1],'' if drop == 0 else (' b dropped' if drop == 1 else ' a,b dropped'),a,b,*row))

# analytic interior kernel (m_N=5) built by kernel_analytic.py (K_analytic_tau.npy) + pole-expansion tail; flux phi_v = int K(v-v') j(v') dv'
import numpy as np, os, sys
_a=sys.argv; sys.argv=[_a[0]]
import transfer as TR
sys.argv=_a
kp=TR.kp; km=TR.km; rp=TR.rp; rm=TR.rm; R1=0.64423; T0=(1+(rp/rm)**2)/2
_here=os.path.dirname(os.path.abspath(__file__))
tau,Kt=np.load(os.path.join(_here,'K_analytic_tau.npy'))
_m=(tau>=60)&(tau<=120); _y=Kt[_m]*np.exp(kp*tau[_m])/R1-1; _X=np.vstack([np.exp(-kp*tau[_m]),np.exp(-2*kp*tau[_m])]).T
(a_,b_),*_=np.linalg.lstsq(_X,_y,rcond=None)
def Kf(t):
    t=np.asarray(t,float); out=np.interp(t,tau,Kt,left=0.0)
    tail=R1*np.exp(-kp*t)*(1+a_*np.exp(-kp*t)+b_*np.exp(-2*kp*t))
    return np.where(t>120,tail,out)
def phi_v(v,k,B):
    """phi_v(v) for horizon data phi_H=B(1+v)^-k, i.e. j=-kB(1+v)^{-k-1} on v>=0 (kernel smoothed with variance 0.5, slightly acausal)"""
    vp=np.concatenate([np.linspace(0,min(v,60),24001),np.linspace(min(v,60),v+12,100001)[1:]])
    return np.trapezoid(Kf(v-vp)*(-k*B*(1+vp)**(-k-1)),vp)

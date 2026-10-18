# E11: same interface as kernel_lib.py, but the interior kernel is that of the static hole with the accumulated mass parameter mu_f (environment variable KERNEL_MU):
# f = 1 - 2(mu_f + M_N(r))/r; kernel by Fourier inversion of the ODE transfer function (as in kernel_analytic.py), tail fitted as K e^{kp tau} = R1 + c1 e^{-kp tau} + c2 e^{-2 kp tau}.
import os,sys,numpy as np
os.environ['MU_F']=os.environ['KERNEL_MU']
_a=sys.argv; sys.argv=[_a[0]]
import transfer_vec_mu as TV
sys.argv=_a
kp=TV.kp; km=TV.km; rp=TV.rp; rm=TV.rm; T0=(1+(rp/rm)**2)/2
_cache='K_mu_%s.npy'%os.environ['KERNEL_MU']
dw=0.004; ws=np.arange(dw/2,6.0,dw)
if os.path.exists(_cache): tau,Kt=np.load(_cache)
else:
    T,_=TV.Tvec(ws,ds=0.002); tau=np.arange(-12,200.5,0.5)
    Kt=(1/np.pi)*np.real((np.exp(-1j*np.outer(tau,ws))*(T*np.exp(-ws**2*0.5/2))).sum(1))*dw
    np.save(_cache,np.vstack([tau,Kt]))
tc=60.0*0.05/kp; _m=(tau>=tc)&(tau<=2*tc); _y=Kt[_m]*np.exp(kp*tau[_m]); _X=np.vstack([np.ones(_m.sum()),np.exp(-kp*tau[_m]),np.exp(-2*kp*tau[_m])]).T
(R1,c1,c2),*_r=np.linalg.lstsq(_X,_y,rcond=None)
def Kf(t):
    t=np.asarray(t,float); out=np.interp(t,tau,Kt,left=0.0); tail=np.exp(-kp*t)*(R1+c1*np.exp(-kp*t)+c2*np.exp(-2*kp*t)); return np.where(t>2*tc,tail,out)
def phi_v(v,k,B):
    vp=np.concatenate([np.linspace(0,min(v,60),24001),np.linspace(min(v,60),v+12,100001)[1:]])
    return np.trapezoid(Kf(v-vp)*(-k*B*(1+vp)**(-k-1)),vp)

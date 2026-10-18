# Crossover estimate with the analytic kernel (transfer.py ODE): phi_v / (T0 f) and local exponent p vs v for several k.  Replaces crossover.py (which used the measured, truncated kernel).
import numpy as np, warnings
warnings.filterwarnings('ignore')
tau,Kt=np.load('K_analytic_tau.npy'); kp=0.04896874; R1=0.64423; a_,b_=1.063,0.056; T0=44.3045; Bp=0.003
def Kf(t):
    t=np.asarray(t,float); out=np.interp(t,tau,Kt,left=0.0); tail=R1*np.exp(-kp*t)*(1+a_*np.exp(-kp*t)+b_*np.exp(-2*kp*t)); return np.where(t>120,tail,out)
def phi_v(v,k):
    vp=np.concatenate([np.linspace(0,min(v,60),24001),np.linspace(min(v,60),v+12,200001)[1:]])
    return np.trapezoid(Kf(v-vp)*(-k*Bp*(1+vp)**(-k-1)),vp)
def p_of(v,k):
    h=0.01*v; return -(np.log(abs(phi_v(v+h,k)))-np.log(abs(phi_v(v-h,k))))/(np.log(v+h+1)-np.log(v-h+1))
print('v:       ',[100,150,200,300,500,1000,3000])
for k in (0.5,1.5,2.0,3.0):
    rat=[phi_v(v,k)/(T0*(-k*Bp*(1+v)**(-k-1))) for v in (100,150,200,300,500,1000,3000)]
    ps=[p_of(v,k) for v in (100,150,200,300,500,1000,3000)]
    vv=np.arange(60,6000,10.0); r=np.array([phi_v(v,k)/(T0*(-k*Bp*(1+v)**(-k-1))) for v in vv]); ok=np.where(abs(r-1)<0.1)[0]
    print('k=%.1f  ratio'%k,np.round(rat,2),' p',np.round(ps,2),' v_c(10%%)=%s'%(vv[ok[0]] if len(ok) else '>6000'))

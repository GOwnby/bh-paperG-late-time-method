# Frequency-domain transfer function of the static interior between H+ and the Cauchy-horizon side (Paper E, Sec. 6.8, item xi).
# Mode phi = exp(-i w v) F(r) in ingoing EF coordinates; regular at r_+ (F(r_+)=1); at r->r_- F -> A + B (r-r_-)^{-i w/kappa_-}; T(w)=A(w).
# In s = ln x (x = U e^{kappa_+ v}): dr/ds = f/(2 kappa_+),  kappa_+ F_ss - i w F_s + (f/r) F_s - i w f F/(2 kappa_+ r) = 0.
import numpy as np, sys
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
mN,aN=5.0,10.0
if len(sys.argv)>1 and sys.argv[1]!='-': mN=float(sys.argv[1]); aN=2*mN
import os
MU=float(os.environ.get('MU_F','0'))   # accumulated mass parameter mu (E11): f = 1 - 2(mu + M_N(r))/r
MNf=lambda r: mN*r**3/(r**3+aN)
f=lambda r: 1-2*(MU+MNf(r))/r
rr=np.linspace(0.05,3*mN,200000); v=f(rr); idx=np.where(v[:-1]*v[1:]<0)[0]
# mu > 0.0278 adds a third, small root r_s ~ 2 mu: the Cauchy horizon r_- and the event horizon r_+ are the two largest roots
rm=brentq(f,rr[idx[-2]],rr[idx[-2]+1],xtol=1e-14); rp=brentq(f,rr[idx[-1]],rr[idx[-1]+1],xtol=1e-14)
h=1e-6; fp=lambda r:(f(r+h)-f(r-h))/(2*h)
kp=fp(rp)/2; km=-fp(rm)/2
def T(w,z0=1e-7,send=None):
    w=complex(w); a=-1j*w/(rp*(kp-1j*w))
    send=send or (40.0*kp/km+np.log(1/z0))      # until r-r_- ~ e^{-40}
    def rhs(s,y):
        r,F,G=y; ff=f(r)
        return [ff.real/(2*kp) if np.iscomplexobj(ff) else ff/(2*kp), G, (1j*w*G-(ff/r)*G+1j*w*ff*F/(2*kp*r))/kp]
    y0=np.array([rp-z0,1+a*z0,a*z0],dtype=complex)
    def rhs2(s,y):
        r=y[0].real; ff=f(r); return [ff/(2*kp), y[2], (1j*w*y[2]-(ff/r)*y[2]+1j*w*ff*y[1]/(2*kp*r))/kp]
    sol=solve_ivp(rhs2,[0,send],y0,method='DOP853',rtol=1e-12,atol=1e-30)
    r,F,G=sol.y[:,-1]
    return F-kp*G/(1j*w), r.real-rm
if __name__=='__main__':
    print('m_N=%g r-=%.6f r+=%.6f kappa-=%.6f kappa+=%.6f ; (1+(r+/r-)^2)/2 = %.4f'%(mN,rm,rp,km,kp,(1+(rp/rm)**2)/2))
    for w in (1e-3,1e-2,0.05,0.1,0.3,1.0):
        A,dr=T(w); print('w=%g  T=A=%.6f%+.6fj   |T|=%.4f  (r-r_- at end %.1e)'%(w,A.real,A.imag,abs(A),dr))

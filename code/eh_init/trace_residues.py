"""R_1 (residue of the interior transfer function at w=-i kappa_+), by central difference and by a contour integral; and T(0).  usage: trace_residues.py [mN]"""
import numpy as np, sys, transfer
kp=transfer.kp; rp=transfer.rp; rm=transfer.rm
print('mN=%g  kappa+=%.5f kappa-=%.5f  r-=%.6f r+=%.6f'%(transfer.mN,kp,transfer.km,rm,rp))
d=2e-4; w1=-1j*kp
Tp,_=transfer.T(w1+d,send=None); Tm,_=transfer.T(w1-d,send=None)
R1=-1j*d*(Tp-Tm)/2
print('R1 (difference of T(w1+-d), d=%g): %.5f %+.1ej'%(d,R1.real,R1.imag))
for rad in (0.3,0.5):
    N=64; th=2*np.pi*(np.arange(N)+0.5)/N; rr=rad*kp
    ws=w1+rr*np.exp(1j*th); vals=np.array([transfer.T(w,send=None)[0] for w in ws])
    Res=np.mean(vals*rr*np.exp(1j*th))   # (1/2 pi i) oint T dw = mean(T * (w-w1))
    R=-1j*Res; print('R1 (contour, radius %.1f kappa+, %d points): %.5f %+.1ej'%(rad,N,R.real,R.imag))
T0=(1+(rp/rm)**2)/2; A,_=transfer.T(1e-3,send=None)
print('T(0)=(1+r+^2/r-^2)/2 = %.4f ; A(w=1e-3) = %.4f %+.1ej ; difference %.4f'%(T0,A.real,A.imag,A.real-T0))

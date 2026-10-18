"""Rate-only version of the ray integration (Sec. ray): r=const, |sigma_v|=kappa' const, phi_v from the kernel with horizon data B(1+v)^-k.
rho'=-kappa' rho+4 pi r phi_v^2, d ln M/dv = 4 pi r phi_v^2/rho (exact for M>>r), q_M=(kappa'-rate)(v+1) -> 2k+2.  The value of kappa' and of r drops out of q_M's limit."""
import numpy as np, sys
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
import kernel_lib as KL
kap=0.7848; V=3000; B=1.0
vs=np.arange(0,V+1,1.0)
print('  k    crossover(10%)   q_M at v=300,1000,2000,3000   (2k+2)   C-ish: ln-rate deficit')
for k in (0.5,1.5,2.0,3.0):
    P=np.array([KL.phi_v(v,k,B) for v in vs]); P0=P.copy(); P=P/np.abs(P).max(); sp=CubicSpline(vs,P)
    sol=solve_ivp(lambda v,y:[-kap*y[0]+sp(v)**2],[0,V],[sp(0)**2/kap],method='DOP853',rtol=1e-11,atol=1e-80,dense_output=True)
    q=lambda v: (kap-sp(v)**2/sol.sol(v)[0])*(v+1)
    # crossover: |phi_v| within 10% of T(0) j(v)
    j=k*B*(1+vs)**(-k-1); T0=KL.T0; rat=np.abs(P0)/(T0*j); cx=vs[np.where(np.abs(rat-1)>0.1)[0][-1]+1]
    print('  %.1f   %5d           %s       %g'%(k,cx,'  '.join('%.4f'%q(v) for v in (300,1000,2000,3000)),2*k+2),flush=True)

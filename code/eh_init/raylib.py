# E3: exact integration of the ray equations at fixed U (fixed s) in double-null gauge ds^2=-W ds dv, W=e^sigma.
# Closed system given sigma_v(v) and phi_v(v) on the ray:
#   r'     = r_v
#   r_v'   = sigma_v r_v - 4 pi r phi_v^2                         (v-Raychaudhuri constraint)
#   Y'     = -Y (sigma_v + r_v/r) - S(r),  Y=r_s/W, S=(1-2M_N'(r))/(4r)   (from r_sv = -r_s r_v/r - (W/4r)(1-2M_N'), dn1)
#   M      = r/2 + 2 r Y r_v                                       (Misner-Sharp mass; = r/2 (1+4 r_s r_v/W))
# We use rho=-r_v>0, y=-Y>0 and L=ln y so that e^{kappa_- v} never overflows: 
#   r' = -rho ; rho' = sigma_v rho + 4 pi r phi_v^2 ; L' = rho/r - sigma_v + S e^{-L};  M = r/2 (1+4 e^L rho)
import numpy as np
from scipy.integrate import solve_ivp
mN,aN=5.0,10.0
def MNp(r,mN=mN,aN=aN): return 3*mN*aN*r**2/(r**3+aN)**2
def MN(r,mN=mN,aN=aN): return mN*r**3/(r**3+aN)
def integrate(v0,v1,r0,rho0,L0,sV,Pv,mN=mN,aN=aN,rtol=1e-12,dense=True,nrt=None):
    """sV(v), Pv(v) callables (sigma_v, phi_v). returns solve_ivp solution with y=[r,rho,L]"""
    def f(v,Y):
        r,rho,L=Y; s=sV(v); p=Pv(v); S=(1-2*MNp(r,mN,aN))/(4*r)
        return [-rho, s*rho+4*np.pi*r*p*p, rho/r-s+S*np.exp(-L)]
    return solve_ivp(f,[v0,v1],[r0,rho0,L0],method='DOP853',rtol=rtol,atol=[1e-14,0,1e-12],dense_output=dense)
def Mof(Y): 
    r,rho,L=Y; return 0.5*r*(1+4*np.exp(L)*rho)
def lnMof(r,rho,L):
    """ln M = ln(r/2) + ln(1 + 4 e^L rho), overflow-safe"""
    return np.log(r/2)+np.logaddexp(0.0,np.log(4.0)+L+np.log(rho))

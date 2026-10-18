# E8: ray equations with the Polyakov (conformal-anomaly) stress tensor added to the v-Raychaudhuri source.
#   r' = -rho ;  rho' = sigma_v rho + 4 pi r ( phi_v^2 + T^q_vv ) ;  L' = rho/r - sigma_v + S e^{-L} ;  M = r/2 (1 + 4 e^L rho)
#   T^q_vv = - hbar (sigma_v^2 - 2 sigma_vv) / (192 pi^2 r^2)    (s-wave, 'in' vacuum: t_v = 0;  1+1 result -hbar/(48 pi)(sigma_v^2-2sigma_vv) divided by 4 pi r^2)
# At sigma_v = -kappa, sigma_vv = 0 this is -hbar kappa^2/(192 pi^2 r^2) = Barcelo-Boyanov-Carballo-Rubio-Garay 2022 (PRD 106, 124006) Eq. (53) with lambda -> 0 (the -kappa^2/2 term).
import numpy as np
from scipy.integrate import solve_ivp
from raylib import MNp, MN, mN, aN
def integrate_sc(v0,v1,r0,rho0,L0,sV,Pv,hbar,sVv=None,rtol=1e-12):
    def f(v,Y):
        r,rho,L=Y; s=sV(v); p=Pv(v); S=(1-2*MNp(r))/(4*r)
        d=1e-3*max(1.0,v*0.01); sv2=(sV(v+d)-sV(v-d))/(2*d) if sVv is None else sVv(v)
        Tq=-hbar*(s*s-2*sv2)/(192*np.pi**2*r*r)
        return [-rho, s*rho+4*np.pi*r*(p*p+Tq), rho/r-s+S*np.exp(-L)]
    return solve_ivp(f,[v0,v1],[r0,rho0,L0],method='DOP853',rtol=rtol,atol=[1e-14,0,1e-12],dense_output=True)
def lnabsM(r,rho,L):
    """ln|M| and sign, overflow-safe: M = r/2 (1 + 4 e^L rho)"""
    a=np.log(4.0)+L+np.log(abs(rho)) if rho!=0 else -np.inf
    if rho>=0: return np.log(r/2)+np.logaddexp(0.0,a),+1
    # 1 - e^a : sign by a
    if a<0: return np.log(r/2)+np.log1p(-np.exp(a)),+1
    return np.log(r/2)+a+np.log1p(-np.exp(-a)) if a>0 else -np.inf,-1

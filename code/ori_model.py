"""Ori thin-null-shell model, state variable = Misner-Sharp mass M_+ on the shell (regular for every closure).
 dR/dv   = f(m_-,R)/2
 dM_+/dv = Rdot * G(M_+,R) + S (1-2M_+/R),     S = dM/dm(m_-,R) mdot_- / f(m_-,R)
 G = (dM/dr)_m expressed through (M,R).  Derivation: DTR relation f_a f_d = f_c f_b  -> dM_+/f_+ = dM_-/f_-  at fixed r=R.
Closure family  M = m r^3/(r^3+a(m)),  a(m) = 2 l0^2 m^{1+s}/m0^s :   G = 6 l0^2 M^2 (m/m0)^s / r^4,
(RN: M = m - Q^2/2r, G = Q^2/(2 r^2) independent of m.)
Closure 'hn' (additive Hayward--NED, used for the nonlinear comparison of Sec. 6): M = mu + m_N r^3/(r^3+a_N), G = M_N'(r) independent of M,
dM/dmu = 1, horizon condition N(r) = r^4 - 2(mu+m_N) r^3 + a_N r - 2 mu a_N = 0 (f = N/(r(r^3+a_N))).
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

class Cl:
    def __init__(c,kind,ell=1.0,m0=5.0,s=0.0,Q=0.8,mN=5.0,aN=10.0):
        c.kind,c.l,c.m0,c.s,c.Q=kind,ell,m0,s,Q
        c.mN,c.aN=mN,aN
    def a(c,m): return 2*c.l**2*m**(1+c.s)/c.m0**c.s
    def ap(c,m): return 2*c.l**2*(1+c.s)*m**c.s/c.m0**c.s
    def _N(c,mu,r): return r**4-2*(mu+c.mN)*r**3+c.aN*r-2*mu*c.aN
    def _Nd(c,mu,r,k):
        co=[1.0,-2*(mu+c.mN),0.0,c.aN,-2*mu*c.aN]
        return np.polyval(np.polyder(co,k) if k>0 else co,r)
    def P(c,m,r):
        if c.kind=='hn': return c._N(m,r)
        return r*r-2*m*r+c.Q**2 if c.kind=='rn' else r**3-2*m*r*r+c.a(m)
    def Pr(c,m,r):
        if c.kind=='hn': return c._Nd(m,r,1)
        return 2*r-2*m if c.kind=='rn' else 3*r*r-4*m*r
    def Prr(c,m,r):
        if c.kind=='hn': return c._Nd(m,r,2)
        return 2.0 if c.kind=='rn' else 6*r-4*m
    def Pm(c,m,r):
        if c.kind=='hn': return -2*r**3-2*c.aN
        return -2*r if c.kind=='rn' else -2*r*r+c.ap(m)
    def D(c,m,r):
        if c.kind=='hn': return r*(r**3+c.aN)
        return r*r if c.kind=='rn' else r**3+c.a(m)
    def M(c,m,r):
        if c.kind=='hn': return m+c.mN*r**3/(r**3+c.aN)
        return m-c.Q**2/(2*r) if c.kind=='rn' else m*r**3/(r**3+c.a(m))
    def dMdm(c,m,r):
        if c.kind in ('rn','hn'): return 1.0
        X=r**3+c.a(m); return r**3*(X-m*c.ap(m))/X**2
    def rminus(c,m):
        if c.kind=='rn': return m-np.sqrt(m*m-c.Q**2)
        rr=np.linspace(0.05*c.l,2*(m+c.mN) if c.kind=='hn' else 2*m,3000); v=c.P(m,rr)
        i=np.where(np.sign(v[:-1])*np.sign(v[1:])<0)[0][0]
        return brentq(lambda x:c.P(m,x),rr[i],rr[i+1],xtol=1e-15,rtol=1e-15)
    def f_taylor(c,m,rm,q):
        if c.kind=='hn':
            Pv=c.Pr(m,rm)*q+0.5*c.Prr(m,rm)*q*q+c._Nd(m,rm,3)/6*q**3+q**4
        else: Pv=c.Pr(m,rm)*q+0.5*c.Prr(m,rm)*q*q+(q**3 if c.kind!='rn' else 0.0)
        return Pv/c.D(m,rm+q)
    def mofM(c,M,r):
        if c.kind=='rn': return M+c.Q**2/(2*r)
        if c.kind=='hn': return M-c.mN*r**3/(r**3+c.aN)
        if c.s==0: return M*r**3/(r**3-2*c.l**2*M)
        if c.s==-1: return M*(r**3+c.a(1.0))/r**3
        # log-space solve for w=m/m0 (safe for huge M)
        lM=np.log(M); l0=np.log(c.m0); a0=np.log(2*c.l**2*c.m0)
        h=lambda lw: l0+lw+3*np.log(r)-np.logaddexp(3*np.log(r),a0+(1+c.s)*lw)-lM
        lo=lM-l0-1e-12; hi=lo+1.0
        while h(hi)<0: hi=lo+2*(hi-lo)
        return c.m0*np.exp(brentq(h,lo,hi,xtol=1e-14,rtol=1e-15))
    def G(c,M,r):
        if c.kind=='rn': return c.Q**2/(2*r*r)
        if c.kind=='hn': return 3*c.mN*c.aN*r*r/(r**3+c.aN)**2
        if c.s==0: return 6*c.l**2*M*M/r**4
        m=c.mofM(M,r); return 6*c.l**2*M*((m/c.m0)**c.s*M)/r**4 if np.isfinite(m) else 3*M/r

def run(cl,minf,delta,p,v0,v1,D0=1e-6,q0=1e-3,rtol=1e-11,dense=True):
    mm=lambda v:minf-delta*v**(-p); dmm=lambda v:p*delta*v**(-p-1)
    def rhs(v,y):
        q,lnD=y; m_=mm(v); rm=cl.rminus(m_); drm=-cl.Pm(m_,rm)/cl.Pr(m_,rm)
        fm=cl.f_taylor(m_,rm,q); R=rm+q
        dq=0.5*fm-drm*dmm(v)
        S=cl.dMdm(m_,R)*dmm(v)/fm
        # evolve Y = M_+ - M_-?  simpler: evolve M_+ directly
        return dq,S
    # state y=(q,M)
    def rhsM(v,y):
        q,M=y; m_=mm(v); rm=cl.rminus(m_); drm=-cl.Pm(m_,rm)/cl.Pr(m_,rm)
        fm=cl.f_taylor(m_,rm,q); R=rm+q; Rdot=0.5*fm
        S=cl.dMdm(m_,R)*dmm(v)/fm
        return [Rdot-drm*dmm(v), Rdot*cl.G(M,R)+S*(1-2*M/R)]
    m_=mm(v0); rm=cl.rminus(m_)
    y0=[q0, cl.M(m_,rm+q0)+D0]
    return solve_ivp(rhsM,[v0,v1],y0,method='LSODA',rtol=rtol,atol=1e-300,dense_output=dense)

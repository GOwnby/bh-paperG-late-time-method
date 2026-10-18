"""Double-null characteristic evolution of the spherically symmetric Einstein--NED(Hayward)--massless-scalar system.

    ds^2 = -W du dv + r^2 dOmega^2 ,  W = e^sigma ,  G = 1
    r_uv    = -r_u r_v / r - (W/4r) (1 - 2 M_N'(r))
    sig_uv  = -2 r_uv / r - 8 pi phi_u phi_v + W M_N''(r) / (2 r)
    phi_uv  = -(r_u phi_v + r_v phi_u)/r
    M       = (r/2)(1 + 4 r_u r_v / W)                      (Misner--Sharp mass)
    Raychaudhuri:  r_uu - sig_u r_u + 4 pi r phi_u^2 = 0   (and u<->v)
  with M_N(r) = m_N r^3/(r^3 + a_N)  (NED monopole, additive closure M = M_N(r) + mu).

First-order form: r, sigma, r_u, r_v, sigma_u, sigma_v, phi_u, phi_v are all evolved, so quantities that are
exponentially small near the Cauchy horizon keep full *relative* precision (no differences of nearly equal numbers).
Scheme: Gundlach--Price--Pullin-type diamond (second order); r, sigma by the 'diamond' identity, the first
derivatives by trapezoidal integration along the characteristic edges; predictor-corrector, 3 sweeps.
Initial data: sigma prescribed (= static background) on both initial null rays; r from Raychaudhuri; phi analytic.
"""
import numpy as np, ctypes, os
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
_here=os.path.dirname(os.path.abspath(__file__))
lib2=ctypes.CDLL(os.path.join(_here,'libdouble_null.so'))
dp=ctypes.POINTER(ctypes.c_double)
lib2.evolve2.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double]+[dp]*8+[ctypes.c_int]

class Bg:
    def __init__(s,mN=5.0,aN=None,tmax=60.0):
        if aN is None: aN=2*mN   # ell=1: a_N = 2 m_N ell^2 (mN=5 -> 10)
        s.mN,s.aN=mN,aN
        P=lambda r:r**3-2*mN*r*r+aN
        rr=np.linspace(0.05,2*mN,20000); v=P(rr); idx=np.where(np.sign(v[:-1])*np.sign(v[1:])<0)[0]
        from scipy.optimize import brentq
        s.rm=brentq(P,rr[idx[0]],rr[idx[0]+1],xtol=1e-15,rtol=1e-15); s.rp=brentq(P,rr[idx[1]],rr[idx[1]+1],xtol=1e-15,rtol=1e-15)
        s.Pp=3*s.rm**2-4*mN*s.rm; s.Ppp=6*s.rm-4*mN
        s.kap=-0.5*s.Pp/(s.rm**3+aN)   # kappa_- = |f'(r_-)|/2
        s.kap_p=0.5*abs((3*s.rp**2-4*mN*s.rp)/(s.rp**3+aN))
        y0=0.5*(s.rp-s.rm)
        fy=lambda y: (s.Pp*y+0.5*s.Ppp*y*y+y**3)/((s.rm+y)**3+aN)
        a=solve_ivp(lambda t,y:[fy(y[0])],[0,tmax],[y0],method='DOP853',rtol=1e-13,atol=1e-300,dense_output=True)
        b=solve_ivp(lambda t,y:[fy(y[0])],[0,-30],[y0],method='DOP853',rtol=1e-13,atol=1e-300,dense_output=True)
        s.a_,s.b_=a,b
        s.fy=fy
    def y(s,rs):
        rs=np.asarray(rs,float); out=np.empty_like(rs)
        pos=rs>=0
        out[pos]=s.a_.sol(rs[pos])[0] if pos.any() else 0
        out[~pos]=s.b_.sol(rs[~pos])[0] if (~pos).any() else 0
        return out
    def W(s,y): return np.abs(s.fy(y))

def MNp(bg,r): d=r**3+bg.aN; return 3*bg.mN*bg.aN*r*r/d**2
def MNpp(bg,r): d=r**3+bg.aN; return 6*bg.mN*bg.aN*r*(bg.aN-2*r**3)/d**3
def fr(bg,r): return (r**3-2*bg.mN*r*r+bg.aN)/(r**3+bg.aN)
def dfr(bg,r):
    d=r**3+bg.aN; P=r**3-2*bg.mN*r*r+bg.aN
    return ((3*r*r-4*bg.mN*r)*d-P*3*r*r)/d**2
def F(bg,r,sg,ru,rv,pu,pv):
    W=np.exp(sg); a=-ru*rv/r-W/(4*r)*(1-2*MNp(bg,r))
    return a, -2*a/r-8*np.pi*pu*pv+W*MNpp(bg,r)/(2*r), -(ru*pv+rv*pu)/r
def run2(bg,arrs,hu,hv,niter=3):
    nv,nu=arrs[0].shape
    p=lambda a:a.ctypes.data_as(dp)
    lib2.evolve2(nu,nv,hu,hv,bg.mN,bg.aN,*[p(a) for a in arrs],niter)
    return arrs
def mass(bg,arrs):
    R,SG,RU,RV=arrs[:4]
    return 0.5*R*(1+4*RU*RV*np.exp(-SG))

def build2(bg,u0,u1,v0,v1,hu,hv,A,B,rtol=1e-12,width=1.0,k=1.5):
    """Gauge: sigma prescribed = background sigma on both initial null lines; r from Raychaudhuri; phi analytic."""
    nu=int(round((u1-u0)/hu))+1; nv=int(round((v1-v0)/hv))+1
    u=u0+hu*np.arange(nu); v=v0+hv*np.arange(nv)
    ph1=lambda x: B+A*np.exp(-(x/width)**2); dph1=lambda x:-2*x/width**2*A*np.exp(-(x/width)**2)
    ph2=lambda x: B*(1+x)**(-k);    dph2=lambda x:-k*B*(1+x)**(-k-1)
    yc=bg.y(np.array([(u0+v0)/2]))[0]; rc=bg.rm+yc; fc=bg.fy(yc)
    out={}
    for name,(s0,s1,n,h,t0,dph,dpt) in {'u':(u0,u1,nu,hu,v0,dph1,dph2(v0)),'v':(v0,v1,nv,hv,u0,dph2,dph1(u0))}.items():
        def rhs(s,Y,t0=t0,dph=dph,name=name):
            r,rs,rt,st,pt=Y
            y=bg.y(np.array([(s+t0)/2]))[0]; rb=bg.rm+y; f=bg.fy(y)
            sg=np.log(abs(f)); ss=dfr(bg,rb)/2          # sigma_s of background (gauge)
            ps=dph(s)
            rss=ss*rs-4*np.pi*r*ps**2
            if name=='u': a,b,c=F(bg,r,sg,rs,rt,ps,pt)
            else:         a,b,c=F(bg,r,sg,rt,rs,pt,ps)
            return [rs,rss,a,b,c]
        Y0=[rc,fc/2,fc/2,dfr(bg,rc)/2,dpt]
        sol=solve_ivp(rhs,[s0,s1],Y0,t_eval=s0+h*np.arange(n),method='DOP853',rtol=rtol,atol=1e-300)
        assert sol.success and sol.y.shape[1]==n,(name,sol.message)
        out[name]=sol.y
    R=np.zeros((nv,nu));SG=np.zeros((nv,nu));RU=np.zeros((nv,nu));RV=np.zeros((nv,nu))
    SU=np.zeros((nv,nu));SV=np.zeros((nv,nu));PU=np.zeros((nv,nu));PV=np.zeros((nv,nu));PH=np.zeros((nv,nu))
    Y=out['u']; yb=bg.y((u+v0)/2); rb=bg.rm+yb
    R[0,:]=Y[0]; SG[0,:]=np.log(np.abs(bg.fy(yb))); RU[0,:]=Y[1]; RV[0,:]=Y[2]; SU[0,:]=dfr(bg,rb)/2; SV[0,:]=Y[3]; PU[0,:]=dph1(u); PV[0,:]=Y[4]; PH[0,:]=ph1(u)
    Y=out['v']; yb=bg.y((u0+v)/2); rb=bg.rm+yb
    R[:,0]=Y[0]; SG[:,0]=np.log(np.abs(bg.fy(yb))); RV[:,0]=Y[1]; RU[:,0]=Y[2]; SV[:,0]=dfr(bg,rb)/2; SU[:,0]=Y[3]; PV[:,0]=dph2(v); PU[:,0]=Y[4]; PH[:,0]=ph2(v)
    return u,v,[R,SG,RU,RV,SU,SV,PU,PV],PH


def invariants(bg,arrs):
    """Curvature pieces from the stored fields: Misner-Sharp mass M and the three terms of the Kretschmann scalar
    K = R2^2 + 8 H_AB H^AB / r^2 + 4 (1-(grad r)^2)^2 / r^4,  H_AB = nabla_A nabla_B r,  R2 = 4 e^{-sigma} sigma_uv (2D curvature),
    H_uu = -4 pi r phi_u^2, H_vv = -4 pi r phi_v^2 (Raychaudhuri), H_uv = r_uv.  Returns M, T1, T2, T3, K."""
    R,SG,RU,RV,SU,SV,PU,PV=arrs; W=np.exp(SG)
    a,b,c=F(bg,R,SG,RU,RV,PU,PV)
    Huu=-4*np.pi*R*PU**2; Hvv=-4*np.pi*R*PV**2
    M=0.5*R*(1+4*RU*RV/W)
    T1=(4*np.exp(-SG)*b)**2
    T2=(8/R**2)*(8/W**2)*(Huu*Hvv+a**2)
    T3=4*(2*M/R)**2/R**4
    return M,T1,T2,T3,T1+T2+T3

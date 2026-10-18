"""Event-horizon-regular initial data: Kruskal-type coordinate U = exp(kappa_+ u); future event horizon H+ = {U=0}.
Static background (mu = 0): r = r_+ + z(x), x = U exp(kappa_+ v), z = -x w(x);  W~ = w G e^{kappa_+ v}/kappa_+  (EF gauge r_U = -W~/2)."""
import numpy as np, os
V0=float(os.environ.get('TAIL_V0','1.0'))
_PULSE=os.environ.get('TAIL_PULSE')   # 'vs,ws': phi_H'(v) = -B exp(-((v-vs)/ws)^2)/(ws sqrt(pi)) (impulse response test); default: power-law tail
def PHVF(k,B,v):
    if _PULSE:
        vs,ws=[float(x) for x in _PULSE.split(',')]
        return -B*np.exp(-((v-vs)/ws)**2)/(ws*np.sqrt(np.pi))
    return -k*B/V0*(1+v/V0)**(-k-1)
from scipy.integrate import solve_ivp, solve_bvp
from scipy.optimize import brentq
from dn2lib import *
class StaticU:
    def __init__(s,mN=5.0,aN=None):
        s.mN=mN; s.aN=2*mN if aN is None else aN
        P=lambda r:r**3-2*mN*r*r+s.aN
        rr=np.linspace(0.05,2*mN,40000); v=P(rr); idx=np.where(np.sign(v[:-1])*np.sign(v[1:])<0)[0]
        s.rm=brentq(P,rr[idx[0]],rr[idx[0]+1],xtol=1e-15,rtol=1e-15); s.rp=brentq(P,rr[idx[1]],rr[idx[1]+1],xtol=1e-15,rtol=1e-15)
        s.P1=3*s.rp**2-4*mN*s.rp; s.P2=6*s.rp-4*mN            # P'(r_+), P''(r_+)
        s.Dp=s.rp**3+s.aN; s.kp=0.5*s.P1/s.Dp                 # kappa_+ = f'(r_+)/2 (f = P/D)
        s.G0=2*s.kp
        s.tmin=np.log(1e-12)
        f=lambda t,w:[w[0]*(s.G(-np.exp(t)*w[0])/(2*s.kp)-1)]
        s.sol=solve_ivp(f,[s.tmin,np.log(5e4)],[1.0],method='DOP853',rtol=1e-13,atol=1e-300,dense_output=True)
    def D(s,z): return (s.rp+z)**3+s.aN
    def G(s,z): return (s.P1+0.5*s.P2*z+z*z)/s.D(z)          # f/(-x w) = G
    def w(s,x):
        x=np.asarray(x,float); out=np.ones_like(x); m=x>1e-12
        if m.any(): out[m]=s.sol.sol(np.log(x[m]))[0]
        return out
    def fields_small(s,U,v):
        U=np.asarray(U,float); x=U*np.exp(s.kp*v); w=s.w(x); z=-x*w; r=s.rp+z; G=s.G(z); Wt=w*G*np.exp(s.kp*v)/s.kp
        sig=np.log(Wt); fr=-x*w*G                              # f(r)
        D=s.D(z); Pp=s.P1+s.P2*z+3*z*z                         # P'(r)
        fp=(Pp*D-(fr*D)*3*r*r)/D**2                            # f'(r) = (P' D - P 3 r^2)/D^2 , P = f D
        rU=-0.5*Wt; rV=0.5*fr
        # sigma_U = (f'-2kappa)/(2 kappa U), written without cancellation:  d/dU ln(w G e^{kv}/k)
        Hz=(0.5*s.P2+z-s.G0*(3*s.rp**2+3*s.rp*z+z*z))/D       # (G-G0)/(z)
        dGdz=((0.5*s.P2+2*z)*D-(s.P1+0.5*s.P2*z+z*z)*3*r*r)/D**2
        zx=-w-x*(w*(s.G(z)/(2*s.kp)-1)/np.where(x>0,x,1))      # dz/dx  (second term -> finite)
        # (G-G0)/(2kappa x) = z/x * Hz/(2kappa) = -w Hz/(2 kappa)
        wlogd=-w*Hz/(2*s.kp)                                   # = (G/(2k)-1)/x
        zx=-w-x*w*wlogd
        sU=np.exp(s.kp*v)*(wlogd+dGdz*zx/G)
        sV=0.5*fp
        return r,sig,rU,rV,sU,sV

def _rho_init(s):
    s.r3=2*s.mN-s.rp-s.rm; s.d0=s.rp-s.rm
    ts=0.0                                    # x_s = 1
    z1=s.w(np.array([1.0]))[0]*(-1.0)         # z at x=1
    L0=np.log(s.d0+z1)
    f=lambda t,L:[ ( (s.rm+np.exp(L[0])-s.rp)*(s.rm+np.exp(L[0])-s.r3)/(s.D(s.rm+np.exp(L[0])-s.rp)) )/(2*s.kp) ]
    s.solL=solve_ivp(f,[0,np.log(5e4)],[L0],method='DOP853',rtol=1e-13,atol=1e-14,dense_output=True)
def fields(s,U,v):
    U=np.asarray(U,float); U,vv=np.broadcast_arrays(U,np.asarray(v,float)); ev=np.exp(s.kp*vv); x=U*ev
    small=x<1.0
    a=s.fields_small(np.where(small,U,0.5*np.exp(-s.kp*vv)),vv)
    if not hasattr(s,'solL'): _rho_init(s)
    xb=np.where(small,2.0,x); rho=np.exp(s.solL.sol(np.log(xb).ravel())[0]).reshape(xb.shape); z=rho-s.d0; r=s.rm+rho
    D=s.D(z); P=z*rho*(r-s.r3); fr=P/D; Pp=s.P1+s.P2*z+3*z*z
    Ub=np.where(small,1.0,U)
    Wt=-fr/(s.kp*Ub); sig=np.log(Wt); rU=-0.5*Wt; rV=0.5*fr
    fp=(Pp*D-P*3*r*r)/D**2; sU=(fp/(2*s.kp)-1)/Ub; sV=0.5*fp
    b=(r,sig,rU,rV,sU,sV)
    return tuple(np.where(small,A,B) for A,B in zip(a,b))
StaticU.fields=fields
if __name__=='__main__':
    S=StaticU(); print('rp',S.rp,'kappa+',S.kp)
    U=np.array([0.0,1e-9,1e-6,1e-3,0.5,2.0,5.0]); 
    for v in (0.0,20.0):
        r,sig,rU,rV,sU,sV=S.fields(U,v)
        print('v',v); print(' r',r); print(' sig',sig); print(' rU',rU); print(' rV',rV); print(' sU',sU); print(' sV',sV)
    # consistency: finite-difference derivatives
    for U0 in (1e-3,0.7,3.0):
        h=1e-6*max(U0,1e-3); a=S.fields(np.array([U0-h,U0+h]),5.0); b=S.fields(np.array([U0]),5.0)
        print('U',U0,'dr/dU err',(a[0][1]-a[0][0])/(2*h)-b[2][0],'dsig/dU err',(a[1][1]-a[1][0])/(2*h)-b[4][0])
        hv=1e-5; c=[S.fields(np.array([U0]),5.0+d) for d in (-hv,hv)]
        print('   dr/dv err',(c[1][0][0]-c[0][0][0])/(2*hv)-b[3][0],'dsig/dv err',(c[1][1][0]-c[0][1][0])/(2*hv)-b[5][0])

def MNp_(S,r): d=r**3+S.aN; return 3*S.mN*S.aN*r*r/(d*d)
def horizon(S,B,k,vH,r0=None):
    """Teleological event horizon H+ in EF gauge (r_U=-W~/2 on U=0). Backward shooting (stable direction) from (r_f,r_v=0) at vH,
    r_f fixed by r(0)=r_+.  Returns object with .sol(v)->(r,r_v), and .rf."""
    from scipy.optimize import brentq
    r0=S.rp if r0 is None else r0
    phv=lambda v:PHVF(k,B,v)
    def f(v,y):
        r,rv=y; return [rv, rv*((1-2*MNp_(S,r))/(2*r)-rv/r)-4*np.pi*r*phv(v)**2]
    def shoot(rf,dense=False):
        return solve_ivp(f,[vH,0.0],[rf,0.0],method='DOP853',rtol=1e-13,atol=1e-300,dense_output=dense)
    g=lambda rf: shoot(rf).y[0,-1]-r0
    if B==0:
        rf=r0
    else:
        a=r0; b=r0+1e-12
        while g(b)<0: b=r0+2*(b-r0)
        rf=brentq(g,a,b,xtol=1e-16,rtol=1e-15)
    so=shoot(rf,True)
    class H: pass
    h=H(); h.rf=rf; h.sol=lambda v: so.sol(v); return h
def build_eh(S,U1,v1,hU,hv,B,k=1.5,vH=None,rtol=1e-12,c=None,pulse=None):
    """If c is None: uniform U grid (spacing hU). Else grid uniform in s (spacing hU) with U=c(e^{kp s}-1)/kp up to U1;
    returned arrays are then in (s,v) with sigma_s=sigma~+ln g', r_s=r_U g', sigma_ss=sigma~_U g'+kp, phi_s=phi_U g'."""
    nv=int(round(v1/hv))+1; v=hv*np.arange(nv)
    if c is None:
        nu=int(round(U1/hU))+1; U=hU*np.arange(nu); gp=np.ones(nu)
    else:
        smax=np.log(1+U1*S.kp/c)/S.kp; nu=int(round(smax/hU))+1; sg_=hU*np.arange(nu); U=c*np.expm1(S.kp*sg_)/S.kp; gp=c*np.exp(S.kp*sg_)
    vH=v1+150.0 if vH is None else vH
    hz=horizon(S,B,k,vH); phv=lambda v:PHVF(k,B,v)
    # ---- along H+ : sigma~, sigma~_U, phi_U ----
    r_,rv_,_,_,sU0,_=[a[0] for a in S.fields(np.array([0.0]),0.0)]
    def rhsH(t,Y):
        sg,sU,pU=Y; r,rv=hz.sol(t); rU=-0.5*np.exp(sg)
        _,b,c=F(S,r,sg,rU,rv,pU,phv(t))
        sgv=-rv/r+(1-2*MNp_(S,r))/(2*r)
        return [sgv,b,c]
    sH=solve_ivp(rhsH,[0,v1],[np.log(2.0),sU0,(0.0 if pulse is None else -2*pulse[0]*(0-pulse[1])/pulse[2]**2*np.exp(-((0-pulse[1])/pulse[2])**2))],t_eval=v,method='DOP853',rtol=rtol,atol=1e-14)
    assert sH.success
    # ---- along v=0 ray : transverse r_v, sigma_v, phi_v ----
    Rs,Sg,RUs,_,SUs,_=S.fields(U,0.0)
    rv0=hz.sol(0)[1]; sgv0=-rv0/r_ + (1-2*MNp_(S,hz.sol(0)[0]))/(2*hz.sol(0)[0])
    def rhs0(t,Y):
        rv,sv,pv=Y; r,sg,rU,sU=[np.interp(t,U,a) for a in (Rs,Sg,RUs,SUs)]  # placeholder replaced below
        return None
    # exact static fields evaluated pointwise (no interpolation error)
    def puls(t):
        if pulse is None: return 0.0
        A,U0,w=pulse; return -2*A*(t-U0)/w**2*np.exp(-((t-U0)/w)**2)
    def rhsT(t,Y):
        r,sg,rU,_,sUt,_=[a[0] for a in S.fields(np.array([t]),0.0)]
        if pulse is None:
            a,b,c_=F(S,r,sg,rU,Y[0],puls(t),Y[2]); return [a,b,c_]
        # constraint-consistent seeded data: r, r_U from the u-constraint r_UU = sigma_U r_U - 4 pi r phi_U^2 (sigma prescribed static)
        r,rU=Y[3],Y[4]
        a,b,c_=F(S,r,sg,rU,Y[0],puls(t),Y[2])
        return [a,b,c_,rU,sUt*rU-4*np.pi*r*puls(t)**2]
    y0=[rv0,sgv0,phv(0)]+([] if pulse is None else [S.rp,-1.0])
    sT=solve_ivp(rhsT,[0,U[-1]],y0,t_eval=U,method='DOP853',rtol=rtol,atol=1e-14); assert sT.success
    if pulse is not None: Rs=sT.y[3].copy(); RUs=sT.y[4].copy()
    R=np.zeros((nv,nu));SG=np.zeros((nv,nu));RU=np.zeros((nv,nu));RV=np.zeros((nv,nu));SU=np.zeros((nv,nu));SV=np.zeros((nv,nu));PU=np.zeros((nv,nu));PV=np.zeros((nv,nu))
    R[0,:]=Rs; SG[0,:]=Sg; RU[0,:]=RUs; SU[0,:]=SUs; RV[0,:]=sT.y[0]; SV[0,:]=sT.y[1]; PV[0,:]=sT.y[2]; PU[0,:]=[puls(t) for t in U]
    rH=np.array([hz.sol(t)[0] for t in v]); rvH=np.array([hz.sol(t)[1] for t in v])
    R[:,0]=rH; SG[:,0]=sH.y[0]; RU[:,0]=-0.5*np.exp(sH.y[0]); RV[:,0]=rvH
    SV[:,0]=-rvH/rH+(1-2*MNp_(S,rH))/(2*rH); SU[:,0]=sH.y[1]; PU[:,0]=sH.y[2]; PV[:,0]=phv(v)
    if c is not None:
        SG=SG+np.log(gp)[None,:]; RU=RU*gp[None,:]; SU=SU*gp[None,:]+S.kp; PU=PU*gp[None,:]
        return sg_,v,[R,SG,RU,RV,SU,SV,PU,PV],hz,U,gp
    return U,v,[R,SG,RU,RV,SU,SV,PU,PV],hz


def build_eh_1d(S,U1,v1,hU,hv,B,k=1.5,vH=None,rtol=1e-12,c=None,pulse=None):
    """If c is None: uniform U grid (spacing hU). Else grid uniform in s (spacing hU) with U=c(e^{kp s}-1)/kp up to U1;
    returned arrays are then in (s,v) with sigma_s=sigma~+ln g', r_s=r_U g', sigma_ss=sigma~_U g'+kp, phi_s=phi_U g'."""
    nv=int(round(v1/hv))+1; v=hv*np.arange(nv)
    if c is None:
        nu=int(round(U1/hU))+1; U=hU*np.arange(nu); gp=np.ones(nu)
    else:
        smax=np.log(1+U1*S.kp/c)/S.kp; nu=int(round(smax/hU))+1; sg_=hU*np.arange(nu); U=c*np.expm1(S.kp*sg_)/S.kp; gp=c*np.exp(S.kp*sg_)
    vH=v1+150.0 if vH is None else vH
    hz=horizon(S,B,k,vH); phv=lambda v:PHVF(k,B,v)
    # ---- along H+ : sigma~, sigma~_U, phi_U ----
    r_,rv_,_,_,sU0,_=[a[0] for a in S.fields(np.array([0.0]),0.0)]
    def rhsH(t,Y):
        sg,sU,pU=Y; r,rv=hz.sol(t); rU=-0.5*np.exp(sg)
        _,b,c=F(S,r,sg,rU,rv,pU,phv(t))
        sgv=-rv/r+(1-2*MNp_(S,r))/(2*r)
        return [sgv,b,c]
    sH=solve_ivp(rhsH,[0,v1],[np.log(2.0),sU0,(0.0 if pulse is None else -2*pulse[0]*(0-pulse[1])/pulse[2]**2*np.exp(-((0-pulse[1])/pulse[2])**2))],t_eval=v,method='DOP853',rtol=rtol,atol=1e-14)
    assert sH.success
    # ---- along v=0 ray : transverse r_v, sigma_v, phi_v ----
    Rs,Sg,RUs,_,SUs,_=S.fields(U,0.0)
    rv0=hz.sol(0)[1]; sgv0=-rv0/r_ + (1-2*MNp_(S,hz.sol(0)[0]))/(2*hz.sol(0)[0])
    def rhs0(t,Y):
        rv,sv,pv=Y; r,sg,rU,sU=[np.interp(t,U,a) for a in (Rs,Sg,RUs,SUs)]  # placeholder replaced below
        return None
    # exact static fields evaluated pointwise (no interpolation error)
    def puls(t):
        if pulse is None: return 0.0
        A,U0,w=pulse; return -2*A*(t-U0)/w**2*np.exp(-((t-U0)/w)**2)
    def rhsT(t,Y):
        r,sg,rU,_,sUt,_=[a[0] for a in S.fields(np.array([t]),0.0)]
        if pulse is None:
            a,b,c_=F(S,r,sg,rU,Y[0],puls(t),Y[2]); return [a,b,c_]
        # constraint-consistent seeded data: r, r_U from the u-constraint r_UU = sigma_U r_U - 4 pi r phi_U^2 (sigma prescribed static)
        r,rU=Y[3],Y[4]
        a,b,c_=F(S,r,sg,rU,Y[0],puls(t),Y[2])
        return [a,b,c_,rU,sUt*rU-4*np.pi*r*puls(t)**2]
    y0=[rv0,sgv0,phv(0)]+([] if pulse is None else [S.rp,-1.0])
    sT=solve_ivp(rhsT,[0,U[-1]],y0,t_eval=U,method='DOP853',rtol=rtol,atol=1e-14); assert sT.success
    if pulse is not None: Rs=sT.y[3].copy(); RUs=sT.y[4].copy()
    R0,SG0,RU0,RV0,SU0,SV0,PU0,PV0=[np.zeros(nu) for _ in range(8)]
    R0[:]=Rs; SG0[:]=Sg; RU0[:]=RUs; SU0[:]=SUs; RV0[:]=sT.y[0]; SV0[:]=sT.y[1]; PV0[:]=sT.y[2]; PU0[:]=[puls(t) for t in U]
    rH=np.array([hz.sol(t)[0] for t in v]); rvH=np.array([hz.sol(t)[1] for t in v])
    Rc=rH; SGc=sH.y[0].copy(); RUc=-0.5*np.exp(sH.y[0]); RVc=rvH
    SVc=-rvH/rH+(1-2*MNp_(S,rH))/(2*rH); SUc=sH.y[1].copy(); PUc=sH.y[2].copy(); PVc=phv(v)
    for a,bv in ((R0,Rc),(SG0,SGc),(RU0,RUc),(RV0,RVc),(SU0,SUc),(SV0,SVc),(PU0,PUc),(PV0,PVc)): a[0]=bv[0]
    if c is not None:
        SG0=SG0+np.log(gp); RU0=RU0*gp; SU0=SU0*gp+S.kp; PU0=PU0*gp
        SGc=SGc+np.log(gp[0]); RUc=RUc*gp[0]; SUc=SUc*gp[0]+S.kp; PUc=PUc*gp[0]
    row0=np.ascontiguousarray(np.vstack([R0,SG0,RU0,RV0,SU0,SV0,PU0,PV0]))
    col0=np.ascontiguousarray(np.vstack([Rc,SGc,RUc,RVc,SUc,SVc,PUc,PVc]))
    return dict(s=(sg_ if c is not None else U),v=v,U=U,gp=gp,row0=row0,col0=col0,hz=hz,nu=nu,nv=nv)

import ctypes, os
_ls=ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)),'libstream.so'))
_dp=ctypes.POINTER(ctypes.c_double)
_ls.evolve_stream.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,_dp,_dp,ctypes.c_int,ctypes.POINTER(ctypes.c_int),_dp,ctypes.c_int]
def run_stream(S,d,hu,hv,cols,niter=3):
    cols=np.ascontiguousarray(np.asarray(cols,dtype=np.int32)); out=np.zeros((len(cols),d['nv'],8))
    _ls.evolve_stream(d['nu'],d['nv'],hu,hv,S.mN,S.aN,d['row0'].ctypes.data_as(_dp),d['col0'].ctypes.data_as(_dp),len(cols),cols.ctypes.data_as(ctypes.POINTER(ctypes.c_int)),out.ctypes.data_as(_dp),niter)
    return out

# Ori shell model ('hn' closure, m_N=5, a_N=10) driven by the kernel-filtered ingoing flux  dm_-/dv = c phi_v(v)^2,  phi_v = K_analytic * f,
# compared with (a) the PDE rate of the Romberg-extrapolated M (tail-only runs, B=0.03) and (b) the same shell model driven by the unfiltered power-law tail.
import numpy as np, json, sys, os, warnings
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))   # ori_model.py lives in code/
from scipy.signal import fftconvolve
from scipy.interpolate import CubicSpline
from scipy.integrate import solve_ivp
import ori_model as O, analyze
warnings.filterwarnings('ignore')
tau,Kt=np.load('K_analytic_tau.npy'); kp=0.04896874; R1=0.64423; a_,b_=1.063,0.056
def Kf(t):
    t=np.asarray(t,float); out=np.interp(t,tau,Kt,left=0.0); tail=R1*np.exp(-kp*t)*(1+a_*np.exp(-kp*t)+b_*np.exp(-2*kp*t)); return np.where(t>120,tail,out)
dv=0.25; V=4000.0; v=np.arange(-12,V+dv,dv)
def phiv(k,B):
    f=np.where(v>=0,-k*B*(1+np.maximum(v,0))**(-k-1),0.0)
    Kg=Kf(v-v[0]-12+ (v[0]+12))   # kernel sampled on tau=v (grid starts at -12)
    ker=Kf(np.arange(-12,V+dv,dv))
    return fftconvolve(f,ker)[:len(v)]*dv   # index i <-> v[i]+v[0] shift handled: kernel starts at tau=-12 and f at v=-12 -> offset 12+12: correct below
def phiv_shift(k,B):
    t=np.arange(-12,V+dv,dv); f=np.where(t>=0,-k*B*(1+np.maximum(t,0))**(-k-1),0.0); ker=Kf(t)
    full=fftconvolve(f,ker)*dv   # full[n] corresponds to time t[0]+t[0]+n*dv = -24+n dv
    n0=int(round(12/dv)); return full[n0:n0+len(t)]          # phi_v at time t = full[(t+24)/dv] ; t index i -> n=i+12/dv
def run(k,B,minf,D0=1e-12,v0=1.0,v1=108.0,filtered=True,delta=None,p=None):
    cl=O.Cl('hn',mN=5.0,aN=10.0)
    _mg=np.linspace(0,minf*1.02,400); _rg=np.array([O.Cl.rminus(cl,m) for m in _mg]); _sp=CubicSpline(_mg,_rg); cl.rminus=lambda m:float(_sp(m))
    if filtered:
        t=np.arange(-12,V+dv,dv); pv=phiv_shift(k,B); w=pv**2
        cum=np.concatenate([[0],np.cumsum(0.5*(w[1:]+w[:-1])*dv)])
        c=minf/np.interp(0.0,t,cum[-1]-cum)   # calibrate: mu(0)=0 => minf = c int_0^inf phi_v^2
        # int_0^inf phi_v^2 ~ remainder beyond V: add analytic asymptote T0^2 f^2 integral
        T0=44.304; rem=(T0*k*B)**2*(1+V)**(-2*k-1)/(2*k+1); tot=(cum[-1]-np.interp(0.0,t,cum))+rem; c=minf/tot
        tailint=lambda x:(cum[-1]-np.interp(x,t,cum))+rem
        xs=np.arange(0.5,130,0.05); cs_m=CubicSpline(xs,minf-c*tailint(xs)); cs_d=CubicSpline(xs,c*np.interp(xs,t,w)); mm=lambda x:float(cs_m(x)); dmm=lambda x:float(cs_d(x))
    else:
        mm=lambda x:minf-delta*x**(-p); dmm=lambda x:p*delta*x**(-p-1)
    def rhsM(x,y):
        q,M=y; m_=mm(x); rm=cl.rminus(m_); drm=-cl.Pm(m_,rm)/cl.Pr(m_,rm)
        fm=cl.f_taylor(m_,rm,q); R=rm+q; Rdot=0.5*fm; S=cl.dMdm(m_,R)*dmm(x)/fm
        return [Rdot-drm*dmm(x), Rdot*cl.G(M,R)+S*(1-2*M/R)]
    m_=mm(v0); rm=cl.rminus(m_); y0=[1e-3,cl.M(m_,rm+1e-3)+D0]
    return solve_ivp(rhsM,[v0,v1],y0,method='LSODA',rtol=1e-9,atol=1e-300,dense_output=True),cl,mm
def rates(sol,ws):
    return [np.log(sol.sol(a+4)[1]/sol.sol(a)[1])/4 for a in ws]
ws=[60,72,84,96,104]
for fn,k,B,minf in (('gen_B0.03_k1.5_A0_U1_w0.3_v110.json',1.5,0.03,9.9555e-3),('gen_B0.03_k0.5_A0_U1_w0.3_v110.json',0.5,0.03,5.912e-3)):
    # PDE rates from the extrapolated M on U=1
    D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq'])
    M=analyze.extrap([np.array(D['data'][h]['M'][2]) for h in hs])[-1][0]; pde=[np.log(M[int(a+4-vq[0])]/M[int(a-vq[0])])/4 for a in ws]
    sol,cl,mm=run(k,B,minf)
    sh=rates(sol,ws)
    S=np.abs(analyze.extrap([np.array(D['data'][h]['sV'][2]) for h in hs])[-1][0]); exc=[np.mean(S[int(a-vq[0]):int(a+4-vq[0])+1])-D['km'] for a in ws]
    pw=[D['km']-(2*k+2)/(a+2+1.0) for a in ws]
    kmu=lambda x:-0.5*cl.Pr(mm(x),cl.rminus(mm(x)))/cl.D(mm(x),cl.rminus(mm(x)))
    print('k=%.1f B=%.2f   windows'%(k,B),ws)
    print('  PDE (Romberg M)           ',np.round(pde,4))
    print('  shell, kernel-filtered    ',np.round(sh,4))
    print('  shell(filtered) + [|sigma_v| - kappa_-(mu_f)] (measured)',np.round(np.array(sh)+np.array(exc),4))
    print('  |sigma_v|-kappa_-(mu_f) (PDE, U=1, window mean)',np.round(exc,4))
    print('  power-law formula kappa_-(mu_f)-(2k+2)/(v+1) at window mid',np.round(pw,4))
    print('  kappa_-(m_-(v)) at window starts',np.round([kmu(a+2) for a in ws],4),'  -2 kappa_+ =',-2*kp)

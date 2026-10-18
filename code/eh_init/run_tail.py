import numpy as np, warnings, time, sys, json
warnings.filterwarnings('ignore')
from dnU import *
import os
S=StaticU(float(os.environ.get("MN","5")))
def MN(r): return S.mN*r**3/(r**3+S.aN)
def kappa_minus(mu):
    P=lambda r: r**3-2*(mu+0)*r**2 - 2*S.mN*r**3/(r**3+S.aN)*0  # placeholder
    return None
def inner(mu):
    # f(r)=1-2(mu+MN(r))/r ; roots
    f=lambda r:1-2*(mu+MN(r))/r
    rr=np.linspace(0.3,S.rp+5,200001); fv=f(rr); idx=np.where(np.sign(fv[:-1])*np.sign(fv[1:])<0)[0]
    roots=[brentq(f,rr[i],rr[i+1],xtol=1e-14) for i in idx]
    rm,rp=roots[0],roots[-1]; d=1e-6
    fp=lambda r:(f(r+d)-f(r-d))/(2*d)
    return rm,rp,abs(fp(rm))/2,fp(rp)/2
def run(B,k,hs,hv,U1=10.0,v1=100.0):
    c=0.2*np.exp(-S.kp*v1)
    t=time.time()
    s_,v,arrs,hz,U,gp=build_eh(S,U1,v1,hs,hv,B,k=k,c=c,vH=v1+300)
    rf=hz.sol(v1)[0]
    run2(S,arrs,hs,hv)
    return s_,v,arrs,hz,U,gp,time.time()-t
if __name__=='__main__':
    B=float(sys.argv[1]); k=float(sys.argv[2]); hs=float(sys.argv[3]); hv=float(sys.argv[4])
    s_,v,arrs,hz,U,gp,tt=run(B,k,hs,hv)
    rf=hz.sol(v[-1])[0]; rinf=hz.sol(v[-1]+300)[0] if False else rf
    print('time %.1f'%tt,'r_H(v=0)=%.8f r_H(v=100)=%.8f'%(hz.sol(0)[0],rf), 'nan',int(np.isnan(arrs[1]).sum()))
    mu_f=rf/2-MN(rf); rm,rp,km,kpp=inner(mu_f)
    print('mu_f=%.4e  r-(mu_f)=%.6f kappa-(mu_f)=%.6f (static kappa- %.6f), kappa+=%.6f'%(mu_f,rm,km,0.795649,kpp))
    M=mass(S,arrs)
    for Ux in (0.03,0.3,3.0,10.0):
        j=int(np.argmin(abs(U-Ux)))
        # rate dlnM/dv and sigma_v
        out=[]
        for vi in (20,40,60,80,98):
            i=int(round(vi/hv)); w=int(round(2.0/hv))
            r1=(np.log(abs(M[i+w,j]))-np.log(abs(M[i-w,j])))/(v[i+w]-v[i-w])
            out.append('v=%d: M=%.2e dlnM/dv=%.4f sV=%.4f'%(vi,M[i,j],r1,arrs[5][i,j]))
        print('U=%.3g'%U[j],' | '.join(out))

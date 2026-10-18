"""E8: effect of the conformal-anomaly flux on the ray integration.  Inputs as in ray_extend.py (PDE sigma_v, phi_v to v_b=250, kernel continuation beyond).
usage: python3 e8_semiclassical.py gen3_B0.003_k1.5_v300.json"""
import json,sys,os,numpy as np
from scipy.interpolate import CubicSpline
import raylib as R, raylib_sc as RS, analyze, kernel_lib as KL
fn=sys.argv[1]; v0=60.; vb=250.; V=3000.; n=2
D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq']); k=D['k']; B=D['B']; km=D['km']
def fld(name):
    arr=[]
    for h in hs:
        d=D['data'][h]; arr.append(np.array(d['rs'][n])*np.exp(-np.array(d['sg'][n])) if name=='Y' else np.array(d[name][n]))
    return analyze.extrap(arr)[-1][0]
F={nm:fld(nm) for nm in ('r','rv','Y','M','sV','PV')}; r,rv,Y=F['r'],F['rv'],F['Y']
ib=int(vb-vq[0]); sVb=np.abs(F['sV']); ex=sVb-km
mm=(vq>=150)&(vq<=vb)&(ex>0); q=-np.polyfit(np.log(vq[mm]),np.log(ex[mm]),1)[0] if mm.sum()>5 else 1.0
vk=np.arange(vb,V+1,1.0); Pk=np.array([KL.phi_v(v,k,B) for v in vk]); ratio=F['PV'][ib]/Pk[0]
Pall=CubicSpline(np.concatenate([vq[:ib+1],vk[1:]]),np.concatenate([F['PV'][:ib+1],ratio*Pk[1:]]))
spl=CubicSpline(vq,F['sV'])
def sV(v): return float(spl(v)) if v<=vb else -(km+ex[ib]*(vb/v)**q)
i0=int(v0-vq[0]); rows=[]
print('%s: k=%g B=%g  kappa_-(mu_f)=%.6f  T0 etc in raylib; flux at v=250: phi_v^2 = %.3e; 4 pi r phi_v^2/kappa = %.3e'%(fn,k,B,km,Pall(250.)**2,4*np.pi*r[ib]*Pall(250.)**2/km))
print('eps=hbar/l^2   |T^q_vv| = hbar kappa^2/(192 pi^2 r^2)   v_flip (rho<0)   r(v=3000)-r(v=250)   ln|M|(3000)  sign   [classical: ln M(3000)]')
cl=R.integrate(v0,V,r[i0],-rv[i0],np.log(-Y[i0]),sV,Pall)
lcl=R.lnMof(*cl.sol(3000.))
for eps in (0.0,1e-30,1e-20,1e-15,1e-12,1e-10,1e-8,1e-6,1e-4):
    sol=RS.integrate_sc(v0,V,r[i0],-rv[i0],np.log(-Y[i0]),sV,Pall,eps)
    vv=np.arange(v0,V,1.0); rho=np.array([sol.sol(x)[1] for x in vv]); neg=np.where(rho<0)[0]
    vf=vv[neg[0]] if len(neg) else np.nan
    r250=sol.sol(250.)[0]; rE=sol.sol(3000.)[0]; lm,sg=RS.lnabsM(*sol.sol(3000.))
    Tq=eps*km**2/(192*np.pi**2*rE**2)
    print('%8.0e   %.3e   %8.1f   %+.3e   %9.2f  %+d   [%9.2f]'%(eps,Tq,vf,rE-r250,lm,sg,lcl))
    rows.append((eps,vf))
json.dump(rows,open('results_e8_semiclassical.json','w'))

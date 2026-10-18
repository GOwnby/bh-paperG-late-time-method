"""E3 (Paper E, Sec. ray): continuation of the ray integration to v=3000.  Inputs: five-grid extrapolated sigma_v, phi_v of a PDE run up to v_b;
beyond v_b phi_v = (PDE/kernel ratio at v_b) x kernel convolution (kernel_lib.py), |sigma_v| = kappa_-(mu_f) + Delta(v_b)(v_b/v)^q (q fitted; two bounds shown).
usage: ray_extend.py gen2_...json [v0=60] [v_b=250] [V=3000]"""
import json,sys,numpy as np
from scipy.interpolate import CubicSpline
import os, raylib as R, analyze
KL=__import__('kernel_lib_mu' if os.environ.get('KERNEL_MU') else 'kernel_lib')   # KERNEL_MU=<mu_f>: kernel of the final hole (E11)
fn=sys.argv[1]; v0=float(sys.argv[2]) if len(sys.argv)>2 else 60.; vb=float(sys.argv[3]) if len(sys.argv)>3 else 250.; V=float(sys.argv[4]) if len(sys.argv)>4 else 3000.
n=2
D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq']); k=D['k']; B=D['B']; km=D['km']
def fld(name):
    arr=[]
    for h in hs:
        d=D['data'][h]; arr.append(np.array(d['rs'][n])*np.exp(-np.array(d['sg'][n])) if name=='Y' else np.array(d[name][n]))
    T=analyze.extrap(arr); return T[-1][0],T[-2][1]
F={nm:fld(nm) for nm in ('r','rv','Y','M','sV','PV')}
r,rv,Y,M=[F[x][0] for x in ('r','rv','Y','M')]
print('%s k=%.1f B=%g: levels diff at v0=%g: y %.1e rho %.1e M %.1e ; M_ext(v0)=%.3e'%(fn,k,B,v0,*[abs(F[x][1][int(v0-vq[0])]/F[x][0][int(v0-vq[0])]-1) for x in ('Y','rv','M')],M[int(v0-vq[0])]))
ib=int(vb-vq[0]); sVb=np.abs(F['sV'][0]); ex=sVb-km
# fit of the excess |sV|-km ~ c v^-q over [150,vb]
mm=(vq>=150)&(vq<=vb)&(ex>0); q=-np.polyfit(np.log(vq[mm]),np.log(ex[mm]),1)[0] if mm.sum()>5 else 1.0
print('excess |sV|-km at v_b=%.1e, fitted power q=%.2f'%(ex[ib],q))
vk=np.arange(vb,V+1,1.0); Pk=np.array([KL.phi_v(v,k,B) for v in vk]); ratio=F['PV'][0][ib]/Pk[0]
print('PDE/kernel phi_v ratio at v_b: %.5f (kernel built for the linear regime; B=%g)'%(ratio,B))
Pall=CubicSpline(np.concatenate([vq[:ib+1],vk[1:]]),np.concatenate([F['PV'][0][:ib+1],ratio*Pk[1:]]))
def make_sV(mode):
    def s(v):
        if v<=vb: return float(CubicSpline(vq,F['sV'][0])(v))
        e={'zero':0.0,'const':ex[ib],'power':ex[ib]*(vb/v)**q}[mode]; return -(km+e)
    return s
i0=int(v0-vq[0]); out={}
for mode in ('power','zero','const'):
    sv=make_sV(mode); sol=R.integrate(v0,V,r[i0],-rv[i0],np.log(-Y[i0]),sv,Pall)
    out[mode]=sol
sol=out['power']
print('\n    v      ln M      rate        q_M=(km-rate)(v+1)   C(v)=lnM-km v+(2k+2)ln(v+1)    d(lnM) mode zero/const vs power')
for v in (290,400,600,1000,1500,2000,2500,3000):
    if v>V-2: continue
    f=lambda x,s=sol:R.lnMof(*s.sol(float(x))); lm=f(v); rate=(f(v+2)-f(v-2))/4
    C=lm-km*v+(2*k+2)*np.log(v+1)
    dz=[R.lnMof(*out[m].sol(float(v)))-lm for m in ('zero','const')]
    print('  %5d  %9.3f  %.7f   %.4f               %.4f                      %+.1e %+.1e'%(v,lm,rate,(km-rate)*(v+1),C,dz[0],dz[1]))
# save the curves for the figure
vv=np.arange(v0+1,V-1,1.0); res={}
for mode in out:
    s=out[mode]; res['lnM_'+mode]=np.array([R.lnMof(*s.sol(float(x))) for x in vv])
np.savez('ray_extend_B%g_k%g%s.npz'%(B,k,'_mu' if os.environ.get('KERNEL_MU') else ''),v=vv,vq=vq,Mext=M,Mlev=F['M'][1],k=k,B=B,km=km,vb=vb,**res)

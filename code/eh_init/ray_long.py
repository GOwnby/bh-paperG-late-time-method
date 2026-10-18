# E3 step 2: exact ray integration beyond v=110 with the five-grid extrapolated sigma_v(v), phi_v(v) of a long run.
# usage: ray_long.py gen2_...json [n=2] [v0 ...]
import json,sys,numpy as np
from scipy.interpolate import CubicSpline
import raylib as R, analyze
fn=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 2
v0s=[float(x) for x in sys.argv[3:]] or [60.0,84.0]
D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq']); k=D['k']; km=D['km']
def fld(name):
    arr=[]
    for h in hs:
        d=D['data'][h]
        arr.append(np.array(d['rs'][n])*np.exp(-np.array(d['sg'][n])) if name=='Y' else np.array(d[name][n]))
    T=analyze.extrap(arr); return T[-1][0],T[-2][1]
F={nm:fld(nm) for nm in ('r','rv','Y','M','sV','PV')}
r,rv,Y,M=[F[x][0] for x in ('r','rv','Y','M')]
print(fn,'k=%.1f B=%g  U=%.1f grids %s mu_f=%.4e kappa-(mu_f)=%.6f'%(k,D['B'],D['Uq'][n],hs,D['mu_f'],km))
print('(a) PDE: relative difference between the two highest Romberg levels (y=-r_s/W, rho=-r_v) and sign of M_ext')
print('   v      M_ext      M       y        rho      r        sigma_v   phi_v')
for v in (60,100,108,115,120,130,140,160,180,200,240,290):
    i=int(v-vq[0])
    if i>=len(vq): continue
    o=[abs(F[nm][1][i]/F[nm][0][i]-1) for nm in ('M','Y','rv','r','sV','PV')]
    print('  %4d  %+.3e  '%(v,M[i])+'  '.join('%.1e'%x for x in o))
sV=CubicSpline(vq,F['sV'][0]); Pv=CubicSpline(vq,F['PV'][0])
lam=np.abs(F['sV'][0])+2*np.gradient(np.log(np.abs(F['PV'][0])),vq); lam2=lam-np.gradient(lam,vq)/lam
res={}
for v0 in v0s:
    i0=int(v0-vq[0]); sol=R.integrate(v0,vq[-1],r[i0],-rv[i0],np.log(-Y[i0]),sV,Pv); res[v0]=sol
    print('(b) ray ODE from v0=%g (M_ext(v0)=%.4e): ln M_ode, M_ode/M_ext (PDE; trust only where (a) is small)'%(v0,M[i0]))
    for v in (84,100,108,115,120,130,140,160,180,200,240,290):
        if v<=v0 or v>vq[-1]: continue
        i=int(round(v-vq[0])); Z=sol.sol(v); lm=R.lnMof(*Z)
        print('    v=%4d  lnM_ode=%9.4f   M_ode/M_ext-1=%+.2e   (next level: %+.2e)'%(v,lm,np.exp(lm)/M[i]-1 if lm<700 else np.nan, np.exp(lm)/F['M'][1][i]-1 if lm<700 else np.nan))
v0=v0s[0]; sol=res[v0]
print('(c) rates from the ODE (v0=%g) vs the flux-level relations, 4 < window; kappa-(mu_f)=%.6f'%(v0,km))
print('   v    dlnM/dv(ODE)   4 pi r phi_v^2/rho   lam-lam\'/lam   lam   kappa-(mu_f)-(2k+2)/(v+1)   ODE-pred   p_loc')
for v in (84,100,108,140,180,220,260,290):
    if v<=v0+2 or v>vq[-1]-2: continue
    f=lambda x:R.lnMof(*sol.sol(x)); rate=(f(v+2)-f(v-2))/4
    Z=sol.sol(v); ex=4*np.pi*Z[0]*Pv(v)**2/Z[1]
    i=int(v-vq[0]); w=4; p=-(np.log(abs(F['PV'][0][i+w]))-np.log(abs(F['PV'][0][i-w])))/(np.log(vq[i+w]+1)-np.log(vq[i-w]+1))
    pred=km-(2*k+2)/(v+1)
    print('  %4d   %.6f      %.6f         %.6f      %.6f   %.6f              %+.2e   %.2f'%(v,rate,ex,lam2[i],lam[i],pred,rate-pred,p))

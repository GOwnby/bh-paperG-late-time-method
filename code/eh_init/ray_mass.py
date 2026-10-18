"""E3 (Paper E, Sec. ray): exact integration of the ray equations for the Misner-Sharp mass at fixed U, driven by the
five-grid Romberg-extrapolated sigma_v(v), phi_v(v) of a streaming run (gen2.py), calibrated on the extrapolated (r, r_v, r_U/W) at v0.
usage: python3 ray_mass.py gen2_...json [ray n=2]   -> prints the tables used in the paper."""
import json,sys,numpy as np
from scipy.interpolate import CubicSpline
import raylib as R, analyze
fn=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 2
D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq']); k=D['k']; km=D['km']; B=D['B']
def fld(name):
    arr=[]
    for h in hs:
        d=D['data'][h]; arr.append(np.array(d['rs'][n])*np.exp(-np.array(d['sg'][n])) if name=='Y' else np.array(d[name][n]))
    T=analyze.extrap(arr); return T[-1][0],T[-2][1]
F={nm:fld(nm) for nm in ('r','rv','Y','M','sV','PV')}
r,rv,Y,M=[F[x][0] for x in ('r','rv','Y','M')]; Mn=F['M'][1]
sV=CubicSpline(vq,F['sV'][0]); Pv=CubicSpline(vq,F['PV'][0])
print('%s: k=%.1f B=%g ray U=%.1f, %d grids h=%s, mu_f=%.5e kappa-(mu_f)=%.6f'%(fn,k,B,D['Uq'][n],len(hs),hs[0]+'..'+hs[-1],D['mu_f'],km))
print('\n[A] ODE from v0 against the extrapolated PDE mass: max |M_ode/M_ext-1| over v0<v<=108 (and over 108<v<=120)')
for v0 in (48,60,72,84):
    i0=int(v0-vq[0]); sol=R.integrate(float(v0),vq[-1],r[i0],-rv[i0],np.log(-Y[i0]),sV,Pv)
    dev=lambda a,b: max(abs(np.exp(R.lnMof(*sol.sol(float(v))))/M[int(v-vq[0])]-1) for v in range(a,b+1))
    print('  v0=%2d  M_ext(v0)=%.3e  M_ext(108)=%.3e   max dev (v<=108): %.1e   (108<v<=120): %.1e'%(v0,M[i0],M[int(108-vq[0])],dev(v0+1,108),dev(109,120)))
v0=60; i0=int(v0-vq[0]); sol=R.integrate(float(v0),vq[-1],r[i0],-rv[i0],np.log(-Y[i0]),sV,Pv)
print('\n[B] v0=60: PDE (top Romberg level, difference to next level) against the ray ODE')
print('    v    ln M_ode    M_ext          levels diff   M_ode/M_ext-1   y_ode/y_ext-1   rho_ode/rho_ext-1')
for v in (84,100,108,120,130,140,160,180,200,240,290):
    if v>vq[-1]: continue
    i=int(v-vq[0]); Z=sol.sol(float(v)); lm=R.lnMof(*Z)
    print('  %4d  %8.3f   %+.4e   %.1e      %+.1e        %+.1e         %+.1e'%(v,lm,M[i],abs(Mn[i]/M[i]-1),np.exp(lm)/M[i]-1,np.exp(Z[2])/(-Y[i])-1,Z[1]/(-rv[i])-1))
print('\n[C] rate d ln M/dv from the ODE (central difference over +-2), exact form 4 pi r phi_v^2/rho, lambda-lambda\'/lambda, power law')
lam=np.abs(F['sV'][0])+2*np.gradient(np.log(np.abs(F['PV'][0])),vq); lam2=lam-np.gradient(lam,vq)/lam
print('    v    ODE rate    4 pi r phi^2/rho   lam-lam\'/lam   |sV|-km     kappa-(mu_f)-(2k+2)/(v+1)   ODE-pred   q_M=(km-rate)(v+1)')
for v in (84,100,108,140,180,220,260,290):
    if v>vq[-1]-3: continue
    f=lambda x:R.lnMof(*sol.sol(float(x))); rate=(f(v+2)-f(v-2))/4; Z=sol.sol(float(v)); ex=4*np.pi*Z[0]*Pv(v)**2/Z[1]; i=int(v-vq[0])
    pred=km-(2*k+2)/(v+1)
    print('  %4d  %.6f    %.6f          %.6f     %+.1e   %.6f                    %+.2e   %.4f'%(v,rate,ex,lam2[i],abs(F['sV'][0][i])-km,pred,rate-pred,(km-rate)*(v+1)))

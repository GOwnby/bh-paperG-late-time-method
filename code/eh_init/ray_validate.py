# E3 step 1: does the exact ray integration reproduce the five-grid Romberg-extrapolated PDE mass M(v), amplitude included?
import json,sys,numpy as np
from scipy.interpolate import CubicSpline
import raylib as R, analyze
fn=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 2
v0s=[float(x) for x in sys.argv[3:]] or [48,60,72,84]
D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq'])
def fld(name):
    arr=[]
    for h in hs:
        d=D['data'][h]
        if name=='Y': a=np.array(d['rs'][n])*np.exp(-np.array(d['sg'][n]))
        else: a=np.array(d[name][n])
        arr.append(a)
    T=analyze.extrap(arr); return T[-1][0],T[-2][1]   # top-order, next-lower-order (error indicator)
F={nm:fld(nm) for nm in ('r','rv','Y','M','sV','PV')}
print(fn,'ray U=%.1f'%D['Uq'][n],'grids',hs,'mu_f=%.4e km=%.6f'%(D['mu_f'],D['km']))
# (a) level agreement
print('(a) relative difference between the two highest Romberg levels:')
print('   v     r        rho=-r_v   y=-r_s/W    M        sigma_v    phi_v')
for v in (40,60,72,84,96,104,108):
    i=int(v-vq[0])
    if i>=len(vq): continue
    out=[abs(F[nm][1][i]/F[nm][0][i]-1) for nm in ('r','rv','Y','M','sV','PV')]
    print('  %4d  '%v+'  '.join('%.1e'%o for o in out))
# (b) identity M = r/2 (1+4 Y r_v) with separately extrapolated factors
r,rv,Y,M=[F[x][0] for x in ('r','rv','Y','M')]
Mid=0.5*r*(1+4*Y*rv)
print('(b) M_ext vs r/2(1+4 Y r_v) from separately extrapolated factors, ratio at v=60,84,108:',['%.6f'%(Mid[int(v-vq[0])]/M[int(v-vq[0])]) for v in (60,84,108) if int(v-vq[0])<len(vq)])
# (c) ODE
sV=CubicSpline(vq,F['sV'][0]); Pv=CubicSpline(vq,F['PV'][0])
print('(c) ray ODE from v0 with extrapolated sigma_v, phi_v: M_ode/M_ext   [y_ode/y_ext, rho_ode/rho_ext, r_ode/r_ext]')
for v0 in v0s:
    i0=int(v0-vq[0]); y0=-Y[i0]; rho0=-rv[i0]
    if y0<=0 or rho0<=0: print('  v0=%g: y0 or rho0 not positive'%v0); continue
    sol=R.integrate(v0,vq[-1],r[i0],rho0,np.log(y0),sV,Pv)
    row=[]
    for v in (v0+12,72,84,96,104,108):
        if v<=v0 or v>vq[-1]: continue
        i=int(round(v-vq[0])); Z=sol.sol(v); Mo=R.Mof(Z)
        row.append('v=%d: %+.1e [%+.1e,%+.1e,%+.1e]'%(v,Mo/M[i]-1,np.exp(Z[2])/(-Y[i])-1,Z[1]/(-rv[i])-1,Z[0]/r[i]-1))
    print('  v0=%g  M_ext(v0)=%.4e  '%(v0,M[i0])+'\n         '.join(row))

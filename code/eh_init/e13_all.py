"""E13 (Paper E, Sec. ray): independent PDE check of the ray-integrated mass at late v.
For each gen3_*.json (five grids) and ray n: constraint-projected mass M_cc=(r/2)(1+4 y_c rho_C), y_c=1/2+I (u-Raychaudhuri integrated over the slice v=const,
Romberg over grids), rho_C,r from the v-Raychaudhuri constraint (started at v0=60), against the ray ODE (y evolved from v0=60).
Also: stability of M_cc under grid subsets, raw per-level error constant of rho, and the curvature bound K >= 16 M^2/r^6.
usage: e13_all.py gen3_...json [ray]"""
import json,sys,numpy as np
sys.argv=[sys.argv[0]]+sys.argv[1:]
fn=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 2
exec(open('e13_project.py').read().split("if __name__")[0])
subsets={'5 grids':None,'4 finest':[1,2,3,4],'4 coarsest':[0,1,2,3],'3 finest':[2,3,4]} if len(hs)==5 else {'%d grids'%len(hs):None}
X={nm:run(sub) for nm,sub in subsets.items()}
ref=X[list(subsets)[0]]
vs=[v for v in (60,84,100,120,140,160,180,200,220,240,260,280) if v<=vq[-1]-2]
def lnMcc(Xr,v):
    i=int(v-vq[0]); C=Xr['solC'].sol(float(v)); yc=0.5+Xr['I'][i]
    return np.log(C[0]/2)+np.logaddexp(0.0,np.log(4.0)+np.log(yc)+np.log(C[1])) if True else None
print('%s: k=%g B=%g, ray s=%.2f (U=%.4f), grids %s, kappa-(mu_f)=%.6f'%(fn,k,D['B'],D['sq'][n],D['Uq'][n],hs,km))
print('  v    ln M_ODE   ln M_cc - ln M_ODE   ln y_c - ln y_ODE   rho_C/rho_ODE-1 | ln M_cc: subsets minus 5-grid | next-lvl I diff | ln K>=')
for v in vs:
    i=int(v-vq[0]); Z=ref['solA'].sol(float(v)); lA=R.lnMof(*Z); lc=lnMcc(ref,v)
    sub=' '.join('%+.1e'%(lnMcc(X[nm],v)-lc) for nm in list(subsets)[1:])
    lnK=np.log(16)+2*lA-6*np.log(Z[0])
    print(' %4d  %8.2f   %+.2e           %+.2e          %+.1e     |  %s | %.1e | %.1f'%(v,lA,lc-lA,np.log(0.5+ref['I'][i])-Z[2],ref['solC'].sol(float(v))[1]/Z[1]-1,sub,abs(ref['Ip'][i]/ref['I'][i]-1),lnK))

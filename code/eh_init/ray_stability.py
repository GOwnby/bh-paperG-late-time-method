"""Grid-count stability of the exact ray integration vs the extrapolated PDE mass (Paper E, Sec. ray).
For subsets of the five grids (h=0.05,...,0.003125) -- all five, the four finest, the four coarsest, the three finest -- extrapolate r, r_v, y, sigma_v, phi_v (signed Romberg), integrate the ray ODE from v0=60 and compare ln M with the five-grid ODE; also the extrapolated PDE mass of each subset.
usage: ray_stability.py gen2_...json"""
import json,sys,numpy as np
from scipy.interpolate import CubicSpline
import raylib as R, analyze
fn=sys.argv[1]; v0=60.; n=2
D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq']); k=D['k']; B=D['B']
def run(sub):
    def fld(name):
        arr=[]
        for h in sub:
            d=D['data'][h]; arr.append(np.array(d['rs'][n])*np.exp(-np.array(d['sg'][n])) if name=='Y' else np.array(d[name][n]))
        return analyze.extrap(arr)[-1][0]
    F={nm:fld(nm) for nm in ('r','rv','Y','M','sV','PV')}
    i0=int(v0-vq[0]); sV=CubicSpline(vq,F['sV']); Pv=CubicSpline(vq,F['PV'])
    sol=R.integrate(v0,vq[-1]-1,F['r'][i0],-F['rv'][i0],np.log(-F['Y'][i0]),lambda v:float(sV(v)),lambda v:float(Pv(v)))
    return sol,F
subs={'five grids (0.05..0.003125)':hs,'four finest':hs[1:],'four coarsest':hs[:4],'three finest':hs[2:]}
res={nm:run(s) for nm,s in subs.items()}
ref,Fref=res['five grids (0.05..0.003125)']
print('%s  k=%g B=%g: ln M from the ray ODE (v0=60) and extrapolated PDE M for subsets of grids'%(fn,k,B))
print('  v   | '+' | '.join('%-30s'%nm for nm in subs))
for v in (84,100,108,140,180,200,240,290):
    row=[]
    for nm,(sol,F) in res.items():
        lm=R.lnMof(*sol.sol(float(v))); Mp=F['M'][int(v-vq[0])]
        row.append('ODE-ODE5 %+.1e  PDE/ODE5 %+.1e'%(lm-R.lnMof(*ref.sol(float(v))), (Mp/np.exp(R.lnMof(*ref.sol(float(v)))) -1) if Mp>0 else float('nan')))
    print('  %3d | '%v+' | '.join('%-30s'%r for r in row))

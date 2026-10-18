"""Domain dependence: A* versus the outer edge u1 (h=0.04, v1=40) and the saturation of r_CH(u)."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
from dn2lib import *
bg=Bg(); h=0.04
def run_amp(A,u1,v1=40.0,RMIN=1e-3):
    u,v,arrs,_=build2(bg,-6,u1,0,v1,h,h,A,0.1*A); run2(bg,arrs,h,h); R=arrs[0]
    return ((~np.isfinite(R))|(R<=RMIN)|(~np.isfinite(arrs[1]))).any(),u,arrs
out={'Astar_vs_u1':[],'profile':{}}
for u1 in (6,8,12,16,24,32):
    lo,hi=0.015,0.03
    for _ in range(45):
        mid=0.5*(lo+hi)
        if run_amp(mid,u1)[0]: hi=mid
        else: lo=mid
    out['Astar_vs_u1'].append([u1,0.5*(lo+hi)]); print(u1,0.5*(lo+hi),flush=True)
As=out['Astar_vs_u1'][-1][1]
for d in (1e-3,1e-5,1e-7):
    col,u,arrs=run_amp(As-d,48.0,60.0); R=arrs[0][-1]
    out['profile']['d=%g'%d]={'u':[float(x) for x in u[::25]],'r':[float(x) for x in R[::25]]}
json.dump(out,open('domain_nonlinear.json','w'),indent=1)

"""Critical threshold and scaling of the Cauchy-horizon radius.  usage: python run_threshold.py h
Initial data: phi = B + A exp(-u^2) on v=0, phi = B (1+v)^-1.5 on u=-6, B = A/10; domain u in [-6,40], v in [0,50].
Collapse := r <= 1e-5 or non-finite somewhere.  r_inf := r(u=40, v=50) (saturated: r_CH(u) is flat for u>~30)."""
import sys, os, numpy as np, json, warnings, time
warnings.filterwarnings('ignore')
from dn2lib import *
bg=Bg(); h=float(sys.argv[1]); u1=40.0; v1=50.0; u0=-6.0; RMIN=1e-5
def run_amp(A,ratio=0.1):
    u,v,arrs,_=build2(bg,u0,u1,0,v1,h,h,A,A*ratio); run2(bg,arrs,h,h)
    R=arrs[0]; return ((~np.isfinite(R))|(R<=RMIN)|(~np.isfinite(arrs[1]))).any(),u,arrs
lo,hi=0.0200,0.0210
for _ in range(50):
    mid=0.5*(lo+hi)
    if run_amp(mid)[0]: hi=mid
    else: lo=mid
    if hi-lo<2e-15: break
As=0.5*(lo+hi); print('h',h,'A* =',As,flush=True)
res=[]
for d in 10**np.linspace(-10,-3,36):
    col,u,arrs=run_amp(As-d)
    if col: res.append([float(d),None,None]); continue
    R=arrs[0][-1]; res.append([float(d),float(R[-1]),float(R[np.argmin(abs(u-4))])])
json.dump({'h':h,'Astar':As,'res':res},open('threshold_h%g.json'%h,'w'))

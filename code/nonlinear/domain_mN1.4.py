"""A_* for m_N=1.4 (kappa_-=0.164) with the box u1=v1 = c/kappa_-, c=20 and 40 (h=0.1): domain independence of the threshold amplitude (Sec. kscan).  usage: python domain_mN1.4.py > domain_mN1.4.log"""
import numpy as np, warnings, sys
warnings.filterwarnings('ignore')
from dn2lib import *
mN=1.4; h=0.1; bg0=Bg(mN); kap=bg0.kap
for c in (20,40):
    L=round(c/kap/h)*h; bg=Bg(mN,tmax=0.5*(L+20))
    def col(A,RMIN=1e-5):
        try: u,v,arrs,_=build2(bg,-6,L,0,L,h,h,A,0.1*A)
        except AssertionError: return True
        run2(bg,arrs,h,h); R=arrs[0]; return bool(((~np.isfinite(R))|(R<=RMIN)|(~np.isfinite(arrs[1]))).any())
    lo=1e-4; hi=lo
    while not col(hi): lo=hi; hi*=2
    for _ in range(50):
        mid=0.5*(lo+hi)
        if col(mid): hi=mid
        else: lo=mid
    print('kappa u1 = %d (L=%.1f): A* = %.10f'%(c,L,0.5*(lo+hi)),flush=True)

# truncation-error mass perturbation mu = M - M_N(r) in the B=0 (static) evolution, log-map grid
import numpy as np, warnings
warnings.filterwarnings('ignore')
from run_tail import *
for hs in (0.1,0.05,0.025):
    c=0.2*np.exp(-S.kp*100.0)
    s_,v,arrs,hz,U,gp=build_eh(S,10.0,100.0,hs,hs,0.0,c=c); run2(S,arrs,hs,hs)
    mu=mass(S,arrs)-MN(arrs[0])
    print('h=%g: mu at (U,v)='%hs,' '.join('(%.2g,%d):%.1e'%(U[j],t,mu[int(round(t/hs)),j]) for t in (30,50) for j in [int(np.argmin(abs(U-x))) for x in (0.1,0.3)]))

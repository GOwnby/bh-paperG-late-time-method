import numpy as np, sys, warnings
warnings.filterwarnings('ignore')
from run_tail import *
B,k,A,U0,w,v1,hs=[float(x) for x in sys.argv[1:8]]
c=0.2*np.exp(-S.kp*v1)
s_,v,arrs,hz,U,gp=build_eh(S,2.5,v1,hs,hs,B,k=k,c=c,vH=v1+300,pulse=(A,U0,w))
run2(S,arrs,hs,hs); PV=arrs[7]; PU=arrs[6]
print('k=%g  H+ tail exponent p0=k+1=%g'%(k,k+1))
for Ux in (1.0,):
    j=int(np.argmin(abs(U-Ux)))
    for vi in (40,48,56,60,64,68,72):
        i=int(round(vi/hs)); wd=int(round(3/hs))
        p=-(np.log(abs(PV[i+wd,j]))-np.log(abs(PV[i-wd,j])))/(np.log(v[i+wd])-np.log(v[i-wd]))
        print('  U=%.2f v=%d phi_v=%.3e  local exponent p=%.2f  (2p=%.2f)  phi_U=%.2e'%(U[j],vi,PV[i,j],p,2*p,PU[i,j]))

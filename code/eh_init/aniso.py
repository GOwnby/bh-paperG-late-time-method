import numpy as np, warnings
warnings.filterwarnings('ignore')
from run_tail import *
v1=100.0; c=0.2*np.exp(-S.kp*v1); ratios=[]
for hs,hv in [(0.05,0.05),(0.025,0.05),(0.05,0.025),(0.1,0.025),(0.025,0.1)]:
    s_,v,arrs,hz,U,gp=build_eh(S,3.0,v1,hs,hv,0.0,c=c); run2(S,arrs,hs,hv)
    mu=mass(S,arrs)-MN(arrs[0]); j=int(np.argmin(abs(U-0.3))); i=int(round(40/hv))
    print('hs=%g hv=%g  mu(U=0.3,v=40)=%.2e  mu(U=1,v=30)=%.2e'%(hs,hv,mu[i,j],mu[int(round(30/hv)),int(np.argmin(abs(U-1)))]))
    ratios.append(mu[i,j]/(hs**2+hv**2))
print('# mu(U=0.3,v=40)/(hs^2+hv^2) = '+', '.join('%.2e'%r for r in ratios)+'   for (hs,hv) = (0.05,0.05), (0.025,0.05), (0.05,0.025), (0.1,0.025), (0.025,0.1)')

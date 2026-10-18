# mechanism of the sign change of M in u (Section 6.3): mu_v = -8 pi r^2 (r_u/W) phi_v^2  => sign of the growing mass is -sign(r_u) on the Cauchy-horizon side
import sys; sys.path.insert(0,'.')
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
from dn2lib import *
bg=Bg(); h=0.04
u,v,arrs,_=build2(bg,-6,8,0,100,h,h,0.02,0.002); run2(bg,arrs,h,h); M=mass(bg,arrs)
R,SG,RU,RV,SU,SV,PU,PV=arrs
print('shape',R.shape, 'u range',u[0],u[-1])
sM=np.sign(M[-1]); sRU=np.sign(RU[-1]); idxM=np.where(sM[1:]!=sM[:-1])[0]; idxR=np.where(sRU[1:]!=sRU[:-1])[0]
print('M(v=100) sign changes at u =',[float(u[i]) for i in idxM])
print('r_u(v=100) sign changes at u =',[float(u[i]) for i in idxR])
for uu in (-5,-4,-3,-2.5,-2,-1.88,-1.5,-1,0,2,5):
    i=int(round((uu+6)/h)); print('u=%5.2f  M(100)=%+.3e  r_u(100)=%+.3e  r_u(50)=%+.3e  r(100)=%.6f'%(uu,M[-1,i],RU[-1,i],RU[int(round(50/h)),i],R[-1,i]))
# r_CH(u) maximum
rch=R[-1]; j=np.argmax(rch); print('max of r(u,v=100) at u=%.2f (r=%.6f)'%(u[j],rch[j]))

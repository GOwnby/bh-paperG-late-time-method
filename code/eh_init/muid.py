import numpy as np, warnings
warnings.filterwarnings('ignore')
from run_tail import *
for hs in (0.05,0.025):
    v1=50.0; c=0.2*np.exp(-S.kp*v1)
    s_,v,arrs,hz,U,gp=build_eh(S,2.5,v1,hs,hs,0.03,k=1.5,c=c,vH=v1+300,pulse=(0.02,1.0,0.3))
    run2(S,arrs,hs,hs); M=mass(S,arrs); R,SG,RU=arrs[0],arrs[1],arrs[2]; PV=arrs[7]; mu=M-MN(R)
    print('h',hs)
    for Ux in (0.5,1.0):
        j=int(np.argmin(abs(U-Ux)))
        for t in (5,10,20,30,40):
            i=int(round(t/hs)); dm=(mu[i+2,j]-mu[i-2,j])/(4*hs); rhs=-8*np.pi*R[i,j]**2*RU[i,j]*np.exp(-SG[i,j])*PV[i,j]**2
            print('  U=%.2f v=%d  dmu/dv=%.5e  rhs=%.5e  ratio=%.5f'%(U[j],t,dm,rhs,dm/rhs))

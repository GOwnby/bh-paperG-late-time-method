# E-sign (2): the position u_*(v) of the sign change of r_u (and of the inflating mass) on v = const slices.
# Exact content: Y(u,v)=r_u/W obeys d_u Y = -4 pi r phi_u^2/W <= 0, so Y is strictly decreasing in u where phi_u != 0 and has at most one zero u_*(v):
#   u_*(v) is the root of Y(u_L,v) = int_{u_L}^{u_*} 4 pi r phi_u^2/W du.   Here: (i) check the identity numerically (trapezoid) on stored slices,
# (ii) report u_*(v) for v = 10..100 and compare with the location of the maximum of r(u,v) (the same condition, r_u = 0), (iii) the limit of u_*(v) for v -> 100.
import sys; sys.path.insert(0,'.')
import numpy as np, warnings
warnings.filterwarnings('ignore')
from dn2lib import *
bg=Bg()
for A,B,h in [(0.02,0.002,0.04),(0.01,0.01,0.04),(0.005,0.001,0.04)]:
    u,v,arrs,_=build2(bg,-6,8,0,100,h,h,A,B); run2(bg,arrs,h,h)
    R,SG,RU,RV,SU,SV,PU,PV=arrs; W=np.exp(SG)
    ok=np.isfinite(R[-1])&np.isfinite(RU[-1]); idx=np.where(ok)[0]; uu=u[idx]
    print('A=%g B=%g h=%g: columns used %d of %d'%(A,B,h,ok.sum(),len(u)))
    print('   v     u_*(r_u=0)   u_max(r)   |  identity: Y(u_L) - int_{u_L}^{u_*} 4 pi r phi_u^2/W du  (relative to |Y(u_L)|)')
    for vv in (10,20,30,40,60,80,100):
        j=int(round(vv/h)); Y=(RU[j]/W[j])[idx]
        s=np.sign(Y); ch=np.where(s[1:]!=s[:-1])[0]
        if len(ch)==0: print('  %3d   none (Y keeps sign)'%vv); continue
        i=ch[0]; ust=uu[i]-Y[i]*(uu[i+1]-uu[i])/(Y[i+1]-Y[i])
        jm=np.argmax(R[j][idx]); 
        # identity from u_L=uu[0] to u_*
        g=(4*np.pi*R[j]*PU[j]**2/W[j])[idx]; I=np.trapezoid(g[:i+1],uu[:i+1])
        print('  %3d   %9.4f   %9.4f   |  %.2e   (Y(u_L)=%.3e)'%(vv,ust,uu[jm],(Y[0]-I)/abs(Y[0]),Y[0]))

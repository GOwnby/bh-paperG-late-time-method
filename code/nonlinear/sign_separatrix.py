# E-sign (3): the ray equation y' = a y + S (y=-r_u/W, a=rho/r-sigma_v>0 -> kappa_-, S=(1-2M_N')/(4r)<0 at r_-) is LINEAR in y, with a, S fixed by the v-constraints along the ray.
# y(v) = Phi(v) [ y(v0) - y_sep(v0) ] + y_sep(v),   y_sep(v0) = -int_{v0}^inf S/Phi dv'   (Phi = exp int_{v0}^v a),
# so sign(y) -> sign(y(v0)-y_sep(v0)) as v -> infinity: the ray u_* on which the mass does not inflate is the zero of y(v0,u)-y_sep(v0,u).
# Test: y_sep from the evolved ray fields (r, rho, sigma_v), y(v0,u) from the evolved r_u/W, zero crossing in u against the sign change of r_u at v=100 (sign_ustar.py).
import sys; sys.path.insert(0,'.')
import numpy as np, warnings
warnings.filterwarnings('ignore')
from dn2lib import *
bg=Bg()
for A,B,h in [(0.02,0.002,0.04),(0.01,0.01,0.04),(0.005,0.001,0.04)]:
    u,v,arrs,_=build2(bg,-6,8,0,100,h,h,A,B); run2(bg,arrs,h,h)
    R,SG,RU,RV,SU,SV,PU,PV=arrs; W=np.exp(SG)
    ok=np.isfinite(R[-1])&np.isfinite(RU[-1])
    sg=np.sign((RU[-1]/W[-1])[ok]); ch=np.where(sg[1:]!=sg[:-1])[0]; uu=u[ok]; Y=(RU[-1]/W[-1])[ok]
    i=ch[0]; ustar=uu[i]-Y[i]*(uu[i+1]-uu[i])/(Y[i+1]-Y[i])
    cols=np.where(ok&(np.abs(u-ustar)<0.5))[0]
    print('A=%g B=%g h=%g: sign change of r_u(v=100) at u_*=%.4f'%(A,B,h,ustar))
    for v0 in (30.,40.,50.):
        j0=int(round(v0/h)); j1=int(round(min(v0+30,100)/h)); out=[]
        for c in cols:
            vv=v[j0:j1+1]; r=R[j0:j1+1,c]; rho=-RV[j0:j1+1,c]; sv=SV[j0:j1+1,c]
            a=rho/r-sv; S=(1-2*MNp(bg,r))/(4*r)
            lnPhi=np.concatenate([[0.0],np.cumsum(0.5*(a[1:]+a[:-1])*np.diff(vv))])
            ysep=-np.trapezoid(S*np.exp(-lnPhi),vv)
            y0=-RU[j0,c]/W[j0,c]
            out.append((u[c],y0,ysep,y0-ysep))
        out=np.array(out); d=out[:,3]; s=np.sign(d); z=np.where(s[1:]!=s[:-1])[0]
        if len(z)==0: print('  v0=%g: no zero of y-y_sep in |u-u_*|<0.5 (y-y_sep range %.3e..%.3e)'%(v0,d.min(),d.max())); continue
        k0=z[0]; uz=out[k0,0]-d[k0]*(out[k0+1,0]-out[k0,0])/(d[k0+1]-d[k0])
        print('  v0=%g: zero of y(v0,u)-y_sep(v0,u) at u=%.4f (u_*-u = %+.4f); y_sep=%.4f, y=%.4f at that point; slope d(y-y_sep)/du=%.3e'%(v0,uz,ustar-uz,np.interp(uz,out[:,0],out[:,2]),np.interp(uz,out[:,0],out[:,1]),(d[k0+1]-d[k0])/(out[k0+1,0]-out[k0,0])))
# Note: y(v0,u) is extremely steep in u near u_* (|dy/du| ~ 3e4 ... 4e12 for v0=30..50), so the zero of y - y_sep coincides with the zero of y itself (r_u=0 on the slice v0) to ~1e-5; the content of the test is that u_* is already fixed at v0 ~ 30 and that
# the late-time sign follows from the linear ray equation. An attempted 'implicit equation' from the u-Raychaudhuri integral across the slice is cancellation-limited at h=0.04 (mismatch O(10)) and is not used.

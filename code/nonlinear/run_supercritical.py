"""Above threshold: where does r first fall below r_s, and is the locus spacelike?  (r=r_s curve v_s(u); spacelike iff dv_s/du<0)."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
from dn2lib import *
bg=Bg(); h=0.04; As=0.020427986618
out={}
for fac in (1.0005,1.01,1.05,1.3):
    A=As*fac
    u,v,arrs,_=build2(bg,-6,40,0,50,h,h,A,0.1*A); run2(bg,arrs,h,h)
    R=arrs[0].copy(); R[~np.isfinite(R)]=-1
    rows=[]
    for rs in (0.2,0.05):
        vs=[]
        for i in range(0,len(u),int(round(2/h))):
            idx=np.where(R[:,i]<rs)[0]
            vs.append([float(u[i]),float(v[idx[0]]) if len(idx) else None])
        rows.append({'r_s':rs,'curve':vs})
    out['A/A*=%g'%fac]=rows
    c=[x for x in rows[1]['curve'] if x[1] is not None]
    print('A/A*=%g'%fac,'r=0.05 locus (u,v):',[(round(a,0),round(b,1)) for a,b in c[::3]],flush=True)
json.dump(out,open('supercritical_nonlinear.json','w'),indent=1)

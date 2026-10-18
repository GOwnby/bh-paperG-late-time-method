"""Validation of the double-null code: (i) static Hayward-NED interior reproduced, 2nd order; (ii) Raychaudhuri constraint, 2nd order."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
from dn2lib import *
bg=Bg(); out={'static':[], 'constraint':[]}
for h in (0.08,0.04,0.02,0.01):
    u,v,arrs,_=build2(bg,-6,6,0,30,h,h,0.0,0.0); run2(bg,arrs,h,h)
    Rex=bg.rm+bg.y(0.5*(u[None,:]+v[:,None]))
    out['static'].append([h,float(np.abs(arrs[0]-Rex).max())])
for h in (0.08,0.04,0.02):
    u,v,arrs,_=build2(bg,-6,8,0,60,h,h,0.02,0.002); run2(bg,arrs,h,h)
    R,SG,RU,RV,SU,SV,PU,PV=arrs
    ruu=np.gradient(RU,h,axis=1,edge_order=2)
    res=(ruu-SU*RU+4*np.pi*R*PU**2)[:,2:-2]; sc=(np.abs(ruu)+np.abs(SU*RU)+4*np.pi*R*PU**2)[:,2:-2]
    row=[h]
    for a,b in [(0,20),(20,40),(40,60)]:
        s=slice(int(round(a/h)),int(round(b/h))+1); row.append(float(np.linalg.norm(res[s])/np.linalg.norm(sc[s])))
    out['constraint'].append(row)
s=out['static']; out['static_orders']=[float(np.log2(s[i][1]/s[i+1][1])) for i in range(len(s)-1)]
c=out['constraint']; out['constraint_orders']=[[float(np.log2(c[i][k]/c[i+1][k])) for k in (1,2,3)] for i in range(len(c)-1)]
json.dump(out,open('validation_nonlinear.json','w'),indent=1); print(json.dumps(out,indent=1))

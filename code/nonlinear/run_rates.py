"""Late-time growth of the Misner--Sharp mass on the Cauchy horizon: full double-null PDE vs Ori shell model with the same closure."""
import sys, os, numpy as np, json, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from dn2lib import *
from ori_model import Cl, run
bg=Bg(); kap=bg.kap; out={'kappa_minus':kap,'rm':bg.rm,'pde':{},'ori':{}}
def rate(m,h,v0,half=1.0):
    k=int(round(half/h)); j=int(round(v0/h))
    return float((np.log(abs(m[j+k]))-np.log(abs(m[j-k])))/(2*k*h))
# amplitude, resolution and u independence
for (A,B,h) in [(0.02,0.002,0.04),(0.02,0.002,0.02),(0.01,0.01,0.02),(0.005,0.001,0.02),(0.0005,0.0001,0.02)]:
    u,v,arrs,_=build2(bg,-6,8,0,100,h,h,A,B); run2(bg,arrs,h,h); M=mass(bg,arrs)
    key='A=%g,B=%g,h=%g'%(A,B,h); out['pde'][key]={}
    for uu in (-3.0,0.0,2.0,5.0):
        m=M[:,int(round((uu+6)/h))]
        out['pde'][key]['u=%g'%uu]={'rate@%g'%v0:rate(m,h,v0) for v0 in (59,79,98)}
        out['pde'][key]['u=%g'%uu]['sign(M)']=int(np.sign(m[-1])); out['pde'][key]['u=%g'%uu]['M(v=100)']=float(m[-1])
        out['pde'][key]['u=%g'%uu]['sigma_v(v=100)']=float(arrs[5][-1,int(round((uu+6)/h))])
# Ori model with the additive Hayward-NED closure, tail m_-(v) = - delta v^-p , p=4 (flux ~ v^-5), v -> v+1 to match (1+v)^-1.5
cl=Cl('hn',mN=5.0,aN=10.0)
for delta in (1e-3,1e-2):
    sol=run(cl,0.0,delta,4,2.0,150.0,D0=1e-8,q0=1e-3)
    d={}
    for vp in (60,80,99):
        r=float((np.log(sol.sol(vp+1)[1])-np.log(sol.sol(vp-1)[1]))/2); d["v'=%d"%vp]=r
    out['ori']['delta=%g'%delta]=d
json.dump(out,open('rates_nonlinear.json','w'),indent=1); print(json.dumps(out,indent=1))

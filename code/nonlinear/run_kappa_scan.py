"""Dependence on kappa_-:  m_N in (5,3,2,1.6,1.4) with a_N = 2 m_N (ell = 1); kappa_- = 0.796 ... 0.164.  usage: python run_kappa_scan.py m_N [h]
Domains scale as 1/kappa_- (u1 = v1 = 40/kappa_- for the threshold; v1 = 90/kappa_- for the rates): the saturation length of r_CH(u) is ~1/kappa_-; a fixed u1 = 30 gives spurious exponents for small kappa_-."""
import numpy as np, sys, json, warnings
warnings.filterwarnings('ignore')
from dn2lib import *
mN=float(sys.argv[1]); h=float(sys.argv[2]) if len(sys.argv)>2 else 0.1
bg0=Bg(mN); kap=bg0.kap; L=round(40/kap/h)*h; LR=round(90/kap/h)*h; bg=Bg(mN,tmax=0.5*(LR+20))
def col(A,RMIN=1e-5):
    try: u,v,arrs,_=build2(bg,-6,L,0,L,h,h,A,0.1*A)
    except AssertionError: return True,None,None
    run2(bg,arrs,h,h); R=arrs[0]
    return ((~np.isfinite(R))|(R<=RMIN)|(~np.isfinite(arrs[1]))).any(),u,arrs
lo=1e-4; hi=lo
while not col(hi)[0]: lo=hi; hi*=2
for _ in range(50):
    mid=0.5*(lo+hi)
    if col(mid)[0]: hi=mid
    else: lo=mid
As=0.5*(lo+hi)
ds=10**np.linspace(-11,-5,13)*As/0.02; rr=[]
for d in ds:
    c,u,a=col(As-d); rr.append(None if c else float(a[0][-1][-1]))
g=np.gradient(np.log(np.array(rr,float)),np.log(ds))
# growth rate at A = A*/2 (subcritical), u = 8
A=0.5*As; u,v,arrs,_=build2(bg,-6,14,0,LR,h,h,A,0.1*A); run2(bg,arrs,h,h); M=mass(bg,arrs)
m=M[:,int(round(14/h))]; k=int(round(1/h)); rates=[]
for frac in (0.5,0.75,0.95):
    v0=round(frac*LR/h)*h; j=int(round(v0/h)); r=float((np.log(abs(m[j+k]))-np.log(abs(m[j-k])))/(2*k*h)); rates.append([v0,r,float((kap-r)*(v0+1))])
out={'mN':mN,'aN':2*mN,'rm':bg.rm,'rp':bg.rp,'kappa':kap,'L':L,'L_rates':LR,'h':h,'Astar':As,'d':[float(x) for x in ds],'r_inf':rr,'local_gamma':[float(x) for x in g],'rates':rates}
json.dump(out,open('kscan_mN%g.json'%mN,'w'),indent=1)
print(mN,'kappa=%.4f'%kap,'A*=%.6g'%As,'rates (v,rate,q):',[(round(a),round(b,4),round(c,3)) for a,b,c in rates],'gamma',np.round(g,3))

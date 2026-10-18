"""(i) Ori exponent q=2k+2 for tails phi ~ (1+v)^-k ; (ii) critical exponent for other initial-data families."""
import sys, os, json, numpy as np, warnings
warnings.filterwarnings('ignore')
from dn2lib import *
bg=Bg(); kap=bg.kap; h=0.04; out={'q':[], 'gamma':[]}
# (i) growth-rate exponent
for k in (1.0,1.5,2.0,2.5):
    u,v,arrs,_=build2(bg,-6,8,0,100,h,h,0.01,0.002,k=k); run2(bg,arrs,h,h); M=mass(bg,arrs)
    m=M[:,int(round(8/h))]; kk=int(round(1/h)); res=[]
    for v0 in (70,98):
        j=int(round(v0/h)); r=(np.log(abs(m[j+kk]))-np.log(abs(m[j-kk])))/(2*kk*h); res.append([v0,float(r),float((kap-r)*(v0+1))])
    out['q'].append({'k':k,'pred_q':2*k+2,'rates':res}); print('k',k,'q_pred',2*k+2,res,flush=True)
# (ii) threshold and local exponent for other data families
def family(width,ratio,k):
    def run_amp(A):
        u,v,arrs,_=build2(bg,-6,40,0,50,h,h,A,ratio*A,width=width,k=k); run2(bg,arrs,h,h); R=arrs[0]
        return ((~np.isfinite(R))|(R<=1e-5)|(~np.isfinite(arrs[1]))).any(),arrs
    lo,hi=0.002,0.2
    # coarse bracket by doubling scan
    As=np.geomspace(0.002,0.3,40); prev=None
    for A in As:
        c=run_amp(A)[0]
        if c: hi=A; break
        lo=A
    for _ in range(50):
        mid=0.5*(lo+hi)
        if run_amp(mid)[0]: hi=mid
        else: lo=mid
        if hi-lo<1e-15*max(1,hi): break
    Ast=0.5*(lo+hi); ds=10**np.linspace(-10,-7,7); rs=[]
    for d in ds*Ast/0.02:      # scale d with A*
        c,arrs=run_amp(Ast-d); rs.append(None if c else float(arrs[0][-1][-1]))
    dd=np.array(ds*Ast/0.02); r=np.array([x for x in rs]); g=np.gradient(np.log(r),np.log(dd))
    return float(Ast),[float(x) for x in g],[float(x) for x in dd],[float(x) for x in r]
for (w,rt,k) in [(2.0,0.1,1.5),(1.0,0.5,1.5),(1.0,0.1,2.0)]:
    Ast,g,dd,r=family(w,rt,k); out['gamma'].append({'width':w,'ratio':rt,'k':k,'Astar':Ast,'local_exponent':g,'d':dd,'r':r}); print('width',w,'ratio',rt,'k',k,'A*',Ast,'local exp',np.round(g,3),flush=True)
json.dump(out,open('universality_nonlinear.json','w'),indent=1)

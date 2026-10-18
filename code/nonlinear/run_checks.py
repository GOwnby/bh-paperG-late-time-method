"""Supporting checks quoted in Section 6 that are not in the other scripts. Run from this directory.
 (a) A* independent of v1;  (b) saturation of r in v (weak data and near threshold);  (c) sign of M versus u at v=100 and growth rate near threshold;
 (d) Raychaudhuri residual in the v direction."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
from dn2lib import *
bg=Bg(); kap=bg.kap; h=0.04; out={}
# (a)
def Astar(u1,v1,RMIN=1e-5,h=h):
    def col(A):
        u,v,arrs,_=build2(bg,-6,u1,0,v1,h,h,A,0.1*A); run2(bg,arrs,h,h); R=arrs[0]
        return ((~np.isfinite(R))|(R<=RMIN)|(~np.isfinite(arrs[1]))).any()
    lo,hi=0.015,0.03
    for _ in range(45):
        mid=0.5*(lo+hi)
        if col(mid): hi=mid
        else: lo=mid
    return 0.5*(lo+hi)
out['Astar_vs_v1(u1=8)']={str(v1):Astar(8,v1) for v1 in (40,60,80,100)}; print(out['Astar_vs_v1(u1=8)'],flush=True)
# (b),(c)
As=0.02042798661782126          # A* for h=0.04, u1=40, RMIN=1e-5 (run_threshold.py)
out['near']={}
def rate(m,j0,k): return float((np.log(abs(m[j0+k]))-np.log(abs(m[j0-k])))/(2*k*h))
for name,A,B in [('weak A=0.02,B=0.002',0.02,0.002)]+[('A*-A=%g'%d,As-d,0.1*(As-d)) for d in (1e-4,1e-6,1e-8,1e-10)]:
    u,v,arrs,_=build2(bg,-6,40,0,100,h,h,A,B); run2(bg,arrs,h,h); M=mass(bg,arrs); R=arrs[0]
    k=int(round(1/h)); row={}
    for uu in (-3,0,2,10,30,40):
        i=int(round((uu+6)/h)); m=M[:,i]
        row['u=%g'%uu]={'rate@79':rate(m,int(round(79/h)),k),'rate@98':rate(m,int(round(98/h)),k),'sign':int(np.sign(m[-1]))}
    sat={}
    for uu in (4,40):
        i=int(round((uu+6)/h)); sat['u=%g'%uu]=float(abs(R[int(round(100/h)),i]-R[int(round(50/h)),i])/R[int(round(100/h)),i])
    out['near'][name]={'rates':row,'|r(100)-r(50)|/r':sat}; print(name,row['u=0'],row['u=40'],sat,flush=True)
# sign scan, weak data
u,v,arrs,_=build2(bg,-6,8,0,100,h,h,0.02,0.002); run2(bg,arrs,h,h); M=mass(bg,arrs)
sg=np.sign(M[-1]); idx=np.where(sg[1:]!=sg[:-1])[0]
out['sign_change_u(A=0.02,B=0.002,v=100)']=[float(u[i]) for i in idx]; print(out['sign_change_u(A=0.02,B=0.002,v=100)'])
# (d)
for hh in (0.08,0.04,0.02):
    u,v,arrs,_=build2(bg,-6,8,0,60,hh,hh,0.02,0.002); run2(bg,arrs,hh,hh)
    R,SG,RU,RV,SU,SV,PU,PV=arrs
    rvv=np.gradient(RV,hh,axis=0,edge_order=2); res=(rvv-SV*RV+4*np.pi*R*PV**2)[2:-2,:]; sc=(np.abs(rvv)+np.abs(SV*RV)+4*np.pi*R*PV**2)[2:-2,:]
    s=slice(0,int(round(20/hh))); t=slice(int(round(20/hh)),int(round(58/hh)))
    out.setdefault('constraint_v',[]).append([hh,float(np.linalg.norm(res[s])/np.linalg.norm(sc[s])),float(np.linalg.norm(res[t])/np.linalg.norm(sc[t]))])
print(out['constraint_v'])
json.dump(out,open('checks_nonlinear.json','w'),indent=1)

# E13: as gen2.py, but (i) rays placed exactly on grid points of the coarsest grid (s_q multiple of 0.05 -> no interpolation error),
# (ii) the streaming evolver also returns I(s_q,v)=int_0^{s_q} 4 pi r phi_s^2/W ds  (u-Raychaudhuri constraint: y=-r_s/W = 1/2 + I exactly).
# usage: gen3.py B k A U0 w v1 hs1 hs2 ...   -> gen3_*.json
import os, numpy as np, sys, warnings, json, time, ctypes
warnings.filterwarnings('ignore')
from run_tail import *
import dnU
from dnU import V0
B,k,A,U0,w,v1=[float(x) for x in sys.argv[1:7]]; hl=[float(x) for x in sys.argv[7:]]
Uq=[0.3,0.6,1.0,1.2]; vq=np.arange(20,v1-1.9,1.0)
pulse=None if A==0 else (A,U0,w)
c=0.2*np.exp(-S.kp*v1)
sq=[np.round(np.log(1+x*S.kp/c)/S.kp/0.05)*0.05 for x in Uq]          # on the coarsest grid
Uact=[c*np.expm1(S.kp*s)/S.kp for s in sq]
_ls2=ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)),'libstream2.so'))
dp=ctypes.POINTER(ctypes.c_double)
_ls2.evolve_stream2.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,dp,dp,ctypes.c_int,ctypes.POINTER(ctypes.c_int),dp,dp,ctypes.c_int]
def run_stream2(S,d,hu,hv,cols,niter=3):
    cols=np.ascontiguousarray(np.asarray(cols,dtype=np.int32)); out=np.zeros((len(cols),d['nv'],8)); oI=np.zeros((len(cols),d['nv']))
    _ls2.evolve_stream2(d['nu'],d['nv'],hu,hv,S.mN,S.aN,d['row0'].ctypes.data_as(dp),d['col0'].ctypes.data_as(dp),len(cols),cols.ctypes.data_as(ctypes.POINTER(ctypes.c_int)),out.ctypes.data_as(dp),oI.ctypes.data_as(dp),niter)
    return out,oI
data={}
for hs in hl:
    t0=time.time()
    d=build_eh_1d(S,1.5,v1,hs,hs,B,k=k,c=c,vH=v1+300,pulse=pulse)
    cols=[int(round(s/hs)) for s in sq]
    out,oI=run_stream2(S,d,hs,hs,cols)
    ii=[int(round(t/hs)) for t in vq]
    F=[[] for f in range(8)]; M=[]; Ic=[]
    for n in range(len(sq)):
        fl=[out[n][ii,f] for f in range(8)]
        r,sg,ru,rv=fl[:4]; M.append(0.5*r*(1+4*ru*rv*np.exp(-sg))); Ic.append(oI[n][ii])
        for f in range(8): F[f].append(fl[f])
    names=['r','sg','rs','rv','sgs','sV','Ps','PV']
    data[hs]=dict(M=np.array(M),I=np.array(Ic),**{names[f]:np.array(F[f]) for f in range(8)})
    rf=d['hz'].sol(v1)[0]; mu_f=rf/2-MN(rf)
    print('h=%g nu=%d nv=%d  %.0fs'%(hs,d['nu'],d['nv'],time.time()-t0),flush=True)
rm,rp,km,kp_=inner(mu_f)
json.dump(dict(Uq=Uact,sq=[float(s) for s in sq],vq=vq.tolist(),mu_f=mu_f,km=km,B=B,k=k,A=A,U0=U0,w=w,v1=v1,data={str(h):{kk:vv.tolist() for kk,vv in dd.items()} for h,dd in data.items()}),open('gen3_B%g_k%g_v%g.json'%(B,k,v1),'w'))
print('done mu_f=%.4e kappa-(mu_f)=%.6f'%(mu_f,km))

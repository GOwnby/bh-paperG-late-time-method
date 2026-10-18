"""E11b: amplitude scaling of the remainder PDE/kernel(mu_f) - 1 at v=100 (final-hole kernel).
usage: MU_F=<mu_f> python3 e11_scaling.py <json>   (the json is a gen/gen3 five-grid file, ray U~1 = index 2)"""
import os,sys,json,numpy as np,warnings
warnings.filterwarnings('ignore')
fn=sys.argv[1]; sys.argv=[sys.argv[0]]
src=open('kernel_mu.py').read().split("D=json.load")[0].replace("fn=sys.argv[1]; sys.argv=[sys.argv[0]]","")
exec(src)
D=json.load(open(fn)); k=D['k']; B=D['B']; hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq'])
P=analyze.extrap([np.array(D['data'][h]['PV'][2]) for h in hs])[-1][0]
def pred(v):
    vp=np.concatenate([np.linspace(0,min(v,60),24001),np.linspace(min(v,60),v+12,100001)[1:]])
    return np.trapezoid(Kf(v-vp)*(-k*B*(1+vp)**(-k-1)),vp)
vs=[v for v in (80,90,100) if v<=vq[-1]-1]
print('%s k=%g B=%g mu_f=%s: ratio-1 at v='%(fn,k,B,os.environ['MU_F']),' '.join('%d: %.3e'%(v,P[int(v-vq[0])]/pred(float(v))-1) for v in vs))

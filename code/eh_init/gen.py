# streaming multi-grid run; saves M, sigma_v, phi_v (+ r_U/W) at target U for v=20..v1-? ; usage: gen.py B k A U0 w v1 hs1 hs2 ...
import os, numpy as np, sys, warnings, json, time
warnings.filterwarnings('ignore')
from run_tail import *
from dnU import V0
B,k,A,U0,w,v1=[float(x) for x in sys.argv[1:7]]; hl=[float(x) for x in sys.argv[7:]]
Uq=[0.3,0.6,1.0,1.2]; vq=np.arange(20,v1-1.9,1.0)
pulse=None if A==0 else (A,U0,w)
data={}
for hs in hl:
    t0=time.time(); c=0.2*np.exp(-S.kp*v1)
    d=build_eh_1d(S,1.5,v1,hs,hs,B,k=k,c=c,vH=v1+300,pulse=pulse)
    st=[np.log(1+x*S.kp/c)/S.kp for x in Uq]
    jj=[int(np.floor(x/hs)) for x in st]; cols=sorted(set(sum([[j,j+1] for j in jj],[])))
    out=run_stream(S,d,hs,hs,cols)
    ii=[int(round(t/hs)) for t in vq]
    def get(n,j,f,sx):
        a=out[cols.index(j)][ii,f]; b=out[cols.index(j+1)][ii,f]; fr=sx/hs-j; return (1-fr)*a+fr*b
    M=[];SV=[];PV=[]
    for n,(sx,j) in enumerate(zip(st,jj)):
        r,sg,ru,rv=[get(n,j,f,sx) for f in (0,1,2,3)]
        M.append(0.5*r*(1+4*ru*rv*np.exp(-sg))); SV.append(get(n,j,5,sx)); PV.append(get(n,j,7,sx))
    data[hs]=dict(M=np.array(M),sV=np.array(SV),PV=np.array(PV))
    rf=d['hz'].sol(v1)[0]; mu_f=rf/2-MN(rf)
    print('h=%g nu=%d nv=%d  %.0fs'%(hs,d['nu'],d['nv'],time.time()-t0),flush=True)
rm,rp,km,kp_=inner(mu_f)
json.dump(dict(Uq=Uq,vq=vq.tolist(),mu_f=mu_f,km=km,B=B,k=k,A=A,U0=U0,w=w,v1=v1,data={str(h):{kk:vv.tolist() for kk,vv in dd.items()} for h,dd in data.items()}),open('gen_B%g_k%g_A%g_U%g_w%g_v%g%s.json'%(B,k,A,U0,w,v1,(('' if V0==1.0 else '_T%g'%V0)+('' if os.environ.get('MN','5')=='5' else '_mN'+os.environ['MN'])+('' if not os.environ.get('TAIL_PULSE') else '_P'+os.environ['TAIL_PULSE'].replace(',','_')))),'w'))
print('done mu_f=%.4e kappa-(mu_f)=%.6f'%(mu_f,km))

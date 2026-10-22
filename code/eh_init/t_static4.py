import numpy as np, warnings, time, sys
warnings.filterwarnings('ignore')
from dnU import *
S=StaticU()
U1,v1=10.0,100.0; c=0.2*np.exp(-S.kp*v1)
def conv(ex,gp):
    r,sg,rU,rV,sU,sV=ex
    return r,sg+np.log(gp)[None,:],rU*gp[None,:],rV,sU*gp[None,:]+S.kp,sV
for (hs,hv) in [(0.2,0.2),(0.1,0.1),(0.05,0.05)]:
    t=time.time()
    s_,v,arrs,hz,U,gp=build_eh(S,U1,v1,hs,hv,0.0,c=c)
    run2(S,arrs,hs,hv)
    UU,VV=np.meshgrid(U,v); ex=conv(S.fields(UU,VV),gp)
    print('h',hs,hv,'nu',len(U),'nan',int(np.isnan(arrs[1]).sum()))
    print('(wall time %.1f s)'%(time.time()-t),file=sys.stderr)    # timing goes to stderr so that the stdout log is reproducible byte for byte
    for vi in (20,50,100):
        i=int(round(vi/hv)); row=[]
        for Ux in (0.01,0.1,1.0,10.0):
            j=int(np.argmin(abs(U-Ux))); row.append('U=%.3g dsig=%.1e dsV=%.1e dlnrU=%.1e'%(U[j],arrs[1][i,j]-ex[1][i,j],arrs[5][i,j]-ex[5][i,j],np.log(abs(arrs[2][i,j]/ex[2][i,j]))))
        print('  v=%g'%vi,' | '.join(row))

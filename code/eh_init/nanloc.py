import numpy as np, sys, warnings
warnings.filterwarnings('ignore')
from run_tail import *
B=float(sys.argv[1]); hs=float(sys.argv[2]); v1=float(sys.argv[3])
s_,v,arrs,hz,U,gp,tt=run(B,1.5,hs,hs,U1=10.0,v1=v1)
bad=np.isnan(arrs[1])
first=[ (int(np.argmax(bad[:,j])),) if bad[:,j].any() else None for j in range(len(U))]
js=[j for j in range(len(U)) if bad[:,j].any()]
print('first column with NaN: U=%.3f'%U[js[0]] if js else 'no NaN')
for j in js[:1]+js[len(js)//2:len(js)//2+1]:
    iv=int(np.argmax(bad[:,j])); print('U=%.3f first NaN at v=%.2f'%(U[j],v[iv]))
    for i in range(max(iv-6,0),iv):
        print('   v=%.2f r=%.5f sig=%.3f rU=%.3e rV=%.3e sU=%.3e sV=%.3e phiU=%.3e phiV=%.3e'%(v[i],*[a[i,j] for a in arrs[:2]],*[a[i,j] for a in arrs[2:]]) )

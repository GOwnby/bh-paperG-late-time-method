# uniform-U grid (no log map): where does the static (B=0) evolution fail?  (c=None path of build_eh)
import numpy as np, warnings
warnings.filterwarnings('ignore')
from dnU import *
S=StaticU()
for hU in (0.04,0.02):
    U,v,arrs,hz=build_eh(S,10.0,100.0,hU,hU*5,0.0)
    run2(S,arrs,hU,hU*5)
    bad=np.isnan(arrs[1]); i=int(np.argmax(bad.any(axis=1))) if bad.any() else None
    print('uniform U grid h_U=%g h_v=%g: first NaN row at v=%s'%(hU,hU*5,None if i is None else '%.1f'%v[i]))

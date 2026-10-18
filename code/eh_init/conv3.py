# three-grid check of sigma_v on U=0.3 at v=95 for B=0.03,k=1.5 tail-only (domain U<=1.5 to fit in memory)
import numpy as np, warnings, gc
warnings.filterwarnings('ignore')
from run_tail import *
vals=[]
for hs in (0.05,0.025,0.0125):
    s_,v,arrs,hz,U,gp,tt=run(0.03,1.5,hs,hs,U1=1.5,v1=100.0)
    j=int(np.argmin(abs(U-0.3))); i=int(round(95/hs)); vals.append(abs(arrs[5][i,j])); del arrs; gc.collect()
    print('h=%g |sigma_v|(U=%.4f,v=95)=%.6f'%(hs,U[j],vals[-1]),flush=True)
r=(vals[0]-vals[1])/(vals[1]-vals[2]); R=vals[2]+(vals[2]-vals[1])/3
print('convergence ratio %.2f ; Richardson(h/2,h/4) = %.6f ; kappa-(mu_f)=0.784821 ; offset %.3f%%'%(r,R,100*(R/0.784821-1)))

import numpy as np, sys, warnings
warnings.filterwarnings('ignore')
from run_tail import *
B=float(sys.argv[1]); k=float(sys.argv[2]); v1=float(sys.argv[3]); hs=float(sys.argv[4])
s_,v,arrs,hz,U,gp,tt=run(B,k,hs,hs,U1=10.0,v1=v1)
rf=hz.sol(v[-1])[0]; mu_f=rf/2-MN(rf); rm,rp,km_f,kpp=inner(mu_f)
M=mass(S,arrs); mu=M-MN(arrs[0])
print('B=%g k=%g h=%g  mu_f=%.5e kappa-(mu_f)=%.6f'%(B,k,hs,mu_f,km_f))
for Ux in (0.1,0.3,1.0):
    j=int(np.argmin(abs(U-Ux)))
    for vi in (40,50,55,60,65):
        i=int(round(vi/hs))
        m=mu[i,j]; a=inner(m)[2] if abs(m)<0.3 else np.nan
        print('  U=%.2g v=%d  mu=%.5e  kappa-(mu_loc)=%.6f   sigma_v=%.6f   -sigma_v-kappa-(mu_loc)=%.2e'%(U[j],vi,m,a,arrs[5][i,j],-arrs[5][i,j]-a))

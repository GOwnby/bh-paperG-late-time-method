import numpy as np, sys, warnings, time
warnings.filterwarnings('ignore')
from run_tail import *
B=float(sys.argv[1]); k=float(sys.argv[2]); v1=float(sys.argv[3]); hs_list=[float(x) for x in sys.argv[4:]]
res={}
for hs in hs_list:
    s_,v,arrs,hz,U,gp,tt=run(B,k,hs,hs,U1=10.0,v1=v1)
    rf=hz.sol(v[-1])[0]; mu_f=rf/2-MN(rf); rm,rp,km,kpp=inner(mu_f)
    M=mass(S,arrs); PV=arrs[7]
    print('h=%g  t=%.0fs  mu_f=%.4e  kappa-(mu_f)=%.6f  static %.6f  nan=%d'%(hs,tt,mu_f,km,0.795649,int(np.isnan(arrs[1]).sum())))
    for Ux in (0.3,3.0):
        j=int(np.argmin(abs(U-Ux))); line=[]
        for vi in (50,60,70,v1-5):
            i=int(round(vi/hs)); w=int(round(2.0/hs))
            lnr=(np.log(abs(M[i+w,j]))-np.log(abs(M[i-w,j])))/(v[i+w]-v[i-w])
            line.append('v=%d sV=%.5f rate=%.4f [Ori %.4f] M=%.2e'%(vi,arrs[5][i,j],lnr,km-(2*k+2)/vi,M[i,j]))
        print('   U=%.2g '%U[j],' | '.join(line))
    del arrs

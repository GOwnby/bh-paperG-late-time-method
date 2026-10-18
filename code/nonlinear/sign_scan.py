# E-sign: is the sign statement sign(M) = -sign(r_u) (for |M| >> r/2) and the position of the sign change independent of data set and grid?
# scans amplitude A, tail amplitude B, grid h in the double-null run of Section 6.3 (domain u in [-6,8], v in [0,100]); u_* = location of the sign change of r_u at v=100
import sys; sys.path.insert(0,'.')
import numpy as np, warnings
warnings.filterwarnings('ignore')
from dn2lib import *
bg=Bg()
print('   A      B       h     u_*(r_u)  u_*(M)   #sign changes (r_u, M)   sign(M)=-sign(r_u) where |M|>10 r (fraction)   M range            rows')
for A,B,h in [(0.02,0.002,0.04),(0.02,0.002,0.02),(0.02,0.002,0.08),(0.005,0.002,0.04),(0.01,0.002,0.04),(0.0204,0.002,0.04),(0.02,0.0005,0.04),(0.02,0.01,0.04),(0.02,0.02,0.04),(0.02,0.002,0.01),(0.01,0.01,0.04),(0.01,0.01,0.02),(0.005,0.001,0.04),(0.005,0.001,0.02),(0.0005,0.0001,0.04),(0.0005,0.0001,0.02),(0.0005,0.0001,0.01)]:
    u,v,arrs,_=build2(bg,-6,8,0,100,h,h,A,B); run2(bg,arrs,h,h); M=mass(bg,arrs); R,SG,RU,RV=arrs[:4]
    ok=np.isfinite(M[-1])&np.isfinite(RU[-1])&np.isfinite(R[-1]); n_bad=int((~ok).sum())
    # columns where the evolution has left the resolved domain (NaN: r reached the cutoff above the threshold) are excluded
    u=u[ok]; M=M[:,ok]; R=R[:,ok]; RU=RU[:,ok]
    SGo=arrs[1][:,ok]; Yu=RU/np.exp(SGo)   # r_u/W: the u-Raychaudhuri equation gives d_u(r_u/W) = -4 pi r phi_u^2/W <= 0
    inc=np.diff(Yu[-1]); mono=inc.max()/np.abs(Yu[-1]).max()
    sM=np.sign(M[-1]); sR=np.sign(RU[-1]); iR=np.where(sR[1:]!=sR[:-1])[0]; iM=np.where(sM[1:]!=sM[:-1])[0]
    big=np.abs(M[-1])>10*R[-1]; frac=np.mean(sM[big]==-sR[big]) if big.any() else np.nan
    print('%6.4f %7.4f %6.3f   %s   %s     (%d,%d)      %.4f      %.2e..%.2e   (excluded NaN columns: %d)  max increase of r_u/W along u / max|r_u/W| = %.1e'%(A,B,h,[round(float(x),2) for x in u[iR]],[round(float(x),2) for x in u[iM]],len(iR),len(iM),frac,M[-1].min(),M[-1].max(),n_bad,mono))

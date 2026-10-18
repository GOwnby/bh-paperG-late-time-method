# v=300, B=0.003 tail-only runs: local exponent of phi_v, |sigma_v| vs kappa_-(mu_f), lambda vs kappa_- - 2(k+1)/(v+1)
import json, numpy as np, sys, warnings, analyze
warnings.filterwarnings('ignore')
for fn in sys.argv[1:]:
    D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq']); k=D['k']; km=D['km']
    print(fn,'k=%.1f mu_f=%.4e kappa-(mu_f)=%.6f grids'%(k,D['mu_f'],km),hs)
    for n in (2,):
        S=analyze.extrap([np.abs(np.array(D['data'][h]['sV'][n])) for h in hs]); P=analyze.extrap([np.array(D["data"][h]["PV"][n]) for h in hs])
        S1,S2=S[-1][0],S[-2][1]; P1,P2=np.abs(P[-1][0]),np.abs(P[-2][1])
        print('  U=%.1f  (top-order extrapolant; in brackets the next-lower one)'%D['Uq'][n])
        print('   v    -dln|phi_v|/dv   local exponent p   |sV|-km        lam   km-2(k+1)/(v+1)  lam-pred')
        for v0 in (60,100,140,180,220,260,290):
            i=int(v0-vq[0]); w=4
            ld=lambda P:-(np.log(P[i+w])-np.log(P[i-w]))/(vq[i+w]-vq[i-w])
            r=ld(P1); r2=ld(P2); p=-(np.log(P1[i+w])-np.log(P1[i-w]))/(np.log(vq[i+w]+1)-np.log(vq[i-w]+1))
            lam=S1+2*np.gradient(np.log(P1),vq); pred=km-2*(k+1)/(vq+1)
            print('  %4d  %.5f [%.5f]  %.3f   %+.1e [%+.1e]  %.5f  %.5f  %+.1e'%(v0,r,r2,p,S1[i]-km,S2[i]-km,lam[i],pred[i],lam[i]-pred[i]))

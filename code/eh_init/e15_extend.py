"""E15 (Paper E, Sec. curvature): extendibility indicators on the ray U~1 of the gen3 runs (constraint-projected mass M_cc, Eq. yc).
(1) C^0 indicator in a Kruskal-type coordinate V=-exp(-kappa_- v): W_UV = W_v e^{kappa v}/kappa. Lambda(v)=sigma(v)+kappa_-(mu_f) v must converge for the metric to extend continuously
    (sigma from the five-grid Romberg of the stored ray field 'sg'; also int (|sigma_v|-kappa_-) dv from the extrapolated sigma_v, and its tail estimate).
(2) Ori-type weakness: along a worldline crossing the Cauchy horizon transversally, d tau ~ e^{-kappa_- v} dv, and the leading tidal component is ~ M/r^3; the integral J(v)=int_{v_a}^v M r^-3 e^{-kappa_- v'} dv' must converge (then the integrated tidal distortion is finite).
usage: e15_extend.py gen3_...json"""
import json,sys,numpy as np
fn=sys.argv[1]; sys.argv=[sys.argv[0],fn,'2']
exec(open('e13_project.py').read().split("if __name__")[0])
X=run(); sg,_=ex('sg'); sVx,_=ex('sV'); Psx,_=ex('Ps'); PVx,_=ex('PV'); 
kmu=km  # kappa_-(mu_f) from the json
vs=np.arange(60,281,1.0)
lnM=[];lnr=[]
for v in vs:
    i=int(v-vq[0]); C=X['solC'].sol(float(v)); yc=0.5+X['I'][i]
    lnM.append(np.log(C[0]/2)+np.logaddexp(0.0,np.log(4.0)+np.log(yc)+np.log(C[1]))); lnr.append(np.log(C[0]))
lnM=np.array(lnM); lnr=np.array(lnr)
f=np.exp(lnM-3*lnr-kmu*vs); f=np.where(np.isfinite(f),f,0.0)    # tidal integrand M r^-3 e^{-kappa v}
from scipy.integrate import cumulative_trapezoid
J=cumulative_trapezoid(f,vs,initial=0.0)
idx=lambda v:int(v-vs[0])
Lam=np.array([sg[int(v-vq[0])]+kmu*v for v in vs])
E=np.abs(sVx[(vs-vq[0]).astype(int)])-kmu       # excess of |sigma_v| over kappa_-(mu_f)
IE=cumulative_trapezoid(E,vs,initial=0.0)
gphi=np.array([abs(Psx[int(v-vq[0])]*PVx[int(v-vq[0])])*np.exp(-(sg[int(v-vq[0])]+kmu*v)) for v in vs])   # |phi_s phi_v|/W e^{-kappa v}: matter (Ricci/H) tidal terms
Jp=cumulative_trapezoid(gphi,vs,initial=0.0)
print('%s: k=%g B=%g kappa-(mu_f)=%.6f ray U=%.4f'%(fn,k,D['B'],kmu,D['Uq'][2]))
print('   v     Lambda(v)-Lambda(100)   int_100^v(|sigma_v|-kappa_-)dv   excess e(v)   |  J(v)      J(v)/J(280)   v^q-fit local exponent of dJ/dv')
for v in (100,140,180,200,240,260,280):
    i=idx(v); i0=idx(100)
    q=-(np.log(f[i]+1e-300)-np.log(f[i-20]+1e-300))/(np.log(v)-np.log(v-20)) if f[i]>0 and f[i-20]>0 else np.nan
    print(' %4d   %+.3e              %+.3e                    %+.3e   |  %.4e  %.5f   %.3f'%(v,Lam[i]-Lam[i0],IE[i]-IE[i0],E[i],J[i],J[i]/J[-1],q))
print('   Lambda(280)-Lambda(200) = %+.3e ;  int_200^280 e dv = %+.3e ;  J(280)-J(200) = %.3e  (%.2e of J(280))'%(Lam[idx(280)]-Lam[idx(200)],IE[idx(280)]-IE[idx(200)],J[idx(280)]-J[idx(200)],(J[idx(280)]-J[idx(200)])/J[idx(280)]))
qe=np.log(E[idx(200)]/E[idx(280)])/np.log(280/200.)
rem=E[idx(280)]*280/(qe-1) if qe>1 else np.inf
qj=-(np.log(f[idx(280)])-np.log(f[idx(200)]))/np.log(280/200.)
print('   SUMMARY: local exponent of e(v) on 200..280: qe=%.2f ; power-law estimate of int_280^inf e dv = %.2e ; exponent of the tidal integrand on 200..280: %.2f (2k+2=%g); Lambda(280)-Lambda(100)=%+.4e'%(qe,rem,qj,2*k+2,Lam[idx(280)]-Lam[idx(100)]))
print('   matter tidal terms |phi_s phi_v| e^{-Lambda}: integral J_phi(v) at v=100,140,200,280: %.4e %.4e %.4e %.4e ; J_phi(280)-J_phi(200) = %.2e of J_phi(280); integrand local exponent on 200..280: %.2f (k+1=%g)'%(Jp[idx(100)],Jp[idx(140)],Jp[idx(200)],Jp[idx(280)],(Jp[idx(280)]-Jp[idx(200)])/Jp[idx(280)],-(np.log(gphi[idx(280)])-np.log(gphi[idx(200)]))/np.log(280/200.),k+1))

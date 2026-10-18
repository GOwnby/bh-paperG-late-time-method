"""Curvature along the Cauchy horizon (Kretschmann scalar).  Checks the invariant code against the analytic static Hayward K and
measures the growth of K at u = 2 for A = 0.02, B = 0.002.  Writes curvature_nonlinear.json."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
from dn2lib import *
bg=Bg(); kap=bg.kap; mN,aN=bg.mN,bg.aN; out={}
def fK(r):                      # static: K = f''^2 + 4 f'^2/r^2 + 4 (1-f)^2/r^4, f = 1 - 2 M_N(r)/r
    d=r**3+aN; f=1-2*mN*r*r/d; e=1e-5
    g=lambda x:1-2*mN*x*x/(x**3+aN)
    fp=(g(r+e)-g(r-e))/(2*e); fpp=(g(r+e)-2*f+g(r-e))/e**2
    return fpp**2+4*fp**2/r**2+4*(1-f)**2/r**4
out['static_rel_err']=[]
for h in (0.08,0.04):
    u,v,a0,_=build2(bg,-6,6,0,30,h,h,0.0,0.0); run2(bg,a0,h,h); K0=invariants(bg,a0)[4]; e=[]
    for (uu,vv) in [(0,10),(0,20),(-3,5),(3,25)]:
        i=int(round((uu+6)/h)); j=int(round(vv/h)); r=a0[0][j,i]; e.append(float(abs(K0[j,i]-fK(r))/fK(r)))
    out['static_rel_err'].append([h,e])
out['K']={}
for h in (0.04,0.02):
    u,v,arrs,_=build2(bg,-6,8,0,100,h,h,0.02,0.002); run2(bg,arrs,h,h); M,T1,T2,T3,K=invariants(bg,arrs)
    R,SG,RU,RV,SU,SV,PU,PV=arrs; W=np.exp(SG); i=int(round(8/h)); rows=[]
    for vv in (40,60,80,100):
        j=int(round(vv/h)); rows.append({'v':vv,'|M|':float(abs(M[j,i])),'K':float(K[j,i]),'T1':float(T1[j,i]),'T2':float(T2[j,i]),'T3':float(T3[j,i]),
          'K/(phi_u phi_v/W)^2':float(K[j,i]/((PU[j,i]*PV[j,i]/W[j,i])**2)),'phi_u':float(PU[j,i]),'phi_v':float(PV[j,i])})
    k=int(round(1/h)); lk=np.log(abs(K[:,i]))
    dl={str(v0):float((lk[int(round(v0/h))+k]-lk[int(round(v0/h))-k])/(2*k*h)) for v0 in (60,80,98)}
    out['K'][str(h)]={'rows':rows,'dlnK/dv':dl,'2kappa-5/(v+1)':{str(v0):float(2*kap-5/(v0+1)) for v0 in (60,80,98)}}
out['2048pi^2']=float(2048*np.pi**2)
# affine length of the ray u = const (null geodesic with d lambda = W dv, since Gamma^v_vv = sigma_v), W e^{kappa v}, r on the ray
h=0.04; u,v,arrs,_=build2(bg,-6,8,0,100,h,h,0.02,0.002); run2(bg,arrs,h,h); R,SG,RU,RV,SU,SV,PU,PV=arrs; W=np.exp(SG)
i=int(round(8/h)); Wi=W[:,i]
out['affine']={'u':2.0,'affine_length_to_v100':float(np.sum(0.5*(Wi[1:]+Wi[:-1])*h)),'W(100)/kappa':float(Wi[-1]/kap),
  'W*exp(kappa v) at v=40,70,100':[float(Wi[int(round(x/h))]*np.exp(kap*x)) for x in (40,70,100)],'r(v=100)':float(R[-1,i]),'sigma_v(v=100)':float(SV[-1,i])}
# other tails and amplitudes: K/(2048 pi^2 (phi_u phi_v/W)^2) and dlnK/dv vs 2kappa-(2k+2)/(v+1)
out['K_other']=[]
for (A,B,k) in [(0.02,0.002,1.0),(0.02,0.002,2.0),(0.005,0.001,1.5),(0.0204,0.00204,1.5)]:
    u,v,arrs,_=build2(bg,-6,8,0,100,h,h,A,B,k=k); run2(bg,arrs,h,h); M,T1,T2,T3,K=invariants(bg,arrs)
    R,SG,RU,RV,SU,SV,PU,PV=arrs; W=np.exp(SG); kk=int(round(1/h)); row={'A':A,'B':B,'k':k,'u':{}}
    for uu in (-3,0,2,5):
        i=int(round((uu+6)/h)); j=int(round(98/h)); lk=np.log(abs(K[:,i]))
        row['u'][str(uu)]={'ratio':float(K[j,i]/(2048*np.pi**2*(PU[j,i]*PV[j,i]/W[j,i])**2)),'dlnK/dv@98':float((lk[j+kk]-lk[j-kk])/(2*kk*h)),'2kappa-(2k+2)/(v+1)':float(2*kap-(2*k+2)/99)}
    out['K_other'].append(row)

json.dump(out,open('curvature_nonlinear.json','w'),indent=1); print(json.dumps(out,indent=1))

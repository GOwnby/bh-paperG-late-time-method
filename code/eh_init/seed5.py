import numpy as np, sys, warnings, gc, json
warnings.filterwarnings('ignore')
from run_tail import *
B,k,A,U0,w,v1=[float(x) for x in sys.argv[1:7]]; hl=[0.05,0.025,0.0125]
Uq=[0.8,1.0,1.2]; vq=np.arange(40,v1-3.9,1.0)
data={}
for hs in hl:
    c=0.2*np.exp(-S.kp*v1)
    s_,v,arrs,hz,U,gp=build_eh(S,2.5,v1,hs,hs,B,k=k,c=c,vH=v1+300,pulse=(A,U0,w))
    run2(S,arrs,hs,hs); M=mass(S,arrs); sV=arrs[5]; PV=arrs[7]
    st=[np.log(1+x*S.kp/c)/S.kp for x in Uq]
    def at(arr,i,sx):
        j=int(np.floor(sx/hs)); f=sx/hs-j; return (1-f)*arr[i,j]+f*arr[i,j+1]
    ii=[int(round(t/hs)) for t in vq]
    data[hs]=dict(M=np.array([[at(M,i,sx) for i in ii] for sx in st]),sV=np.array([[at(sV,i,sx) for i in ii] for sx in st]),PV=np.array([[at(PV,i,sx) for i in ii] for sx in st]))
    if hs==hl[-1]:
        # exact consequence check: mu_v = -8 pi r^2 (r_u/W) phi_v^2 , mu=M-M_N(r)
        j=int(round(st[1]/hs)); R,SG,RU=arrs[0],arrs[1],arrs[2]; mu=M-MN(R)
        print('mu_v identity check (U~1, finest grid): v, dmu/dv, -8 pi r^2 r_u phi_v^2/W, ratio')
        for t in (50,55,60,65,70):
            i=int(round(t/hs)); dm=(mu[i+4,j]-mu[i-4,j])/(8*hs); rhs=-8*np.pi*R[i,j]**2*RU[i,j]*np.exp(-SG[i,j])*PV[i,j]**2
            print('   v=%d  %.4e  %.4e  %.5f'%(t,dm,rhs,dm/rhs))
        # u-constraint residual C_u = r_ss - sigma_s r_s + 4 pi r phi_s^2 at a few rows, relative to phi term
        for t in (0,30,50):
            i=int(round(t/hs)); rss=np.gradient(RU[i],s_); cu=rss-arrs[4][i]*RU[i]+4*np.pi*R[i]*arrs[6][i]**2
            sel=(abs(U-1)<0.4); print('   u-constraint residual v=%d: max %.2e vs phi term max %.2e'%(t,np.abs(cu[sel]).max(),np.abs(4*np.pi*R[i]*arrs[6][i]**2)[sel].max()))
    rf=hz.sol(v[-1])[0]; mu_f=rf/2-MN(rf); del arrs,M; gc.collect()
rm,rp,km,kp_=inner(mu_f)
json.dump({str(h):{kk:np.asarray(vv).tolist() for kk,vv in d.items()} for h,d in data.items()},open('seed5_B%g_k%g_A%g.json'%(B,k,A),'w'))
print('done k=%g mu_f=%.4e kappa-(mu_f)=%.5f'%(k,mu_f,km),flush=True)

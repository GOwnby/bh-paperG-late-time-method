import sys, os, json, glob, numpy as np, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from dn2lib import *
from ori_model import Cl, run
bg=Bg(); kap=bg.kap
fig,ax=plt.subplots(2,2,figsize=(10.5,7.6))
# (a) growth rate of |M| on the Cauchy horizon
h=0.04
u,v,arrs,_=build2(bg,-6,8,0,100,h,h,0.02,0.002); run2(bg,arrs,h,h); M=mass(bg,arrs)
m=M[:,int(round((2+6)/h))]; k=int(round(1/h)); js=np.arange(int(30/h),int(99/h),int(1/h)); vs=js*h
rate=np.array([(np.log(abs(m[j+k]))-np.log(abs(m[j-k])))/(2*k*h) for j in js])
cl=Cl('hn'); sol=run(cl,0.0,1e-3,4,2.0,150.0,D0=1e-8,q0=1e-3)
vo=np.arange(31,100.0); ro=np.array([(np.log(sol.sol(x+1)[1])-np.log(sol.sol(x-1)[1]))/2 for x in vo])
a=ax[0,0]; a.plot(vs,rate,'k-',lw=2.2,label='double-null PDE ($u=2$)'); a.plot(vo-1,ro,'C3--',lw=1.6,label="Ori shell model, same closure")
vv=np.linspace(30,99,100); a.plot(vv,kap-5/(vv+1),'C0:',lw=1.6,label=r'$\kappa_--5/(v+1)$'); a.axhline(kap,color='gray',lw=.8)
a.text(31,kap+0.004,r'$\kappa_-=0.7956$',fontsize=9); a.set_xlabel('$v$'); a.set_ylabel(r'$d\ln|M|/dv$'); a.set_ylim(0.55,0.82); a.legend(fontsize=8,loc='lower right'); a.set_title('(a) mass-inflation rate on the Cauchy horizon')
# (b) r_inf vs distance below threshold
a=ax[0,1]
for f,c in zip(sorted(glob.glob('threshold_h*.json')),['C0','C1','C2']):
    d=json.load(open(f)); rr=[x for x in d['res'] if x[1] is not None]; ds=np.array([x[0] for x in rr]); ri=np.array([x[1] for x in rr])
    a.loglog(ds,ri,'o-',ms=3,color=c,label='$h=%g$'%d['h'])
dd=np.logspace(-10,-4,10); a.loglog(dd,41*np.sqrt(dd),'k--',lw=1,label=r'$41\,(A_*-A)^{1/2}$')
a.set_xlabel(r'$A_*-A$'); a.set_ylabel(r'$r_\infty$ (Cauchy-horizon radius)'); a.legend(fontsize=8); a.set_title('(b) critical scaling')
# (c) local exponent
a=ax[1,0]
for f,c in zip(sorted(glob.glob('threshold_h*.json')),['C0','C1','C2']):
    d=json.load(open(f)); rr=[x for x in d['res'] if x[1] is not None]; ds=np.array([x[0] for x in rr]); ri=np.array([x[1] for x in rr])
    a.semilogx(ds,np.gradient(np.log(ri),np.log(ds)),'o-',ms=3,color=c,label='$h=%g$'%d['h'])
a.axhline(0.5,color='k',ls='--',lw=1); a.set_xlabel(r'$A_*-A$'); a.set_ylabel(r'$d\ln r_\infty/d\ln(A_*-A)$'); a.set_ylim(0.2,0.6); a.legend(fontsize=8); a.set_title('(c) local critical exponent')
# (d) r_CH(u)
a=ax[1,1]; P=json.load(open('domain_nonlinear.json'))['profile']
for key,c in zip(P,['C0','C1','C3']):
    a.plot(P[key]['u'],P[key]['r'],'o-',ms=3,color=c,label=key.replace('d=','$A_*-A=$'))
a.axhline(bg.rm,color='gray',lw=.8); a.set_ylim(-0.03,1.2); a.text(14,bg.rm+0.03,r'static $r_-$',fontsize=9)
a.set_xlabel('$u$'); a.set_ylabel(r'$r_{CH}(u)$'); a.legend(fontsize=8); a.set_title('(d) Cauchy-horizon radius profile, saturating at large $u$')
plt.tight_layout(); plt.savefig('../../fig_nonlinear.png',dpi=170); print('saved')

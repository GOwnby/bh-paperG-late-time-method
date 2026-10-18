"""E13 figure: (a) single-grid errors of the evolved mass (B=0.03,k=3/2) against the constraint-projected mass, (b) |ln M_cc - ln M_ODE| for the cases available, with grid-subset spread of ln M_cc.
usage: e13_fig.py  (reads gen3_*_v300.json present) -> fig_e13.png"""
import json,sys,glob,numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.argv=['x','gen3_B0.03_k1.5_v300.json','2']
ns={}; exec(open('e13_project.py').read().split("if __name__")[0],ns)
R=ns['R']; arr=ns['arr']; hs=ns['hs']; vq=ns['vq']; run=ns['run']
X=run()
fig,ax=plt.subplots(1,2,figsize=(11,4.2))
v=np.arange(60,141,1.0)
for h,m in zip(hs,arr('M')):
    pass
lnref=np.array([np.log(0.5*X['solC'].sol(x)[0])+np.logaddexp(0,np.log(4)+np.log(0.5+X['I'][int(x-vq[0])])+np.log(X['solC'].sol(x)[1])) for x in v])
Mref=np.exp(lnref)
for h,m in zip(hs,arr('M')):
    mm=np.array([m[int(x-vq[0])] for x in v]); ax[0].semilogy(v,np.abs(mm/Mref-1),label='h=%s'%h)
Mx=np.array([X['M'][int(x-vq[0])] for x in v]); ax[0].semilogy(v,np.abs(Mx/Mref-1),'k--',label='Romberg (5 grids)')
ax[0].set_xlabel('v'); ax[0].set_ylabel(r'$|M_{\rm PDE}/M_{\rm cc}-1|$'); ax[0].set_title('(a) evolved PDE mass, $k=3/2$, $B=0.03$'); ax[0].legend(fontsize=7); ax[0].set_ylim(1e-12,1e3)
cases=[('gen3_B0.03_k1.5_v300.json','k=3/2, B=0.03'),('gen3_B0.03_k0.5_v300.json','k=1/2, B=0.03'),('gen3_B0.003_k1.5_v300.json','k=3/2, B=0.003'),('gen3_B0.003_k0.5_v300.json','k=1/2, B=0.003'),('gen3_B0.03_k2_v300.json','k=2, B=0.03'),('gen3_B0.03_k3_v300.json','k=3, B=0.03')]
import os
for fn,lab in cases:
    if not os.path.exists(fn): continue
    sys.argv=['x',fn,'2']; ns={}; exec(open('e13_project.py').read().split("if __name__")[0],ns)
    Y=ns['run'](); vq_=ns['vq']; vv=np.arange(62,vq_[-1]-2,2.0)
    dl=[]
    for x in vv:
        C=Y['solC'].sol(x); yc=0.5+Y['I'][int(x-vq_[0])]; lc=np.log(C[0]/2)+np.logaddexp(0,np.log(4)+np.log(yc)+np.log(C[1])); dl.append(abs(lc-ns['R'].lnMof(*Y['solA'].sol(x))))
    ax[1].semilogy(vv,np.maximum(dl,1e-16),label=lab)
ax[1].set_xlabel('v'); ax[1].set_ylabel(r'$|\ln M_{\rm cc}-\ln M_{\rm ODE}|$'); ax[1].set_title('(b) constraint-projected PDE mass vs ray ODE'); ax[1].legend(fontsize=7)
plt.tight_layout(); plt.savefig('fig_e13.png',dpi=140)

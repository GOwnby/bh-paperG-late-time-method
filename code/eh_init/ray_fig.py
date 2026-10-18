import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
D={k:np.load('ray_extend_B0.03_k%g.npz'%k) for k in (1.5,0.5)}
col={1.5:'#0072B2',0.5:'#D55E00'}; km=0.784821
fig,ax=plt.subplots(1,3,figsize=(13.2,3.9))
for k,d in D.items():
    kmk=float(d['km']); v=d['v']; vq=d['vq']; Me=d['Mext']; lev=d['Mlev']
    # (a) deviation of ODE from the extrapolated PDE mass, and the PDE level difference
    lnode=d['lnM_power']; sel=(Me>0)&(vq>=61)&(vq<=292)
    vs=vq[sel]; dev=np.abs(np.exp(np.interp(vs,v,lnode)-np.log(Me[sel]))-1)
    ax[0].semilogy(vs,dev,'-',color=col[k],lw=1.4,label=r'$|M_{\rm ODE}/M_{\rm PDE}-1|$, $k=%g$'%k)
    ax[0].semilogy(vs,np.abs(lev[sel]/Me[sel]-1),'--',color=col[k],lw=1.0,label=r'PDE: top two Romberg levels, $k=%g$'%k)
    # (b) ln M - kappa v
    ax[1].plot(v,lnode-kmk*v+(2*k+2)*np.log(v+1),'-',color=col[k],lw=1.6,label=r'$k=%g$'%k)
    for m,ls in (('zero',':'),('const','--')):
        ax[1].plot(v,d['lnM_'+m]-kmk*v+(2*k+2)*np.log(v+1),ls,color=col[k],lw=0.9)
    # (c) q_M
    rate=np.gradient(lnode,v); qM=(kmk-rate)*(v+1)
    ax[2].plot(v[5:],qM[5:],'-',color=col[k],lw=1.6,label=r'$k=%g$'%k); ax[2].axhline(2*k+2,color=col[k],lw=0.8,ls=':')
ax[0].set_xlabel(r'advanced time $v$'); ax[0].set_title('(a) exact ray integration vs extrapolated PDE',fontsize=10); ax[0].set_ylim(1e-10,1e1)
ax[0].legend(fontsize=7,loc='upper left',frameon=False)
ax[1].set_xscale('log'); ax[1].set_xlabel(r'$v$'); ax[1].set_ylabel(r'$\ln M-\kappa_-(\mu_f)v+(2k+2)\ln(v+1)$',fontsize=9)
ax[1].set_title('(b) approach to the Ori law (solid: excess $\\propto v^{-q}$;\n dotted/dashed: excess $=0$ / held)',fontsize=9); ax[1].legend(fontsize=8,frameon=False)
ax[2].set_xscale('log'); ax[2].set_xlabel(r'$v$'); ax[2].set_ylabel(r'$q_M=(\kappa_-(\mu_f)-d\ln M/dv)(v+1)$'); ax[2].set_ylim(2,12)
ax[2].set_title('(c) tail exponent of $M$ (dotted: $2k+2$)',fontsize=10); ax[2].legend(fontsize=8,frameon=False)
for a in ax: a.grid(alpha=0.2); a.tick_params(labelsize=8)
plt.tight_layout(); plt.savefig('fig_ray_mass.png',dpi=170)

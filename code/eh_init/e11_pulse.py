"""E11 (matching factor, compact-pulse test).  usage: MU_F=<mu> python3 e11_pulse.py <json> <v_s> [w_s=2]
PDE response to a Gaussian horizon-flux pulse (area -B at v_s, width w_s) compared with the linear-response kernel of the static
interior with f = 1-2(MU_F+M_N(r))/r.  A compact pulse has all of its mass added at v ~ v_s, so any difference between the PDE and the
kernel built from the FINAL mass mu_f is the second-order (nonlinear) remainder, with no accumulation of mu(v) over a long tail."""
import os,sys,json,numpy as np,warnings
warnings.filterwarnings('ignore')
fn=sys.argv[1]; VS=float(sys.argv[2]); WS=float(sys.argv[3]) if len(sys.argv)>3 else 2.0; sys.argv=[sys.argv[0]]
import transfer_vec_mu as TV, analyze
kp=TV.kp; km=TV.km; rp=TV.rp; rm=TV.rm; T0=(1+(rp/rm)**2)/2
D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq']); B=D['B']; muf=D['mu_f']
dw=0.004; ws=np.arange(dw/2,6.0,dw); T,_=TV.Tvec(ws,ds=0.002)
R=analyze.extrap([np.array(D['data'][h]['PV'][2]) for h in hs])[-1][0]; tau=vq-VS; Kp=R/(-B)
Ka=(1/np.pi)*np.real((np.exp(-1j*np.outer(tau,ws))*(T*np.exp(-(WS*ws/2)**2))).sum(1))*dw
print('%s  B=%g mu_f(PDE)=%.4e  MU_F(kernel)=%s  r-=%.5f kappa-=%.5f T0=%.3f'%(fn,B,muf,os.environ.get('MU_F','0'),rm,km,T0))
out=[]
for t in (10,20,30,40,60,80):
    if t>tau[-1]-1 or t<tau[0]: continue
    i=int(np.where(tau==t)[0][0]); out.append((t,Kp[i]/Ka[i])); print('  tau=%3d K_PDE %.4e K_kernel %.4e ratio-1 %+.4e   (ratio-1)/mu_f %+.3f'%(t,Kp[i],Ka[i],Kp[i]/Ka[i]-1,(Kp[i]/Ka[i]-1)/muf))

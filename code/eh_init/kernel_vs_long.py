# SUPERSEDED -- not used for any number in the paper. This early script compares a kernel measured from the v_s=60 pulse run (continued as
# exp(-kappa_+ tau)) with the v=300 runs; it gives flux ratios of 1.06-1.145, i.e. it does not reproduce the 4e-4 agreement quoted in the paper.
# The comparison of the paper is kernel_analytic.py (derived kernel from the ODE transfer function) -> results_kernel_analytic.txt.
# Compare the kernel convolution (K_inf from the v_s=60 pulse run, continued as exp(-kappa_+ tau) beyond tau=85) with the measured phi_v of the v=300 tail-only runs (B=0.003, U=1).
import json, numpy as np, analyze, warnings
warnings.filterwarnings('ignore')
kp=0.04896874; Bp=0.003
D=json.load(open('gen_B0.003_k1.5_A0_U1_w0.3_v150_P60_2.json')); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq'])
R=analyze.extrap([np.array(D['data'][h]['PV'][2]) for h in hs])[-1][0]; tau=vq-60; K=R/(-Bp); m=tau>=0; t0=tau[m]; K0=K[m]
sel=t0<=85; t0=t0[sel]; K0=K0[sel]; tmax=t0[-1]
Kf=lambda t: np.where(np.asarray(t)>tmax,K0[-1]*np.exp(-kp*(np.asarray(t)-tmax)),np.interp(t,t0,K0,left=K0[0]))
def pred(v,k):
    vp=np.concatenate([np.linspace(0,min(v,50),20001),np.linspace(min(v,50),v,200001)[1:]]) if v>50 else np.linspace(0,v,100001)
    return np.trapezoid(Kf(v-vp)*(-k*Bp*(1+vp)**(-k-1)),vp)
for k,fn in ((0.5,'gen_B0.003_k0.5_A0_U1_w0.3_v300.json'),(1.5,'gen_B0.003_k1.5_A0_U1_w0.3_v300.json')):
    L=json.load(open(fn)); hl=sorted(L['data'],key=float,reverse=True); vl=np.array(L['vq'])
    P=analyze.extrap([np.array(L['data'][h]['PV'][2]) for h in hl])[-1][0]
    print('k=%.1f   v: measured phi_v, predicted, ratio; local exponent p measured / predicted'%k)
    for v in (60,100,140,180,220,260,290):
        i=int(v-vl[0]); meas=P[i]; pr=pred(v,k)
        pm=-(np.log(abs(P[i+4]))-np.log(abs(P[i-4])))/(np.log(vl[i+4]+1)-np.log(vl[i-4]+1))
        pp=-(np.log(abs(pred(v+4,k)))-np.log(abs(pred(v-4,k))))/(np.log(v+5)-np.log(v-3))
        print('  %4d  %.4e  %.4e  %.3f   %.2f / %.2f'%(v,meas,pr,meas/pr,pm,pp))

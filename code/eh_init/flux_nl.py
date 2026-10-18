# B=0.03 tail-only: measured phi_v (U=1, Romberg) vs the linear kernel prediction (B scaled), amplitude ratio and local exponents
import json, numpy as np, analyze, warnings
warnings.filterwarnings('ignore')
tau,Kt=np.load('K_analytic_tau.npy'); kp=0.04896874; R1=0.64423; a_,b_=1.063,0.056
def Kf(t):
    t=np.asarray(t,float); out=np.interp(t,tau,Kt,left=0.0); tail=R1*np.exp(-kp*t)*(1+a_*np.exp(-kp*t)+b_*np.exp(-2*kp*t)); return np.where(t>120,tail,out)
def pred(v,k,B):
    vp=np.concatenate([np.linspace(0,min(v,60),24001),np.linspace(min(v,60),v+12,100001)[1:]]); return np.trapezoid(Kf(v-vp)*(-k*B*(1+vp)**(-k-1)),vp)
for k,fn in ((1.5,'gen_B0.03_k1.5_A0_U1_w0.3_v110.json'),(0.5,'gen_B0.03_k0.5_A0_U1_w0.3_v110.json')):
    D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq']); P=analyze.extrap([np.array(D['data'][h]['PV'][2]) for h in hs])[-1][0]
    print('k=%.1f B=0.03   v  meas/linear-kernel  p_meas  p_lin'%k)
    for v in (40,60,80,100):
        i=int(v-vq[0]); pm=-(np.log(abs(P[i+3]))-np.log(abs(P[i-3])))/(np.log(vq[i+3]+1)-np.log(vq[i-3]+1))
        pl=-(np.log(abs(pred(v+3,k,0.03)))-np.log(abs(pred(v-3,k,0.03))))/(np.log(v+4)-np.log(v-2))
        print('   %4d  %.4f   %.2f  %.2f'%(v,P[i]/pred(v,k,0.03),pm,pl))

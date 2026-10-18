# summary of the streaming 5-grid runs (gen.py JSONs): rate vs lambda, phi_v local exponent, sigma_v excess, phi_v sign changes
import json, numpy as np, analyze, warnings
warnings.filterwarnings('ignore')
files=[('gen_B0.03_k0.5_A0_U1_w0.3_v110.json',.5),('gen_B0.03_k1.5_A0_U1_w0.3_v110.json',1.5),
 ('gen_B0.03_k0.5_A0.02_U1_w0.3_v110.json',.5),('gen_B0.03_k1.5_A0.02_U1_w0.3_v110.json',1.5),('gen_B0.03_k2.5_A0.02_U1_w0.3_v110.json',2.5),
('gen_B0.05_k0.5_A0_U1_w0.3_v110.json',.5),('gen_B0.05_k1.5_A0_U1_w0.3_v110.json',1.5),
 ('gen_B0.03_k1.5_A0.01_U1_w0.3_v110.json',1.5),('gen_B0.03_k1.5_A0.02_U0.7_w0.2_v110.json',1.5),('gen_B0.03_k1.5_A0.02_U1_w0.5_v110.json',1.5),('gen_B0.03_k1.5_A0.03_U0.6_w0.3_v110.json',1.5)]
for fn,k in files:
    analyze.analyze(fn,n=2,t0s=(60,72,84,96,104))
    D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq'])
    try:
        P=analyze.extrap([np.array(D['data'][h]['PV'][2]) for h in hs])[-1][0]
        if np.all(np.isfinite(P)) and np.all(P!=0):
            out=[]
            for v0 in (60,80,100):
                i=int(v0-vq[0]); p=-(np.log(abs(P[i+3]))-np.log(abs(P[i-3])))/(np.log(vq[i+3])-np.log(vq[i-3]))
                out.append('v=%d: |phi_v|=%.2e local exponent %.2f ratio to transported tail %.1f'%(v0,abs(P[i]),p,abs(P[i])/(k*float(D['B'])*(1+v0)**(-k-1)*9.36)))
            print('   phi_v:',' | '.join(out)); print('   sign changes of phi_v at v =',[float(vq[i]) for i in range(len(vq)-1) if P[i]*P[i+1]<0])
    except Exception as e: print('   phi_v analysis failed',e)

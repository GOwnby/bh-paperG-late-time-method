# local exponent of |phi_v| on U=1 from the 3-grid Richardson-extrapolated phi_v (seed5 JSON), window v=70..74
import numpy as np, json
vq=np.arange(40,77.0)
for k in (0.5,1.5,2.5):
    d=json.load(open('seed5_B0.03_k%g_A0.02.json'%k)); hs=['0.05','0.025','0.0125']
    P=[np.array(d[h]['PV'][1]) for h in hs]; E=np.abs((4*P[2]-P[1])/3); P=[np.abs(x) for x in P]
    i=72-40; p=-(np.log(E[i+2])-np.log(E[i-2]))/(np.log(vq[i+2])-np.log(vq[i-2]))
    tail=k*0.03*(1+72)**(-k-1)*9.37
    print('k=%g: phi_v(72) extrapolated %.2e, transported tail %.2e (ratio %.0f), local exponent over v in [70,74]: %.2f ; single-grid h=0.0125: %.2f'%(k,E[i],tail,E[i]/tail,p,-(np.log(P[2][i+2])-np.log(P[2][i-2]))/(np.log(vq[i+2])-np.log(vq[i-2]))))

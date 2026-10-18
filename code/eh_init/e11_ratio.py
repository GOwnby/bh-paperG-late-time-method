"""E11: PDE / kernel flux ratio phi_v(PDE, Romberg)/phi_v(kernel) on the ray U~1 as a function of v (B=0.03 and 0.003, k=1/2, 3/2; gen3 runs to v1=300)."""
import json,sys,numpy as np
import kernel_lib as KL, analyze
print('case        ratio at v = 100  150  200  250  280  290')
for tag in ('B0.03_k1.5','B0.03_k0.5','B0.003_k1.5','B0.003_k0.5','B0.03_k2','B0.03_k3','B0.003_k2','B0.003_k3'):
    import os
    fn='gen3_%s_v300.json'%tag
    if not os.path.exists(fn): continue
    D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq']); k=D['k']; B=D['B']
    P=analyze.extrap([np.array(D['data'][h]['PV'][2]) for h in hs])[-1][0]
    row=[]
    for v in (100,150,200,250,280,290):
        if v>vq[-1]-1: row.append(np.nan); continue
        row.append(P[int(v-vq[0])]/KL.phi_v(float(v),k,B))
    print('%-12s'%tag,' '.join('%.5f'%x for x in row))

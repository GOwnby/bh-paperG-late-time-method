"""E12: PDE / kernel flux ratio phi_v(PDE, Romberg)/phi_v(kernel) on the ray U~1 for the run to v1=450 (B=0.003, k=3/2; four grids h=0.05..0.00625)."""
import json,sys,numpy as np
import kernel_lib as KL, analyze
D=json.load(open('gen3_B0.003_k1.5_v450.json')); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq']); k=D['k']; B=D['B']
arrs=[np.array(D['data'][h]['PV'][2]) for h in hs]
lev=analyze.extrap(arrs)
print('grids',hs,'levels',len(lev),'Uq',D['Uq'][2] if 'Uq' in D else '')
print(' v     ratio(Romberg top)  ratio(2nd level)  ratio(finest raw)  kernel_phi_v')
for v in (60,100,150,200,250,300,350,400,420,440):
    if v>vq[-1]-1: continue
    i=int(v-vq[0]); kv=KL.phi_v(float(v),k,B)
    print('%4d  %.6f  %.6f  %.6f  %.4e'%(v,lev[-1][0][i]/kv,lev[-2][0][i]/kv,arrs[-1][i]/kv,kv))

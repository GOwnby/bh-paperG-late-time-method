"""B=0 (static interior): y=-r_U/W~ must equal 1/2.  Single-grid y and its 3-grid Romberg extrapolation on U=1 (Paper E, Sec. ehdata and Sec. ray).  Needs gen2.py output of
   python3 gen2.py 0 1.5 0 1 0.3 110 0.05 0.025 0.0125"""
import json,numpy as np,analyze,glob
D=json.load(open(glob.glob('gen2_B0_k1.5*v110.json')[0])); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq'])
Y=[-np.array(D['data'][h]['rs'][2])*np.exp(-np.array(D['data'][h]['sg'][2])) for h in hs]; T=analyze.extrap(Y)
print('static y (exact 1/2); h =',hs)
for v in (40,50,60,80,100,108):
    i=int(v-vq[0]); print('v=%3d single grids %s | Romberg 2 grids %.5g, 3 grids %.5g'%(v,' '.join('%.3e'%y[i] for y in Y),T[1][-1][i],T[2][0][i]))

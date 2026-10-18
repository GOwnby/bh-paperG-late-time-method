# local decay rate -dln|phi_v|/dv of the Romberg-extrapolated phi_v on the four rays, and a two-exponential/power diagnostic
import json, numpy as np, analyze, sys, warnings
warnings.filterwarnings('ignore')
def load(fn,n):
    D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq'])
    P=analyze.extrap([np.array(D['data'][h]['PV'][n]) for h in hs])[-1][0]; return vq,P,D
if __name__=='__main__':
    for fn in sys.argv[1:]:
        print(fn)
        for n in range(4):
            vq,P,D=load(fn,n); out=[]
            for v0 in (40,50,60,70,80,90,100):
                i=int(v0-vq[0]); r=-(np.log(abs(P[i+3]))-np.log(abs(P[i-3])))/(vq[i+3]-vq[i-3]); out.append('%.4f'%r)
            sg=[int(vq[i]) for i in range(len(vq)-1) if P[i]*P[i+1]<0]
            print('  U=%.1f  -dln|phi_v|/dv at v=40..100:'%D['Uq'][n],' '.join(out),' |phi_v|(100)=%.2e'%abs(P[int(100-vq[0])]),' nodes',sg)

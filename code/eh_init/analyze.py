import numpy as np, json, sys
def richardson(arrs, order=2):
    """arrs: list of arrays at h, h/2, h/4,...; returns list of successive extrapolation levels T[m] (each a list)"""
    T=[arrs]
    for m in range(1,len(arrs)):
        p=order*(2*m if False else 1)  # placeholder
    return T
def extrap(a):
    # standard Romberg-like for error expansion h^2, h^4, h^6
    T=[list(a)]
    for m in range(1,len(a)):
        f=4.0**m
        prev=T[-1]
        T.append([(f*prev[i+1]-prev[i])/(f-1) for i in range(len(prev)-1)])
    return T
def analyze(fn,n=2,w=4,t0s=(56,60,64,68,72,76,80,84,88,92,96)):
    D=json.load(open(fn)); hs=sorted(D['data'].keys(),key=float,reverse=True); vq=np.array(D['vq'])
    M=[np.array(D['data'][h]['M'][n]) for h in hs]; S=[np.array(D['data'][h]['sV'][n]) for h in hs]; P=[np.array(D['data'][h]['PV'][n]) for h in hs]  # SIGNED: Romberg is linear, abs() is applied only after extrapolation (a series that changes sign on a coarse grid is wrong otherwise)
    TM,TS,TP=extrap(M),extrap(S),extrap(P)
    best=lambda T:T[-1][0]; prev=lambda T:T[-2][1]  # highest-order estimate, and the same-order-1 estimate from finer grids
    Mb,Mp=best(TM),prev(TM); Sb,Pb=np.abs(best(TS)),np.abs(best(TP))
    lam=Sb+2*np.gradient(np.log(Pb),vq); lam2=lam-np.gradient(lam,vq)/lam
    print(fn,'U=%.2f'%D['Uq'][n],'grids',hs,' mu_f=%.4e kappa-(mu_f)=%.5f'%(D['mu_f'],D['km']))
    rows=[]
    for t0 in t0s:
        i=int(t0-vq[0])
        if i<0 or i+w>=len(vq): continue
        if not(Mb[i]>0 and Mb[i+w]>0): print('   [%d,%d] M_ext not positive'%(t0,t0+w)); continue
        rate=np.log(Mb[i+w]/Mb[i])/w; l1=lam[i:i+w+1].mean(); l2=lam2[i:i+w+1].mean()
        dis=abs(Mp[i+w]/Mb[i+w]-1)
        # alternative rate from next-lower-order extrapolant (error indicator)
        rate_p=np.log(Mp[i+w]/Mp[i])/w if (Mp[i]>0 and Mp[i+w]>0) else np.nan
        rows.append((t0,rate,l1,l2,dis,rate_p,Sb[i:i+w+1].mean()))
        print('   [%3d,%3d] rate %.4f  lambda %.4f  lam-lam\'/lam %.4f  diff2 %+.4f  | rate(lower-order extrap) %.4f  extrap.disagr %.1f%%  |sV| %.4f'%(t0,t0+w,rate,l1,l2,rate-l2,rate_p,100*dis,Sb[i:i+w+1].mean()))
    return rows
if __name__=='__main__':
    for fn in sys.argv[1:]:
        analyze(fn,n=2)

import numpy as np, json
vq=np.arange(40,77.0,1.0)
print('Seeded runs (constraint-consistent seed), ray U=1.0; Richardson-extrapolated M, sigma_v, phi_v from h_s=h_v=0.05,0.025,0.0125')
print('columns: window | rate=dlnM/dv | lambda=|sV|+2dln|phi_v|/dv | lambda-lambda\'/lambda | diff1=rate-lambda | diff2=rate-(lambda-lambda\'/lambda) | M extrap. disagreement at window end')
for k in (0.5,1.5,2.5):
    d=json.load(open('seed5_B0.03_k%g_A0.02.json'%k)); hs=['0.05','0.025','0.0125']; n=1
    def ex(key,which):
        a=[np.array(d[h][key][n]) for h in hs]
        return (4*a[2]-a[1])/3 if which==2 else (4*a[1]-a[0])/3
    M2,M1=ex('M',2),ex('M',1); S2=ex('sV',2); P2=np.abs(ex('PV',2))
    lam=np.abs(S2)+2*np.gradient(np.log(P2),vq)
    lamp=np.gradient(lam,vq); lam2=lam-lamp/lam
    print('k=%g'%k)
    for t0 in (56,60,64,68,72):
        i=t0-40; w=4
        rate=np.log(M2[i+w]/M2[i])/w; l1=lam[i:i+w+1].mean(); l2=lam2[i:i+w+1].mean(); pd=abs(M1[i+w]/M2[i+w]-1)
        print('   [%d,%d]  rate %.4f  lam %.4f  lam-lam\'/lam %.4f  diff1 %+.4f  diff2 %+.4f   disagreement %.0f%%'%(t0,t0+w,rate,l1,l2,rate-l1,rate-l2,100*pd))

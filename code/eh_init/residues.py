# Residues of the transfer function at the horizon-regularity poles w_n = -i n kappa_+ :  K(tau) = sum_n R_n e^{-n kappa_+ tau}, R_n = -i Res_{w_n} T
import numpy as np, transfer, sys, json
kp=transfer.kp; out={}
d=2e-4
for n in range(1,7):
    wn=-1j*n*kp
    Tp,_=transfer.T(wn+d,send=None); Tm,_=transfer.T(wn-d,send=None)
    Res=d*(Tp-Tm)/2; Rn=-1j*Res
    out[n]=[Rn.real,Rn.imag]; print('n=%d  R_n=%.5f%+.2ej   (e^{-n kp tau} at tau=60: %.3e)'%(n,Rn.real,Rn.imag,np.exp(-n*kp*60)),flush=True)
json.dump(out,open('residues_mN%g.json'%transfer.mN,'w'))

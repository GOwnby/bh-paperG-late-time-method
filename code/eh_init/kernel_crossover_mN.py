# For the fixed-l Hayward metric (m_N=M, a_N=2M, l=1) tabulate kappa_-, kappa_+, T(0)=(1+(r+/r-)^2)/2 and the intermediate Ori rate kappa_- - 2 kappa_+ ; and the v at which phi_v is within 10% of T0 f(v).
import sys, numpy as np, subprocess, json
rows=[]
for mN in (1.35,1.4,1.435,1.5,1.6,2.0,3.0,5.0):
    out=subprocess.run([sys.executable,'-c','''
import sys; sys.argv=["x","%g"]
import transfer as T
print(T.mN,T.rm,T.rp,T.km,T.kp)'''%mN],capture_output=True,text=True).stdout.split()
    m,rm,rp,km,kp=[float(x) for x in out]; T0=(1+(rp/rm)**2)/2
    rows.append((m,km,kp,km/kp,km-2*kp,T0)); print('M=%.3f  kappa-=%.4f kappa+=%.4f  ratio %.3f  kappa- - 2 kappa+ = %+.4f   T0=%.3f'%rows[-1])

# Vectorised (over omega) RK4 solution for the transfer function T(w)=A(w); r(s) is omega independent. See transfer.py for the equation.
import numpy as np, sys
from scipy.integrate import solve_ivp
import transfer_mu as TR
f=TR.f; kp=TR.kp; km=TR.km; rp=TR.rp; rm=TR.rm
def Tvec(ws,z0=1e-8,ds=0.002,send=None):
    ws=np.asarray(ws,dtype=complex)
    send=send or (45.0*kp/km+np.log(1/z0))
    n=int(np.ceil(send/ds)); s=np.arange(0,2*n+1)*ds/2
    sol=solve_ivp(lambda s,y:[f(y[0])/(2*kp)],[0,s[-1]],[rp-z0],method='DOP853',rtol=1e-13,atol=1e-30,t_eval=s)
    r=sol.y[0]; ff=f(r)
    a=-1j*ws/(rp*(kp-1j*ws)); F=1+a*z0; G=a*z0
    def rhs(F,G,i):
        return G,(1j*ws*G-(ff[i]/r[i])*G+1j*ws*ff[i]*F/(2*kp*r[i]))/kp
    for j in range(n):
        i0,i1,i2=2*j,2*j+1,2*j+2
        k1F,k1G=rhs(F,G,i0)
        k2F,k2G=rhs(F+ds/2*k1F,G+ds/2*k1G,i1)
        k3F,k3G=rhs(F+ds/2*k2F,G+ds/2*k2G,i1)
        k4F,k4G=rhs(F+ds*k3F,G+ds*k3G,i2)
        F=F+ds/6*(k1F+2*k2F+2*k3F+k4F); G=G+ds/6*(k1G+2*k2G+2*k3G+k4G)
    return F-kp*G/(1j*ws), r[-1]-rm
if __name__=='__main__':
    import time; t=time.time()
    A,dr=Tvec([0.001,0.1,0.3,1.0]); print(A,dr,'%.1fs'%(time.time()-t))

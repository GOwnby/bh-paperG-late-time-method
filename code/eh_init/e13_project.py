"""E13: constraint-projected mass.  Both pieces of M=(r/2)(1+4 y rho) are fixed by constraints of the PDE solution, not by evolved first-derivative fields:
   y   = 1/2 + I(v),  I = int_0^s 4 pi r phi_s^2 / W ds'   (u-Raychaudhuri integrated along the slice v=const; positive integrand; Romberg over grids)
   rho from the v-Raychaudhuri constraint along the ray, r'=-rho, rho'=sigma_v rho+4 pi r phi_v^2, driven by Romberg sigma_v, phi_v; started at v0=60 from the extrapolated PDE r, rho (after the infall transient; the Delta v=1 sampling of sigma_v, phi_v is too coarse for v<40).
Compared with (a) the full ray ODE (y evolved from v0=60), (b) the evolved PDE fields.  usage: e13_project.py gen3_...json [n]"""
import json,sys,numpy as np
from scipy.interpolate import CubicSpline
import raylib as R, analyze
fn=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 2
D=json.load(open(fn)); hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq']); k=D['k']; km=D['km']
def arr(name):
    out=[]
    for h in hs:
        d=D['data'][h]
        if name=='Ye': out.append(-np.array(d['rs'][n])*np.exp(-np.array(d['sg'][n])))
        elif name=='rho': out.append(-np.array(d['rv'][n]))
        else: out.append(np.array(d[name][n]))
    return out
def ex(name,sub=None):
    a=arr(name); a=a if sub is None else [a[i] for i in sub]
    T=analyze.extrap(a); return T[-1][0],T[-2][1]
def run(sub=None,v0p=60.,v0c=60.):
    r,_=ex('r',sub); rho,_=ex('rho',sub); Ye,_=ex('Ye',sub); I,Ip=ex('I',sub); sV,_=ex('sV',sub); PV,_=ex('PV',sub); M,Mp=ex('M',sub)
    sVs=CubicSpline(vq,sV); Pvs=CubicSpline(vq,PV)
    # (a) full ray ODE
    i0=int(v0p-vq[0]); solA=R.integrate(v0p,vq[-1]-1,r[i0],rho[i0],np.log(Ye[i0]),lambda v:float(sVs(v)),lambda v:float(Pvs(v)))
    # (c) rho only, started at v=20 from the extrapolated PDE r, rho ; y := 1/2+I
    from scipy.integrate import solve_ivp
    f=lambda v,Y:[-Y[1],float(sVs(v))*Y[1]+4*np.pi*Y[0]*float(Pvs(v))**2]
    ic=int(v0c-vq[0]); solC=solve_ivp(f,[v0c,vq[-1]-1],[r[ic],rho[ic]],method='DOP853',rtol=1e-12,atol=[1e-14,0],dense_output=True)
    return dict(r=r,rho=rho,I=I,Ip=Ip,M=M,Mp=Mp,Ye=Ye,solA=solA,solC=solC)
if __name__=='__main__':
    X=run()
    print(fn,'ray s=%.2f U=%.4f grids %s'%(D['sq'][n],D['Uq'][n],hs))
    print('   v    lnM_ODE(y evolved)  M_cc/M_ODE-1   y_c/y_ODE-1   rho_C/rho_ODE-1  | PDE: M_ext/M_ODE-1  I(next-lvl)/I-1')
    for v in (60,70,84,100,108,120,140,160,180,200,240,280):
        if v>vq[-1]-2: continue
        i=int(v-vq[0]); Z=X['solA'].sol(float(v)); lm=R.lnMof(*Z) if v>=60 else np.nan
        C=X['solC'].sol(float(v)); yc=0.5+X['I'][i]; Mcc=0.5*C[0]*(1+4*yc*C[1])
        if v<60: print('  %4d  (before calibration point)  M_cc=%.4e'%(v,Mcc)); continue
        print('  %4d  %9.3f    %+.2e     %+.2e     %+.2e      |  %+.2e        %.1e'%(v,lm,Mcc/np.exp(lm)-1,yc/np.exp(Z[2])-1,C[1]/Z[1]-1,X['M'][i]/np.exp(lm)-1,abs(X['Ip'][i]/X['I'][i]-1)))

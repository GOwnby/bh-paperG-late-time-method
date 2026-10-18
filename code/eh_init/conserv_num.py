# numerical check of  nabla_a T^a_u = -rho_u - 2 r_u (rho+p_t)/r  (and v) for T^u_u=T^v_v=-rho, T^th_th=T^ph_ph=p_t, ds^2=-e^sigma du dv + r^2 dOmega^2
import numpy as np
r  =lambda u,v: 2+0.3*np.sin(u+0.7*v)+0.1*u*v
sg =lambda u,v: 0.4*np.cos(0.5*u-v)+0.2*u
rho=lambda u,v: 0.5+0.2*np.sin(1.3*u-0.4*v)
pt =lambda u,v: -0.3+0.25*np.cos(0.8*u+v)
def metric(x):
    u,v,th,ph=x; g=np.zeros((4,4)); g[0,1]=g[1,0]=-np.exp(sg(u,v))/2; g[2,2]=r(u,v)**2; g[3,3]=(r(u,v)*np.sin(th))**2; return g
def Tmix(x):
    u,v,th,ph=x; return np.diag([-rho(u,v),-rho(u,v),pt(u,v),pt(u,v)])
def d(f,x,i,h=1e-5):
    e=np.zeros(4); e[i]=h; return (f(x+e)-f(x-e))/(2*h)
def Gamma(x):
    g=metric(x); gi=np.linalg.inv(g); dg=[d(metric,x,i) for i in range(4)]
    G=np.zeros((4,4,4))
    for a in range(4):
        for b in range(4):
            for c in range(4):
                G[a,b,c]=0.5*sum(gi[a,e]*(dg[c][e,b]+dg[b][e,c]-dg[e][b,c]) for e in range(4))
    return G
x0=np.array([0.31,0.17,1.1,0.4]); G=Gamma(x0); T=Tmix(x0)
res=[]
for b in (0,1):
    val=sum(d(lambda y:Tmix(y)[a,b],x0,a) for a in range(4))
    val+=sum(G[a,a,c]*T[c,b]-G[c,a,b]*T[a,c] for a in range(4) for c in range(4))
    res.append(val)
u,v=x0[:2]
pred_u=-d(lambda y:rho(y[0],y[1]),x0,0)-2*d(lambda y:r(y[0],y[1]),x0,0)*(rho(u,v)+pt(u,v))/r(u,v)
pred_v=-d(lambda y:rho(y[0],y[1]),x0,1)-2*d(lambda y:r(y[0],y[1]),x0,1)*(rho(u,v)+pt(u,v))/r(u,v)
print('brute force:',res,' formula:',[pred_u,pred_v])

"""Numerical (finite-difference, 4th order) checks for Paper E, Sec. nlsetup and curv.  [sympy is not available in the workspace.]
 (1) Einstein equations G_ab = 8 pi T_ab for ds^2 = -W du dv + r^2 dOmega^2, W = e^sigma, T = massless scalar + NED monopole
     (T_uu = T_vv = 0, T^u_u = T^v_v = -rho, T^th_th = T^ph_ph = p_t = -rho - r rho'/2, rho = M_N'/(4 pi r^2)).
     G_ab - 8 pi T_ab is affine in the second derivatives (r_uu, r_vv, r_uv, sigma_uv, phi_uv).  We build explicit fields (quadratic jets) whose second derivatives
     are set equal to Eqs. dn1, dn2, dn3 and the two constraints, and verify that ALL components of G - 8 pi T then vanish at the point; then change each second derivative
     by a finite amount and show that the corresponding component no longer vanishes (the check can fail).
 (2) Kretschmann scalar of the 4D metric (full Riemann contraction) against K = R2^2 + 8 H_ab H^ab / r^2 + 4 (2M/r)^2 / r^4 for generic fields."""
import numpy as np, itertools
mN,aN=5.0,10.0
MN=lambda r: mN*r**3/(r**3+aN)
MNp=lambda r: 3*mN*aN*r**2/(r**3+aN)**2
def MNpp(r,e=1e-5): return (MNp(r+e)-MNp(r-e))/(2*e)
def rho(r): return MNp(r)/(4*np.pi*r**2)
def rhop(r,e=1e-5): return (rho(r+e)-rho(r-e))/(2*e)
def pt(r): return -rho(r)-r*rhop(r)/2
H=0.02
def d1(f,x,i,h=H):   # 4th-order central derivative of f(x) (scalar/array valued) wrt x[i]
    e=np.zeros(4); e[i]=h
    return (-f(x+2*e)+8*f(x+e)-8*f(x-e)+f(x-2*e))/(12*h)
def christoffel(gf,x):
    g=gf(x); gi=np.linalg.inv(g); dg=np.array([d1(gf,x,i) for i in range(4)])  # dg[c,a,b]=d_c g_ab
    G=np.zeros((4,4,4))
    for a,b,c in itertools.product(range(4),repeat=3):
        G[a,b,c]=0.5*sum(gi[a,d]*(dg[c,d,b]+dg[b,d,c]-dg[d,b,c]) for d in range(4))
    return G
def riemann(gf,x):
    G0=christoffel(gf,x)
    dG=np.array([d1(lambda y: christoffel(gf,y),x,i) for i in range(4)])  # dG[c,a,b,d]=d_c Gamma^a_bd
    R=np.zeros((4,4,4,4))
    for a,b,c,d in itertools.product(range(4),repeat=4):
        R[a,b,c,d]=dG[c,a,b,d]-dG[d,a,b,c]+sum(G0[a,c,e]*G0[e,b,d]-G0[a,d,e]*G0[e,b,c] for e in range(4))
    return R,G0
# --- fields: quadratic jets about (u,v)=(0,0): f = f0 + fu u + fv v + fuu u^2/2 + fvv v^2/2 + fuv u v
class Jet:
    def __init__(s,f0,fu,fv,fuu,fvv,fuv): s.c=(f0,fu,fv,fuu,fvv,fuv)
    def __call__(s,u,v):
        f0,fu,fv,fuu,fvv,fuv=s.c; return f0+fu*u+fv*v+0.5*fuu*u*u+0.5*fvv*v*v+fuv*u*v
def metric_from(rj,sj):
    def gf(x):
        u,v,th,ph=x; r=rj(u,v); W=np.exp(sj(u,v))
        g=np.zeros((4,4)); g[0,1]=g[1,0]=-W/2; g[2,2]=r*r; g[3,3]=r*r*np.sin(th)**2; return g
    return gf
def einstein(gf,x):
    R,G0=riemann(gf,x); g=gf(x); gi=np.linalg.inv(g)
    Ric=np.einsum('abad->bd',R); Rs=np.einsum('ab,ab',gi,Ric); return Ric-0.5*Rs*g, R
def stress(rj,sj,pj,x,gf):
    u,v,th,ph=x; r=rj(u,v); g=gf(x); gi=np.linalg.inv(g)
    dphi=np.array([ (pj(u+H,v)-pj(u-H,v))/(2*H), (pj(u,v+H)-pj(u,v-H))/(2*H),0,0])   # first derivs of a quadratic jet are exact at 2nd order; fine at the point
    kin=gi@dphi@dphi
    Ts=np.outer(dphi,dphi)-0.5*g*kin
    Tn=np.zeros((4,4)); Tn[0,1]=Tn[1,0]=g[0,1]*(-rho(r)); Tn[2,2]=g[2,2]*pt(r); Tn[3,3]=g[3,3]*pt(r)
    return Ts+Tn
x0=np.array([0.0,0.0,0.7,0.3])
r0,ru,rv=3.0,0.21,-0.34; s0,su,sv=0.1,0.12,-0.25; p0,pu,pv=0.0,0.05,-0.08
W=np.exp(s0); phiuu,phivv=0.03,-0.02; sigma_uu,sigma_vv=0.04,0.02
def build(dr_uv=0.0,ds_uv=0.0,dr_uu=0.0,dr_vv=0.0,dphi_uv=0.0):
    ruu=su*ru-4*np.pi*r0*pu**2+dr_uu; rvv=sv*rv-4*np.pi*r0*pv**2+dr_vv           # constraints r_uu - sigma_u r_u + 4 pi r phi_u^2 = 0
    ruv=-ru*rv/r0-W/(4*r0)*(1-2*MNp(r0))+dr_uv                                          # dn1
    suv=-2*ruv/r0-8*np.pi*pu*pv+W*MNpp(r0)/(2*r0)+ds_uv                                 # dn2
    puv=-(ru*pv+rv*pu)/r0+dphi_uv                                                       # dn3
    return Jet(r0,ru,rv,ruu,rvv,ruv),Jet(s0,su,sv,sigma_uu,sigma_vv,suv),Jet(p0,pu,pv,phiuu,phivv,puv)
def E_of(**kw):
    rj,sj,pj=build(**kw); gf=metric_from(rj,sj); G,_=einstein(gf,x0); return G-8*np.pi*stress(rj,sj,pj,x0,gf), (rj,sj,pj,gf)
names=['uu','vv','uv','thth']; idx=[(0,0),(1,1),(0,1),(2,2)]
def show(tag,E):
    scale=np.abs(E).max()
    print('%-34s'%tag+'  '.join('E_%s=%+.2e'%(n,E[i]) for n,i in zip(names,idx)))
print('(1) G_ab - 8 pi T_ab at a point; fields obey dn1, dn2, dn3 and the constraints (m_N=5, a_N=10, r=3):')
E0,_=E_of(); show('equations imposed',E0)
G0n,_=einstein(E_of()[1][3],x0); print('    size of the individual terms: |G|max = %.3f, |8 pi T|max = %.3f'%(np.abs(G0n).max(),np.abs(8*np.pi*stress(*E_of()[1][:3],x0,E_of()[1][3])).max()))
for kw in ({'dr_uu':0.1},{'dr_vv':0.1},{'dr_uv':0.1},{'ds_uv':0.1}):
    E,_=E_of(**kw); show('perturbed '+list(kw)[0]+'+=0.1',E)
# scalar equation: box phi = g^ab (d_a d_b phi - Gamma^c_ab d_c phi)
def boxphi(dphi_uv):
    rj,sj,pj=build(dphi_uv=dphi_uv)[0:3]; gf=metric_from(rj,sj); gi=np.linalg.inv(gf(x0)); G0=christoffel(gf,x0)
    dp=np.array([pu,pv,0,0]); dd=np.zeros((4,4)); dd[0,0]=phiuu; dd[1,1]=phivv; dd[0,1]=dd[1,0]=pj.c[5]
    return sum(gi[a,b]*(dd[a,b]-sum(G0[c,a,b]*dp[c] for c in range(4))) for a in range(4) for b in range(4))
print('    box phi with phi_uv = dn3: %+.2e ; with phi_uv = dn3 + 0.1: %+.2e'%(boxphi(0.0),boxphi(0.1)))
# mass function: 1 - 2M/r = g^ab r_a r_b
gi=np.linalg.inv(metric_from(*build()[0:2])(x0)); Mm=r0/2*(1+4*ru*rv/W)
print('    1-2M/r = %.10f ; g^{ab} r_a r_b = %.10f'%(1-2*Mm/r0, gi[0,1]*2*ru*rv))
print('\n(2) Kretschmann scalar, generic fields (second derivatives not constrained):')
for rj,sj in ((Jet(3.0,0.21,-0.34,0.15,-0.1,0.07),Jet(0.1,0.12,-0.25,0.04,0.02,-0.06)),(Jet(1.7,-0.4,0.3,-0.2,0.25,0.11),Jet(-0.3,0.2,0.15,-0.05,0.07,0.09))):
    gf=metric_from(rj,sj); R,G0=riemann(gf,x0); g=gf(x0); gi=np.linalg.inv(g)
    Rl=np.einsum('ae,ebcd->abcd',g,R); Ru=np.einsum('bg,ch,di,agh i->abcd'.replace(' ',''),gi,gi,gi,R) if False else np.einsum('bf,cg,dh,afgh->abcd',gi,gi,gi,R)
    Kfull=np.einsum('abcd,abcd',Rl,Ru)
    r_,ru_,rv_=rj.c[0],rj.c[1],rj.c[2]; s_,su_,sv_=sj.c[0],sj.c[1],sj.c[2]; W_=np.exp(s_)
    R2=4*np.exp(-s_)*sj.c[5]; Huu=rj.c[3]-su_*ru_; Hvv=rj.c[4]-sv_*rv_; Huv=rj.c[5]
    HH=(8/W_**2)*(Huu*Hvv+Huv**2); M_=r_/2*(1+4*ru_*rv_/W_)
    Kdec=R2**2+8*HH/r_**2+4*(2*M_/r_)**2/r_**4
    print('    K(full Riemann) = %.8f ; K(decomposition) = %.8f ; relative difference %.1e ; terms: R2^2=%.4f, 8HH/r^2=%.4f, mass term=%.4f'%(Kfull,Kdec,abs(Kfull/Kdec-1),R2**2,8*HH/r_**2,4*(2*M_/r_)**2/r_**4))

"""E13: raw (single-grid) PDE error of rho=-r_v and of the evolved y=-r_s/W against the constraint values, as C(v) h^2.
usage: e13_errconst.py gen3_...json [ray]"""
import json,sys,numpy as np
fn=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 2
exec(open('e13_project.py').read().split("if __name__")[0])
X=run()
print('%s k=%g B=%g ray s=%.1f: C_rho(v)=(rho_h/rho_C-1)/h^2 [h=%s], C_y=(y_e/y_c-1)/h^2, and ratio of C_rho between h=%s and h=%s'%(fn,k,D['B'],D['sq'][n],hs[-2],hs[-2],hs[-1]))
prev=None
for v in (40,50,60,70,80,90,100,110):
    if v>vq[-1]: continue
    i=int(v-vq[0]); rho_ref=X['solC'].sol(float(v))[1] if v>=60 else X['rho'][i]; yc=0.5+X['I'][i]
    h1,h2=hs[-2],hs[-1]
    a1=arr('rho')[-2][i]/rho_ref-1; a2=arr('rho')[-1][i]/rho_ref-1
    b2=arr('Ye')[-1][i]/yc-1
    C=a2/float(h2)**2
    print('  v=%3d  C_rho=%+.3e   (h-ratio of errors %.2f)   C_y=%+.2f   %s'%(v,C,a1/a2 if a2 else np.nan,b2/float(h2)**2,('d lnC/dv=%.3f'%(np.log(abs(C/prev[1]))/(v-prev[0])) if prev else '')))
    prev=(v,C)

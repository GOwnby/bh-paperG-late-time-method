"""E13: LaTeX rows for Table tab:proj from gen3_*_v300.json (ray n=2 and n=0).
usage: python3 e13_table.py [case ...]   (case = B0.03_k0.5, B0.03_k1.5, B0.03_k2, B0.03_k3, B0.003_k0.5, B0.003_k1.5; default all six; prints the rows
and writes them to frag11/rows.tex; output of the full run: results_e13_table.txt)"""
import json,sys,os,numpy as np
cases=[('B0.03_k0.5','$1/2$','0.03'),('B0.03_k1.5','$3/2$','0.03'),('B0.03_k2','$2$','0.03'),('B0.03_k3','$3$','0.03'),('B0.003_k0.5','$1/2$','0.003'),('B0.003_k1.5','$3/2$','0.003')]
VS=(84,140,200,280)
rows=[];info=[];vals=[]
sel=sys.argv[1:]; cases=[c for c in cases if not sel or c[0] in sel]; sys.argv=sys.argv[:1]
def fmt(x):
    if x==0: return '0'
    e=int(np.floor(np.log10(abs(x)))); m=x/10**e
    return '$%+.1f\\times10^{%d}$'%(m,e)
for tag,kk,BB in cases:
    fn='gen3_%s_v300.json'%tag
    if not os.path.exists(fn): continue
    out={}
    for n in (2,0):
        sys.argv=['x',fn,str(n)]; ns={}; exec(open('e13_project.py').read().split("if __name__")[0],ns)
        R=ns['R']; vq=ns['vq']; run=ns['run']; Xf=run(); Xs=run([1,2,3,4]); 
        def lnc(X,v):
            C=X['solC'].sol(float(v)); yc=0.5+X['I'][int(v-vq[0])]; return np.log(C[0]/2)+np.logaddexp(0,np.log(4)+np.log(yc)+np.log(C[1]))
        row=[]
        for v in VS:
            lA=R.lnMof(*Xf['solA'].sol(float(v))); row.append((lnc(Xf,v)-lA,lnc(Xs,v)-lnc(Xf,v),lA))
        allv=range(84,281,2); 
        mx=max(abs(lnc(Xf,v)-R.lnMof(*Xf['solA'].sol(float(v)))) for v in allv)
        mxs=max(abs(lnc(Xs,v)-lnc(Xf,v)) for v in allv)
        Z=Xf['solA'].sol(280.0); lnK=np.log(16)+2*R.lnMof(*Z)-6*np.log(Z[0])
        out[n]=(row,mx,mxs,lnK,ns['D']['Uq'][n])
    r=out[2][0]
    rows.append('%s & %s & '%(kk,BB)+' & '.join(fmt(x[0]) for x in r)+' & %s & %s & %.0f\\\\'%(fmt(out[2][1]),fmt(out[2][2]),out[2][3]))
    info.append((tag,[round(float(x[2]),1) for x in r],fmt(out[0][1]),fmt(out[2][1])))
    vals.append((tag,out))

os.makedirs('frag11',exist_ok=True)
open('frag11/rows.tex','w').write('\n'.join(rows)+'\n')   # LaTeX rows of Table tab:proj
print('\n'.join(rows))
for x in info: print(x)
# numbers for verify.py (VALUE <name> <x>): ln M_cc - ln M_ODE at v = 84, 140, 200, 280 (U ~ 1), their maximum over 84 <= v <= 280, the 4-finest spread, ln M_ODE, ln K bound, U ~ 0.3 maximum
for tag,out in vals:
    row,mx,mxs,lnK,Uq=out[2]
    for (d,sp,lA),v in zip(row,VS): print('VALUE e13_%s_dlnM_v%d %.4e'%(tag,v,d)); print('VALUE e13_%s_lnM_ODE_v%d %.2f'%(tag,v,lA))
    print('VALUE e13_%s_max_dlnM %.4e'%(tag,mx)); print('VALUE e13_%s_spread_4finest %.4e'%(tag,mxs)); print('VALUE e13_%s_lnK_v280 %.1f'%(tag,lnK))
    print('VALUE e13_%s_max_dlnM_U0.3 %.4e'%(tag,out[0][1]))

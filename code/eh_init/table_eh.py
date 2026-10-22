"""Table tab:eh of Paper G: |sigma_v| at v=95 for tail-only data on H+ (v1=110), single grids h=0.05, 0.0125, 0.003125 on the ray U=0.3,
and the five-grid Romberg extrapolation on U=0.3 and U=1; prediction kappa_-(mu_f).  Run from this directory:  python3 table_eh.py
Needs gen_B{0.03,0.05}_k{1.5,0.5}_A0_U1_w0.3_v110.json (see MANIFEST.md).  Prints the rows (and writes them to results_table_eh.txt)."""
import json, numpy as np, analyze
V=95
out=[]
out.append('%-4s %-5s %-12s %-10s %-9s %-9s %-9s %-11s %-11s'%('k','B','mu_f','kappa-(mu_f)','h=0.05','0.0125','0.003125','extrap U=.3','extrap U=1'))
for B,k in ((0.03,1.5),(0.05,1.5),(0.03,0.5),(0.05,0.5)):
    D=json.load(open('gen_B%g_k%g_A0_U1_w0.3_v110.json'%(B,k)))
    hs=sorted(D['data'],key=float,reverse=True); vq=np.array(D['vq']); i=int(np.where(vq==V)[0][0])
    S=[np.array(D['data'][h]['sV']) for h in hs]            # signed, rays 0..3 = U 0.3, 0.6, 1.0, 1.2
    ext=lambda n: abs(analyze.extrap([s[n] for s in S])[-1][0][i])
    single=[abs(S[j][0][i]) for j in (0,2,4)]
    out.append('%-4g %-5g %-12.4e %-10.6f %-9.5f %-9.5f %-9.5f %-11.5f %-11.5f'%(k,B,D['mu_f'],D['km'],*single,ext(0),ext(2)))
print('\n'.join(out)); open('results_table_eh.txt','w').write('\n'.join(out)+'\n')

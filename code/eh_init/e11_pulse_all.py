"""Regenerates results_e11_pulse.txt: runs e11_pulse.py for each pulse data set with the static-hole kernel (MU_F=0) and with the final-hole
kernel (MU_F=mu_f read from the JSON), then tabulates the second-order remainder at tau = 60 after the pulse.
usage: python3 e11_pulse_all.py   (about 1 min; needs the gen_*_P*_2.json files listed in MANIFEST.md)"""
import json, os, re, subprocess, sys
cases=[('gen_B0.0003_k1.5_A0_U1_w0.3_v150_P60_2.json',60),('gen_B0.003_k1.5_A0_U1_w0.3_v110_P3_2.json',3),('gen_B0.003_k1.5_A0_U1_w0.3_v110_P10_2.json',10),
       ('gen_B0.003_k1.5_A0_U1_w0.3_v150_P30_2.json',30),('gen_B0.003_k1.5_A0_U1_w0.3_v150_P60_2.json',60),('gen_B0.0003_k1.5_A0_U1_w0.3_v110_P10_2.json',10),
       ('gen_B0.003_k1.5_A0_U1_w0.3_v150_P10_2.json',10),('gen_B0.0003_k1.5_A0_U1_w0.3_v150_P30_2.json',30)]
READING='''Reading: (i) eps scales as B^2 to 3 digits over two decades in B for every v_s>=10 (so it is intrinsic second order, not truncation or
the accumulation of mu(v), which a compact pulse does not have); (ii) replacing mu=0 by the final-hole kernel removes 35% of the
deviation for v_s>=30 (9.3 -> 6.0 mu_f) and ~93% for v_s=10, i.e. the kernel parameters (r_-, kappa_-, T(0)) of the final hole are the right
leading-order object; (iii) the remaining coefficient eps/mu_f depends on the injection time v_s (0.25 at v_s=10, 5.9 for v_s=30,60) and
on the profile (0.48-0.67 for tails k>=3/2, 3-4 for k=1/2): there is NO universal matching factor; the remainder is the third-order (in phi)
response, bounded by ~6 mu_f in all tested cases. v1=110 vs 150 gives the same result for v_s=10 (checked at B=3e-3), so it is not an
artefact of the ray position.'''
here=os.path.dirname(os.path.abspath(__file__)); out=[]; rows=[]
def run(fn,vs,mu):
    env=dict(os.environ,MU_F=repr(mu)); p=subprocess.run([sys.executable,'e11_pulse.py',fn,str(vs)],cwd=here,env=env,capture_output=True,text=True)
    if p.returncode: sys.exit(p.stderr)
    return p.stdout
for fn,vs in cases:
    D=json.load(open(os.path.join(here,fn))); mu=D['mu_f']; B=D['B']; res=[]
    for m in (0.0,mu):
        t=run(fn,vs,m); out.append(t.rstrip('\n'))
        res.append(float(re.search(r'tau= 60 .*?ratio-1 ([+-][0-9.e+-]+)',t).group(1)))
    rows.append((vs,B,mu,res[0],res[1],int(D['v1'])))
out.append('\n=== SUMMARY (tau=60 after the pulse; Gaussian horizon-flux pulse, width 2, area -B; m_N=5, k irrelevant) ===')
out.append('v_s   B       v1    mu_f(PDE)   ratio-1 (mu=0 kernel)  ratio-1 (final-hole kernel)  eps/mu_f   eps/B^2')
for vs,B,mu,r0,r1,v1 in sorted(rows,key=lambda x:(x[0],x[1],x[5])):
    out.append('%3d   %-6g  %3d   %.2e    %+.2e              %+.2e                    %+.2f      %.0f'%(vs,B,v1,mu,r0,r1,r1/mu,r1/B**2))
out.append('(v_s=3: single B, not checked for linearity -> not used.)')
out.append(READING)
txt='\n'.join(out)+'\n'; print(txt); open(os.path.join(here,'results_e11_pulse.txt'),'w').write(txt)

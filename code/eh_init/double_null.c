// First-order double-null characteristic scheme (relative precision for exponentially small r_u, r_v).
// Fields per grid point: r, sg, ru, rv, su, sv, pu, pv    (arrays [nv][nu], i=u index, j=v index)
// Equations: d_v ru = d_u rv = Fr ; d_v su = d_u sv = Fs ; d_v pu = d_u pv = Fp
//  Fr = -ru rv/r - W/(4r)(1-2MN'(r)) ; Fs = -2 Fr/r - 8 pi pu pv + W MN''(r)/(2r) ; Fp = -(ru pv + rv pu)/r ; W=exp(sg)
#include <math.h>
static double mN,aN;
static inline double MNp(double r){double d=r*r*r+aN; return 3*mN*aN*r*r/(d*d);}
static inline double MNpp(double r){double d=r*r*r+aN; return 6*mN*aN*r*(aN-2*r*r*r)/(d*d*d);}
static inline void F(double r,double sg,double ru,double rv,double pu,double pv,double *fr,double *fs,double *fp){
  double W=exp(sg);
  double a=-ru*rv/r-W/(4*r)*(1-2*MNp(r));
  *fr=a; *fs=-2*a/r-8*M_PI*pu*pv+W*MNpp(r)/(2*r); *fp=-(ru*pv+rv*pu)/r;
}
void evolve2(int nu,int nv,double hu,double hv,double mN_,double aN_,double *R,double *SG,double *RU,double *RV,double *SU,double *SV,double *PU,double *PV,int niter)
{
  mN=mN_; aN=aN_;
  for(int j=0;j<nv-1;j++) for(int i=0;i<nu-1;i++){
    int S=j*nu+i,E=j*nu+i+1,Wn=(j+1)*nu+i,N=(j+1)*nu+i+1;
    double fS[3],fE[3],fW[3],fN[3],fC[3];
    F(R[S],SG[S],RU[S],RV[S],PU[S],PV[S],&fS[0],&fS[1],&fS[2]);
    F(R[E],SG[E],RU[E],RV[E],PU[E],PV[E],&fE[0],&fE[1],&fE[2]);
    F(R[Wn],SG[Wn],RU[Wn],RV[Wn],PU[Wn],PV[Wn],&fW[0],&fW[1],&fW[2]);
    // predictor
    double rN=R[E]+R[Wn]-R[S]+hu*hv*fS[0], sN=SG[E]+SG[Wn]-SG[S]+hu*hv*fS[1];
    double ruN=RU[E]+hv*fE[0], rvN=RV[Wn]+hu*fW[0], suN=SU[E]+hv*fE[1], svN=SV[Wn]+hu*fW[1], puN=PU[E]+hv*fE[2], pvN=PV[Wn]+hu*fW[2];
    for(int it=0;it<niter;it++){
      F(rN,sN,ruN,rvN,puN,pvN,&fN[0],&fN[1],&fN[2]);
      double rc=0.25*(R[S]+R[E]+R[Wn]+rN), sc=0.25*(SG[S]+SG[E]+SG[Wn]+sN);
      double ruc=0.25*(RU[S]+RU[E]+RU[Wn]+ruN), rvc=0.25*(RV[S]+RV[E]+RV[Wn]+rvN);
      double puc=0.25*(PU[S]+PU[E]+PU[Wn]+puN), pvc=0.25*(PV[S]+PV[E]+PV[Wn]+pvN);
      F(rc,sc,ruc,rvc,puc,pvc,&fC[0],&fC[1],&fC[2]);
      rN=R[E]+R[Wn]-R[S]+hu*hv*fC[0]; sN=SG[E]+SG[Wn]-SG[S]+hu*hv*fC[1];
      ruN=RU[E]+0.5*hv*(fE[0]+fN[0]); rvN=RV[Wn]+0.5*hu*(fW[0]+fN[0]);
      suN=SU[E]+0.5*hv*(fE[1]+fN[1]); svN=SV[Wn]+0.5*hu*(fW[1]+fN[1]);
      puN=PU[E]+0.5*hv*(fE[2]+fN[2]); pvN=PV[Wn]+0.5*hu*(fW[2]+fN[2]);
    }
    R[N]=rN;SG[N]=sN;RU[N]=ruN;RV[N]=rvN;SU[N]=suN;SV[N]=svN;PU[N]=puN;PV[N]=pvN;
  }
}

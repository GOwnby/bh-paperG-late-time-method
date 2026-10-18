// Streaming version of evolve2: keeps only two rows; writes selected columns of every row. Same scheme as double_null.c (bitwise-identical arithmetic).
#include <math.h>
#include <stdlib.h>
#include <string.h>
static double mN,aN;
static inline double MNp(double r){double d=r*r*r+aN; return 3*mN*aN*r*r/(d*d);}
static inline double MNpp(double r){double d=r*r*r+aN; return 6*mN*aN*r*(aN-2*r*r*r)/(d*d*d);}
static inline void F(double r,double sg,double ru,double rv,double pu,double pv,double *fr,double *fs,double *fp){
  double W=exp(sg);
  double a=-ru*rv/r-W/(4*r)*(1-2*MNp(r));
  *fr=a; *fs=-2*a/r-8*M_PI*pu*pv+W*MNpp(r)/(2*r); *fp=-(ru*pv+rv*pu)/r;
}
// row0: [8][nu] ; col0: [8][nv] ; out: [ncol][nv][8]
// stream2: additionally outI[c*nv+j] = int_0^{s_c} 4 pi r phi_s^2 / W ds (trapezoid along row j) : the u-Raychaudhuri constraint integral y_c-1/2, y=-r_s/W
static inline double gI(double r,double sg,double pu){return 4*M_PI*r*pu*pu*exp(-sg);}
void evolve_stream2(int nu,int nv,double hu,double hv,double mN_,double aN_,const double *row0,const double *col0,int ncol,const int *cols,double *out,double *outI,int niter)
{
  mN=mN_; aN=aN_;
  double *buf=(double*)malloc(sizeof(double)*8*nu*2);
  double *P[8],*C[8]; for(int f=0;f<8;f++){P[f]=buf+f*nu; C[f]=buf+(8+f)*nu; memcpy(P[f],row0+(size_t)f*nu,sizeof(double)*nu);}
  for(int c=0;c<ncol;c++) for(int f=0;f<8;f++) out[((size_t)c*nv+0)*8+f]=P[f][cols[c]];
  double *cum=(double*)malloc(sizeof(double)*nu);
  { cum[0]=0; for(int i=0;i<nu-1;i++) cum[i+1]=cum[i]+0.5*hu*(gI(P[0][i],P[1][i],P[6][i])+gI(P[0][i+1],P[1][i+1],P[6][i+1])); }
  for(int c=0;c<ncol;c++) outI[(size_t)c*nv+0]=cum[cols[c]];
  for(int j=0;j<nv-1;j++){
    for(int f=0;f<8;f++) C[f][0]=col0[(size_t)f*nv+(j+1)];
    for(int i=0;i<nu-1;i++){
      double fS[3],fE[3],fW[3],fN[3],fC[3];
      F(P[0][i],P[1][i],P[2][i],P[3][i],P[6][i],P[7][i],&fS[0],&fS[1],&fS[2]);
      F(P[0][i+1],P[1][i+1],P[2][i+1],P[3][i+1],P[6][i+1],P[7][i+1],&fE[0],&fE[1],&fE[2]);
      F(C[0][i],C[1][i],C[2][i],C[3][i],C[6][i],C[7][i],&fW[0],&fW[1],&fW[2]);
      double Rs=P[0][i],Re=P[0][i+1],Rw=C[0][i],Ss=P[1][i],Se=P[1][i+1],Sw=C[1][i];
      double rN=Re+Rw-Rs+hu*hv*fS[0], sN=Se+Sw-Ss+hu*hv*fS[1];
      double ruN=P[2][i+1]+hv*fE[0], rvN=C[3][i]+hu*fW[0], suN=P[4][i+1]+hv*fE[1], svN=C[5][i]+hu*fW[1], puN=P[6][i+1]+hv*fE[2], pvN=C[7][i]+hu*fW[2];
      for(int it=0;it<niter;it++){
        F(rN,sN,ruN,rvN,puN,pvN,&fN[0],&fN[1],&fN[2]);
        double rc=0.25*(Rs+Re+Rw+rN), sc=0.25*(Ss+Se+Sw+sN);
        double ruc=0.25*(P[2][i]+P[2][i+1]+C[2][i]+ruN), rvc=0.25*(P[3][i]+P[3][i+1]+C[3][i]+rvN);
        double puc=0.25*(P[6][i]+P[6][i+1]+C[6][i]+puN), pvc=0.25*(P[7][i]+P[7][i+1]+C[7][i]+pvN);
        F(rc,sc,ruc,rvc,puc,pvc,&fC[0],&fC[1],&fC[2]);
        rN=Re+Rw-Rs+hu*hv*fC[0]; sN=Se+Sw-Ss+hu*hv*fC[1];
        ruN=P[2][i+1]+0.5*hv*(fE[0]+fN[0]); rvN=C[3][i]+0.5*hu*(fW[0]+fN[0]);
        suN=P[4][i+1]+0.5*hv*(fE[1]+fN[1]); svN=C[5][i]+0.5*hu*(fW[1]+fN[1]);
        puN=P[6][i+1]+0.5*hv*(fE[2]+fN[2]); pvN=C[7][i]+0.5*hu*(fW[2]+fN[2]);
      }
      C[0][i+1]=rN;C[1][i+1]=sN;C[2][i+1]=ruN;C[3][i+1]=rvN;C[4][i+1]=suN;C[5][i+1]=svN;C[6][i+1]=puN;C[7][i+1]=pvN;
    }
    for(int c=0;c<ncol;c++) for(int f=0;f<8;f++) out[((size_t)c*nv+(j+1))*8+f]=C[f][cols[c]];
    cum[0]=0; for(int i=0;i<nu-1;i++) cum[i+1]=cum[i]+0.5*hu*(gI(C[0][i],C[1][i],C[6][i])+gI(C[0][i+1],C[1][i+1],C[6][i+1]));
    for(int c=0;c<ncol;c++) outI[(size_t)c*nv+(j+1)]=cum[cols[c]];
    for(int f=0;f<8;f++){double *t=P[f];P[f]=C[f];C[f]=t;}
  }
  free(buf); free(cum);
}

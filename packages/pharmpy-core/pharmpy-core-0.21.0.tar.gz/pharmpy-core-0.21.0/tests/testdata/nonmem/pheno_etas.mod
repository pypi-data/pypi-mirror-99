;; 1. Based on: 5
; $SIZE  MOD=23
$PROBLEM    PHENOBARB SIMPLE MODEL
$DATA      'pheno.dta' IGNORE=@
$INPUT      ID TIME AMT WGT APGR DV FA1 FA2
$SUBROUTINE ADVAN1 TRANS2
$PK


IF(AMT.GT.0) BTIME=TIME
TAD=TIME-BTIME
      TVCL=THETA(1)*WGT
      TVV=THETA(2)*WGT
IF(APGR.LT.5) TVV=TVV*(1+THETA(3))
      CL=TVCL*EXP(ETA(1))
      V=TVV*EXP(ETA(2))
      S1=V
$ERROR

      W=F
      Y=F+W*EPS(1)

      IPRED=F         ;  individual-specific prediction
      IRES=DV-IPRED   ;  individual-specific residual
      IWRES=IRES/W    ;  individual-specific weighted residual

$THETA  (0,0.00469307) ; CL
$THETA  (0,1.00916) ; V
$THETA  (-.99,.1)
$OMEGA  DIAGONAL(2)
 0.0309626  ;       IVCL
 0.031128  ;        IVV
$SIGMA  0.0130865
$ESTIMATION METHOD=1 INTERACTION PRINT=1
$COVARIANCE UNCONDITIONAL
$TABLE      ID TIME AMT WGT APGR IPRED PRED TAD CWRES NPDE NOAPPEND
            NOPRINT ONEHEADER FILE=pheno_real.tab
$ETAS FILE=pheno_real.phi

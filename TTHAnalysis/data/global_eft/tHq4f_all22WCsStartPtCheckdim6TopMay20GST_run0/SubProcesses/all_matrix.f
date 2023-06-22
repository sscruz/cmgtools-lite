
C     PY ((21, -2), (-6, -1, 5, 25)) : (21, -2, -6, 5, -1, 25) # M4_
C     PY ((21, -3), (-5, -4, 6, 25)) : (21, -3, 6, -5, -4, 25) # M1_
C     PY ((4, -3), (-5, 6, 21, 25)) : (4, -3, 6, -5, 21, 25) # M2_
C     PY ((21, 1), (-6, 2, 5, 25)) : (21, 1, -6, 5, 2, 25) # M3_
C     PY ((2, -1), (-5, 6, 21, 25)) : (2, -1, 6, -5, 21, 25) # M2_
C     PY ((3, -4), (-6, 5, 21, 25)) : (3, -4, -6, 5, 21, 25) # M5_
C     PY ((21, 2), (-5, 1, 6, 25)) : (21, 2, 6, -5, 1, 25) # M0_
C     PY ((21, -1), (-5, -2, 6, 25)) : (21, -1, 6, -5, -2, 25) # M1_
C     PY ((21, 4), (-5, 3, 6, 25)) : (21, 4, 6, -5, 3, 25) # M0_
C     PY ((21, 3), (-6, 4, 5, 25)) : (21, 3, -6, 5, 4, 25) # M3_
C     PY ((21, -4), (-6, -3, 5, 25)) : (21, -4, -6, 5, -3, 25) # M4_
C     PY ((1, -2), (-6, 5, 21, 25)) : (1, -2, -6, 5, 21, 25) # M5_
      SUBROUTINE SMATRIXHEL(PDGS, NPDG, P, ALPHAS, SCALE2, NHEL, ANS)
      IMPLICIT NONE

CF2PY double precision, intent(in), dimension(0:3,npdg) :: p
CF2PY integer, intent(in), dimension(npdg) :: pdgs
CF2PY integer, intent(in) :: npdg
CF2PY double precision, intent(out) :: ANS
CF2PY double precision, intent(in) :: ALPHAS
CF2PY double precision, intent(in) :: SCALE2
      INTEGER PDGS(*)
      INTEGER NPDG, NHEL
      DOUBLE PRECISION P(*)
      DOUBLE PRECISION ANS, ALPHAS, PI,SCALE2
      INCLUDE 'coupl.inc'

      PI = 3.141592653589793D0
      G = 2* DSQRT(ALPHAS*PI)
      CALL UPDATE_AS_PARAM()
      IF (SCALE2.NE.0D0) STOP 1

      IF(21.EQ.PDGS(1).AND.-2.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.-1.EQ.PDGS(5).AND.25.EQ.PDGS(6)) THEN  ! 5
        CALL M4_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-3.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.-4.EQ.PDGS(5).AND.25.EQ.PDGS(6)) THEN  ! 5
        CALL M1_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(4.EQ.PDGS(1).AND.-3.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.25.EQ.PDGS(6)) THEN  ! 5
        CALL M2_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.1.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.2.EQ.PDGS(5).AND.25.EQ.PDGS(6)) THEN  ! 5
        CALL M3_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(2.EQ.PDGS(1).AND.-1.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.25.EQ.PDGS(6)) THEN  ! 5
        CALL M2_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(3.EQ.PDGS(1).AND.-4.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.25.EQ.PDGS(6)) THEN  ! 5
        CALL M5_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.2.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.1.EQ.PDGS(5).AND.25.EQ.PDGS(6)) THEN  ! 5
        CALL M0_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-1.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.-2.EQ.PDGS(5).AND.25.EQ.PDGS(6)) THEN  ! 5
        CALL M1_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.4.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.3.EQ.PDGS(5).AND.25.EQ.PDGS(6)) THEN  ! 5
        CALL M0_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.3.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.4.EQ.PDGS(5).AND.25.EQ.PDGS(6)) THEN  ! 5
        CALL M3_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-4.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.-3.EQ.PDGS(5).AND.25.EQ.PDGS(6)) THEN  ! 5
        CALL M4_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(1.EQ.PDGS(1).AND.-2.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.25.EQ.PDGS(6)) THEN  ! 5
        CALL M5_SMATRIXHEL(P, NHEL, ANS)
      ENDIF

      RETURN
      END

      SUBROUTINE INITIALISE(PATH)
C     ROUTINE FOR F2PY to read the benchmark point.
      IMPLICIT NONE
      CHARACTER*512 PATH
CF2PY INTENT(IN) :: PATH
      CALL SETPARA(PATH)  !first call to setup the paramaters
      RETURN
      END

      SUBROUTINE GET_PDG_ORDER(PDG)
      IMPLICIT NONE
CF2PY INTEGER, intent(out) :: PDG(12,6)
      INTEGER PDG(12,6), PDGS(12,6)
      DATA PDGS/ 21,21,4,21,2,3,21,21,21,21,21,1,-2,-3,-3,1,-1,-4,2,-1
     $ ,4,3,-4,-2,-6,6,6,-6,6,-6,6,6,6,-6,-6,-6,5,-5,-5,5,-5,5,-5,-5,
     $ -5,5,5,5,-1,-4,21,2,21,21,1,-2,3,4,-3,21,25,25,25,25,25,25,25
     $ ,25,25,25,25,25 /
      PDG = PDGS
      RETURN
      END

      SUBROUTINE GET_PREFIX(PREFIX)
      IMPLICIT NONE
CF2PY CHARACTER*20, intent(out) :: PREFIX(12)
      CHARACTER*20 PREFIX(12),PREF(12)
      DATA PREF / 'M4_','M1_','M2_','M3_','M2_','M5_','M0_','M1_'
     $ ,'M0_','M3_','M4_','M5_'/
      PREFIX = PREF
      RETURN
      END




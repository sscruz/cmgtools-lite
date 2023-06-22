
C     PY ((3, -3), (-6, -6, 6, 6)) : (3, -3, 6, -6, 6, -6) # M4_
C     PY ((1, -1), (-6, -6, 6, 6)) : (1, -1, 6, -6, 6, -6) # M4_
C     PY ((4, -4), (-6, -6, 6, 6)) : (4, -4, 6, -6, 6, -6) # M3_
C     PY ((21, 21), (-6, -6, 6, 6)) : (21, 21, 6, -6, 6, -6) # M1_
C     PY ((5, -5), (-6, -6, 6, 6)) : (5, -5, 6, -6, 6, -6) # M0_
C     PY ((2, -2), (-6, -6, 6, 6)) : (2, -2, 6, -6, 6, -6) # M2_
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

      IF(3.EQ.PDGS(1).AND.-3.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -6.EQ.PDGS(4).AND.6.EQ.PDGS(5).AND.-6.EQ.PDGS(6)) THEN  ! 5
        CALL M4_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(1.EQ.PDGS(1).AND.-1.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -6.EQ.PDGS(4).AND.6.EQ.PDGS(5).AND.-6.EQ.PDGS(6)) THEN  ! 5
        CALL M4_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(4.EQ.PDGS(1).AND.-4.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -6.EQ.PDGS(4).AND.6.EQ.PDGS(5).AND.-6.EQ.PDGS(6)) THEN  ! 5
        CALL M3_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.21.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -6.EQ.PDGS(4).AND.6.EQ.PDGS(5).AND.-6.EQ.PDGS(6)) THEN  ! 5
        CALL M1_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(5.EQ.PDGS(1).AND.-5.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -6.EQ.PDGS(4).AND.6.EQ.PDGS(5).AND.-6.EQ.PDGS(6)) THEN  ! 5
        CALL M0_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(2.EQ.PDGS(1).AND.-2.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -6.EQ.PDGS(4).AND.6.EQ.PDGS(5).AND.-6.EQ.PDGS(6)) THEN  ! 5
        CALL M2_SMATRIXHEL(P, NHEL, ANS)
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
CF2PY INTEGER, intent(out) :: PDG(6,6)
      INTEGER PDG(6,6), PDGS(6,6)
      DATA PDGS/ 3,1,4,21,5,2,-3,-1,-4,21,-5,-2,6,6,6,6,6,6,-6,-6,-6,
     $ -6,-6,-6,6,6,6,6,6,6,-6,-6,-6,-6,-6,-6 /
      PDG = PDGS
      RETURN
      END

      SUBROUTINE GET_PREFIX(PREFIX)
      IMPLICIT NONE
CF2PY CHARACTER*20, intent(out) :: PREFIX(6)
      CHARACTER*20 PREFIX(6),PREF(6)
      DATA PREF / 'M4_','M4_','M3_','M1_','M0_','M2_'/
      PREFIX = PREF
      RETURN
      END




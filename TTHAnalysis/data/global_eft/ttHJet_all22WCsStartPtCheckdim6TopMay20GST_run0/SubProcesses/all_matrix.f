
C     PY ((21, -3), (-6, -3, 6, 25)) : (21, -3, 6, -6, 25, -3) # M9_
C     PY ((1, -1), (-6, 6, 21, 25)) : (1, -1, 6, -6, 25, 21) # M12_
C     PY ((21, 21), (-6, 6, 21, 25)) : (21, 21, 6, -6, 25, 21) # M3_
C     PY ((2, -2), (-6, 6, 25)) : (2, -2, 6, -6, 25) # M15_
C     PY ((3, -3), (-6, 6, 25)) : (3, -3, 6, -6, 25) # M17_
C     PY ((2, -2), (-6, 6, 21, 25)) : (2, -2, 6, -6, 25, 21) # M10_
C     PY ((21, 1), (-6, 1, 6, 25)) : (21, 1, 6, -6, 25, 1) # M6_
C     PY ((1, -1), (-6, 6, 25)) : (1, -1, 6, -6, 25) # M17_
C     PY ((21, 3), (-6, 3, 6, 25)) : (21, 3, 6, -6, 25, 3) # M6_
C     PY ((4, -4), (-6, 6, 25)) : (4, -4, 6, -6, 25) # M16_
C     PY ((21, 21), (-6, 6, 25)) : (21, 21, 6, -6, 25) # M14_
C     PY ((21, -1), (-6, -1, 6, 25)) : (21, -1, 6, -6, 25, -1) # M9_
C     PY ((21, 2), (-6, 2, 6, 25)) : (21, 2, 6, -6, 25, 2) # M4_
C     PY ((21, -4), (-6, -4, 6, 25)) : (21, -4, 6, -6, 25, -4) # M8_
C     PY ((21, -5), (-6, -5, 6, 25)) : (21, -5, 6, -6, 25, -5) # M1_
C     PY ((21, -2), (-6, -2, 6, 25)) : (21, -2, 6, -6, 25, -2) # M7_
C     PY ((21, 4), (-6, 4, 6, 25)) : (21, 4, 6, -6, 25, 4) # M5_
C     PY ((3, -3), (-6, 6, 21, 25)) : (3, -3, 6, -6, 25, 21) # M12_
C     PY ((5, -5), (-6, 6, 21, 25)) : (5, -5, 6, -6, 25, 21) # M2_
C     PY ((21, 5), (-6, 5, 6, 25)) : (21, 5, 6, -6, 25, 5) # M0_
C     PY ((5, -5), (-6, 6, 25)) : (5, -5, 6, -6, 25) # M13_
C     PY ((4, -4), (-6, 6, 21, 25)) : (4, -4, 6, -6, 25, 21) # M11_
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
      IF (NPDG.EQ.5)THEN
        IF(2.EQ.PDGS(1).AND.-2.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5)) THEN  ! 4
          CALL M15_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(3.EQ.PDGS(1).AND.-3.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5)) THEN  ! 4
          CALL M17_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(1.EQ.PDGS(1).AND.-1.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5)) THEN  ! 4
          CALL M17_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(4.EQ.PDGS(1).AND.-4.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5)) THEN  ! 4
          CALL M16_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(21.EQ.PDGS(1).AND.21.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5)) THEN  ! 4
          CALL M14_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(5.EQ.PDGS(1).AND.-5.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5)) THEN  ! 4
          CALL M13_SMATRIXHEL(P, NHEL, ANS)
        ENDIF
      ELSE IF (NPDG.EQ.6)THEN
        IF(21.EQ.PDGS(1).AND.-3.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.-3.EQ.PDGS(6)) THEN  ! 5
          CALL M9_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(1.EQ.PDGS(1).AND.-1.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.21.EQ.PDGS(6)) THEN  ! 5
          CALL M12_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(21.EQ.PDGS(1).AND.21.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.21.EQ.PDGS(6)) THEN  ! 5
          CALL M3_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(2.EQ.PDGS(1).AND.-2.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.21.EQ.PDGS(6)) THEN  ! 5
          CALL M10_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(21.EQ.PDGS(1).AND.1.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.1.EQ.PDGS(6)) THEN  ! 5
          CALL M6_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(21.EQ.PDGS(1).AND.3.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.3.EQ.PDGS(6)) THEN  ! 5
          CALL M6_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(21.EQ.PDGS(1).AND.-1.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.-1.EQ.PDGS(6)) THEN  ! 5
          CALL M9_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(21.EQ.PDGS(1).AND.2.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.2.EQ.PDGS(6)) THEN  ! 5
          CALL M4_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(21.EQ.PDGS(1).AND.-4.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.-4.EQ.PDGS(6)) THEN  ! 5
          CALL M8_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(21.EQ.PDGS(1).AND.-5.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.-5.EQ.PDGS(6)) THEN  ! 5
          CALL M1_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(21.EQ.PDGS(1).AND.-2.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.-2.EQ.PDGS(6)) THEN  ! 5
          CALL M7_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(21.EQ.PDGS(1).AND.4.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.4.EQ.PDGS(6)) THEN  ! 5
          CALL M5_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(3.EQ.PDGS(1).AND.-3.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.21.EQ.PDGS(6)) THEN  ! 5
          CALL M12_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(5.EQ.PDGS(1).AND.-5.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.21.EQ.PDGS(6)) THEN  ! 5
          CALL M2_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(21.EQ.PDGS(1).AND.5.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.5.EQ.PDGS(6)) THEN  ! 5
          CALL M0_SMATRIXHEL(P, NHEL, ANS)
        ELSE IF(4.EQ.PDGS(1).AND.-4.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $   -6.EQ.PDGS(4).AND.25.EQ.PDGS(5).AND.21.EQ.PDGS(6)) THEN  ! 5
          CALL M11_SMATRIXHEL(P, NHEL, ANS)
        ENDIF
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
CF2PY INTEGER, intent(out) :: PDG(22,6)
      INTEGER PDG(22,6), PDGS(22,6)
      DATA PDGS/ 21,1,21,2,3,2,21,1,21,4,21,21,21,21,21,21,21,3,5,21,5
     $ ,4,-3,-1,21,-2,-3,-2,1,-1,3,-4,21,-1,2,-4,-5,-2,4,-3,-5,5,-5,-4
     $ ,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,-6,-6,-6,-6,-6,-6,
     $ -6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,-6,25,25,25,25,25
     $ ,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,-3,21,21,0
     $ ,0,21,1,0,3,0,0,-1,2,-4,-5,-2,4,21,21,5,0,21 /
      PDG = PDGS
      RETURN
      END

      SUBROUTINE GET_PREFIX(PREFIX)
      IMPLICIT NONE
CF2PY CHARACTER*20, intent(out) :: PREFIX(22)
      CHARACTER*20 PREFIX(22),PREF(22)
      DATA PREF / 'M9_','M12_','M3_','M15_','M17_','M10_','M6_','M17_'
     $ ,'M6_','M16_','M14_','M9_','M4_','M8_','M1_','M7_','M5_','M12_'
     $ ,'M2_','M0_','M13_','M11_'/
      PREFIX = PREF
      RETURN
      END




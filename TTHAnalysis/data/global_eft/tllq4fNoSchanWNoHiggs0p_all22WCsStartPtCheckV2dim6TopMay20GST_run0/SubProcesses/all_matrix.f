
C     PY ((21, -2), (-15, -6, -1, 5, 15)) : (21, -2, -6, 5, -1, -15,
C      15) # M11_
C     PY ((1, -2), (-11, -6, 5, 11, 21)) : (1, -2, -6, 5, 21, -11, 11)
C      # M14_
C     PY ((21, -3), (-15, -5, -4, 6, 15)) : (21, -3, 6, -5, -4, -15,
C      15) # M5_
C     PY ((21, -2), (-13, -6, -1, 5, 13)) : (21, -2, -6, 5, -1, -13,
C      13) # M9_
C     PY ((21, 1), (-11, -6, 2, 5, 11)) : (21, 1, -6, 5, 2, -11, 11) #
C      M6_
C     PY ((21, -3), (-11, -5, -4, 6, 11)) : (21, -3, 6, -5, -4, -11,
C      11) # M2_
C     PY ((21, -2), (-11, -6, -1, 5, 11)) : (21, -2, -6, 5, -1, -11,
C      11) # M8_
C     PY ((21, 2), (-13, -5, 1, 6, 13)) : (21, 2, 6, -5, 1, -13, 13) #
C      M1_
C     PY ((3, -4), (-15, -6, 5, 15, 21)) : (3, -4, -6, 5, 21, -15, 15)
C      # M15_
C     PY ((21, -3), (-13, -5, -4, 6, 13)) : (21, -3, 6, -5, -4, -13,
C      13) # M3_
C     PY ((21, -1), (-15, -5, -2, 6, 15)) : (21, -1, 6, -5, -2, -15,
C      15) # M5_
C     PY ((21, 3), (-15, -6, 4, 5, 15)) : (21, 3, -6, 5, 4, -15, 15) #
C      M10_
C     PY ((21, -4), (-13, -6, -3, 5, 13)) : (21, -4, -6, 5, -3, -13,
C      13) # M9_
C     PY ((4, -3), (-11, -5, 6, 11, 21)) : (4, -3, 6, -5, 21, -11, 11)
C      # M12_
C     PY ((2, -1), (-13, -5, 6, 13, 21)) : (2, -1, 6, -5, 21, -13, 13)
C      # M12_
C     PY ((21, -4), (-15, -6, -3, 5, 15)) : (21, -4, -6, 5, -3, -15,
C      15) # M11_
C     PY ((4, -3), (-13, -5, 6, 13, 21)) : (4, -3, 6, -5, 21, -13, 13)
C      # M12_
C     PY ((4, -3), (-15, -5, 6, 15, 21)) : (4, -3, 6, -5, 21, -15, 15)
C      # M13_
C     PY ((21, 4), (-11, -5, 3, 6, 11)) : (21, 4, 6, -5, 3, -11, 11) #
C      M0_
C     PY ((3, -4), (-11, -6, 5, 11, 21)) : (3, -4, -6, 5, 21, -11, 11)
C      # M14_
C     PY ((21, 1), (-13, -6, 2, 5, 13)) : (21, 1, -6, 5, 2, -13, 13) #
C      M7_
C     PY ((21, 2), (-15, -5, 1, 6, 15)) : (21, 2, 6, -5, 1, -15, 15) #
C      M4_
C     PY ((3, -4), (-13, -6, 5, 13, 21)) : (3, -4, -6, 5, 21, -13, 13)
C      # M14_
C     PY ((1, -2), (-15, -6, 5, 15, 21)) : (1, -2, -6, 5, 21, -15, 15)
C      # M15_
C     PY ((21, 4), (-13, -5, 3, 6, 13)) : (21, 4, 6, -5, 3, -13, 13) #
C      M1_
C     PY ((21, 1), (-15, -6, 2, 5, 15)) : (21, 1, -6, 5, 2, -15, 15) #
C      M10_
C     PY ((2, -1), (-15, -5, 6, 15, 21)) : (2, -1, 6, -5, 21, -15, 15)
C      # M13_
C     PY ((21, 3), (-11, -6, 4, 5, 11)) : (21, 3, -6, 5, 4, -11, 11) #
C      M6_
C     PY ((21, 4), (-15, -5, 3, 6, 15)) : (21, 4, 6, -5, 3, -15, 15) #
C      M4_
C     PY ((21, 2), (-11, -5, 1, 6, 11)) : (21, 2, 6, -5, 1, -11, 11) #
C      M0_
C     PY ((1, -2), (-13, -6, 5, 13, 21)) : (1, -2, -6, 5, 21, -13, 13)
C      # M14_
C     PY ((21, -1), (-11, -5, -2, 6, 11)) : (21, -1, 6, -5, -2, -11,
C      11) # M2_
C     PY ((2, -1), (-11, -5, 6, 11, 21)) : (2, -1, 6, -5, 21, -11, 11)
C      # M12_
C     PY ((21, 3), (-13, -6, 4, 5, 13)) : (21, 3, -6, 5, 4, -13, 13) #
C      M7_
C     PY ((21, -4), (-11, -6, -3, 5, 11)) : (21, -4, -6, 5, -3, -11,
C      11) # M8_
C     PY ((21, -1), (-13, -5, -2, 6, 13)) : (21, -1, 6, -5, -2, -13,
C      13) # M3_
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
     $ .AND.5.EQ.PDGS(4).AND.-1.EQ.PDGS(5).AND.-15.EQ.PDGS(6)
     $ .AND.15.EQ.PDGS(7)) THEN  ! 6
        CALL M11_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(1.EQ.PDGS(1).AND.-2.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.-11.EQ.PDGS(6)
     $ .AND.11.EQ.PDGS(7)) THEN  ! 6
        CALL M14_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-3.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.-4.EQ.PDGS(5).AND.-15.EQ.PDGS(6)
     $ .AND.15.EQ.PDGS(7)) THEN  ! 6
        CALL M5_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-2.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.-1.EQ.PDGS(5).AND.-13.EQ.PDGS(6)
     $ .AND.13.EQ.PDGS(7)) THEN  ! 6
        CALL M9_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.1.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.2.EQ.PDGS(5).AND.-11.EQ.PDGS(6)
     $ .AND.11.EQ.PDGS(7)) THEN  ! 6
        CALL M6_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-3.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.-4.EQ.PDGS(5).AND.-11.EQ.PDGS(6)
     $ .AND.11.EQ.PDGS(7)) THEN  ! 6
        CALL M2_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-2.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.-1.EQ.PDGS(5).AND.-11.EQ.PDGS(6)
     $ .AND.11.EQ.PDGS(7)) THEN  ! 6
        CALL M8_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.2.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.1.EQ.PDGS(5).AND.-13.EQ.PDGS(6)
     $ .AND.13.EQ.PDGS(7)) THEN  ! 6
        CALL M1_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(3.EQ.PDGS(1).AND.-4.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.-15.EQ.PDGS(6)
     $ .AND.15.EQ.PDGS(7)) THEN  ! 6
        CALL M15_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-3.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.-4.EQ.PDGS(5).AND.-13.EQ.PDGS(6)
     $ .AND.13.EQ.PDGS(7)) THEN  ! 6
        CALL M3_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-1.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.-2.EQ.PDGS(5).AND.-15.EQ.PDGS(6)
     $ .AND.15.EQ.PDGS(7)) THEN  ! 6
        CALL M5_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.3.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.4.EQ.PDGS(5).AND.-15.EQ.PDGS(6)
     $ .AND.15.EQ.PDGS(7)) THEN  ! 6
        CALL M10_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-4.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.-3.EQ.PDGS(5).AND.-13.EQ.PDGS(6)
     $ .AND.13.EQ.PDGS(7)) THEN  ! 6
        CALL M9_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(4.EQ.PDGS(1).AND.-3.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.-11.EQ.PDGS(6)
     $ .AND.11.EQ.PDGS(7)) THEN  ! 6
        CALL M12_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(2.EQ.PDGS(1).AND.-1.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.-13.EQ.PDGS(6)
     $ .AND.13.EQ.PDGS(7)) THEN  ! 6
        CALL M12_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-4.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.-3.EQ.PDGS(5).AND.-15.EQ.PDGS(6)
     $ .AND.15.EQ.PDGS(7)) THEN  ! 6
        CALL M11_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(4.EQ.PDGS(1).AND.-3.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.-13.EQ.PDGS(6)
     $ .AND.13.EQ.PDGS(7)) THEN  ! 6
        CALL M12_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(4.EQ.PDGS(1).AND.-3.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.-15.EQ.PDGS(6)
     $ .AND.15.EQ.PDGS(7)) THEN  ! 6
        CALL M13_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.4.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.3.EQ.PDGS(5).AND.-11.EQ.PDGS(6)
     $ .AND.11.EQ.PDGS(7)) THEN  ! 6
        CALL M0_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(3.EQ.PDGS(1).AND.-4.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.-11.EQ.PDGS(6)
     $ .AND.11.EQ.PDGS(7)) THEN  ! 6
        CALL M14_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.1.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.2.EQ.PDGS(5).AND.-13.EQ.PDGS(6)
     $ .AND.13.EQ.PDGS(7)) THEN  ! 6
        CALL M7_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.2.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.1.EQ.PDGS(5).AND.-15.EQ.PDGS(6)
     $ .AND.15.EQ.PDGS(7)) THEN  ! 6
        CALL M4_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(3.EQ.PDGS(1).AND.-4.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.-13.EQ.PDGS(6)
     $ .AND.13.EQ.PDGS(7)) THEN  ! 6
        CALL M14_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(1.EQ.PDGS(1).AND.-2.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.-15.EQ.PDGS(6)
     $ .AND.15.EQ.PDGS(7)) THEN  ! 6
        CALL M15_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.4.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.3.EQ.PDGS(5).AND.-13.EQ.PDGS(6)
     $ .AND.13.EQ.PDGS(7)) THEN  ! 6
        CALL M1_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.1.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.2.EQ.PDGS(5).AND.-15.EQ.PDGS(6)
     $ .AND.15.EQ.PDGS(7)) THEN  ! 6
        CALL M10_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(2.EQ.PDGS(1).AND.-1.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.-15.EQ.PDGS(6)
     $ .AND.15.EQ.PDGS(7)) THEN  ! 6
        CALL M13_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.3.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.4.EQ.PDGS(5).AND.-11.EQ.PDGS(6)
     $ .AND.11.EQ.PDGS(7)) THEN  ! 6
        CALL M6_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.4.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.3.EQ.PDGS(5).AND.-15.EQ.PDGS(6)
     $ .AND.15.EQ.PDGS(7)) THEN  ! 6
        CALL M4_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.2.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.1.EQ.PDGS(5).AND.-11.EQ.PDGS(6)
     $ .AND.11.EQ.PDGS(7)) THEN  ! 6
        CALL M0_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(1.EQ.PDGS(1).AND.-2.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.-13.EQ.PDGS(6)
     $ .AND.13.EQ.PDGS(7)) THEN  ! 6
        CALL M14_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-1.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.-2.EQ.PDGS(5).AND.-11.EQ.PDGS(6)
     $ .AND.11.EQ.PDGS(7)) THEN  ! 6
        CALL M2_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(2.EQ.PDGS(1).AND.-1.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.21.EQ.PDGS(5).AND.-11.EQ.PDGS(6)
     $ .AND.11.EQ.PDGS(7)) THEN  ! 6
        CALL M12_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.3.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.4.EQ.PDGS(5).AND.-13.EQ.PDGS(6)
     $ .AND.13.EQ.PDGS(7)) THEN  ! 6
        CALL M7_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-4.EQ.PDGS(2).AND.-6.EQ.PDGS(3)
     $ .AND.5.EQ.PDGS(4).AND.-3.EQ.PDGS(5).AND.-11.EQ.PDGS(6)
     $ .AND.11.EQ.PDGS(7)) THEN  ! 6
        CALL M8_SMATRIXHEL(P, NHEL, ANS)
      ELSE IF(21.EQ.PDGS(1).AND.-1.EQ.PDGS(2).AND.6.EQ.PDGS(3).AND.
     $ -5.EQ.PDGS(4).AND.-2.EQ.PDGS(5).AND.-13.EQ.PDGS(6)
     $ .AND.13.EQ.PDGS(7)) THEN  ! 6
        CALL M3_SMATRIXHEL(P, NHEL, ANS)
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
CF2PY INTEGER, intent(out) :: PDG(36,7)
      INTEGER PDG(36,7), PDGS(36,7)
      DATA PDGS/ 21,1,21,21,21,21,21,21,3,21,21,21,21,4,2,21,4,4,21,3
     $ ,21,21,3,1,21,21,2,21,21,21,1,21,2,21,21,21,-2,-2,-3,-2,1,-3,-2
     $ ,2,-4,-3,-1,3,-4,-3,-1,-4,-3,-3,4,-4,1,2,-4,-2,4,1,-1,3,4,2,-2,
     $ -1,-1,3,-4,-1,-6,-6,6,-6,-6,6,-6,6,-6,6,6,-6,-6,6,6,-6,6,6,6,-6
     $ ,-6,6,-6,-6,6,-6,6,-6,6,6,-6,6,6,-6,-6,6,5,5,-5,5,5,-5,5,-5,5,
     $ -5,-5,5,5,-5,-5,5,-5,-5,-5,5,5,-5,5,5,-5,5,-5,5,-5,-5,5,-5,-5,5
     $ ,5,-5,-1,21,-4,-1,2,-4,-1,1,21,-4,-2,4,-3,21,21,-3,21,21,3,21,2
     $ ,1,21,21,3,2,21,4,3,1,21,-2,21,4,-3,-2,-15,-11,-15,-13,-11,-11,
     $ -11,-13,-15,-13,-15,-15,-13,-11,-13,-15,-13,-15,-11,-11,-13,-15
     $ ,-13,-15,-13,-15,-15,-11,-15,-11,-13,-11,-11,-13,-11,-13,15,11
     $ ,15,13,11,11,11,13,15,13,15,15,13,11,13,15,13,15,11,11,13,15,13
     $ ,15,13,15,15,11,15,11,13,11,11,13,11,13 /
      PDG = PDGS
      RETURN
      END

      SUBROUTINE GET_PREFIX(PREFIX)
      IMPLICIT NONE
CF2PY CHARACTER*20, intent(out) :: PREFIX(36)
      CHARACTER*20 PREFIX(36),PREF(36)
      DATA PREF / 'M11_','M14_','M5_','M9_','M6_','M2_','M8_','M1_'
     $ ,'M15_','M3_','M5_','M10_','M9_','M12_','M12_','M11_','M12_'
     $ ,'M13_','M0_','M14_','M7_','M4_','M14_','M15_','M1_','M10_'
     $ ,'M13_','M6_','M4_','M0_','M14_','M2_','M12_','M7_','M8_','M3_'/
      PREFIX = PREF
      RETURN
      END




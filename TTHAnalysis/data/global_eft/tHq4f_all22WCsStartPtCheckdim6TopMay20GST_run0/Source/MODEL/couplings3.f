ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      written by the UFO converter
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE COUP3()

      IMPLICIT NONE
      INCLUDE 'model_functions.inc'

      DOUBLE PRECISION PI, ZERO
      PARAMETER  (PI=3.141592653589793D0)
      PARAMETER  (ZERO=0D0)
      INCLUDE 'input.inc'
      INCLUDE 'coupl.inc'
      GC_738 = (MDL_CTP*MDL_COMPLEXI*MDL_VEV__EXP__2)
     $ /(MDL_LAMBDA__EXP__2*MDL_SQRT__2)
      GC_739 = (MDL_CTPI*MDL_VEV__EXP__2)/(MDL_LAMBDA__EXP__2
     $ *MDL_SQRT__2)
      GC_741 = -((MDL_CBWI*MDL_VEV)/MDL_LAMBDA__EXP__2)+(MDL_CBW
     $ *MDL_COMPLEXI*MDL_VEV)/MDL_LAMBDA__EXP__2
      GC_742 = (MDL_CBWI*MDL_VEV)/MDL_LAMBDA__EXP__2+(MDL_CBW
     $ *MDL_COMPLEXI*MDL_VEV)/MDL_LAMBDA__EXP__2
      GC_767 = -((MDL_CTWI*MDL_VEV)/MDL_LAMBDA__EXP__2)+(MDL_CTW
     $ *MDL_COMPLEXI*MDL_VEV)/MDL_LAMBDA__EXP__2
      GC_768 = (MDL_CTWI*MDL_VEV)/MDL_LAMBDA__EXP__2+(MDL_CTW
     $ *MDL_COMPLEXI*MDL_VEV)/MDL_LAMBDA__EXP__2
      GC_953 = -((MDL_COMPLEXI*MDL_YB)/MDL_SQRT__2)
      GC_954 = -((MDL_COMPLEXI*MDL_YT)/MDL_SQRT__2)
      END

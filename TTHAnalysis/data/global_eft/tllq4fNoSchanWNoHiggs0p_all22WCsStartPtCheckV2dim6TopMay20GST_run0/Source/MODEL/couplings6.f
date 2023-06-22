ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      written by the UFO converter
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE COUP6()

      IMPLICIT NONE
      INCLUDE 'model_functions.inc'

      DOUBLE PRECISION PI, ZERO
      PARAMETER  (PI=3.141592653589793D0)
      PARAMETER  (ZERO=0D0)
      INCLUDE 'input.inc'
      INCLUDE 'coupl.inc'
      GC_7 = MDL_COMPLEXI*G
      GC_725 = (MDL_CTG*MDL_COMPLEXI*MDL_GSTRONG*MDL_VEV)
     $ /(MDL_LAMBDA__EXP__2*MDL_SQRT__2)
      GC_726 = (MDL_CTGI*MDL_GSTRONG*MDL_VEV)/(MDL_LAMBDA__EXP__2
     $ *MDL_SQRT__2)
      END

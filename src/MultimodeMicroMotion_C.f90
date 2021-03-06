 SUBROUTINE MULTIMODEFLOQUETTRANSFORMATION_C(D,NM,MODES_NUM,U_F_MODES,E_MULTIFLOQUET,D_BARE,T1,U,INFO) 

  ! TIME-DEPENDENT TRANSFORMATION BETWEEN THE EXTENDED BARE BASIS AND THE FLOQUET STATES
  ! U(T1) = sum_ U^n exp(i n omega T1)
  ! 
!!$  D              (IN)   : DIMENSION OF THE EXTENDED HILBERT SPACE (SIZE OF THE MULTIMODE FLOQUET MATRIX)
!!$  NM             (IN)   : NUMBER OF MODES            
!!$  MODES_NUM      (IN)   : VECTOR (NM) INDICATING THE NUMBER OF HARMONICS OF EACH MODE
!!$  U_F_MODES      (IN)   : TRANSFORMATION, DIMENSOON (D,D) 
!!$  E_MULTIFLOQUET (IN)   : MULTIMODE FLOQUET SPECTRUM
!!$  D_BARE         (IN)   : DIMENSION OF THE BARE HILBERT SPACE
!!$  FIELD          (IN)   : STRUCTURE DESCRIBING THE COUPLINGS
!!$  T1             (IN)   : TIME. THE BARE 2 DRESSED TRANSFORMATINO IS TIME DEPENDENT
!!$  U              (OUT)  : TRANFORMATION BETWEEN THE EXTENDED BARE BASIS AND THE FLOQUET STATES, DIMENSION (D_BARE,D)
!!$  INFO           (INOUT): (POSSIBLE) ERROR FLAG
 
  USE TYPES_C
  USE TYPES
  USE MODES_4F
  USE SUBINTERFACE_LAPACK

  IMPLICIT NONE
  INTEGER,                                    INTENT(IN)    :: D,D_BARE,NM ! DIMENSION OF THE MULTIMODE FLOQUET SPACE AND THE BARE BASIS
  INTEGER,                                    INTENT(INOUT) :: INFO
  INTEGER,          DIMENSION(NM),            INTENT(IN)    :: MODES_NUM
  !TYPE(MODE_C),     DIMENSION(NM),            INTENT(IN)    :: FIELD  ! FIELDS PROPERTIES: FREQUENCY, AMPLITUDES AND PHASES
  DOUBLE PRECISION,                           INTENT(IN)    :: T1 ! IN SECONDS
  DOUBLE PRECISION, DIMENSION(D),             INTENT(IN)    :: E_MULTIFLOQUET ! SET OF MULTIMODE FLOQUET ENERGIES, IN Hz, TO AVOID HBAR FACTORS
  COMPLEX*16,       DIMENSION(D,D),           INTENT(IN)    :: U_F_MODES ! TRANFORMATION MATRIX BETWEEN DRESSED FLOQUET AND BARE EXTENDED BASIS
  COMPLEX*16,       DIMENSION(D_BARE,D),      INTENT(OUT)   :: U ! TIME-DEPENDENT TRANSFORMATINO BETWEEN THE DRESSED AND EXTENDED BARE BASIS

  INTEGER INDEX0
  
  !WRITE(*,*) "ME"
  CALL MULTIMODEFLOQUETTRANSFORMATION(D,NM,MODES_NUM,U_F_MODES,E_MULTIFLOQUET,D_BARE,COUPLING,T1,U,INFO) 
  INDEX0 = D_BARE*COUPLING(2)%N_FLOQUET
  !write(*,*) D,NM,MODES_NUM
!  write(*,*)U_F_MODES
  !write(*,*)E_MULTIFLOQUET
  !write(*,*)D_BARE,T1
 ! write(*,*)U,INFO
  !CALL WRITE_MATRIX(ABS(U(1:D_BARE,INDEX0+1:INDEX0+D_BARE)))
  

END SUBROUTINE MULTIMODEFLOQUETTRANSFORMATION_C

SUBROUTINE MULTIMODEMICROMOTION_C(ID_C,D,NM,MODES_NUM,U_F_MODES,E_MULTIFLOQUET,D_BARE,T1,U,INFO) 

  ! TIME-DEPENDENT TRANSFORMATION BETWEEN THE EXTENDED BARE BASIS AND THE FLOQUET STATES
  ! U(T1) = sum_ U^n exp(i n omega T1)
  ! 
!!$  D              (IN)   : DIMENSION OF THE EXTENDED HILBERT SPACE (SIZE OF THE MULTIMODE FLOQUET MATRIX)
!!$  NM             (IN)   : NUMBER OF MODES            
!!$  MODES_NUM      (IN)   : VECTOR (NM) INDICATING THE NUMBER OF HARMONICS OF EACH MODE
!!$  U_F_MODES      (IN)   : TRANSFORMATION, DIMENSOON (D,D) 
!!$  E_MULTIFLOQUET (IN)   : MULTIMODE FLOQUET SPECTRUM
!!$  D_BARE         (IN)   : DIMENSION OF THE BARE HILBERT SPACE
!!$  FIELD          (IN)   : STRUCTURE DESCRIBING THE COUPLINGS
!!$  T1             (IN)   : TIME. THE BARE 2 DRESSED TRANSFORMATINO IS TIME DEPENDENT
!!$  U              (OUT)  : TRANFORMATION BETWEEN THE EXTENDED BARE BASIS AND THE FLOQUET STATES, DIMENSION (D_BARE,D)
!!$  INFO           (INOUT): (POSSIBLE) ERROR FLAG
 
  USE TYPES_C
  USE TYPES
  USE MODES_4F
  USE SUBINTERFACE_LAPACK

  IMPLICIT NONE
  TYPE(ATOM_C),                               INTENT(IN)   :: ID_C
  INTEGER,                                    INTENT(IN)    :: D,D_BARE,NM ! DIMENSION OF THE MULTIMODE FLOQUET SPACE AND THE BARE BASIS
  INTEGER,                                    INTENT(INOUT) :: INFO
  INTEGER,          DIMENSION(NM),            INTENT(IN)    :: MODES_NUM
  !TYPE(MODE_C),     DIMENSION(NM),            INTENT(IN)    :: FIELD  ! FIELDS PROPERTIES: FREQUENCY, AMPLITUDES AND PHASES
  DOUBLE PRECISION,                           INTENT(IN)    :: T1 ! IN SECONDS
  DOUBLE PRECISION, DIMENSION(D),             INTENT(IN)    :: E_MULTIFLOQUET ! SET OF MULTIMODE FLOQUET ENERGIES, IN Hz, TO AVOID HBAR FACTORS
  COMPLEX*16,       DIMENSION(D,D),           INTENT(IN)    :: U_F_MODES ! TRANFORMATION MATRIX BETWEEN DRESSED FLOQUET AND BARE EXTENDED BASIS
  COMPLEX*16,       DIMENSION(D_BARE,D_BARE), INTENT(OUT)   :: U ! TIME-DEPENDENT TRANSFORMATINO BETWEEN THE DRESSED AND EXTENDED BARE BASIS

!  COMPLEX*16,       DIMENSION(D_BARE,D),      INTENT(OUT)   :: U_AUX ! TIME-DEPENDENT TRANSFORMATINO BETWEEN THE DRESSED AND EXTENDED BARE BASIS

  INTEGER INDEX0
  

  !WRITE(*,*) "ME"
  CALL MULTIMODEMICROMOTION(ATOM_,D,NM,MODES_NUM,U_F_MODES,E_MULTIFLOQUET,D_BARE,COUPLING,T1,U,INFO) 

  
  
END SUBROUTINE MULTIMODEMICROMOTION_C


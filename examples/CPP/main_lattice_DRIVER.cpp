

#include <iostream>
#include <cstdlib>
#include <complex>
#include <ctime>
#include <stdio.h>
#include <math.h>
#include <string.h>


using namespace std;
typedef std::complex<double> dcmplx;

#include "MultimodeFloquet.h"

extern "C" int h_floquet_size;


void coupling_init(mode_c_f *fields,int *n,int *d,int *info){

  // HERE WE PASS TO THIS FUNCTION:
  // mode_c_f  AN ARRAY OF STRUCTURES 
  // n         THE NUMBER OF MODES
  // d         THE HILBERT SPACE DIMENSION
    
  // 1. DECLARE AND ALLOCATE MEMORY FOR ONE INSTANCE OF MODE_C_F   

  int r,s,counter,j;
  int my_size;
  mode_c * field;
  c_storage_size_(&my_size);
  field = (mode_c *)malloc(my_size);

  std::cout << *d << "\n";
  //THE FOLLOWING FUNCTION ALLOCATES
  // THE THE MEMORY SROTRAGE FOR 
  // THE ARRAY V THAT BELONGS TO 
  // field
  c_opaque_alloc_f_(field, d);

  // NOW WE COPY THE ARRAY OF OBJECTS
  // TO INDIVIDUAL INSTANCES OF 
  // THE TYPE(MODE) DERIVED DATA TYPE
  // THUS, WE SET THE COUPLING MATRICES IN FORTRAN
  
  for(j=0;j<*n;j++){

    field->omega     = fields[j].omega;
    field->x         = fields[j].x;
    field->y         = fields[j].y;
    field->z         = fields[j].z;
    field->phi_x     = fields[j].phi_x;
    field->phi_y     = fields[j].phi_y;
    field->phi_z     = fields[j].phi_z;
    field->N_Floquet = fields[j].N_Floquet;

    counter = 0;
    for(r=0;r<*d;r++){      
      for(s=0;s<*d;s++){      
	field->V[counter] = fields[j].V[r][s];
	counter += 1;
      }
    }
    // HERE WE MAP EACH FIELD TO A GLOBAL DERIVED TYPE
    // COUPLING, DEFINED IN MODES_4F IN modes_C.f90
    c_matrix_exposedin_f_(&j,field,n,d);  
    

  }
  // NOW, WE DEALLOCATE FIELD 
  //  c_opaque_free_(field);

  // WHEN THE USER MODIFIES ANY ELEMENT OF THE ARRAY FIELDS
  // SHE/HE SHOULD CALL THIS FUNCTION AGAIN


}

int main(){

  // RANDOM SEED
  std::srand(1);
  double random_variable = 2.0*(std::rand()/RAND_MAX - 0.5);
  std::cout << random_variable << "\n";

  atom_c id;
  int info;
  char name[]     = "lattice";
  char manifold[] = "U";
  FILE *disco0,*disco1;
  
  int r,m,l,N_;
  int d_bare,total_frequencies;

  double t1,t2,jtotal;

  disco1 = fopen("lattice_timeevol_driver.dat","w+");


  info   = 0;
  jtotal = 3.0;
  t1     = 2.0;
  floquetinit_c(&id,name,&jtotal,&info);
  
  d_bare = id.d_bare;

  printf("%d\n",d_bare);

  int nm = 3;
  int * modes_num = new int [nm];

  modes_num[0] = 1;
  modes_num[1] = 1;
  modes_num[2] = 1;
  
  total_frequencies = 0;
  for(r=0;r<nm;r++){
    total_frequencies += modes_num[r];
  }
  
  mode_c_f * fields = new mode_c_f [total_frequencies];

  // ALLOCATE MEMORY FOR THE COUPLING MATRICES
  for(r=0;r<total_frequencies;r++){
    fields[r].V = new dcmplx *[d_bare];
    for(l=0;l<d_bare;l++){
      fields[r].V[l] = new dcmplx [d_bare];
    }
  }
  
  
  fields[0].x    = 0.0;
  fields[0].y    = 0.0;
  fields[0].z    = 1.0;
  fields[0].phi_x = 0.0;
  fields[0].phi_y = 0.0;
  fields[0].phi_z = 0.0;
  fields[0].omega = 0.0;
  fields[0].N_Floquet = 0;

  fields[1].x     = 2.0;
  fields[1].y     = 0.0;
  fields[1].z     = 0.0;
  fields[1].phi_x = 0.0;
  fields[1].phi_y = 0.0;
  fields[1].phi_z = 0.0;
  fields[1].omega = 1.0;
  fields[1].N_Floquet = 3;
  
  fields[2].x     = 2.0;
  fields[2].y     = 0.0;
  fields[2].z     = 0.0;
  fields[2].phi_x = 0.0;
  fields[2].phi_y = 0.0;
  fields[2].phi_z = 0.0;
  fields[2].omega = 2.0;
  fields[2].N_Floquet = 3;

  // FEED THE COUPLING MATRICES WITH RANDOM VALUES
  for(l=0;l<total_frequencies;l++){
    for(r=0;r<d_bare;r++){
      for(m=0;m<d_bare;m++){
	fields[l].V[r][m] = 2.0*(std::rand()/(RAND_MAX+1.0) - 0.5);
      }
    }
  }
  
  coupling_init(fields,&total_frequencies,&d_bare,&info);
  
  
  N_ = 1; //28;  
  dcmplx * U_AUX = new dcmplx [d_bare*d_bare];
  double * p_avg =  new double [d_bare*d_bare];
  info = 0;
  for(m=1;m<=N_;m++){
    
    // --- SET DRIVING PARAMETERS 
    fields[1].omega = 0.2 + (m-1)*2.0/N_;
    coupling_init(fields,&total_frequencies,&d_bare,&info);

    //--- EVALUATE TIME-EVOLUTION OPERATOR IN THE BARE BASIS
    t1= 0.0;
    for(r=1;r<=N_;r++){      
      t2 = r*32.0*4.0*atan(1.0)/N_;
      //timeevolutionoperator_c_(&id,&d_bare,&nm,&total_frequencies,modes_num,&t1,&t2,U_AUX,&info);           
      //for(l=0;l<d_bare*d_bare;l++) p_avg[l] = pow(abs(U_AUX[l]),2);
      //fprintf(disco1,"%f %f %f \n",fields[1].omega,t2,p_avg[0]);
    }
    fprintf(disco1,"\n");
  }
 
  return 0;

}

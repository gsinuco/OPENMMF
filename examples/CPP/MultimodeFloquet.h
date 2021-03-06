

#ifndef MULTIMODEFLOQUET_H
#define MULTIMODEFLOQUET_H

#include <iostream>
#include <cstdlib>
#include <complex> 
#include <ctime>
#include <stdio.h>
#include <math.h>
#include <string.h>

extern "C" 


using namespace std;
typedef std::complex<double> dcmplx;

struct mode_c{
  double omega;
  dcmplx x,y,z;
  double phi_x,phi_y,phi_z;
  int N_Floquet;
  dcmplx *V;
  dcmplx *VALUES;
  int *ROW,*COLUMN;
};

struct mode_c_f{
  double omega;
  dcmplx x,y,z;
  double phi_x,phi_y,phi_z;
  int N_Floquet;
  dcmplx **V;
  dcmplx *VALUES;
  int *ROW,*COLUMN;
};

struct atom_c{
  int id_system;
  int d_bare;
};

int A__;

extern "C" {

  // DIMENSION OF THE MULTIMODE FLOQUET MATRIX. CALCULATED INTERNALLY
  int h_floquet_size;
  int h_floquet_c; // Floquet matrix in the bare basis

  // GENERAL INIT SUBROUTINE
  void floquetinit_qubit_c_ (atom_c *id, int *lenght_name, char * atomicspecie,                                      int * info);
  void floquetinit_spin_c_  (atom_c *id, int *lenght_name, char * atomicspecie, double * jtotal,                     int * info);
  void floquetinit_alkali_c_(atom_c *id, int *lenght_name, char * atomicspecie, int * lenght_name2, char * manifold, int * info);
  
       
  // SET HAMILTONIAN OF SPIN-LIKE MODELS
  void  sethamiltoniancomponents_c_(atom_c *id,int * nm, int * total_frequencies,int * modes_num,int * info);
  
  
  // BUILDING FLOQUET MATRIX OF GENERIC MODEL
  void    multimodefloquetmatrix_c_       (atom_c *id,int * nm, int * total_frequencies,int * modes_num, int * info);
  void get_h_floquet_c_(int * h, dcmplx * values, int* info);
  int     multimodefloquetmatrix_c_python_(atom_c *id,int * nm, int * total_frequencies,int * modes_num,int * info);
  void multimodefloquetmatrix_sp_c_       (atom_c *id,int * nm, int * total_frequencies,int * modes_num, int * info);
  //int  multimodefloquetmatrix_python_sp_c_(atom_c *id,int * nm, int * total_frequencies,int * modes_num,mode_c * fields, int * info);
  void multimodefloquetmatrix_python_sp_c_(atom_c *id,int * nm, int * total_frequencies,int * modes_num, int * h_f,int * info);
  void get_h_floquet_sp_c_(int * h_f, dcmplx * values, int * row_index, int * column, int * info);
  //void get_h_floquet_sp_c_(int * h_f, int * row_index, int * column, int * info);

  
  // CALCULATE THE SPECTRUM OF THE FLOQUET HAMILTONIAN
  void   lapack_fulleigenvalues_c_(dcmplx * u_f,int * h_floquet_size,double * e_floquet,int *info);
  void mklsparse_fulleigenvalues_c_(int * h_floquet_size,double * e_l,double * e_r,double * e_floquet,dcmplx *U_F, int * info);
  void matmul_c_(int * op, dcmplx * a, int * ra, int * ca, dcmplx * b, int * rb, int * cb, dcmplx * c,int * info);
  
  
  // CONTSRUCTION OF THE TIME-EVOLUTION OPERATOR
  void         multimodetransitionavg_c_ (int * h_floquet_size,int * nm,int * modes_num,dcmplx * U_F,double * e_floquet,int * d_bare,double * p_avg,int *info);
  void multimodefloquettransformation_c_ (int * h_floquet_size,int * nm,int * modes_num,dcmplx * U_F,double * e_floquet,int * d_bare,double * t1,dcmplx * U_B2D,int * info); 
  void multimodemicromotion_c_(atom_c *id,int * h_floquet_size,int * nm,int * modes_num,dcmplx * U_F,double * e_floquet,int * d_bare,double * t1,dcmplx * U_B2D,int * info); 
  void multimodetimeevolutionoperator_c_ (int * h_floquet_size,int * nm,int * modes_num,dcmplx * U_F,double * e_floquet,int * d_bare,double * t1,double * t2,dcmplx * U_AUX,int * info);
  void timeevolutionoperator_c_(atom_c *id, int *d_bare, int *nm, int *nf, int * modes_num, double *t1, double *t2, dcmplx *U, int *info); 

  
    
  // DEFINITION OF DRESSED BASIS
  void            dressedbasis_c_(int * h_floquet_size,atom_c *id,int * nm, int * modes_num, dcmplx * U_FD, double * e_dressed,int * info); 
  void  dressedbasis_subset_c_(atom_c *id , int * dressingfloquetdimension,int * dressingfields, int * nm, int * dressingfields_indices, int * modes_num, dcmplx * U_FD, double * e_dressed,int * info);
  void  dressedbasis_subset_sp_c_(atom_c * id, int * dressingfloquetdimension,int * dressingfields,int * nm, int * dressingfields_indices, int * modes_num, dcmplx * U_FD, double * e_dressed,int * info);
  void  dressedbasis_sp_c_(int h_floquet_size, atom_c *id, int * nm, int * modes_num, dcmplx * U_FD, double * e_dressed, int * info);
  void micromotionfourierdressedbasis_c_(atom_c *id , int *DF, int * dressingfields_indices, int * nm, int * modes_num, int *nf,int * nd,dcmplx * U_FD, double *e_dressed,int * info);
  //  void micromotionfourierdressedbasis_c_(atom_c *id , int * dressingfields_indices, int * modes_num,mode_c * fields,int * nd,dcmplx * U_FD, double *e_dressed,int * info);
  //void micromotionfourierdressedbasis_c_(atom_c *id , int * dressingfields_indices, int * nd,dcmplx * U_FD, double *e_dressed,int * info);
  void micromotiondressedbasis_c_(atom_c *id , int * modes_num, int * dressingfields_indices, double T1, dcmplx * U, int * info);

  
  // TODO: UTILITY FUNCTION: EXTRACT GLOBAL VARIABLES WITH SCOPE ONLY WITHIN FORTRAN
  //                   H_FLOQUET : MULTIMODE FLOQUET HAMILTONIAN
  //                   VALUES, ROW,COLUMN: SPARSE REPRESETNATION OF THE FLOQUET HAMILTONIAN  
  //                   VALUES, ROW_INDEX, COLUMN: SPARSE REPRESENTATION OF THE FLOQUET HAMILTONIAN
  
  
  // UTILITY FUNCTIONS: WRITE MATRICES ON THE SCREEN
  void write_matrix_c_(double *A,int * A_dim);
  void rec_write_matrix_c_(double *A,int * A_dim1, int * A_dim2);
  
  
  // deallocate all arrays allocated with fortran
  void deallocateall_c_(int *id);


  // PASS ALLOCATABLE ARRAYS BETWEEN CPP STRUCTURES AND FORTRAN DERIVED TYPES
  void c_storage_size_(int *my_size);
  void c_opaque_alloc_f_(mode_c * field, int *d_bare);
  void c_matrix_exposedin_f_(int *j,mode_c * c_obj,int *nm, int *d_bare);
  void c_opaque_free_(mode_c * field);

} 

void floquetinit_c(atom_c * id, char *name,int *info){
  
  int length_name;
  
  length_name = strlen(name);
  floquetinit_qubit_c_(id,&length_name,name,info);
  
}
void floquetinit_c(atom_c * id,char *name,char *manifold,int *info){
  
  int length_name,length_name2;
  
  length_name = strlen(name);
  length_name2 = strlen(manifold);
  floquetinit_alkali_c_(id,&length_name,name,&length_name2,manifold,info);
  
}
 
void floquetinit_c(atom_c *id, char *name, double  *jtotal,int *info){
  
  int length_name;
  //printf("me \n");
  length_name = strlen(name);
  floquetinit_spin_c_(id,&length_name,name,jtotal,info);
  //printf("info: %d \n",length_name);

}

void matmul_c(int * op , dcmplx * a, int * ra, int * ca, dcmplx * b, int * rb, int * cb, dcmplx * c,int * info){
  matmul_c_(op, a, ra, ca, b, rb, cb, c, info);
}


void coupling_init(mode_c_f *fields,int *n,int *d,int *info);

#endif  

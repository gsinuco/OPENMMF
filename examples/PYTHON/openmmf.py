#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 09:44:01 2020

@author: german
"""

import ctypes 
from ctypes import CDLL, POINTER, c_int, c_double,c_char_p#,c_int_p,c_double_p
from numpy import empty
import numpy as np
from numpy.ctypeslib import ndpointer


openmmfC = ctypes.CDLL('../../lib/libopenmmf.so')
c_dcmplx = ctypes.c_double*2

#===================================================================
#===================================================================

class atom_c_T(ctypes.Structure):
    _fields_ = [
                ("id_system", c_int),
                ("d_bare", c_int)            
            ]

#===================================================================
#===================================================================

class mode_c_T(ctypes.Structure):
    c_dcmplx = ctypes.c_double*2
    _fields_ = [
                ("omega",     c_double),
                ("x",         c_dcmplx),
                ("y",         c_dcmplx),
                ("z",         c_dcmplx),            
                ("phi_x",     c_double),
                ("phi_y",     c_double),
                ("phi_z",     c_double),
                ("N_Floquet", c_int)
            ]

#===================================================================
#   // GENERAL INIT SUBROUTINE
#===================================================================
def floquetinit(id,*argsv,info):
#def floquetinit(id,name,info):
    id_p         = ctypes.pointer(id)
    info         = c_int(info)
    
    #print(len(argsv))
    if(len(argsv)==2):
        if(isinstance(argsv[0],str) and isinstance(argsv[1],str)):    
            name     = argsv[0]
            manifold = argsv[1]
            atomicSpecie = ctypes.c_char_p(bytes(name,'utf-8'))
            manifold_ = ctypes.c_char_p(bytes(manifold,'utf-8'))
            openmmfC.floquetinit_alkali_c_(id_p,ctypes.byref(c_int(len(name))),atomicSpecie,ctypes.byref(c_int(len(manifold))),manifold_,ctypes.byref(info));
            
        if(isinstance(argsv[0],str) and isinstance(argsv[1],float)):    
            name     = argsv[0]
            j_       = c_double(argsv[1])
            atomicSpecie = ctypes.c_char_p(bytes(name,'utf-8'))
            openmmfC.floquetinit_spin_c_(id_p,ctypes.byref(c_int(len(name))),atomicSpecie,ctypes.byref(j_),ctypes.byref(info));

    #if(len(argsv)==2):
    
    if(len(argsv)==1):
        name = argsv[0]
        atomicSpecie = ctypes.c_char_p(bytes(name,'utf-8'))
        openmmfC.floquetinit_qubit_c_(id_p,ctypes.byref(c_int(len(name))),atomicSpecie,ctypes.byref(info))
    


#===================================================================
#   // GENERAL INIT SUBROUTINE
#===================================================================
def floquetinit_(*argsv,info):
    id   = atom_c_T()
    info = c_int(info)
    args_index_off = 0
    
    if(len(argsv)==7):
        args_index_off = 1
        if(isinstance(argsv[0],str) and isinstance(argsv[1],str)):    
            
            name     = argsv[0]
            manifold = argsv[1]
            id_p         = ctypes.pointer(id)
            atomicSpecie = ctypes.c_char_p(bytes(name,'utf-8'))
            manifold_ = ctypes.c_char_p(bytes(manifold,'utf-8'))
            id_p         = ctypes.pointer(id)
            
            openmmfC.floquetinit_alkali_c_(id_p,ctypes.byref(c_int(len(name))),atomicSpecie,ctypes.byref(c_int(len(manifold))),manifold_,ctypes.byref(info));
            
        if(isinstance(argsv[0],str) and isinstance(argsv[1],float)):    
            
            name     = argsv[0]
            j_       = c_double(argsv[1])
            atomicSpecie = ctypes.c_char_p(bytes(name,'utf-8'))
            id_p         = ctypes.pointer(id)
            openmmfC.floquetinit_spin_c_(id_p,ctypes.byref(c_int(len(name))),atomicSpecie,ctypes.byref(j_),ctypes.byref(info));

    #if(len(argsv)==2):
    
    if(len(argsv)==6):
        args_index_off = 0
        name = argsv[0]
        atomicSpecie = ctypes.c_char_p(bytes(name,'utf-8'))
        id_p         = ctypes.pointer(id)
        openmmfC.floquetinit_qubit_c_(id_p,ctypes.byref(c_int(len(name))),atomicSpecie,ctypes.byref(info))

    modes_num = argsv[1+args_index_off]
    FIELD     = argsv[2+args_index_off]
    PHI       = argsv[3+args_index_off]
    OMEGA     = argsv[4+args_index_off]
    N_FLOQUET = argsv[5+args_index_off]

    nm        = np.sum(modes_num)
    fields    = mode_c_T*nm # THIS INSTRUCTION DEFINES A TYPE OF ARRAY OF modes WITH nm COMPONENTS
    field     = fields()    # THIS INSTANCE DECLARES THE FIELD

    for r in range(nm):
        field[r].x     = FIELD[r,0],0
        field[r].y     = FIELD[r,1],0
        field[r].z     = FIELD[r,2],0
        field[r].phi_x = PHI[r,0]
        field[r].phi_y = PHI[r,1]
        field[r].phi_z = PHI[r,2]
        field[r].omega = OMEGA[r]
        field[r].N_Floquet = N_FLOQUET[r]
    
    return id,field
        
#===================================================================
#   EVALUATE THE HAMILTONIAN COMPONENTS OF PRE-DEFINED SYSTEMS. 
#===================================================================
def sethamiltoniancomponents(id,modes_num,fields,info):
    id_p = ctypes.pointer(id)
    nm                = c_int(modes_num.size)
    total_frequencies = c_int(np.sum(modes_num))
    info = c_int(info)
    modes_num_p = modes_num.ctypes.data_as(POINTER(c_int))
    fields_p = ctypes.pointer(fields)
    openmmfC.sethamiltoniancomponents_c_(id_p,ctypes.byref(nm),ctypes.byref(total_frequencies),modes_num_p,fields_p,ctypes.byref(info))

#===================================================================
#   // BUILDING FLOQUET MATRIX OF GENERIC MODEL
#===================================================================
def multimodefloquetmatrix(id,modes_num,fields,info):
    id_p              = ctypes.pointer(id)
    nm                = c_int(modes_num.size)
    total_frequencies = c_int(np.sum(modes_num))    
    info              = c_int(info)
    modes_num_p       = modes_num.ctypes.data_as(POINTER(c_int))
    fields_p          = ctypes.pointer(fields)
    h_floquet_size =    openmmfC.multimodefloquetmatrix_c_python_(id_p,ctypes.byref(nm),ctypes.byref(total_frequencies),modes_num_p,fields_p,ctypes.byref(info))
    return h_floquet_size

def get_h_floquet(h_floquet_size, info):
    c_dcmplx = ctypes.c_double*2
    info              = c_int(info)
    VALUES            = np.zeros([h_floquet_size*h_floquet_size],dtype=np.complex)    
    h_floquet_size_p  = c_int(h_floquet_size)#h_floquet_size.ctypes.data_as(POINTER(c_int))
    VALUES_p          = VALUES.ctypes.data_as(POINTER(c_dcmplx))        
    openmmfC.get_h_floquet_c_(ctypes.byref(h_floquet_size_p),VALUES_p,ctypes.byref(info))
    return VALUES


def multimodefloquetmatrix_sp(id,modes_num,fields,info):
    id_p              = ctypes.pointer(id)
    nm                = c_int(modes_num.size)
    total_frequencies = c_int(np.sum(modes_num))    
    #info              = c_int(info)
    info              = c_int(int(6))
    modes_num_p       = modes_num.ctypes.data_as(POINTER(c_int))
    fields_p          = ctypes.pointer(fields)
    h_floquet_size    = np.zeros([4],dtype=np.int32)
    h_floquet_size_p  = h_floquet_size.ctypes.data_as(POINTER(c_int))

    openmmfC.multimodefloquetmatrix_python_sp_c_(id_p,ctypes.byref(nm),ctypes.byref(total_frequencies),modes_num_p,fields_p,h_floquet_size_p,ctypes.byref(info))
    return h_floquet_size


def get_h_floquet_sp(h_floquet_size, info):
    c_dcmplx = ctypes.c_double*2
    info              = c_int(info)
    VALUES            = np.empty([h_floquet_size[0]],dtype=np.complex)
    ROW_INDEX         = np.empty([h_floquet_size[1]],dtype=np.int32)
    COLUMN            = np.empty([h_floquet_size[2]],dtype=np.int32)
    
    h_floquet_size_p  = h_floquet_size.ctypes.data_as(POINTER(c_int))
    VALUES_p          =    VALUES.ctypes.data_as(POINTER(c_dcmplx))
    ROW_INDEX_p       = ROW_INDEX.ctypes.data_as(POINTER(c_int))
    COLUMN_p          =    COLUMN.ctypes.data_as(POINTER(c_int))
        
    openmmfC.get_h_floquet_sp_c_(h_floquet_size_p,VALUES_p,ROW_INDEX_p,COLUMN_p,ctypes.byref(info))
    #openmmfC.get_h_floquet_sp_c_(h_floquet_size_p,VALUES_p)

    return VALUES,ROW_INDEX,COLUMN    

#===================================================================
#  // CALCULATE THE SPECTRUM OF THE FLOQUET HAMILTONIAN
#===================================================================
def lapack_fulleigenvalues(U_F,h_floquet_size,e_floquet,info):    
    info = c_int(info)
    U_F_p = U_F.ctypes.data_as(POINTER(c_dcmplx))
    e_floquet_p = e_floquet.ctypes.data_as(POINTER(c_double))
    h_floquet_size = c_int(h_floquet_size)        
    openmmfC.lapack_fulleigenvalues_c_(U_F_p,ctypes.byref(h_floquet_size),e_floquet_p,ctypes.byref(info))

def mklsparse_fulleigenvalues(h_floquet_size,U_F,e_floquet,e_l,e_r,info):    
    
    info           = c_int(info)
    h_floquet_size = c_int(h_floquet_size)        
    e_l_p          = c_double(e_l)
    e_r_p          = c_double(e_r)
    U_F_p          = U_F.ctypes.data_as(POINTER(c_dcmplx))
    e_floquet_p    = e_floquet.ctypes.data_as(POINTER(c_double))   
    openmmfC.mklsparse_fulleigenvalues_c_(ctypes.byref(h_floquet_size),e_l_p,e_r_p,e_floquet_p,U_F_p,ctypes.byref(info))

#===================================================================
#   EVALUATES THE TIME AVERAGE TRANSITIONS PROBABILITIES
#===================================================================
def multimodetransitionavg(h_floquet_size,fields,modes_num,U_F,e_floquet,d_bare,p_avg,info):
    info           = c_int(info)
    d_bare         = c_int(d_bare)
    nm             = c_int(modes_num.size)
    h_floquet_size = c_int(h_floquet_size)        
    modes_num_p    = modes_num.ctypes.data_as(POINTER(c_int))
    U_F_p          = U_F.ctypes.data_as(POINTER(c_dcmplx))
    e_floquet_p    = e_floquet.ctypes.data_as(POINTER(c_double))
    fields_p       = ctypes.pointer(fields)
    p_avg_p        = p_avg.ctypes.data_as(POINTER(c_double))
    openmmfC.multimodetransitionavg_c_(ctypes.byref(h_floquet_size),ctypes.byref(nm),fields_p,modes_num_p,U_F_p,e_floquet_p,ctypes.byref(d_bare),p_avg_p,ctypes.byref(info));

#===================================================================
# FOURIER COMPONENTS OF THE TRANSFORMATION BETWEEN THE DRESSED AND THE BARE BASIS
# U_B2D is of dimension [D_bare*D_floquet]
#===================================================================
def multimodefloquettransformation(modes_num, U_F,e_floquet,d_bare,fields,t1, U_B2D,info): 
    
    info           = c_int(info)
    d_bare         = c_int(d_bare)
    t1             = c_double(t1)
    nm             = c_int(modes_num.size)
    h_floquet_size = c_int(int(np.sqrt(U_F.size)))        
    modes_num_p    = modes_num.ctypes.data_as(POINTER(c_int))
    U_F_p          =       U_F.ctypes.data_as(POINTER(c_dcmplx))
    U_B2D_p        =     U_B2D.ctypes.data_as(POINTER(c_dcmplx))
    e_floquet_p    = e_floquet.ctypes.data_as(POINTER(c_double))
    fields_p       = ctypes.pointer(fields)
    openmmfC.multimodefloquettransformation_c_(ctypes.byref(h_floquet_size),ctypes.byref(nm),modes_num_p,U_F_p,e_floquet_p,ctypes.byref(d_bare),fields_p,ctypes.byref(t1),U_B2D_p,ctypes.byref(info)) 

#===================================================================
# CALCULATE THE MICROMOTION OPERATOR
# U_B2D is of dimension [D_bare*D_bare]
#===================================================================
def multimodemicromotion(id,h_floquet_size,modes_num,U_F,e_floquet,d_bare,fields,t1, U_B2D,info):
    id_p           = ctypes.pointer(id)
    info           = c_int(info)
    d_bare         = c_int(d_bare)
    t1             = c_double(t1)
    nm             = c_int(modes_num.size)
    h_floquet_size = c_int(h_floquet_size)        
    modes_num_p    = modes_num.ctypes.data_as(POINTER(c_int))
    U_F_p          = U_F.ctypes.data_as(POINTER(c_dcmplx))
    U_B2D_p        = U_B2D.ctypes.data_as(POINTER(c_dcmplx))
    e_floquet_p    = e_floquet.ctypes.data_as(POINTER(c_double))
    fields_p       = ctypes.pointer(fields)
    openmmfC.multimodemicromotion_c_(id_p,ctypes.byref(h_floquet_size),ctypes.byref(nm),modes_num_p,U_F_p,e_floquet_p,ctypes.byref(d_bare),fields_p,ctypes.byref(t1),U_B2D_p,ctypes.byref(info));

#===================================================================
# COMP. ROUTINE: EVALUATE THE TIME EVOULUTION OPERATOR BETWEEN T1 AND T2 USING THE FOURIER DECOMPOSITION
# OF THE MICROMOTION OPERATOR, WHICH IS STORE IN U_F.
#===================================================================
def multimodetimeevolutionoperator(h_floquet_size,modes_num,U_F,e_floquet,d_bare,fields,t1,t2,U_AUX,info):
    d_bare         = c_int(d_bare)
    t1             = c_double(t1)
    t2             = c_double(t2)
    info           = c_int(info)
    nm             = c_int(modes_num.size)
    h_floquet_size = c_int(h_floquet_size)        
    modes_num_p    = modes_num.ctypes.data_as(POINTER(c_int))
    U_F_p          = U_F.ctypes.data_as(POINTER(c_dcmplx))
    e_floquet_p    = e_floquet.ctypes.data_as(POINTER(c_double))
    fields_p       = ctypes.pointer(fields)
    U_AUX_p        = U_AUX.ctypes.data_as(POINTER(c_dcmplx))
    openmmfC.multimodetimeevolutionoperator_c_(ctypes.byref(h_floquet_size),ctypes.byref(nm),modes_num_p,U_F_p,e_floquet_p,ctypes.byref(d_bare),fields_p,ctypes.byref(t1),ctypes.byref(t2),U_AUX_p,ctypes.byref(info))

#===================================================================
# DRIVER ROUTINE: EVALUATE THE TIME EVOULUTION OPERATOR BETWEEN T1 AND T2
#===================================================================
def timeevolutionoperator(id,d_bare,modes_num,fields,t1,t2,U,info):
    id_p           = ctypes.pointer(id)
    d_bare         = c_int(d_bare)
    t1             = c_double(t1)
    t2             = c_double(t2)
    info           = c_int(info)
    nm             = c_int(modes_num.size)
    nf             = c_int(np.sum(modes_num))
    modes_num_p    = modes_num.ctypes.data_as(POINTER(c_int))
    U_p            = U.ctypes.data_as(POINTER(c_dcmplx))
    fields_p       = ctypes.pointer(fields)
    openmmfC.timeevolutionoperator_c_(id_p, ctypes.byref(d_bare), ctypes.byref(nm), ctypes.byref(nf),modes_num_p, fields_p, ctypes.byref(t1), ctypes.byref(t2),U_p, ctypes.byref(info))
        

#===================================================================
#  // DEFINITION OF DRESSED BASIS WITH ALL FIELDS
#===================================================================
def dressedbasis(h_floquet_size,id,modes_num,fields,U_FD,e_dressed,info):
    id_p           = ctypes.pointer(id)
    h_floquet_size = c_int(h_floquet_size)
    info           = c_int(info)
    nm             = c_int(modes_num.size)
    modes_num_p    = modes_num.ctypes.data_as(POINTER(c_int))
    U_FD_p         = U_FD.ctypes.data_as(POINTER(c_dcmplx))
    fields_p       = ctypes.pointer(fields)
    e_dressed_p    = ctypes.pointer(e_dressed)
    openmmfC.dressedbasis_c_(ctypes.byref(h_floquet_size),id_p,ctypes.byref(nm),modes_num_p,fields_p,U_FD_p,e_dressed_p,ctypes.byref(info))

def dressedbasis_sp(h_floquet_size,id,modes_num,fields,U_FD,e_dressed,info):
    id_p           = ctypes.pointer(id)
    h_floquet_size = c_int(h_floquet_size)
    info           = c_int(info)
    nm             = c_int(modes_num.size)
    modes_num_p    = modes_num.ctypes.data_as(POINTER(c_int))
    U_FD_p         = U_FD.ctypes.data_as(POINTER(c_dcmplx))
    fields_p       = ctypes.pointer(fields)
    e_dressed_p    = ctypes.pointer(e_dressed)
    openmmfC.dressedbasis_sp_c_(ctypes.byref(h_floquet_size),id_p,ctypes.byref(nm),modes_num_p,fields_p,U_FD_p,e_dressed_p,ctypes.byref(info))


#===================================================================
#  // DEFINITION OF DRESSED BASIS WITH A SUBSET OF THE FIELDS
#===================================================================
def dressedbasis_subset(id,dressingfields_indices,modes_num,fields,U_FD,e_dressed,info):
    
    dressingfields_indices_p = dressingfields_indices.ctypes.data_as(POINTER(c_int))
    dressingfloquetdimension = c_int(int(np.sqrt(U_FD.shape[0])))
    dressingfields           = c_int(dressingfields_indices.shape[0])
    id_p                     = ctypes.pointer(id)
    nm             = c_int(modes_num.size)
    modes_num_p    = modes_num.ctypes.data_as(POINTER(c_int))
    fields_p       = ctypes.pointer(fields)
    U_FD_p         = U_FD.ctypes.data_as(POINTER(c_dcmplx))
    e_dressed_p    = e_dressed.ctypes.data_as(POINTER(c_double))
    info           = c_int(info)
    openmmfC.dressedbasis_subset_c_(id_p, ctypes.byref(dressingfloquetdimension),ctypes.byref(dressingfields),ctypes.byref(nm),dressingfields_indices_p,modes_num_p,fields_p,U_FD_p,e_dressed_p,ctypes.byref(info));


def dressedbasis_subset_sp(id,dressingfields_indices,modes_num,fields,U_FD,e_dressed,info):
    
    dressingfields_indices_p = dressingfields_indices.ctypes.data_as(POINTER(c_int))
    dressingfloquetdimension = c_int(int(np.sqrt(U_FD.shape[0])))
    dressingfields           = c_int(dressingfields_indices.shape[0])
    id_p                     = ctypes.pointer(id)
    nm             = c_int(modes_num.size)
    modes_num_p    = modes_num.ctypes.data_as(POINTER(c_int))
    fields_p       = ctypes.pointer(fields)
    U_FD_p         = U_FD.ctypes.data_as(POINTER(c_dcmplx))
    e_dressed_p    = e_dressed.ctypes.data_as(POINTER(c_double))
    info           = c_int(info)
    openmmfC.dressedbasis_subset_sp_c_(id_p, ctypes.byref(dressingfloquetdimension),ctypes.byref(dressingfields),ctypes.byref(nm),dressingfields_indices_p,modes_num_p,fields_p,U_FD_p,e_dressed_p,ctypes.byref(info));

     

#===================================================================
#  // DEFINITION OF DRESSED BASIS WITH A SUBSET OF THE FIELDS
#===================================================================
def dressedbasis_subset_(id,dressingfields_indices,modes_num,field,info):

    dressingfields = dressingfields_indices.size

    dressingfloquetdimension = id.d_bare; # This variable will be the dimension of the floquet space of the dressed basis
    for m in range(dressingfields):
        dressingfloquetdimension =  dressingfloquetdimension*(2*field[dressingfields_indices[m]].N_Floquet + 1)
  
    print(dressingfloquetdimension)
    U_FD      = np.zeros([dressingfloquetdimension*dressingfloquetdimension],dtype=np.complex)
    e_dressed = np.zeros([dressingfloquetdimension],dtype=np.double)

   
    dressingfloquetdimension  = c_int(int(e_dressed.shape[0]))
    dressingfields            = c_int(int(dressingfields_indices.shape[0]))
    nm                        = c_int(modes_num.size)
    info                      = c_int(info)
    id_p                      = ctypes.pointer(id)
    fields_p                  = ctypes.pointer(field)
    U_FD_p                    =                   U_FD.ctypes.data_as(POINTER(c_dcmplx))
    modes_num_p               =              modes_num.ctypes.data_as(POINTER(c_int))
    e_dressed_p               =              e_dressed.ctypes.data_as(POINTER(c_double))
    dressingfields_indices_p  = dressingfields_indices.ctypes.data_as(POINTER(c_int))
    #print(dressingfloquetdimension,dressingfields,nm,id.d_bare,info)
    
    #openmmfC.dressedbasis_subset_c_(id_p, ctypes.byref(dressingfloquetdimension),ctypes.byref(dressingfields),ctypes.byref(nm),dressingfields_indices_p,modes_num_p,fields_p,U_FD_p,e_dressed_p,ctypes.byref(info));

  
    modes_num_         = np.array([1,1],dtype=np.int32) # // Modes of the dressing fields
    nm_                = modes_num_.size   # // number of fundamental modes

    fields_    = mode_c_T*nm_ # THIS INSTRUCTION DEFINES A TYPE OF ARRAY OF modes WITH nm   COMPONENTS
    field_     = fields_()            # THIS INSTANCE DECLARES THE FIELDS

    field_offset = 0
  
    for r in range(dressingfields_indices.shape[0]):
        field_offset = 0
        for l in range(dressingfields_indices[r]):
            field_offset += modes_num[l]
    
        for m in range(modes_num_[r]):
            field_[r] = field[field_offset + m]

 #   modes_num_ = 0
 #   field_ = 0
 #   U_FD= 0
 #   e_dressed= 0
    return modes_num_,field_,U_FD,e_dressed

#===================================================================
#===================================================================
     
 # void  dressedbasis_subset_sp_c_(atom_c * id, int * dressingfloquetdimension,int * dressingfields,int * nm, int * dressingfields_indices, int * modes_num,mode_c * fields, dcmplx * U_FD, double * e_dressed,int * info);
 # void  dressedbasis_sp_c_(int h_floquet_size, atom_c *id, int * nm, int * modes_num, mode_c * fields, dcmplx * U_FD, double * e_dressed, int * info);

#===================================================================
#  EVALUATE THE FOURIER COMPONENTS OF THE MICROMOTION OPERATOR USING THE DRESSING FIELDS
#===================================================================
def micromotionfourierdressedbasis(id,dressingfields_indices,modes_num,fields,U_FD,e_dressed,info):
    id_p                     = ctypes.pointer(id)
    dressingfields_indices_p = dressingfields_indices.ctypes.data_as(POINTER(c_int))
    modes_num_p    = modes_num.ctypes.data_as(POINTER(c_int))
    fields_p       = ctypes.pointer(fields)
    U_FD_p         = U_FD.ctypes.data_as(POINTER(c_dcmplx))
    e_dressed_p    = ctypes.pointer(e_dressed)
    info           = c_int(info)
    openmmfC.micromotionfourierdressedbasis_c_(id_p,dressingfields_indices_p,modes_num_p,fields_p,U_FD_p,e_dressed_p,ctypes.byref(info));


#===================================================================
#  EVALUATE THE MICROMOTION OPERATOR USING THE DRESSING FIELDS
#===================================================================
def micromotiondressedbasis(id,modes_num,dressingfields_indices,fields,t1,U,info):
    id_p                     = ctypes.pointer(id)
    dressingfields_indices_p = dressingfields_indices.ctypes.data_as(POINTER(c_int))
    modes_num_p    = modes_num.ctypes.data_as(POINTER(c_int))
    fields_p       = ctypes.pointer(fields)
    t1             = c_double(t1)
    U_p            = U.ctypes.data_as(POINTER(c_dcmplx))
    info           = c_int(info)
    openmmfC.micromotiondressedbasis_c_(id_p,modes_num_p,dressingfields_indices_p,fields_p,ctypes.byref(t1),U_p,ctypes.byref(info));


#===================================================================
#  DEALLOCATE ALL MEMORY ARRAYS
#===================================================================

def deallocateall(id):
    openmmfC.deallocateall_c_(ctypes.byref(c_int(id.id_system)))

#===================================================================
#===================================================================

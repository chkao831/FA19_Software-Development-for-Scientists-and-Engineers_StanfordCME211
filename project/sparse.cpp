/**
* @file sparse.cpp
* @author Chih-Hsuan Kao
* Contact: chkao831@stanford.edu
* Date: Dec 9, 2019
* The SparseMatrix object contains matrix in vector forms as its attributes
*/

#include <iostream>
#include <stdio.h>
#include <vector>

#include "CGSolver.hpp"
#include "COO2CSR.hpp"
#include "sparse.hpp"

SparseMatrix::SparseMatrix(){
    this -> i_idx = std::vector<int>();
    this -> j_idx = std::vector<int>();
    this -> a = std::vector<double>();
    this -> ncols = 0;
    this -> nrows = 0;
}

/* Method to modify sparse matrix dimensions (Setter) */
void SparseMatrix::Resize(int nrows, int ncols){
    this -> nrows = nrows;
    this -> ncols = ncols;
}//end Resize

/* Method to add entry to matrix in COO format */
void SparseMatrix::AddEntry(int i, int j, double val){
    i_idx.push_back(i);
    j_idx.push_back(j);
    a.push_back(val);
}//end AddEntry

/* Method to convert COO matrix to CSR format using provided function */
void SparseMatrix::ConvertToCSR(){
    COO2CSR(a,i_idx,j_idx);
}//end ConvertToCSR

/* Getter of i_idx */
std::vector<int> SparseMatrix::GetRowPtr(){
    return i_idx;
}

/* Getter of j_idx */
std::vector<int> SparseMatrix::GetColIdx(){
    return j_idx;
}

std::vector<double> SparseMatrix::GetCSRVal(){
    return a;
}



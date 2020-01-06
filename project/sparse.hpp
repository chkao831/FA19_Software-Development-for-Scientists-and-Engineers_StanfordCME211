/**
* @file sparse.hpp
* @author Chih-Hsuan Kao
* Contact: chkao831@stanford.edu
* Date: Dec 9, 2019
* Prototype of sparse.cpp
*/


#ifndef SPARSE_HPP
#define SPARSE_HPP

#include <stdio.h>
#include <vector>

class SparseMatrix
{
  private:
    std::vector<int> i_idx;
    std::vector<int> j_idx;
    std::vector<double> a;
    int ncols;
    int nrows;

  public:
    /* Method to modify sparse matrix dimensions (Setter) */
    void Resize(int nrows, int ncols);

    /* Method to add entry to matrix in COO format */
    void AddEntry(int i, int j, double val);

    /* Method to convert COO matrix to CSR format using provided function */
    void ConvertToCSR();

    /* Method to perform sparse matrix vector multiplication using CSR formatted matrix*/
    std::vector<int> GetRowPtr();
    std::vector<int> GetColIdx();
    std::vector<double> GetCSRVal();

    /* Default Constructor */
    SparseMatrix();
};

#endif /* SPARSE_HPP */

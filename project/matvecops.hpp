/**
 * @file matvecops.hpp
 * @author Chih-Hsuan Kao
 * Contact: chkao831@stanford.edu
 * Date: Nov 18, 2019
 */

#ifndef matvecops_HPP
#define matvecops_HPP

#include <cmath>                                                               
#include <iostream>                                                            
#include <vector>

/* This is the prototype of matvecops.cpp 
 * These functions perform basic matrix and vector operations
 */
/* Calculates the l2 norm of a given vector.  */
double calculateL2Norm(const std::vector<double> &vec);
/* alculates the inner product of two given vectors. */
double calculateVecTrans(const std::vector<double> &vec1,
                         const std::vector<double> &vec2);
/* Performs matrix and vector multiplication. */
std::vector<double> matvecmult(const std::vector<double> &val,
                               const std::vector<int>    &row_ptr,
                               const std::vector<int>    &col_idx,
                               const std::vector<double> &vec,
                               const int                 rowsize);
/* Performs scalar vector multiplication. */
std::vector<double> vecScalarMult(const std::vector<double> &vec,
                                  const double scalar);
/* Adds up or performs subtraction of two vectors. */
std::vector<double> vecvecAddition(const std::vector<double> &vec1,
                                   const std::vector<double> &vec2,
                                   const bool addition);
#endif /* matvecops_HPP */


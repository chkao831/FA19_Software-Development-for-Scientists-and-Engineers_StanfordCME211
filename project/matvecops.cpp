/**
 * @file matvecops.cpp
 * @author Chih-Hsuan Kao   
 * Contact: chkao831@stanford.edu
 * Date: Nov 18, 2019
 * This file contains functions to perform common vector and matrix operations 
 * that occur in CG algorithm. 
 */

#include <cmath>
#include <iostream>
#include <vector>
#include "matvecops.hpp"

/** Function calculateL2Norm()
  * This function calculates the l2 norm of a given vector. 
  * @param &vec a reference to a vector<double>
  * @return norm a double that represents the l2 norm of the vector
  */
double calculateL2Norm(const std::vector<double> &vec){
    int vecsize;
    vecsize = (int)vec.size();
    double norm = 0.0;
    for(unsigned int i=0; i< (unsigned int)vecsize; i++){
        norm += vec[i] * vec[i];
    }
    norm = sqrt(norm);
    return norm;
}//end calculateL2Norm

/** Function calculateVecTrans()
  * This function calculates the inner product of two given vectors. 
  * @param &vec1 a reference to the first vector<double>
  * @param &vec2 a reference to the second vector<double> 
  * @return vectrans a double that represents the inner prod of two vectors
  */
double calculateVecTrans(const std::vector<double> &vec1,
                         const std::vector<double> &vec2){
    int vecsize;
    vecsize = (int)vec1.size();
    double vectrans = 0.0;
    for(unsigned int i=0; i<(unsigned int)vecsize; i++){
        vectrans += vec1[i] * vec2[i];
    }
    return vectrans;
}//end calculateVectranspose

/** Function matvecmult()
  * This function performs matrix and vector multiplication.
  * @param &val a reference to vector<double> that stores matrix value  
  * @param &row_ptr a reference to vector<int> that stores row pointer
  * @param &col_idx a reference to vector<int> that stores column value
  * @param &vec a reference to a vector<double> in the multiplication
  * @param int rowsize is an integer that represents the row/col size of 
  *                    matrix (square) and the length of vector
  * @return sol a vector<double> that is the solution. 
  */
std::vector<double> matvecmult(const std::vector<double> &val,
                               const std::vector<int>    &row_ptr,
                               const std::vector<int>    &col_idx,
                               const std::vector<double> &vec,
                               const int                 rowsize){
    unsigned int start;
    unsigned int end;
    unsigned int col;
    double matval;
    std::vector<double> sol;
    
    //iterate through row pointer
    for(unsigned int i = 0; i < (unsigned int)rowsize; i++){
    //current row is i
        start = (unsigned int)row_ptr[i];
        end = (unsigned int)row_ptr[i+1];
        double sum = 0;
        //iterate through column value in this row and multiply by vector
        for(unsigned int j = start; j < end; j++){
            col = (unsigned int)col_idx[j];
            matval = (double)val[j];
            sum += matval * (double)vec[col];
        }
        sol.push_back(sum);
    }
    return sol;
}//end matvecmult

/** Function vecScalarMult()
  * This function performs scalar vector multiplication. 
  * @param &vec a reference to a vector<double>  
  * @param scalaer a double scalar
  * @return vecResult the resulting scaled vector<double> 
  */
std::vector<double> vecScalarMult(const std::vector<double> &vec,
                                  const double scalar){
    std::vector<double> vecResult(vec.size()); 
    for (unsigned int i = 0; i<vec.size(); i++){
        vecResult[i] = (vec[i]*scalar) ;
    }
    return vecResult;
}//end vecScalarMult

/** Function vecvecAddition()
  * This function adds up or performs subtraction of two vectors.
  * @param &vec1 a reference to the first vector<double>
  * @param &vec2 a reference to the second vector<double>
  * @param addition a boolean variable. If true performs addition; 
  *                 if false performs subtraction. 
  * @return vecResult the resulting vector<double> 
  */
std::vector<double> vecvecAddition(const std::vector<double> &vec1,
                                   const std::vector<double> &vec2,
                                   const bool addition){
    std::vector<double> vecResult(vec1.size());
    for (unsigned int i = 0; i<vec1.size(); i++){
        if(addition == true){
            vecResult[i] = (vec1[i] + vec2[i]);
        } else {
            vecResult[i] = (vec1[i] - vec2[i]);
        }
    } 
    return vecResult;
}//end vecvecAddition

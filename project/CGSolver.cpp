/**
 * @file CGSolver.cpp
 * @author Chih-Hsuan Kao
 * Contact: chkao831@stanford.edu
 * Date: Dec 9, 2019
 * CSR format of matrix is passed into solver.
 * The main functionality of this file is to use Conjugate Gradient Algorithm
 * to iterate through a matrix and find solution.
 */

#include <fstream>
#include <iomanip>
#include <iostream>
#include <vector>

#include "CGSolver.hpp"
#include "matvecops.hpp"
#include "sparse.hpp"

/**CGSolver()
 * This function takes in A, b in linear system Ax=b and initial guess of x
 * with all ones, as well as tolerance (a threshold) and performs CG.
 * @param b  reference to vector<double> that represents RHS of system
 * @param x  reference to vector<double> which is a initial guess
 * @param tol a double that serves as a threshold as break condition in algo
 * @param soln_str a string that contains solution prefix passed from command line
 * @param T_x_vec a double vector that contains the bottom row temperature
 * @param Th double that contains value of top row temperature
 * @param collength the number of column in the matrix system
 * @return niter the number of iterations taken upon convergence
 */
int CGSolver(SparseMatrix        A,
            std::vector<double> &b,
            std::vector<double> &x,
            double              tol,
            std::string        soln_str,
            std::vector<double> &T_x_vec,
            double              Th,
            int                 collength){

    //Use getter to obtain private attributes of SparseMatrix
    const std::vector<int>& row_ptr = A.GetRowPtr();
    const std::vector<int>& col_idx = A.GetColIdx();
    const std::vector<double>& val = A.GetCSRVal();
    
    int rowsize;
    rowsize = static_cast<int>(row_ptr.size() - 1);
    std::vector<double> r0;
    r0 = matvecmult(val,row_ptr,col_idx,x,rowsize);
    r0 = vecvecAddition(b,r0,false);
    //decalre current r_n and r_n+1
    std::vector<double> r;
    std::vector<double> r_next;
    //initialize p
    std::vector<double> p;
    p = r0; //deep copy
    //initialize L2norm_r0 and declare L2norm_r
    double L2norm_r0;
    L2norm_r0 = calculateL2Norm(r0);
    double L2norm_r;
    //initialize niter to count iteration
    int niter = 0;
    //declaration for intermediate usage
    std::vector<double> A_p;
    std::vector<double> alpha_p;
    std::vector<double> alpha_Ap;
    std::vector<double> beta_p;

    std::string txtstr = ".txt";

    //start of CG algorithm
    while(niter < rowsize){
        if(niter == 0){
            //initially let current residual to be r0
            r = r0;
        }
        niter = niter + 1;
        A_p = matvecmult(val,row_ptr,col_idx,p,rowsize);
        double alpha = calculateVecTrans(r,r) / calculateVecTrans(p,A_p);
        alpha_p = vecScalarMult(p,alpha);
        x = vecvecAddition(x,alpha_p,true);
        alpha_Ap = vecScalarMult(A_p,alpha);
        r_next = vecvecAddition(r,alpha_Ap,false);
        L2norm_r = calculateL2Norm(r_next);
        if((L2norm_r/L2norm_r0)<tol){
            break;
        }
        double beta = calculateVecTrans(r_next,r_next) / calculateVecTrans(r,r);
        beta_p = vecScalarMult(p,beta);
        p = vecvecAddition(r_next,beta_p,true);
        r = r_next;

        //write to file in the convergence process
        if(niter == 1 || niter % 10 == 0){
            //do something
            std::ofstream file;

            std::string newfilestring = soln_str + std::to_string(niter) + txtstr;

            file.open(newfilestring);
            for(unsigned int i=0; i < (unsigned)T_x_vec.size(); i++){
                file << T_x_vec[i] << std::endl;
            }
            for(unsigned int i=0; i < (unsigned)rowsize; i++){
                file << std::setprecision(5) << x[i] << std::endl;
            }
            for(unsigned int i=0; i < (unsigned)collength; i++){
                file << Th << std::endl;
            }
            file.close();
        }
    }//end while
    

    //output last iteration to file
    std::ofstream lastfile;
    std::string lastfilestring = soln_str + std::to_string(niter) + txtstr;

    lastfile.open(lastfilestring);
    
    for(unsigned int i=0; i < (unsigned)T_x_vec.size(); i++){
        lastfile << T_x_vec[i] << std::endl;
    }
    for(unsigned int i=0; i < (unsigned)rowsize; i++){
        lastfile << std::setprecision(5) << x[i] << std::endl;
    }
    for(unsigned int i=0; i < (unsigned)collength; i++){
        lastfile << Th << std::endl;
    }

    lastfile.close();
    
    if(niter == rowsize){
        return -1;
    }

    return niter;
}//end CGSolver

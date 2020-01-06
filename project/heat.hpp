/**
* @file heat.hpp
* @author Chih-Hsuan Kao
* Contact: chkao831@stanford.edu
* Date: Dec 9, 2019
* Prototype of heat.cpp
*/

#ifndef HEAT_HPP
#define HEAT_HPP

#include <stdio.h>
#include <string>
#include <vector>

#include "sparse.hpp"

class HeatEquation2D
{
  private:
    SparseMatrix A;
    std::vector<double> b, x;
    double length;
    double width;
    int matrixsize;
    double h;
    double T_c;
    double T_h;
    double T_x;
    std::vector<double> T_x_vec;
    std::string input_prefix;
    
  public:
    /* Method to setup Ax=b system */
    int Setup(std::string inputfile);

    /* Method to solve system using CGsolver */
    int Solve(std::string soln_prefix);

    /* Default Constructor */
    HeatEquation2D();

};

#endif /* HEAT_HPP */


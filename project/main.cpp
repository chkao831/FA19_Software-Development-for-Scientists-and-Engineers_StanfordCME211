
/**
 * @file main.cpp
 * @author Chih-Hsuan Kao
 * Contact: chkao831@stanford.edu
 * Date: Dec 9, 2019
 * The main functionality is to load an input file from command line,
 * in which information describing heat geometry is contained.
 * Then, by creating HeatEquation2D and calling its function,
 * the linear system is generated and solved using CG Algorithm.
 */

#include <iostream>
#include <string>

#include "heat.hpp"

int main(int argc, char *argv[])
{
  //Get command line arguments
  if (argc != 3)
  {
    std::cout << "Usage:" << std::endl;
    std::cout << "  " << argv[0] << " <input file> <soln prefix>" << std::endl;
    return 0;
  }
  std::string inputfile = argv[1];
  std::string soln_prefix = argv[2];

  /* Setup 2D heat equation system */
  HeatEquation2D sys;
  int status = sys.Setup(inputfile);
  if (status)
  {
    std::cerr << "ERROR: System setup was unsuccessful!" << std::endl;
    return 1;
  }

  /* Solve system using CG */
  status = sys.Solve(soln_prefix);
  if (status)
  {
    std::cerr << "ERROR: System solve was unsuccessful!" << std::endl;
    return 1;
  }

  return 0;
}

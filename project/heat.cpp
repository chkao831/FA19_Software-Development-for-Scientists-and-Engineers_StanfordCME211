/**
* @file heat.cpp
* @author Chih-Hsuan Kao
* Contact: chkao831@stanford.edu
* Date: Dec 9, 2019
* From passed-in input file, set up SparseMatrix object with corresponding
*right hand side vector b. Then with solve function, call CGSolver.
*/

#include <fstream>
#include <iostream>
#include <math.h>
#include <stdio.h>
#include <string>
#include <vector>

#include "CGSolver.hpp"
#include "heat.hpp"
#include "sparse.hpp"

/* Default Constructor */
HeatEquation2D::HeatEquation2D(){
    this -> A = SparseMatrix();; //A is SparseMatrix
    this -> b = std::vector<double>();
    this -> x = std::vector<double>();
    
    this -> length = 0;
    this -> width = 0;
    this -> matrixsize = 0;
    this -> h = 0;
    this -> T_c = 0;
    this -> T_h = 0;
    this -> T_x = 0;
    this -> T_x_vec = std::vector<double>();
    this -> input_prefix = std::string();
}
 
/**Setup()
* This function takes in inputfile and set up matrix A
* @param inputfile input file string
* @return 0 upon successful setup; -1 if failed
*/
int HeatEquation2D::Setup(std::string inputfile){
    std::ifstream inputf;
    int self;
    bool booLeft;
    bool booRight;
    double x;
    double expon;
    double l;

    //know which inputfile is read in (get number)
    input_prefix = inputfile.substr(5,1);
    
    inputf.open(inputfile);
    if(inputf.is_open()){
        
        inputf >> length >> width >> h;
        length /= h;
        width = width/h - 1;
        
        inputf >> T_c >> T_h;

        inputf.close();

    } else {
        //if failed to open file, print out error message and return
        std::cout << "Failed to open file" << std::endl;
        return -1; //indicate failure
    }
    
    //set SparseMatrix Dimension
    matrixsize = (int)width*(int)length;
    A.Resize(matrixsize,matrixsize);
    //call A.addEntry() to modify matrix and modify b
    for(int row = 1; row <= width; row++){
        for(int col = 1; col <= length; col++){
            //locate current self
            self = int(col + (row-1)*length);
            //test for left boundary
            if(col==1){ //reached left
                booLeft = true;
                booRight = false;
            } else if(col==length) { //reached right
                booRight = true;
                booLeft = false;
            } else { //not on left or right boundary
                booLeft = false;
                booRight = false;
            }
            
            //test for lower boundary
            if(row == 1){ //reached lower
                x = h*col;
                l = length * h;
                expon = -10*(pow(x-(l/2),2));
                T_x = -T_c*(exp(expon)-2);
                T_x_vec.push_back(T_x);
                
                b.push_back(pow(h,-2)*T_x);
                if(booLeft==true){ //reached lower and left, not modify down
                    A.AddEntry(self-1,(self+(int)length-1)-1,-pow(h,-2));//special left
                    A.AddEntry(self-1,(self+1)-1,-pow(h,-2));//right
                    A.AddEntry(self-1,(self+(int)length)-1,-pow(h,-2));//up
                    A.AddEntry(self-1,self-1,4*pow(h,-2));//self
                } else if(booRight==true){ //reached lower and right, not modify down
                    A.AddEntry(self-1,(self-(int)length+1)-1,-pow(h,-2));//special right
                    A.AddEntry(self-1,(self-1)-1,-pow(h,-2));//left
                    A.AddEntry(self-1,(self+(int)length)-1,-pow(h,-2));//up
                    A.AddEntry(self-1,self-1,4*pow(h,-2));//self
                } else { //reached lower yet neither right nor left, not modify down
                    A.AddEntry(self-1,(self-1)-1,-pow(h,-2));//left
                    A.AddEntry(self-1,(self+1)-1,-pow(h,-2));//right
                    A.AddEntry(self-1,(self+(int)length)-1,-pow(h,-2));//up
                    A.AddEntry(self-1,self-1,4*pow(h,-2));//self
                }
            //test for upper boundary
            } else if(row == width) { //reached upper
                //std::cout << "-pow(h,-2)*T_h is " << -pow(h,-2)*T_h << std::endl;
                b.push_back(pow(h,-2)*T_h);
                if(booLeft==true){ //reached upper and left, not modify up
                    A.AddEntry(self-1,(self+(int)length-1)-1,-pow(h,-2));//special left
                    A.AddEntry(self-1,(self+1)-1,-pow(h,-2));//right
                    A.AddEntry(self-1,(self-(int)length)-1,-pow(h,-2));//down
                    A.AddEntry(self-1,self-1,4*pow(h,-2));//self
                } else if(booRight==true){ //reached upper and right, not modify up
                    A.AddEntry(self-1,(self-(int)length+1)-1,-pow(h,-2));//special right
                    A.AddEntry(self-1,(self-1)-1,-pow(h,-2));//left
                    A.AddEntry(self-1,(self-(int)length)-1,-pow(h,-2));//down
                    A.AddEntry(self-1,self-1,4*pow(h,-2));//self
                } else { //reached upper yet neither right nor left, not modify up
                    A.AddEntry(self-1,(self-1)-1,-pow(h,-2));//left
                    A.AddEntry(self-1,(self+1)-1,-pow(h,-2));//right
                    A.AddEntry(self-1,(self-(int)length)-1,-pow(h,-2));//down
                    A.AddEntry(self-1,self-1,4*pow(h,-2));//self
                }
            } else { //not reached lower nor upper boundary
                b.push_back(0);
                if(booLeft==true){
                    A.AddEntry(self-1,(self+(int)length-1)-1,-pow(h,-2));//special left
                    A.AddEntry(self-1,(self+1)-1,-pow(h,-2));//right
                    A.AddEntry(self-1,(self+(int)length)-1,-pow(h,-2));//up
                    A.AddEntry(self-1,(self-(int)length)-1,-pow(h,-2));//down
                    A.AddEntry(self-1,self-1,4*pow(h,-2));//self
                } else if(booRight==true){
                    A.AddEntry(self-1,(self-(int)length+1)-1,-pow(h,-2));//special right
                    A.AddEntry(self-1,(self-1)-1,-pow(h,-2));//left
                    A.AddEntry(self-1,(self+(int)length)-1,-pow(h,-2));//up
                    A.AddEntry(self-1,(self-(int)length)-1,-pow(h,-2));//down
                    A.AddEntry(self-1,self-1,4*pow(h,-2));//self
                } else { //absolutely interior
                    A.AddEntry(self-1,(self-1)-1,-pow(h,-2));//left
                    A.AddEntry(self-1,(self+1)-1,-pow(h,-2));//right
                    A.AddEntry(self-1,(self+(int)length)-1,-pow(h,-2));//up
                    A.AddEntry(self-1,(self-(int)length)-1,-pow(h,-2));//down
                    A.AddEntry(self-1,self-1,4*pow(h,-2));//self
                }
            }
        }//inner for loop (col-wise)
    }//outer for loop (row-wise)

    return 0; //complete for loop--success
}//end Setup

/**Solve()
* This function takes in solution prefix and call CGSolver
* @param soln_prefix solution file prefix
* @return 0 upon successful solve; -1 if failed to converge
*/
int HeatEquation2D::Solve(std::string soln_prefix){
    //call COO2CSR on matrix A to convert in place
    A.ConvertToCSR();
    std::vector<double> x;
    x.assign((unsigned)matrixsize,1);
    double tolerance = 1.e-5;
    int iteration = 0;
   
    //customize (hard-code) solution format
    std::string sol = soln_prefix + input_prefix + "_";
    iteration = CGSolver(A,b,x,tolerance,sol,T_x_vec,T_h,(int)length);

    //if does not converge in CG
    if(iteration==-1){
        return -1;
    }
    
    //if CG succeeds, print to console
    std::cout << "SUCCESS: CG solver converged in " << iteration << " iterations." << std::endl;
    return 0;
}


#define ROW 201 //define a static array height
#define COLUMN 201 //define a static array width
#include <fstream>
#include <iostream>
#include <string>
using namespace std;

/* This file, mazesolver.cpp, implements the right hand wall following algo. 
 * This program confirms appropriate command line arguments, set up static
 * array with specific size, find maze entrance in the first row and use
 * the right-hand algo to move through the maze until reaching the last row
 * and exiting the last position. This program would write its position to 
 * a text file. 
 */

/**
 * @file mazesolver.cpp
 * @author Chih-Hsuan Kao
 * Contact: chkao831@stanford.edu
 * Date: Nov 3, 2019
 */

/** Forward declaration
  * Signature of identifiers prior to its usage
  */
bool checkForward(int dir, int r, int c);
bool checkRight(int dir, int r, int c);
int moveForward(int dir, ofstream& fout);
int turnLeft(int dir);
int turnRight(int dir);

/* Global variable declaration */
int entryRow; //entry is (0,entryCol)
int entryCol; //entry is (0,entryCol)
int exitRow;  //exit is (exitRow,exitCol)
int exitCol;  //exit is (exitRow,exitCol)
int currentRow; //keeps track of current position (row) in maze 
int currentCol; //keeps track of current position (col) in maze 
int rowsize; //height of this maze
int colsize; //width of this maze
int direction; //keeps track of current position (row) in maze 
int a[ROW][COLUMN]; //static array with prespecified size
fstream f; //input fstream
ofstream fout; //output fstream


/** Main function: start of the program
  * This function reads in command line arguments, stores the maze in a 
  * static array by putting binary 1 if wall is present. 
  * Then, it would find entrance and exit index of the maze. 
  * Then, using the right hand following algorithm, the function would move 
  * through the maze and finally store the path in pairs into a text file
  * specified by the user in command line. 
  * @param argc an int variable representing the number of arguments
  * @param argv a char variable representing the arguments from command line
  * @return 0 (int variable)
  * @throws overflow_error Thrown if the static array a is not large enough
  *                        for the storage of the maze. 
  */
int main(int argc, char** argv){
    //open inputfile
    f.open(argv[1]);
    //open outputfile
    fout.open(argv[2]);
    //verify appropriate command line arguments
    if(argc < 3){
        cout << "Usage:" <<endl;
        cout << "./mazesolver <maze file> <solution file>" << endl;
        exit(1); //terminate with error
    }
    //if appropriate, read in the maze and store in matrix a
    short loop=0; //keep track of line
    string line;
    string delimiter = " "; //as two numbers in line are separate by a space
    if(f.is_open()){
        while(getline(f,line)){
            //token1 stores the first number and token2 stores the second 
            string token1 = line.substr(0, line.find(delimiter));
            string token2 = line.substr(line.find(delimiter)+1,line.length());
            int t1 = std::stoi(token1);
            int t2 = std::stoi(token2);
            //first line contains the number of rows and cols respectively
            if(loop==0){
                rowsize = t1;
                colsize = t2;
                //confirm there is sufficient storage space in the array
                //in RunTime, if not, throw exception
                if(rowsize>ROW || colsize>COLUMN){
                    throw std::overflow_error("Static Array too small");
                }
            } else {
                a[t1][t2] = 1;
            }
            loop++;
        }
    }//end if file open
    f.close(); //close the input maze file
    
    /** For debugging usage: 
    Matrix entry printing: row by row from top left to bottom right
    
    for(int x=0; x<rowsize; x++){
        for(int y=0; y<colsize; y++){
            cout << "x,y = (" << x << "," << y << ")" <<endl;
            cout << a[x][y] << endl;
        }
    }
    */
    
    //iterate through first row of maze, find entrace
    for(int c=0; c<colsize; c++){
        if(a[0][c] !=1){
            entryRow = 0;
            entryCol = c;
        }
    }
    //iterate through last row of maze, find exit
    for(int c=0; c<colsize; c++){
        if(a[rowsize-1][c] !=1){
            exitRow = rowsize-1;
            exitCol = c;
        }
    }
    
    //direction is an int variable that keeps track of current direction
    //in the maze; in my setting, 
    //direction = 1 means heading East
    //direction = 2 means heading West
    //direction = 3 means heading South
    //direction = 4 means heading North
    direction = 3; //by default, starting direction is South    
    currentRow = entryRow;
    currentCol = entryCol;
    fout << currentRow << " " << currentCol << endl;
    //As long as not arrived the exit, keep moving through the maze
    while(currentRow!=exitRow || currentCol!=exitCol){
        //if the RHS is open, turn right and move a step forward
        if(checkRight(direction,currentRow,currentCol)){
            turnRight(direction);
            moveForward(direction,fout);
        //otherwise, if the RHS is closed but front is open, move forward
        } else if(checkForward(direction,currentRow,currentCol)){
            moveForward(direction,fout);
        //now if RHS and front are both closed, turn left
        } else {
            turnLeft(direction);
        }
    }//end finding target, arrived the exit. 
    fout.close(); //close the output file
    return 0;
}//end main()

/** checkForward: This function helps determine if there's wall in the front.
 * case 1: heading east; 2: west; 3: south; 4: north. 
 * @param dir an int variable indicating the current direction
 * @param r an int variable indicating the current row
 * @param c an int variable indicating the current column
 * @return true if the front is open; false otherwise
 */
bool checkForward(int dir, int r, int c){
    switch(dir){
        case 1:
            if(a[r][c+1]!=1){
                return true;
                break; 
            } else { return false; }
        case 2:
            if(a[r][c-1]!=1){ 
                return true; 
                break; 
            } else { return false; }
        case 3: 
            if(a[r+1][c]!=1){ 
                return true; 
                break; 
            } else { return false; }
        case 4:
            if(a[r-1][c]!=1){ 
                return true; 
                break; 
            } else { return false; }
	    return false;
    }//end switch
    return false;
}//end checkForward method

/** checkRight: This function helps determine if there's wall at the right.
 * case 1: heading east; 2: west; 3: south; 4: north. 
 * @param dir an int variable indicating the current direction
 * @param r an int variable indicating the current row
 * @param c an int variable indicating the current column
 * @return true if the right is open; false otherwise
 */
bool checkRight(int dir, int r, int c){
    switch(dir){
        case 1:
            if(a[r+1][c]!=1){ 
                return true; 
                break; 
            } else { return false; }
        case 2:
            if(a[r-1][c]!=1){
                return true; 
                break;
            } else { return false; }
        case 3: 
            if(a[r][c-1]!=1){
                return true; 
                break; 
            } else { return false; }
        case 4:
            if(a[r][c+1]!=1){ 
                return true; 
                break; 
            } else { return false; }
        return false;
    }//end switch
    return false;
}//end checkRight method

/** moveForward: This function moves the position one step forward.
 * case 1: heading east; 2: west; 3: south; 4: north. 
 * @param dir an int variable indicating the current direction
 * @param fout an output fstream to which the path should be written to
 * @return 0 (int)
 */
int moveForward(int dir, ofstream& fout){
    switch(dir){
        case 1:
            currentCol += 1; 
            fout << currentRow << " " << currentCol << endl; 
            return 0; 
            break;
        case 2:
            currentCol -= 1;
            fout << currentRow << " " << currentCol << endl; 
            return 0; 
            break;
        case 3:
            currentRow += 1;
            fout << currentRow << " " << currentCol << endl; 
            return 0; 
            break;
        case 4:
            currentRow -= 1;
            fout << currentRow << " " << currentCol << endl; 
            return 0; 
            break;
    }//end switch
    return 0;
}//end moveForward method

/** turnList: This function changes the direction 90 degree to the left
 * case 1: heading east; 2: west; 3: south; 4: north. 
 * @param dir an int variable indicating the current direction
 * @return 0 (int)
 */
int turnLeft(int dir){
    switch(dir){
        case 1:
            direction = 4; //to North
            return 0; break; 
        case 2:
            direction = 3; //to South
            return 0; break;
        case 3:
            direction = 1; //to East
            return 0; break;
        case 4:
            direction = 2; //to West
            return 0; break;
    }//end switch
    return 0;
}//end turnLeft method

/** turnRight: This function changes the direction 90 degree to the right
 * case 1: heading east; 2: west; 3: south; 4: north. 
 * @param dir an int variable indicating the current direction
 * @return 0 (int)
 */
int turnRight(int dir){
    switch(dir){
        case 1:
            direction = 3; //to South
            return 0; break; 
        case 2:
            direction = 4; //to North
            return 0; break;
        case 3:
            direction = 2; //to West
            return 0; break;
        case 4:
            direction = 1; //to East
            return 0; break;
    }//end switch
    return 0;
}//end turnRight method


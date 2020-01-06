#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <string>

#include "Stock.hpp"

int main(int argc, char * argv[]) {

    /* Read in command line arguments */
    if(argc != 3){
        std::cout << "Usage:" << std::endl;
        std::cout << "./main <textfile> <stockticker>" << std::endl;
        return 0; //terminate
    }
    
    std::fstream f;
    std::string ticker;
    double current_term;
    int count = 0;
    ticker = argv[2];
    std::vector<double> term; //to catch each line
    f.open(argv[1]);
    if(f.is_open()){
        while(f >> current_term){
            /* Import prices to std::vector<double> */
            term.push_back(current_term);
            count = count + 1;
        }
        f.close();
    } else {
        std::cerr << "fail to open input file" << std::endl;
        return 1;
    }
    
    /* Call the Stock class constructor */
    Stock thisstock(term,ticker);
    /* Perform reqired calculations */
    std::string result1 = thisstock.getTicker();
    thisstock.dailyReturn();
    double result2 = thisstock.meanReturn();
    double result3 = thisstock.varReturn();
    
    std::cout << result1 << std::endl;
    std::cout << result2 << std::endl;
    std::cout << result3 << std::endl;
    
    /* Write out to results.txt */
    std::string outputfilename = "results.txt";
    std::ofstream fout; //output
    fout.open(outputfilename);
    if(fout.is_open()){
        fout << result1 << std::endl;
        fout << result2 << std::endl;
        fout << result3 << std::endl;
        fout.close();
    } else {
        std::cerr << "fail to open output file" << std::endl;
        return 1;
    }
    return 0;
}


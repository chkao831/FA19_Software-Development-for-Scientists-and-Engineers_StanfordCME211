//
//  Stock.cpp
//  Final
//
//  Created by Chih-Hsuan Kao on 12/5/19.
//  Copyright © 2019 Chih-Hsuan Kao. All rights reserved.
//

#include <vector>
#include <string>
#include <fstream>
#include <iostream>

#include "Stock.hpp"

/* Ordinary Constructor */
Stock::Stock( std::vector<double> price_vec, std::string tckr){
    this -> returnmean = -2.0;
    this -> size = price_vec.size();
    this -> stockname = tckr;
    this -> price = price_vec;
    this -> returnvec = std::vector<double>(size-1,0.0);
}//end constructor

std::vector<double> Stock::dailyReturn(){
    //initialize the vector to be returned
    double p_cur;
    double p_pre;
    double p_return;
    for(unsigned int i=0; i<size-1; i++){
        p_pre = price[i];
        p_cur = price[i+1];
        p_return = (p_cur - p_pre)/p_pre;
        returnvec.push_back(p_return);
    }

    return returnvec;
}//end dailyReturn

double Stock::meanReturn(){
    double sum = 0.0;
    for(double p : returnvec){
        sum = sum + p;
    }
    sum = sum / (size-1);
    returnmean = sum;
    return sum;
}//end meanReturn

double Stock::varReturn(){
    if(returnmean == -2.0){
        meanReturn();
    }
    double eachterm;
    double summation = 0.0;
    for(double p : returnvec){
        eachterm = p - returnmean;
        eachterm = eachterm * eachterm;
        summation = summation + eachterm;
    }
    summation = summation / (size-2);
    return summation;
}//end varReturn

/* ticker getter */
std::string Stock::getTicker(){
    return stockname;
}

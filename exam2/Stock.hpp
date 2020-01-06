//
//  Stock.hpp
//  Final
//
//  Created by Chih-Hsuan Kao on 12/5/19.
//  Copyright © 2019 Chih-Hsuan Kao. All rights reserved.
//

#include <vector>
#include <string>

class Stock {
    private:
        /* private member variables */
        double returnmean;
        unsigned long size;
        std::string stockname;
        std::vector<double> price;
        std::vector<double> returnvec;
        

    public:

        /* public member variables */

        //constructor
        Stock( std::vector<double> price_vec, std::string tckr);
         
        //calculate daily return
        std::vector<double> dailyReturn();

        //calculate mean return
        double meanReturn();
        
        //calcualte return variance
        double varReturn();
        
        /* add additional methods as needed */
        std::string getTicker();
};

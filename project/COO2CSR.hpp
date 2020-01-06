//
//  COO2CSR.hpp
//  project
//
//  Created by Chih-Hsuan Kao on 11/28/19.
//  Copyright © 2019 Chih-Hsuan Kao. All rights reserved.
//

#ifndef COO2CSR_HPP
#define COO2CSR_HPP

#include <vector>

/* In place conversion of square matrix from COO to CSR format */
void COO2CSR(std::vector<double> &val,
             std::vector<int>    &i_idx,
             std::vector<int>    &j_idx);

#endif /* COO2CSR_HPP */

CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wextra -Wpedantic -Wconversion
TARGET := main
CPP := main.cpp CGSolver.cpp matvecops.cpp COO2CSR.cpp heat.cpp sparse.cpp
HPP := CGSolver.hpp matvecops.hpp COO2CSR.hpp heat.hpp sparse.hpp

main: $(CPP) $(HPP)
	$(CXX) -O3 $(CXXFLAGS) -o $(TARGET) $(CPP)

.PHONY: clean
clean: 
	rm *.o *~ $(TARGET)

1.1
A. (3) i and n are both intergers, so it is valid to initialize i with the value of n.
B. (2) matrix[4][3] is an out-of-bound access, which is an undefined behavior and it is not safe.
C. (3) array[0] and dt are both double type,  so it is valid to initialize array[0] with the value of dt.
D. (1) n has been declared as an integer, so it is invalid to redefine it as a double type variable.

E. 0 is expected to be printed. The reason is that the 8 bit representation of 255 is 11111111, and 
after adding 1 it becomes 00000000, which represents 0.
F. When modelling probability, we don't want probability of zero. But when multiplying a series of very small
probabilities, we might get some values of zeros due to underflow problem. This is not desired in our
numerical calculation. This is because in machine calculation, double type has some lower limit. 

1.2
A. (1) Stack is fixed memory allocation, while heap can contain data of arbitrary size.
    (2) Stack is limited to local variables, heap is global scope.
B. Because stack is limited to local variables, and stack memory is automatically managed by compiler.
After the make_triplet function is called, the stack memory which stores (1, 3, 5) or (1, 2, 3) will be freed.
So we cannot access triplet[1] as we expect in main function.
C. Because heap memory is global scope and managed by programmer, the values which triplet[0],  
triplet[1], triplet[2] store in make_triplet function can also be accessed in main function.
D.Yes. Because after a heap memory is created, we do not  delete the pointer to interger. 
E. We can use vector on stack instead of creating array (using new) on heap. In this case, we only
need deep copy of three integers, not their references.


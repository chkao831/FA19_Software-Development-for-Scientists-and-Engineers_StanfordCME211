Design Considerations In the separate markdown file README.md, describe and justify your design choices by answering the following questions;
//
• What data members (attributes, variables) does the Stock class have? Are they public or private, and justify your choice.

A: I set all attributes to be private such that they cannot be accessed by outside of class. 
Encapsulation provides data hiding and more control on the member variables. 
On the other hand, if an attribute is public, then anyone can access it and can assign any value to it, which is not secure and it goes against the OOP design concept. That's why I provided a getter for stock ticker for user to get access to it from program main().
The private attributes include:
returnmean a double that represents the mean of each return
size an int that represents the size of stock prices from the input file
stockname a string that represents the stock ticker (stock name)
price a double vector that stores the price of stock (from input file); vector length is size
returnvec a double vector that stores the return of stock; vector length is size-1
//
• What arguments do your dailyReturn and meanReturn functions accept, and why?

A: I have stored important information as class attributes. Attributes are characteristics of an object. 
For a single stock, from an OOP perspective, it becomes more clear to program user when we
represent all information regarding the stock object as the stock instances, instead of passing
in additional arguments while calling functions outside of the class. Hence, both functions accept
no argument in my design. 

//
• What considerations did you make to minimize repetitive calls?

A: I created a std::vector<double> returnvec as a Stock class private attribute within the class. 
This helps minimize repetitive calls primarily because I know I need to get access to it for multiple 
times throughout the task, but if I don't do so and instead create new double vecs (deep copy) every
time when I need it, not only it's not efficient storage-wise but also it generates unnecessary calls. 
Such an approach, by the way, is similar to passing by reference. Secondly, in my varReturn() function, 
we do a condition check
if(returnmean == -2.0){
    meanReturn();
}
which not only avoids errors when dividing by zero if mean function not called before var function, 
but also minimizes calling mean function for the second time if it's already called by the program user. 

//
• Discuss whether the keyword new appears in your program, and why this is appropriate.

A: I didn't create anything on heap. From the review lecture, it is pointed out that Herb Sutter says we should
always prefer to user vectors[] instead of arrays (created on Heap). Firstly, programmer does not have to worry about memory allocation and deallocation of stack variables.  If a programmer does not handle heap memory well, memory leak can happen, which is disastrous. Additionally, access time on stack is faster and cost is less. 

//
• Discuss ONE of the following: (1) an aspect of your program that you are proud of or (2) a possible improvement to your program, or (3) if you did not finish the assignment, the next step needed to fix the program.
Include as part of your README.md the command used to compile your program.

A: (1) I am proud of the OOP design. OOP is a software design pattern that allows users to think about 
problems in terms of objects and their interactions. It also allows future users to utilize, for example, 
to do other stock calculation in the future. The encapsulation characteristics also bind together the data
and functions that manipulate data, keeping both safe from outside interference and misuse. 

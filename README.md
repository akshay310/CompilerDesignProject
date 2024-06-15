This mini project is designed with the key objective of implementing the initial phases of a 
compiler, specifically focusing on lexical analysis and syntax analysis for a provided code 
snippet. In the lexical analysis phase, the program takes the source code as input and produces 
output in the form of tokens. This phase serves as a tokenizer by removing extraneous 
elements such as spaces, new lines, and comment lines from the program. 

The subsequent step involves the creation of a parse table containing entries for both 
terminals and non-terminals identified within the code. To prepare for the parse table 
generation, we employ a recursive method to determine the FIRST and FOLLOW sets for each 
terminal. The final stage centers on parsing, utilizing the standard CLR parsing steps.  

The project's deliverables encompass not only the identification of parsing actions executed 
by the grammar for both valid and invalid source code but also the generation of a parse table 
tailored to the provided input. This comprehensive approach aims to lay the foundation for a 
robust and efficient compiler for the given programming language


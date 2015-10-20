Create complex data types
like c, this would be all the fields stored on contiguous memory. this could be the oposite as the reference memory model. 
this should be solved in order to have compatibility with c libraries.

C:
struct X{
	int i;
	char a,b,c;
}

Z:
comp X:
	int i
	char a, b, c
	
X x
x.a = 'a'

# P1: 
	Refs Pointers.
	IF variables inside a struct behaves like normal variables and we use the reference model,
	we need a way to state that the variables will be non-referencial (normal memory-based model of C) 
	ie, like a normal C variable.
	The compiler could take the effective address of each variable and use internally the reference model anyway.
	
	A: Add a notation to the class, stating that the variables are memory locations. 
		
		full comp X:
			int i
			char a, b, c
			
	B: add notation to the variable itself, allows for more control
		The notation should be decided later. Is better if its not similar to C symbols (*&)
		C: 
		struct X{
			int i; 
			char a, *b;
		}
		Z:
		comp X:
			int *i
			char *a,b
			

# P2:
	Allow for function pointers
	comp X:
		int a, b, c
		int fun F(int i) #might change
			
			
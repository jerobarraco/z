The most complex part because this is what needs more modifications
Pointers:
One variable has ownership
copy is explicit

Problems:
	ownership
	automatic deleting
	small types (byte<integer)
	structures
		Fields wouldn't be stored as contiguous memory.
			needed for library compatibility with C
			maybe there could be a notation for a direct-variable, just like there's a notation for a pointer.
			or a notation in the struct declaration (this could be better)
	
Proposal

In C by default everything is copied. That makes data more controllable, and avoid mistakes like
stepping on another data. But on the other side, it creates too many copies of a value. When you
are working with structures this can lead to problems like cache misses and slow code.

There are 3 basic stages when working with data.
1) Passing a value to a function and returning
2) Assigning a value to a variable
3) Creating a new value from an expression

Usually there's no actual need to share a memory location, and modify that memory and read from many 
places. But is usual to use the same value to pass it around for many places (write once read many).
So, even if we don't need the address, copying the value makes it slower without purpose.
By making pointers an explicit thing, it makes the use of them too complicated (also the syntax sucks).

The compiler can optimize this, but any compiler optimization is working against the tao, because
it reduces predictability and makes optimization a hit/miss, and is not constant.

In 1) there's no need to copy the value every time. Most of the times, we only need to pass a value that
will be used in a calculation, never modified.
So, to optimize the code we need to use "const type &v" is too much for something that should be the 
common way to use a function.
In 2) there's no actual need to copy anything.
in 3) we can simply create a new value and store a reference in the variable, leaving the old value
untouched. Just like in python. This requires some sort of ownership control if we want to controll
the memory. Garbage collection is not an option (thought it CAN (and prolly will) be implemented as a lib).

RAII is desirable. Most c++ ppl brag on this being the most wanted feature.
It would be desired that the compiler manages the memory in a similar way than c. 
That is, creates the memory for a variable when it's defined (or assigned), and releases it when it gets
out of scope.

# P1
A way to avoid the need for a GC is to give each variable an OWNING flag.
Each time a variable releases the a value reference (is asigned a new value, or gets out of scope), if 
it is the OWNER, then the memory gets freed. if not, it ignores it.
And each time a variable is assigned to another (ie a=b), passed to a function or returned by one,
the variable which is "more global" gets the OWNING flag.

The problem with this is when 2 variables at the same level of "globality" shares a reference. 
In most cases that is the equivalent to share pointers in C, which requires extra control from the 
developer, so Z has no need to add complexity to solve this, it can simply be managed by the developer
in the same way (check for null).

A problem that could be solved is this case.
Reference sharing, then the OWNER gets another value, but there's another var still referencing.
Z:
	int a = 10
	int b = a
	#Here a is the owner
	a = 20 # if we don't add any rule, as a is the OWNER, 10 gets deleted and b gets a lost reference
	b ?
	
A solution would be to hold a table with "equivalent variables", that holds all the variables in the
same level pointing to the same value. And when one of those values gets another value, it is removed
from that row, when the last one gets removed, the value gets destroyed.

Another one is using the same idea, but using simply a refcount, when it reaches 0, it gets destroyed.
When a variable in the same level gets assigned, the refcount gets added. When that var gets out-of-scope
it gets decremented. And when the value gets assigned to a var of a more global level, the refcount
gets resseted to 1.

Both solutions require more memory and are not thread safe probably.

When dealing with pointers there are several scenarios.
1) Data sharing: Just pass some data without copying.
2) Memory Sharing: Share a memory position so that you could modify it and it gets modified in
the other variable.
3) Variable sharing? Something weird, but sometimes we need a pointer of a pointer, so we can modify
a variable pointing at other.
4) Random Memory Access. Pointer arithmetics. 

1) This is not a problem
2) This requires an special notation to tell the compiler to overwrite the memory position
3) Requires notation for reverse reference (address reference)
4) Also special notation, maybe like 3. 

# Ex 1
1) 
int *a, *b = new int;
*a = 10;
b = a;
....
delete a;

z:
	int a, b; #una variable no inicializada es un puntero a NULL
	a = 10# new int; *a=10;
	b = a #ambos apuntan al mismo lugar
	.....
	#fuera de scope
	#delete a (because a is the OWNER) (or because a and b are out of scope and reefcount is 2)
	
On functions
int &f(const int &i){
	return i*2;
}
int a = 10;
int b = f(a)

z: 
	func f(int i):
		return i*2
	int a = 10
	int b = f(i)

Sharing memory
void f(const int &i){
	i = 20;
}

int a;
f(a);

z:
	func f(int i):
		&i = 20#the notation needs to be decided
		#this declares that the value will be stored on the memory referenced,
		#and the variable isnt changing references
	int a = 10; #needs to have some memory assigned
	f(a)
	
3) Variable modification
void f(int *&a){
	a = new int;
	
}
int *a;
f(a)
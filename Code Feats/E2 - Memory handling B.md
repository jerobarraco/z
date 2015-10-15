Refered from Variables and Pointers

Related to _Pointers_ and _E1 Memory Handler_

One possible solution is to divide the values into two sets:
	1. PODs (Plain old datatypes)
	2. Complex

# 1 PODs
These types have the particularity of being handled by assembly
(most of the time) and fit in a register.
This means that storing a reference to them is a loss of time and memory
And also the spected behaviour is to overwrite the value.
Just like inmutable objects:
	a = 7
	b = a
	a = 8
	You don't expect that b is 8 now

So this could be handled in the "normal way". A POD variable will represent
a memory space. hence it can be _written into_ and _referenced_.
Will work like normal C style variables.

# Complex datatypes
As the register sizes are determined, there's no actual way to create a 
complex datatype that can fit in one register.
There's a possible far fetched situation in which it does.
(Like when floating point coprocessors didnt exists)
then the calculations can be "created" from scratch, and
it should work directly with the binary value.
In such cases the type can be simply a redefinition (alias) of a pod
(like byte, int, long, etc).
Then, it will fall into the previous case and everything will be fine on earth.

Other complex types would be bigger than a register and hence
will need to be handled as pointers in the underlying assembly anyway.
(It could be splitted in several registers but doesnt make sense
 because it will be really hard to handle and there are no asm 
 instructions to support it, so creating a new semantic for them
 would not be really desirable, because it will need to create
 a handling code (it wont be transparent) and will beat the purpose
 of this language (be as faithful representation of asm as possible))

So, most complex datatypes are created as structures. 
Which are created based on the same blocks: 1) pods 2) other complexs
	(As this is a recursive problem we can say that if we fix the problem
	for the upper level we fix it for the lowers too)

So, _modifying_ a structure implies _overwriting_ *one* attribute
*not the whole structure* (which would be really inneficient).
It also makes sense to make a virtual copy of a complex type. 
That's because a structure has a special identity apart from its atributes by separate.
If we need to modify *all* the attributes, then, it's basically a new complex, and in such case is far more efficient to alter the reference 
and drop the last memspace.
Also, that's precisely the place where it needs to be optimized.
Example:
	C: 
	struct a;
	function(a);
	void function(struct b){
		int avalue = b.value;
		
	background memcpy from a to b. slow and unnecesary.
	b needs to be reserved, memcpy'd and then deleted.
	
	struct function(){
		return struct
	}
	struct a = function()
	
	memory reserved on function, memory also reserved on var, on return gets memcpy'd, then deleted.
	why not simply set the reference of the return to the var, if its going to be deleted anyway.
	This could be optimized in many ways:
		from inside the func
		on the return
		Or simply by knowing that the value is going to be stored, use the reserved memory for the variable as the temporal storage.

In the end, it will behave pretty much like C's array:
	The identifier is a memspace that holds a reference. 
	The memory needs to be explicitely created. Cannot be resized. 
	Passing them as parameters makes them shared (by nature).
	Accessing them is an indirection operation.
	Copy means copying the reference.
	*1 Copy the _values_ needs a special operation (memcpy)
	
*1: This could be done with a special operator to make it look nicer :)
	
In conclusion:
	1 Needs pointer handling
	2 Makes no sense to override the memory space, 
		changing the pointer is fine
	3 If any part of it needs to be changed it is a
		pod.
	4 Just like python's mutable datatypes.
	
In this sense we can "handle" the complex by it's reference always, instead of it's memory space. In such a way, a complex becomes also 
a "pod" because now it is his reference, not memspace. This solves the problem and also for its recursion (of the problem).


# Example pod:
	simple operations are the same in c
	int a, b
	#int c
	a = 7
	b = 6
	a = b
	>>> a=7, b=7 (separated memspace)
	
	c = #b
	@c = 10
	>>> a = 7, b = 10, c = 0x44
	
	c = c-4
	@c = 20
	>>> a = 20, b = 10, c = 0x40
	
# Example complex (provisory sintax)
	struct cmp{ int x, y } 
	cmp a, b
	@cmp c
	
	1)
	a.x = 10
	a.y = 20
	b = a
	b.x = 15
	
	c = @b //notice is the same as @a
	c->y = 25
	
	__memory__
	  POD		ADDITIONAL
	a 0x60		[15|25]		0x60
	b 0x60		
	c 0x60	

	2)
	same but b = ^a instead of b=a

	__memory__
	  POD		ADDITIONAL
	a 0x60		[10|20]		0x60
	b 0x80		[15|20]		0x80
	c 0x80
	
	3) Extra
	##int d
	d = #c
	@d = #b
	(@@d).y == (@c).y = b.y
	>>> d = 0x48, c=0x80

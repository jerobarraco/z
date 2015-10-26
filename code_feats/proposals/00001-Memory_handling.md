Refered from Variables and Pointers

There are 5 basic actions that could be wanted

1) asign a VALUE to a Variables
2) use a variable in an expression to create a new value
2.2) Use 2 and store the result (1)
3) Take the address of a VALUE
4) Use the VALUE at an adress
5) Overwrite a value. Being on a variable or a calculated address.

Given that 1 and 2 are the most used ones, it would be nice to make
it natural AND efficient.
3, 4 and 5 is more "low level" stuff, direct memory handling should be
explicit, therefore no priority should be given.
Then we can think of this solution

for 1 and 2 we can use normal notation, and use a "shared memory" model.
Something like python and java reference.
(But not using GC (more on this later)).
So, instead of thinking of a variable as a memory space, we should
think them as a "tag" to access a value. 
in that sense, it's already obvious that variables are "cheaper" this
way.
	int a = 1
	int b = a
	int c = a+b

Memory ends up like this	
	A _____[1]
	B __|   |
	        | (A+B creates a new value)
	C _____[2]
	
now we do 
	b = 3
	
	A _____[1]
	B _____[3]
	C _____[2]
	
By assigning a new value, we are changing the value of B.
semantically, as we forget about memory, this is logical.
We are not talking about modifying memory, but instead naming values.
Same behaviour is natural on python. 
With exceptions of mutables (we should behave like mutables on
struct members, also doing that would be only logical, natural and
coherent in this model)

For 3, 4 and 5 we must be explicit.
Sadly i cant think (yet) of a way to make this without using new 
symbols (im open to suggestions).
Read on _E2_ about it.

# 3 Take the address
	char b = 'x'
	int add = #b
	
	_memory_
	b ____['x']		(0x40)
	a ____[0x40]	(0x60)
	

# 4 get value from address
	char val = @add
	
	_memory_
	b ____['x'] (0x40)
	val _|

	a ____[0x40]
	
	char val = @#b
	negates, and is easy to read too.

# 5 Overwrite value
	char a = 'x'
	char c = 'p'
	int b = #a
	
	
	a <= 'z'
	_memory_
	a ____['z']		0x40
	b ____[0x40]
	
	
	@b <= 'y'
	_memory_
	a ____['y']		0x40
	b ____[0x40]
	
	
	@b <= @(#a+1) 
	_memory_
	a ____['p']		0x40
	c ____['p']		0x41
	b ____[0x40]
	
	@(b+1) <= 't'
	_memory_
	a ____['p']		0x40
	c ____['t']		0x41
	b ____[0x40]
	
	
# Conclusion

This method, is feasible. But doesnt seem reasonable to implement.
I've thought it long enough, but i can't think of a way to do this 
without the need to create another operand for "Overwriting" (<=)
or some "other way to operate".
Either i make the compiler try to "guess" what type of operation 
you are trying to make (overwrite vs asignation) or i use two different
semantics to differentiate the two intentions.
But that only shows that there are two intentions inherently different.
Other way could be by differentiating betwean "pod" values and referenced 
ones. Much like Java's unboxing. Which is the same as a dual semantic.

That would make it confusing and complicated so its not really valuable.

Also sadly the nature of asm is tied to memory and shared locations.
So overwriting will be something wanted, and will ocurr more times than what is 
convenient.
On structures like arrays or structures, overwriting could be the only reasonable
thing to do.

So, C's semantic of "asignment is copy" is more natural to what assembly is doing,
also it makes the RAI behaviour more logical, and reflects the nature of 
assembly's actual working: 
	MOV actually don't move anything, it copies to another place. And the 
	registers are memory locations that exists before with no regard to their
	value.
	So its memory before value, and sometimes before address too.
	
What we could do, is focus on simplifying the pointer sintax as well as changing
the default behaviour. (Like, all vars are passed by ref unless noted 
(this has to be studied)).


possibilities
1) type after the var name
	a int
	a, b, c=0 int
	
	Not very legible
	
2) Type before var name. Similar to C

C:
	int a;
	int a = 0;
	int a, b, c=0;
Z:
	int a
	int a = 0
	int a, b, c=0

Type first, followed by variable name. 
Variable can be initialized using "= exp". 
Several variables can be separated by ","
No ending separator needed ";"

Feat 0, typed constants.
	# proposal 1
	-126ub..0ub..127ub = signed byte
	0b..255ub = unsigned byte
	0s..2^16us = ushort = 16 bit short (also s)
 	0i..2^32ui = uint = 32bit integer (also i)
	0l..2^64ul = ulong = 64bit integer (also l)
	-float..float = float
	
	# Proposal 2
	-126ub..0ub..127ub = signed byte
	0b..255b = signed byte
	0b2..2^16b2 = short = 16 bit short (also us)
 	0b3..2^32b3 = int = 32bit integer (also ui)
	0b4..2^64b4 = long = 64bit integer (also ul)
	
	
	
Feat 1 - deductive type declaration
	c: int a = 0;
	Z: a = 0i
	
	I doubt this would be of any use. And would add to confusion. It could sound too dynamic for a low level language
	
Feat -1 - same type creation 
	relative to classes, which wont be on the first version
	also relative to pointer which is not fixed yet
	1)
	c: A *a = new A();
	z: new A a();
	
	2)
	c:
		A *a;
		a = new A();
	z:
		A a;
		new a();
s	
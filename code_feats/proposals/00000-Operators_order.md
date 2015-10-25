# Operator order
One nice feature to take into account is the operator order.
Usually every operator appears anyway. Sometimes before the operand, sometimes after.
It would be nice to have the operators always appear after.
This seems natural if we think of operators as operations that could be done upon operators.
Following this we could think the operators as methods of the operands.
This could be desirable, specially if we strive to create user-defined types and overrideables operators.

The more heavily affected operators would be:

	Note that Z doesn't target the creation of "Objects" (in this first stage) so this two aren't valid examples
	creation
		new a()	-> a.new() or a()
	deletion
		delete a -> a.del() or a~ 
			This is specially interesting as it makes specially obvious that all the classes should inherit from one
			base class that handles memory for them. This could be specially powerfull but also confusing.
	
	the most problematic are the unary operator, because in C they tend to come before the operand. But that's 
	exactly what brings problem in complex expressions.
	This will likely feel unnatural, and also will look suboptimal because they'll require parenthesis for 
	some of the expressions, but that compensates to the fact that in C you depend on "operation precedence"
	and you need parethesis when they aren't obvious or play against you anyway.
	
	de/reference
		&a -> a#
		*a -> a*
		This one is interesting and is the most special case for me. 
		ie, this can create some confusion:
			*a+4	| &a+4
		While in Z this is more explicit. It is a pointer until you derreference it.
			a+4@	| a+4# nonsense but makes mandatory to write a#+4
	
	inc/dec
		a++, a--	| idem
		--a, ++a 	| doesnt exists
	negation
		looks weird on z
		not a		| a not (in z) 
		
## What about Arithmetics ¿?
In arithmetics usually [the operator stands between both operators](https://en.wikipedia.org/wiki/Infix_notation),
we could change this and use something like the [polish notation](https://en.wikipedia.org/wiki/Polish_notation) 
but i fear would be much too confusing and doesn't fit to the previous statement.
Normal arithmetics could be thought as the same (in fact c++'s operation-override works like that)

	a+b -> a.add(b)

This makes parsing much easier. And expressions would always resolve in a predictable manner.
Much like recursion or stacking results.

	a+b+c -> a.add(b.add(c))

The only problem would be to distinguish between a substraction (operation) and a negative constant (or sign negation).
This is a big problem, mostly because in school they taught us one way and it'll be hard to go against.
But secondly because the operator for sign and substraction are the same.
And also by the case that a--b is the same as a+b. Having the sign before the operand makes it obvious.
So is very probably that the sign operator will be the only exception.
(practicality beats purity?)

	-4	-> not X.sub(4) though is notable that it would be the same as 0.sub(4)
	But is not a big problem.
	
	

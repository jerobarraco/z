No extra characters. No exception.
No separator for everything.
Natural
Unobstrusive
Well done.
# NOT  DONE  BY  STATISTICS
That means: "most people do it like this" is NOT and will NOT be a acceptable argument, EVER.

[Bandwagon_effect](https://en.wikipedia.org/wiki/Bandwagon_effect)ś

# Operator order
One nice feature to take into account is the operator order.
Usually every operator appears anyway. Sometimes before the operand, sometimes after.
It would be nice to have the operators always appear after.
This seems natural if we think of operators as operations that could be done upon operators.
Following this we could think the operators as methods of the operands.
This could be desirable, specially if we strive to create user-defined types and overrideables operators.

The more heavily affected operators would be:
	
	creation
		new a()	-> a.new()
			This is specially interesting as it makes specially obvious that all the classes should inherit from one
			base class that handles memory for them. This could be specially powerfull but also confusing.
			Also note that Z doesn't target the creation of "Objects".
	
	deletion
		delete a -> a.del()
		
	de/reference
		&a -> a#
		*a -> a*
		This one is interesting and is the most special case for me. 
		ie, this can create some confusion:
			*a+4	| &a+4
		While this is more explicit that a is a pointer until you derreference it.
			a+4@	| a+4# nonsense but makes mandatory to make a#+4
	inc/dec
		a++, a--	| idem
		--a, ++a 	| doesnt exists

## What about Arithmetics ¿?
In arithmetics usually [the operator stands between both operators](https://en.wikipedia.org/wiki/Infix_notation),
we could change this and use something like the [polish notation](https://en.wikipedia.org/wiki/Polish_notation) 
but i fear would be much too confusing and doesn't fit to the previous statement.
Normal arithmetics could be thought as the same (in fact c++'s operation-override works like that)

	a+b -> a.add(b)

This makes parsing much easier. And expressions would always resolve in a predictable manner.
Much like recursion or stacking results.

	a+b+c -> a.add(b.add(c))

Only problem would be to distinguish between a substraction (operation) and a negative constant.

	-4	-> not X.sub(4) though is notable that it would be the same as 0.sub(4)
	But is not a big problem.
	
	
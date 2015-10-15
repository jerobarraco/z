What:
	Z is a "new" _language_ *designed* to replace C

What is a language:
	A language is mostly its syntax. The compiler is the compiler, 
	if i want to improve the compiler i would be making a compiler.
	For a compiled language like C, the language itself is the interface
	between the compiled code and the ideas wanted to be expressed.
	In this way, the language is how the human communicates his ideas
	and command the compiler.
	

What is design:
	design is to do things on purpose, not only because you can, and
	not because the environment forces you to.
	Is to think before doing, it is planning, is is having A goal.
	It is improvement, it is innovation, it is change.
	It is not how much you can add to something to make it cooler,
	is how much you can take from it and still having something cool.
	
Why replace C:
	I've been teaching C/++ for many years and it sucks.
	If you feel emotionally attacked for that sentence i will ask you to
	stop readning now, beacause you need to be able to accept that 
	some things could change in order to understand the idea behind all this.
	
	Ok, good bye.
	
	
	
	
	
	seriously, no need to keep reading, you should stop now.
	
	
	
	
	
	There's nothing interesting here.
	
	
	
	
	
	ok, you continue at your own risk, no complaints will be accepted. 
	Let's explore this idea together, this idea that we could have a
	different goal.
	I've been teaching C++ for 6 years now, and i especially give 
	support to people with difficulty, so i know first hand what
	are the complications people have when learning it.
	Also i'be been using c++ for some more than 6 years, so i also
	know first hand the complications in big or mid sized projects.
	The compiler is great, but the language is a joke.
	Is hard to read, hard to understand, hard to write, unintuitive,
	full of side-effects, etc. It's what i call 0D-sign (zero design).
	Is completely unnecessary, suboptimal, and a waste of time for everyone,
	from the people that teaches it, to the ones learning it; from the 
	people writing in it, to the people maintaining it.
	It will be less painful to replace it than mutate it over uncontrollably.
	

General outline of interests is this
1st Gen		2nd G		3rd Gen		Object Oriented		HLOO
Bytecode	Assembler	Z			Nimrod				Python

What should be achieved:
- Design
- - Focus on design, not on implementation. No cutting corners. No need to do that now
- - - Like Linus said "we take no crap!"
- - Low level 3rd generation.
- - - Must be able to generate code for a kernel.
- - - Compile to binary
- - - Use ASM and hardware instructions
- Abstraction
- - Abstraction layers (osi layer, too much complexity)
- c not Simple
- c old
- - c needs some new stuff like concurrency
- coherent
- - pointers, casts, by reference
- - type rewrite on new
- - typecasts
- Fast? 
- - c too slow to write on (too much overhead)
- - c lacks CISC instructions
- - c by defaults it copies everything

The Tao of Z (taken from Python (By Tim Peters))

There should be one-- and preferably only one --obvious way to do it.
In the face of ambiguity, refuse the temptation to guess.
Although that way may not be obvious at first unless you're Dutch.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Sparse is better than dense.
Flat is better than nested.
Readability counts.
Beautiful is better than ugly.
Errors should never pass silently.
Unless explicitly silenced.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!

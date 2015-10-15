One way to take the address of a variable could be 
	int b
	a = [b]
which reminds a lot to ASM (though it does the opposite), 
also i don't like using 2 characters (especially the one at the beggining)

# a = *b 
Thats horrible.
1) It confuses with arithmetic *
2) It goes BEFORE the identifier. thats aweful, specially when trying 
to take the address of a struct's member.

# a = ·b , a = b·
Nobody uses that character anyway

# a = b._address a = b._dir
Virtual members look cool :) we should consider this

# a = ^b = b^ 
Looks cool, hard to write, can put emoticons with it d^-^b

# b$
Because the address is where the money is (?) also code will be full
of B$ or M$. I dont like it, it reminds me to PHP, i don't want to be
related to THAT.

# b¬ ¬b
Unused char. cool. check if it can be easily written on any keyboard 
locale (it's on spanish (qwerty+dvorak)). Looks like negation on 
logic.

# b~ 
more similar to negation, also hard to write

# #b
Yeah why not. ethimologically means "number". So "number of b"

# @b 
hmmmmm. might be. might be. this is more for the inverse reference. 
"value 'at' b".

# b? 
Why not? "()" is an operand..

# bº
Not sure about the ethimology of it. 

import string
blank = " \t"
nl = "\n"#fuck cross platform, mywayorthehighway
blanknl = blank+nl
main_name = "_start"
letters = string.ascii_letters + "_"
nums = string.digits
hex = string.hexdigits
oct = string.octdigits

sizes = {1:'BYTE', 2:'WORD', 4:'DWORD'}#1, 2, 4 bytes
types = ['byte', 'short', 'int', 'str', 'ptr']
tsizes = [1, 2, 4, 4, 4]
trefs = types[-2:]

regs1 = [
	"ah", "al",
	"bh", "bl",
	"ch", "cl",
	"dh", "dl",
]

regs2 = [ "ax", "bx", "cx", "dx" ]
regs4 = [ "eax", "ebx", "ecx", "edx", "edi", "esi", "ebp", "esp" ]
regs = regs1 +regs2 +regs4
"""regs = [
	"eax", "ax", "ah", "al",
	"ebx", "bx", "bh", "bl",
	"ecx", "cx", "ch", "cl",
	"edx", "dx", "dh", "dl",
	"edi", "esi", "ebp", "esp"
]
"""
cmps = {
	"==": "je",
	"<": "jl",
	">": "jg",
	"!=": "jne",
	"<=":"jle",#the operator is important in this way
	">=": "jge"
}#Todo fix

cmpsn = {
	"==": "jne",
	"<": "jnl",
	">": "jng",
	"!=": "je",
	"<=":"jg",#the operator is important in this way
	">=": "jl"
}#Todo fix


class Hell(Exception):pass

class Basic:
	def __init__(self, name="", lvl=0):
		self.res = self.name = name
		self.l = lvl
		self.asm = []

	def result(self):
		print (" > !STUB basic.result")
		from parsers import exp
		if isinstance(self.res, exp.Identifier):
			return self.res
		return exp.Identifier(self.res, self.l, "int")

	def __str__(self):
		return "".join(map(str, self.asm))
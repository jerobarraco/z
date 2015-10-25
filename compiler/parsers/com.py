import string
blank = " \t"
nl = "\n"#fuck cross platform, mywayorthehighway
blanknl = blank+nl
main_name = "_start"
letters = string.ascii_letters + "_"
nums = string.digits
hex = string.hexdigits
oct = string.octdigits
x86 = False

sizes = {1:'BYTE', 2:'WORD', 4:'DWORD', 8:'QWORD'}#1, 2, 4 bytes
types = ['byte', 'short', 'int', 'long', 'str', 'ptr']
type_f = ['float', 'double']# floating point types, not implemented yet
tsizes = [1, 2, 4, 4, 4]
trefs = types[-2:]

regs1_32 = [ "ah", "al", "bh", "bl", "ch", "cl", "dh", "dl",
			"sp", "bp", "si", "di", "spl", "bpl", "sil", "dil"]
regs1 = regs1_32 +['r8b', 'r9b', 'r10b', 'r11b', 'r12b', 'r13b', 'r14b', 'r15b']
#2 Bytes (16 bits)
regs2_32 = [ "ax", "bx", "cx", "dx" ]
regs2 = regs2_32 +['r8w', 'r9w', 'r10w', 'r11w', 'r12w', 'r13w', 'r14w', 'r15w']
#4 Bytes (32 bits)
regs4_32 = [ "eax", "ebx", "ecx", "edx", "edi", "esi", "ebp", "esp" ]
regs4 = regs4_32 + ['r8d', 'r9d', 'r10d', 'r11d', 'r12d', 'r13d', 'r14d', 'r15d']
#8 Bytes (64 bits)
regs8 = [ "rax", "rbx", "rcx", "rdx", "rdi", "rsi", "rbp", "rsp" ,
		"r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15" ]
regs16 = [ "xmm"+str(i) for i in range(16)]

regs = regs1 +regs2 +regs4 +regs16

call_regs_i = ("rdi", "rsi", "rdx", "rcx", "r8", "r9")
call_regs_f = tuple(("xmm"+str(i) for i in range(8)))
# http://i.imjpggur.com/Sx9agGN.

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
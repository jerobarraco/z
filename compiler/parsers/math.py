#coding: utf-8
"""Should be "arithmetic" but math is shorter"""
__author__ = 'nande'

from parsers import com, asm
from parsers.com import Hell


class Add(com.Basic):
	def __init__(self, a, b, lvl=0, c='' ):
		n = "add "+str(a)+"+"+str(b)
		if not c: c = n
		super().__init__(n, lvl)
		#todo support different sizes
		reg = "rax"
		if reg in (a.n, b.n):
			reg = "rdx"
			if reg in (a.n, b.n):
				reg = "rcx"

		self.asm = []
		self.asm.append(asm.Asm("mov %s, %s"%(reg, a.ref()), lvl, "add op 1"))
		self.asm.append(asm.Asm("add %s, %s"%(reg, b.ref()), lvl, "add op 2"))
		self.res = reg
		#adc can be used to add two-register-long numbers (ie 64b on 32b)

class Sub(com.Basic):
	def __init__(self, a, b, lvl=0):
		n = "sub "+str(a)+"+"+str(b)
		super().__init__(n, lvl)
		#todo support different sizes
		reg = "rax"
		if reg in (a.n, b.n):
			reg = "rdx"
			if reg in (a.n, b.n):
				reg = "rcx"

		self.asm = []
		self.asm.append(asm.Asm("mov %s, %s"%(reg, a.ref()), lvl, "sub op 1"))
		self.asm.append(asm.Asm("sub %s, %s"%(reg, b.ref()), lvl, "sub op 2"))
		self.res = reg

class DivMod(com.Basic):
	def __init__(self, a, b, lvl=0, is_div=True):
		n = "sub "+str(a)+"+"+str(b)
		super().__init__(n, lvl)
		ds = b.size
		#todo support different sizes
		#todo every literal is always 4, this will tend to be 4
		op = {1:self.do1, 2:self.do2, 4:self.do4, 8:self.do8}
		op[b.size](a, b, is_div)

	def do1(self, a, b, isdiv):
		raise Hell("> i cant divide size 1")

	def do2(self, a, b, isdiv):
		raise Hell("> i cant divide size 2")

	def do4(self, a, b, isdiv):
		raise Hell("> i cant divide size 1")

	def do8(self, a, b, isdiv):
		#http://www.csee.umbc.edu/portal/help/nasm/sample.shtml#intarith
		#IDIV r/m64 (no inmediate support!) Signed divide RDX:RAX by r/m64, with result stored in RAX ← Quotient, RDX ← Remainder.
		#rax=rcx/r8;
		#xor  rdx, rdx   ; clear high bits of dividend
		#mov  rax, rcx   ; copy dividend argument into rax
		#idiv r8         ; divide by divisor in scratch register
		from parsers.exp import Assign, Identifier
		self.asm = []
		#used registers
		rega = "rax"
		regb = "rdx"
		regc = "rcx"
		#1st check registers collisions, we will need to use rax and rdx. and also avoid colissions with the operands
		#order is important, i shuld check both vars in both ifs, but i don't want, so it will be unefficient
		#if a==rcx and b==rax then we are screwed
		#check if the other operand is not rax
		if b.n in (rega, regb) or b.is_const :
			reg_to_b = a.n=="rcx" and "r8" or "rcx" #if a is rcx use r8
			#here we could move a to rega (if b!=rax and a!=rcx) but i don't want to duplicate my code... so inefficient will be
			#get another register to store it to
			new_b = Identifier(reg_to_b)
			self.asm.append(Assign(new_b, b, self.l), "move B to rcx")
			b = new_b

		#now rax is unused, move A there if necesary
		if a.n != rega: #if they are the same, no need to move
			new_a = Identifier(rega)
			self.asm.append(Assign(new_a, a, self.l, "copy dividend to rax"))
			a = new_a

		#mov rdx,0 ; avoid error
		self.asm.extend( [
			asm.Asm("xor rdx, rdx", self.l, "clear the high bits"), #this is used to divide 16 by 8 Bytes
			asm.Asm("idiv qword %s"%(b.ref(),), self.l, "divide double register rdx:rax by B"),
		] )
		self.res = isdiv and rega or regb

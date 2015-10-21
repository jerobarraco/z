#coding: utf-8
"""Should be "arithmetic" but math is shorter"""
__author__ = 'nande'

from parsers import com, asm

class Add(com.Basic):
	def __init__(self, a, b, lvl=0, c='' ):
		n = "add "+str(a)+"+"+str(b)
		if not c: c = n
		super().__init__(n, lvl)
		reg = "eax"
		if reg in (a.n, b.n):
			reg = "edx"

		self.asm = []
		self.asm.append(asm.Asm("mov %s, %s"%(reg, a.ref()), lvl, "add op 1"))
		self.asm.append(asm.Asm("add %s, %s"%(reg, b.ref()), lvl, "add op 2"))
		self.res = reg
		#adc can be used to add two-register-long numbers (ie 64b on 32b)

class Sub(com.Basic):
	def __init__(self, a, b, lvl=0):
		n = "sub "+str(a)+"+"+str(b)
		super().__init__(n, lvl)
		reg = "eax"
		if reg in (a.n, b.n):
			reg = "edx"

		self.asm = []
		self.asm.append(asm.Asm("mov %s, %s"%(reg, a.ref()), lvl, "sub op 1"))
		self.asm.append(asm.Asm("sub %s, %s"%(reg, b.ref()), lvl, "sub op 2"))
		self.res = reg

class DivMod(com.Basic):
	def __init__(self, a, b, lvl=0, is_div=True):
		n = "sub "+str(a)+"+"+str(b)
		super().__init__(n, lvl)
		ds = b.size
		#todo every literal is always 4, this will tend to be 4
		op = {1:self.do1, 2:self.do2, 4:self.do4}
		op[b.size](a, b, is_div)

	def do1(self, a, b, isdiv):
		pass
	def do2(self, a, b, isdiv):
		pass
	def do4(self, a, b, isdiv):
		#http://www.csee.umbc.edu/portal/help/nasm/sample.shtml#intarith
		#c=c/a;
		#mov	eax,[c]	 	; load c
		#mov	edx,0		; load upper half of dividend with zero
		#idiv	dword [a]	; divide double register edx eax by a
		#mov	[c],eax		; store quotient into c
		from parsers.exp import Assign, Identifier
		self.asm = []
		rega = "eax"
		regb = "edx"
		regc = "ecx"
		if a.n == regc:
			regc = "ebx"

		if (b.n in (rega, regb)) or b.is_const:
			self.asm.append(Assign(Identifier(regc), b, self.l))
		else:
			regc = b.ref()
		self.asm.extend( [
			asm.Asm("mov %s, %s"%(rega, a.ref()), self.l, "dividend"),
			asm.Asm("mov edx, 0", self.l, "upper half of dividend"),
			asm.Asm("idiv dword %s"%(regc,), self.l, "divide double register edx:eax by regc"),
		 ] )
		self.res = isdiv and rega or regb

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
		if a.n == reg:
			reg = "edx"

		self.asm = []
		self.asm.append(asm.Asm("mov %s, %s"%(reg, a.ref()), lvl, "add op 1"))
		self.asm.append(asm.Asm("add %s, %s"%(reg, b.ref()), lvl, "add op 2"))
		self.res = reg
		#adc can be used to add two-register-long numbers (ie 64b on 32b)

class Sub(com.Basic):
	def __init__(self, a, b, lvl=0, c='' ):
		n = "sub "+str(a)+"+"+str(b)
		if not c: c = n
		super().__init__(n, lvl)
		reg = "eax"
		if a.n == reg:
			reg = "edx"

		self.asm = []
		self.asm.append(asm.Asm("mov %s, %s"%(reg, a.ref()), lvl, "sub op 1"))
		self.asm.append(asm.Asm("sub %s, %s"%(reg, b.ref()), lvl, "sub op 2"))
		self.res = reg

class IncDec(com.Basic):
	def __init__(self, a, lvl=0, c='', is_inc=True ):
		n = "incdec "+str(a)
		if not c: c = n
		super().__init__(n, lvl)
		op = is_inc and "inc" or "dec"
		self.asm = [asm.Asm(op + a.ref(), lvl, c),]
		self.res = a
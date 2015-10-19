#coding: utf-8
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

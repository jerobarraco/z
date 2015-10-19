#coding:utf-8
from parsers import com, asm, exp

class Exit:
	def __init__(self, c=0, l=0):
		self.c = c
		self.l = l
		s = [	";exiting!",
			 	"mov eax, 1",
			 	"mov ebx, %s"%self.c,
			 	"int 80h  ;byebyecruelworld",
				""]
		self.asms = [ asm.Asm(i, l) for i in s ]

	def __str__(self):
		return "".join(map(str, self.asms))

class Fun:
	insts = None
	name = ""
	def __init__(self, name="", l=0, taip=None, params=[]):
		self.insts = []
		self.l = l
		self.ps = params
		#if name == "main": name = "_start" #TODO fix
		self.name = name
		self.taip = taip

	def __str__(self):
		n = self.name.n
		is_main = n == "main"
		true_name = is_main and com.main_name or n
		lines = []
		if is_main:
			lines.append(str(asm.Asm("section .text", self.l, " ; code goes here")))
			lines.append(str(asm.Asm("global "+true_name, self.l, " ;entry point")))
			if true_name != "_start":
				lines.append(str(asm.Asm("_start:", self.l-1)))
		lines.append(str(asm.Asm(true_name+":", self.l-1)))
		lines.extend([
			 str(i) for i in self.insts
	 	])

		if is_main:
			lines.append(str(Exit(0, self.l)))
		else:
			lines.append(str(asm.Asm("ret", self.l, "; end "+true_name )))
		lines.append("\n")
		return "".join(lines)

def parse_proc(r, lvl=0):
	print("got a 'fun' line buff is", repr(r.l), "level is", repr(r.level))
	mylvl = lvl
	r.getWhile(com.blank)
	taip = exp.get_ident(r)
	if taip.is_type:
		r.getWhile(com.blank)
		name = exp.get_ident(r)#r.getWhile(com.letters)
	else:
		name = taip
	#name = r._getTill(" (:\n")#TODO this whill consume extra chars between funcname and (
	r.getWhile(com.blank)
	if not r.get("("): raise Exception ("Expected '(' ")
	print("myname is", repr(name))
	r.getWhile(com.blank)
	pars = exp.get_params(r)
	if not r.get(")"):
		raise Exception("Expected )")
	r.getWhile(com.blank)
	if not r.get(":"):
		Exception("Expected ':'")
	r.getWhile(com.blank)
	r.getWhile(com.nl)
	l = r.level
	proc = Fun(name, l, pars)
	print ("level is ", r.level)

	block = exp.get_block(r, mylvl)
	proc.insts.extend(block)
	return str(proc)
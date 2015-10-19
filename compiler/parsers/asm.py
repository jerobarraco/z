#coding:utf-8
from parsers import com

class Asm:
	def __init__(self, inst=0, lvl=0, com=""):
		self.inst = inst
		self.lvl = lvl
		self.com = com

	def __str__(self):
		s =  (self.lvl*"\t")+self.inst
		if self.com:
			s += " ;"+self.com
		s += com.nl
		return s

class PushPop(com.Basic):
	def __init__(self, ident, ispush=True, lvl=0):
		super().__init__(str(ident), lvl)
		self.i = ident
		a = ispush and "push " or "pop "
		if not ident.is_reg:
			a += com.sizes[ident.size] + " "
		a += ident.ref()
		self.asm = [ Asm(a, lvl) ]

def parse_asm_line(r, lvl=0):
	print("inside asm_line")
	r.lstrip()
	line = r.getTill("\n")
	if line[-1] == "\n": line =line[:-1]
	print ("got asm line", repr(line))
	#global p
	#p.writeAsm(line)
	return Asm(line, lvl)

def parse_asm(r, lvl =0):
	print("got an asm line buff is,",repr(r.l))
	mylvl = lvl
	print ("level is ", mylvl)
	r.getWhile(com.blank)
	if not r.get(":"): Exception("no : after asm")
	r.stripBlankLines()
	#r._getWhile(com.blank)
	#r._getWhile(com.nl)
	l = r.level
	print ("level is ", r.level)
	if l<=mylvl:#todo use getblock
		print("level is wrong, quit ", mylvl, l)
		return
	lines = []
	while r.level >mylvl :
		print("inside asm")
		lines.append(parse_asm_line(r, mylvl))
		r.stripBlankLines()
	return list(map(str, lines))

#coding:utf-8
from parsers import com

class Asm:
	def __init__(self, c=0, l=0, com=""):
		self.c = c
		self.l = l
		self.com = com

	def __str__(self):
		s =  (self.l*"\t")+self.c
		if self.com:
			s += " ;"+self.com
		s += com.nl
		return s

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
	if l<=mylvl:
		print("level is wrong, quit ", mylvl, l)
		return
	lines = []
	while r.level >mylvl :
		print("inside asm")
		lines.append(parse_asm_line(r, mylvl))
		r.stripBlankLines()

	return map(str, lines)

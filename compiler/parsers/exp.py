#coding:utf-8
import traceback
from urllib.response import addbase
from parsers.com import letters, blank, blanknl, nl, nums, Hell
from parsers import asm


class Basic:
	def __init__(self, name="", lvl=0):
		self.name = name
		self.l = lvl
		self.asm = []
	def __str__(self):
		return "".join(map(str, self.asm))

#It is necessary that the procedure preserve the contents of the registers ESI, EDI, EBP, and all segment registers. If these registers are corrupted, it is possible that the computer will produce errors when returning to the calling C program.
#When C executes the function call to Sum, it pushes the input arguments onto the stack in reverse order, then executes a call to Sum.
#the assembly code returns the value of the result to the C program through EAX implicitly.
"""Assembly can return values to the C calling program using only the EAX register. If the returned value is only four bytes or less, the result is returned in register EAX. If the item is larger than four bytes, a pointer is returned in EAX which points to the item. Here is a short table of the C variable types and how they are returned by the assembly code:

Data Type	Register
char	AL
short	AX
int, long, pointer (*)	EAX
"""
_types = ['byte', 'short', 'int', 'str', 'ptr']
_tsizes = [1, 2, 4, 4, 4]
_trefs = _types[-2:]
_sizes = {1:'BYTE', 2:'WORD', 4:'DWORD'}#1, 2, 4 bytes
_regs = [
	"eax", "ax", "ah", "al",
	"ebx", "bx", "bh", "bl",
	"ecx", "cx", "ch", "cl",
	"edx", "dx", "dh", "dl",
	"edi", "esi", "ebp", "esp"
]
_cmps = {
	"==": "je",
	"<": "jl",
	">": "jg",
	"!=": "jne",
	"=<":"jle",#the operator is important in this way
	"=>": "jge"}#Todo fix

class FunCall(Basic):#todo move to fun?
	def __init__(self, name="", lvl=0, params=[]):
		super().__init__(name, lvl)
		self.name = name
		self.l = lvl
		#for now pass params on the stack by value
		#todo modify Identifier to be able to get type information
		self.params = params
		self.asm = []

		if self.name == "sys":
			self.asm.append(asm.Asm("int %s"%params[0], lvl))
			return

		params = list(reversed(params))
		s =  "push %s %s"
		for i, p in enumerate(params):
			size = p.is_ref and 4 or p.size
			self.asm.append(asm.Asm(s%(_sizes[size], p.ref()), lvl+1, "%s param %s"%(self.name, i)))

		self.asm.append( asm.Asm("call "+name, lvl) )
		totsize = sum([i.size for i in params])
		if totsize:
			self.asm.append( asm.Asm("add esp, "+str(totsize), lvl, "end %s"%self.name))

"""DB - Define Byte. 8 bits
DW - Define Word. Generally 2 bytes on a typical x86 32-bit system
DD - Define double word. Generally 4 bytes on a typical x86 32-bit system"""
#TODO until i make a way to keep account of identifiers and their types, everything must be a DD
#so functions can return safely

class Var:
	def __init__(self, name="", val=0, t="int", lvl=0):
		self.name = name
		self.l = lvl
		self.v = val
		self.t = t
		if isinstance(t, Identifier):
			if not t.is_type :
				print ("the type is unknown:", t)
			t = str(t)

		if t in ("int", "short", "long"):
			v = {"byte":"db", "short":"dw", "int":"dd"}
			self.asm = [ asm.Asm(name.n+": "+v[t]+" "+str(val), lvl), ]
		elif t == "str":
			val = str(val)
			self.asm = [
				asm.Asm(name.n+": db '"+val+"',0", lvl),
				asm.Asm(name.n+"Len: dd %s"%len(val), lvl)
				#TODO until i have a way to get the information of the variables everything must be dd for calling functions
			]

	def __str__(self):
		return "".join(map(str, self.asm))

class Assign(Basic):
	def __init__(self, name="", val="", lvl=0):
		super().__init__(name, lvl)
		#if isinstance(val, Identifier) or isinstance(val, int):
		#	val = str(val)
		self.v = val
		#ops = [ (i.is_ref and "[%s]"%i or str(i) ) for i in (self.name, self.v)]
		#if self.name.is_ref and self.v.is_reg:
		#	s = _sizes[self.v.size]
		#	ops[1] = s+ " "+ ops[1]
		#if isinstance(val, Cmp):
		#	#if its a comparison let's put some tricks
		self.asm = [asm.Asm("mov %s, %s"%(self.name.ref(), self.v.ref()), self.l),]

class Cmp(Basic):
	def __init__(self, cmp="==", ops=[], lvl = 0):
		super().__init__("", lvl)
		self.ops = tuple([i.ref() for i in ops])
		self.j = _cmps[cmp]

	def falseJumpTo(self, tag=None):
		self.asm = [
			asm.Asm( "cmp %s, %s"%self.ops, self.l),
		]
		if tag :# note that setting tag to none effectively "removes" the jump
			self.asm.append(asm.Asm(self.j+" "+tag, self.l, "jump to true, below must be jmp to false"))#enough space to put the "false unconditional jump"


class Condition(Basic):
	def __init__(self, cmp, true=[], false=[], lvl = 0):
		super().__init__("", lvl)
		self.false = "_false_%s"%id(self)
		self.end = "_end_%s"%id(self)
		cmp.falseJumpTo(self.false)
		self.asm = [ cmp ]
		#TODO if there is no false, dont jump after true
		self.asm.extend(true)
		self.asm.append(asm.Asm("jmp "+self.end, lvl))
		self.asm.append(asm.Asm(self.false+":", lvl))
		self.asm.extend(false)
		self.asm.append(asm.Asm(self.end+":", lvl))

class Identifier:
	size = 4
	mytype = "int"
	is_ref = False
	is_type = False
	is_reg = False
	def __init__(self, name="", lvl=0, taip = "int"):
		self.n = name
		self.l = lvl
		self.const = False
		self.checkConstant()
		self.setType(	(name in _types) and "type" or taip	)

	def checkConstant(self):
		self.const = False
		if self.n and self.n.isdigit():
			self.const = True
			self.setType(_types[2])

	def setType(self, t):
		self.mytype = t
		self.is_type = self.mytype == "type"
		try :
			self.size = _tsizes[_types.index(t)]
		except:
			self.size = 4

		self.is_ref = False
		self.is_reg = sum(map(self.n.startswith, _regs))>0
		if not self.is_type:
			self.is_ref = not (self.const or self.is_reg )#t in _trefs
			if self.mytype in _trefs:
				self.is_ref = not self.is_ref# looks like an optimization, hard to explain

			#if self.is_reg:
			#	self.is_ref = False
			#	self.is_ref = not self.is_ref
	def ref(self):
		return self.is_ref and "[%s]"%self.n or self.n

	def __str__(self):
		return self.n

	def tryCall(self, r):
		try:
			r.getWhile(blank)
			if not r.get("("): #opened
				raise Exception("Expected (, not a function call")
			pars = get_params(r)
			print ("Params are ", list(map(str, pars)))
			if not r.get(")"):
				raise Exception("Expected )")
			r.getWhile(blank)
			r.getWhile(nl)
			return FunCall(str(self), self.l, pars)
		except Exception as e:
			print(e)
			print(traceback.format_exc())
			print("lol not callable expression, i don't now anything else")
		return None

	def tryLen(self, r): pass
	def tryMath(self, r): pass #this probably needs to call parse_real_exp
	def tryCmp(self, r):
		r.lstrip()
		c = r.get(list(_cmps.keys()))
		if not c : return
		other = get_ident(r)
		if not other:
			raise Exception ("other identifier expected")
		return Cmp(c, [self, other], self.l)

	def trySet(self, r):
		r.lstrip()
		if not r.get("="): return
		#todo parse_true_real_exp
		r.lstrip(True)
		i = get_ident(r)#todo parse_real_exp
		if not i:
			#i = r.getWhile(nums) #todo getNum
			raise Exception(" > value or identifier expected")
		return Assign(self, i, self.l)

class Loop(Basic):
	def __init__(self, pre, cmp, inc, block, lvl = 0):
		super().__init__("", lvl)
		#self.false = "_for_%s"%id(self)
		self.end = "_forend_%s"%id(self)
		self.start = "_forstart_%s"%id(self)
		cmp.falseJumpTo(self.end)
		self.asm = [
			pre,
			asm.Asm(self.start+":", lvl),
			cmp,
		]
		#TODO if there is no false, dont jump after true
		self.asm.extend(block)
		self.asm.append(inc)
		self.asm.append(asm.Asm("jmp "+self.start, lvl+1))
		self.asm.append(asm.Asm(self.end+":", lvl))

def get_block(r, lvl):
	insts = []
	while r.level >lvl:
		insts.extend(parse_exp(r, r.level))
		r.stripBlankLines()
	return insts

def parse_loop(r, lvl):
	r.lstrip()
	pre = parse_real_exp(r, lvl+1)

	r.lstrip()
	if not r.get(";"): raise Hell( "You need a ;")
	r.lstrip()
	cond = parse_real_exp(r, lvl+1)

	r.lstrip()
	if not r.get(";"): raise Hell( "You need a ;")
	r.lstrip()
	inc = parse_real_exp(r, lvl+1)

	r.lstrip()
	if not r.get(":"): raise Hell( "You need a :")
	r.stripBlankLines()
	block = get_block(r, lvl)
	return Loop(pre, cond, inc, block, lvl)

def parse_condition(r, lvl):
	r.lstrip()
	i = get_ident(r, lvl)
	if not i: raise Hell("identifier expected")
	c = i.tryCmp(r)
	if not c: #literal if ( ej if (x))
		c = Cmp("!=", [i, Identifier(0)])

	if not r.get(":"): raise Hell("You need the : (well not actually)")
	r.stripBlankLines()

	true = get_block(r, lvl)
	r.stripBlankLines()
	r.lstrip()
	false =  []
	if r.get(["else"]):
		r.lstrip()
		if not r.get(":"): raise Hell("What about the ':'?")
		r.stripBlankLines()
		false = get_block(r, lvl)
	return Condition(c, true, false, lvl)


def get_params(r):
	print("get_params stub, lol")
	ps = []
	while True:
		#type this is a hotfix until i make a global variables information to store definitions
		r.lstrip(True)
		t = get_ident(r)
		if not (t and t.is_type):
			print(" > No Type, no params")
			break
		#name
		r.lstrip(True)
		i = get_ident(r)
		if not i: break
		i.setType(t.n)
		ps.append(i)

		r.lstrip(True)
		r.getWhile(",")
	return ps

def get_ident(r, lvl=0):
	"""tries to get an identifier
	(type, varname, constant)"""
	#Todo restrict types of ident to pick
	#Type here only affects adressing mode,
	#ptr -> mov ecx, [val]
	#int -> mov ecx, val
	r.lstrip()
	address = bool(r.get("#"))
	r.lstrip()
	valat = bool(r.get("@"))
	r.lstrip()
	if address and valat:
		address = valat = False

	#var name
	#in case of labels: adress is "label" (int), normal is "[label]" (ptr), valat is "[[label]]" (invalid)
	#this applies to registers too!
	i = r.getWhile(letters)
	isregister = i in _regs
	if i and not isregister:
		return Identifier(i, lvl, (address and "ptr") or "int")

	#number
	#in case of number (constant): adress is "*9999" (invalid), normal is "99999" (int), valat is "[9999]" (ptr)
	s = r.get(["+", "-"])
	r.lstrip()
	n = r.getWhile(nums)
	if n or isregister:
		if not n: n = i
		if valat and s:
			if not i: i = "esp"
			n = i+s+n
		return Identifier(n, lvl, (valat and "ptr") or "int")

def parse_var(r, lvl=0):
	"""tries to parse a variable definiton"""
	#todo add to class? as "try to"
	r.getWhile(blank)
	taip = get_ident(r)
	if not taip: return

	r.getWhile(blank)
	name = get_ident(r, lvl)
	if not name : raise Exception("expected name")
	r.getWhile(blank)
	val = 0
	eq = r.get("=")

	if eq:
		r.getWhile(blank)
		tn = str(taip)
		if tn == "str":#todo use get_ident instead make val an ident
			if not r.get('"'): raise Exception("expected \"")
			val = r.getTill(['"'])
			if val[-1] == '"' : val = val[:-1]
		elif tn in _types[:3]:
			val = get_ident(r) or 0
			#val = r.getWhile(nums) or 0
	#todo pass only Idents to Var
	v = Var(name, val, taip, lvl )
	return str(v)#para sacar cuando saque los vars a los funcs

def parse_real_exp(r, lvl=0):
	"tries to parse an expression"
	#TODO this will need major refactoring when the expressions are done
	r.getWhile(blank)
	ident = get_ident(r, lvl)
	if not ident: return
	if ident.n == "pass":
		ret = asm.Asm("nop", lvl)
		r.stripBlankLines()
		return ret
	#try to see if its a calling
	for act in (ident.trySet, ident.tryCall, ident.tryLen,
				ident.tryMath, ident.tryCmp):
		ret = act(r)
		if ret : return ret

def parse_exp(r, lvl=0): #expressions are separated by \n so one liners here only, level cares not
	print ("parsing expression", repr(r.l))
	l = r.level
	insts = []
	r.getWhile(blank)
	#1str try pass
	#if r.get(["pass",]):
	#	print("just a pass")
	#	insts.append(asm.Asm("nop", lvl))
	#	r.getWhile(blank)
	#	r.getWhile(nl)
	#try var declaration
	#todo remove "var"
	if r.get(["var"]):
		parse_var(r, lvl)
	elif r.get(["if"]):
		insts.append(parse_condition(r, lvl))
	elif r.get(["for"]):
		insts.append(parse_loop(r, lvl))
	else:
		print ("is another thing ")
		t = parse_real_exp(r, lvl)
		insts.append(t)
	return insts


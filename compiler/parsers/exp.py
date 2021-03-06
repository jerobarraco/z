#coding:utf-8
import traceback
from parsers.com import letters, blank, blanknl, nl, nums, Hell, Basic
from parsers import asm, com, math

#lets have modules! Yay!
#now let's put everything important into one big file! Yay!
#todo refactor

#It is necessary that the procedure preserve the contents of the registers ESI, EDI, EBP, and all segment registers.
#If these registers are corrupted, it is possible that the computer will produce errors when returning to the calling C program.
#When C executes the function call to Sum, it pushes the input arguments onto the stack in reverse order, then executes a call to Sum.
#the assembly code returns the value of the result to the C program through EAX implicitly.
"""Assembly can return values to the C calling program using only the EAX register.
If the returned value is only four bytes or less, the result is returned in register EAX.
If the item is larger than four bytes, a pointer is returned in EAX which points to the item.
Here is a short table of the C variable types and how they are returned by the assembly code:

Data Type	Register
char	AL
short	AX
int, long, pointer (*)	EAX
"""
#why the fuck it returns char on AL but short on AX?! whats the big difference?!!!
_tsizes = [1, 2, 4, 4, 4]

_cmps = {
	"==": "je",
	"<": "jl",
	">": "jg",
	"!=": "jne",
	"<=":"jle",#the operator is important in this way
	">=": "jge"
}#Todo fix

_cmpsn = {
	"==": "jne",
	"<": "jnl",
	">": "jng",
	"!=": "je",
	"<=":"jg",#the operator is important in this way
	">=": "jl"
}#Todo fix

class FunCall(Basic):#todo move to fun?
	def __init__(self, name="", params=[], lvl=0):
		super().__init__(name, lvl)
		self.name = name
		#for now pass params on the stack by value
		#todo modify Identifier to be able to get type information
		self.params = params
		self.asm = []

		if self.name == "sys":
			self.asm.append(asm.Asm("syscall", lvl))
			return

		params = list(params)
		regs_i = list(com.call_regs_i)#creates a copy
		regs_f = list(com.call_regs_f)#creates a copy
		#for the way the call convention works you need te pass them in different order,
		# so this will be more complicated
		#1st registers
		#2nd pass the stack ones
		stack_pars = []#yo i heard you like stacks, so we use a stack for stack params
		xmms = 0
		for i, p in enumerate(params):
			reg = None
			if p.mytype in com.type_f : #not implemented lol
				if regs_f:#no, dont "and"-it to the prev if
					reg = regs_f.pop(0)
					xmms += 1 #wtf
			else:
				if regs_f:
					reg = regs_i.pop(0)

			if reg:
				ir = Identifier(reg)
				self.asm.append(Assign(ir , p, lvl+1,  "'%s' reg param %s"%(self.name, i)  ))
			else:
				stack_pars.insert(p, 0)

		stack_size = 0
		for i, p in enumerate(stack_pars):
			self.asm.append(asm.PushPop(p, False, lvl+1, "'%s' stack param %s"%(self.name, i)))
			stack_size += p.size
			#size = p.is_ref and 4 or p.size
			#self.asm.append(asm.Asm(s%(com.sizes[p.size], p.ref()), lvl+1, "%s param %s"%(self.name, i)))

		#force boundary
		boundary = stack_size % 16
		if boundary :
			self.asm.append(asm.Asm("sub rsp, %s"%boundary, lvl+1, "keep boundary aligned to 16"))
			stack_size += boundary

		#wtf why did they had to make everything SO convoluted! registers call convention is such a good idea but such a bad implementation!
		self.asm.append(asm.Asm("mov rax, %s"%xmms, lvl+1, "xmm registers"))

		self.asm.append( asm.Asm("call "+name, lvl) )
		if stack_size:
			self.asm.append( asm.Asm("add rsp, "+str(stack_size), lvl, "end %s"%self.name))

	def result(self):
		#todo func return type
		return Identifier("rax", 0, "long")

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

		if t == "str":
			val = str(val)
			val = val.replace("\\n", "',10,'")
			val = "'"+val
			if val.endswith(",'"):
				val = val[:-1]
			else:
				val += "',"
			val += "0"
			self.asm = [
				asm.Asm(name.n+": db "+val, lvl),
				asm.Asm(name.n+"Len: dd %s"%len(val), lvl)
				#TODO until i have a way to get the information of the variables everything must be dd for calling functions
			]
		else:
			#if t in ('byte', "int", "short", "long"):
			s = com.typeSize(t)
			sd = com.sizes_d[s]
			self.asm = [ asm.Asm(name.n+": "+sd+" "+str(val), lvl), ]

	def __str__(self):
		return "".join(map(str, self.asm))

class Assign(Basic):
	def __init__(self, name="", val=None, lvl=0, comm = ""):
		super().__init__(name, lvl)

		self.v = val
		#ops = [ (i.is_ref and "[%s]"%i or str(i) ) for i in (self.name, self.v)]
		#if self.name.is_ref and self.v.is_reg:
		#	s = _sizes[self.v.size]
		#	ops[1] = s+ " "+ ops[1]
		#if isinstance(val, Cmp):
		#	#if its a comparison let's put some tricks
		size = ""
		self.asm = []
		if isinstance(val, Identifier):
			src = self.v
			if self.name.is_ref and self.v.is_ref:
				size = self.name.size
				reg = com.regss[size][0] #surely an A register
				src = Identifier(reg, self.l)#here src is dest
				self.asm.append(asm.Asm("mov %s, %s"%(src, self.v.ref()), self.l, "expand mem2mem mov"),)
				#need an intermediary mov
			self.asm.append(asm.Asm("mov %s, %s"%(self.name.ref(), src.ref()), self.l, comm))
		else:
			if isinstance(val, Cmp):
				#todo improve this so a Cmp could be used just like evrything else
				#also funccall should work similarly....
				#in fact every expression should work alike, even the identifiers
				val.setToBool(self.name.size)
			#TOdO multyexpression, funccall
			if self.name.is_ref and self.v.result().is_ref:
				size = com.sizes[self.name.size]
			self.asm = val.asm[:]
			self.asm.append(asm.Asm("mov %s, %s"%(self.name.ref(), self.v.result().ref()), self.l, "store previous result"))

class Cmp(Basic):
	def __init__(self, cmp="==", ops=[], lvl = 0):
		super().__init__("", lvl)
		self.s = com.sizes[ops[0].size]
		self.ops = (self.s,)+tuple([i.ref() for i in ops])

		self.j = _cmpsn[cmp]
		self.asm = []

	def falseJumpTo(self, tag=None):
		self.asm.append( asm.Asm( "cmp %s %s, %s"%self.ops, self.l))
		if tag :# note that setting tag to none effectively "removes" the jump
			self.asm.append(asm.Asm(self.j+" "+tag, self.l, "jump to false, below is 'true'"))

	def setToBool(self, size=8):
		"""Stores a bool on a register,
		 @size is the size of the register"""
		endtag = self.newTag("toBool_end")
		falsetag = self.newTag("toBool_false")
		reg = com.regss[size][0]#an A register
		ireg = Identifier(reg)
		self.falseJumpTo(falsetag)
		#true
		self.asm.append(Assign(ireg, Identifier("-1"), self.l))
		self.asm.append(asm.Asm("jmp "+endtag, self.l))
		self.asm.append(asm.Asm(falsetag+":", self.l))
		self.asm.append(Assign(ireg, Identifier("0"), self.l))
		#end
		self.asm.append(asm.Asm(endtag+":", self.l))
		self.res = ireg
		return self.res

class Condition(Basic):
	def __init__(self, cmp, true=[], false=[], lvl = 0):
		super().__init__("", lvl)
		self.false = "_if_else_%s"%id(self)#todo newTag
		self.end = "_if_end_%s"%id(self)
		#todo if cmp is not a Cmp create a new one Cmp("!=", [cmp, "0"])
		self.asm = [ cmp ]
		self.asm.extend(true)
		if false:
			cmp.falseJumpTo(self.false)
			self.asm.append(asm.Asm("jmp "+self.end, lvl))
			self.asm.append(asm.Asm(self.false+":", lvl))
			self.asm.extend(false)
		else:
			cmp.falseJumpTo(self.end)
		self.asm.append(asm.Asm(self.end+":", lvl))

class Identifier:
	size = 8
	mytype = com.types[com.tdefault]
	is_ref = False
	is_type = False
	is_reg = False
	is_const = False
	def __init__(self, name="", lvl=0, taip = com.types[com.tdefault]):
		self.n = name
		self.l = lvl
		self.is_const = False
		self.checkConstant()
		self.setType(	(name in com.types) and "type" or taip	)

	def checkConstant(self):
		self.is_const = False
		n = self.n
		if n[0] == "-": n = n[1:]
		if n and n.isdecimal():
			self.is_const = True
			self.setType(com.types[com.tdefault])

	def setType(self, t):
		self.mytype = t
		self.is_type = self.mytype == "type"
		try :
			self.size = com.tsizes[com.types.index(t)]
		except:
			self.size = 8

		self.is_ref = False
		self.is_reg = sum(map(self.n.startswith, com.regs))>0
		if not self.is_type:
			self.is_ref = not (self.is_const or self.is_reg )#t in _trefs
			if self.mytype in com.trefs:
				self.is_ref = not self.is_ref# looks like an optimization, hard to explain
		if self.is_reg:
			if self.n in com.regs1:
				self.size = 1
			elif self.n in com.regs2:
				self.size = 2
			elif self.n in com.regs4:
				self.size = 4
			elif self.n in com.regs16: #notice skip for regs8
				self.size = 16
			else:
				self.size = 8 #default is reg8
			#if self.is_reg:
			#	self.is_ref = False
			#	self.is_ref = not self.is_ref

	def refSize(self):#shouldnt exist
		return self.is_ref and 8 or self.size

	def ref(self):
		return self.is_ref and ("[%s]"%self.n) or self.n

	def __str__(self):#todo change where this is necesary and use self.n instead, and use .ref() as __str__ (maybe)
		return self.n

	def tryCall(self, r):
		#todo fix level here, fails only on call.
		try:
			r.lstrip()
			if not r.get("("):
				raise Exception("Expected (, not a function call")
			pars = get_params(r)
			print ("Params are ", list(map(str, pars)))
			if not r.get(")"):
				raise Exception("Expected )")
			r.stripBlankLines()
			return FunCall(str(self), pars, self.l)
		except Exception as e:
			print(e)
			print(traceback.format_exc())
			print("lol not callable expression, i don't now anything else")
		return None

	def tryLen(self, r): pass
	def tryMath(self, r):
		#this probably needs to call parse_real_exp
		#todo careful to not collide with pointer arithmetic expressions
		r.lstrip()
		unary = r.get(["++", "--"])
		if unary:
			inc = (unary == "++")
			return asm.IncDec(self, self.l, is_inc = inc)
		#else
		op = r.get("+-*/%")
		if not op : return

		#todo multiexpress parse_real_expression
		i = parse_real_exp(r, self.l)
		if not i: raise Hell("identifier expected")

		if op == "+":
			return math.Add(self, i, self.l)
		elif op == "-":
			return math.Sub(self, i, self.l)
		elif op in ("/", "%"):
			is_div = (op=="/")
			return math.DivMod(self, i, self.l, is_div)
		elif op == "*":
			return math.Mult(self, i, self.l)


	def tryCmp(self, r):
		r.lstrip()
		c = None
		for i in list(sorted(_cmps.keys(), key=len, reverse=True)):
			#"get" orders just the opposite way as we need. so force it.
			#todo fix this hack
			c = r.get([i])
			if c : break
		if not c : return
		other = get_ident(r)
		if not other:
			raise Exception ("> other identifier expected got this ", repr(r.l))
		return Cmp(c, [self, other], self.l)

	def trySet(self, r):
		r.lstrip()
		if not r.get("="): return
		#todo parse_true_real_exp

		r.lstrip()
		exp = parse_real_exp(r, self.l)
		#i = get_ident(r)#todo parse_real_exp
		if not exp:
			#i = r.getWhile(nums) #todo getNum
			raise Exception(" > value or identifier expected got ",repr(r.l))
		#if isinstance(exp, Identifier):
		return Assign(self, exp, self.l)

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
		self.asm.extend(block)
		self.asm.append(inc)
		self.asm.append(asm.Asm("jmp "+self.start, lvl+1))
		self.asm.append(asm.Asm(self.end+":", lvl))

def comment(r, l):
	c = r.getTill("\n")[:-1]
	return [str(asm.Asm("", l, c)),]

def get_block(r, lvl):
	insts = []
	while r.level >lvl:
		insts.extend(parse_exp(r, r.level))
		r.stripBlankLines()
	return insts

def parsePushPop(r, ispop, lvl):
	r.lstrip()
	i = get_ident(r, lvl)
	if not i: raise Hell ("Identifier expected")
	p = asm.PushPop(i, ispop, lvl)
	return p

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
		c = Cmp("!=", [i, Identifier("0")])

	r.lstrip()
	if not r.get(":"): raise Hell("You need the : (well not actually)")
	r.stripBlankLines()

	true = get_block(r, lvl)
	r.stripBlankLines()
	_lv = r.level
	_sp = r.lstrip()
	false =  []
	if r.get(["else"]):
		r.lstrip()
		if not r.get(":"): raise Hell("What about the ':'?")
		r.stripBlankLines()
		false = get_block(r, lvl)
	else:
		r.l = _sp + r.l
		r.level = _lv
	return Condition(c, true, false, lvl)


def get_params(r):
	print("get_params stub, lol")
	ps = []
	while True:
		#type this is a hotfix until i make a global variables information to store definitions
		r.lstrip()
		t = get_ident(r)
		if not (t and t.is_type):
			print(" > No Type, no params")
			break
		#name
		r.lstrip()
		i = get_ident(r)
		if not i: break
		i.setType(t.n)
		ps.append(i)

		r.lstrip()
		r.getWhile(",")
	return ps

def get_ident(r, lvl=0):
	"""tries to get an identifier
	(type, varname, constant)"""
	#this whole thing is a big mess, this should be solved if we implement
	#de/reference as an operator & "operator always after operand" model
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
	isregister = i in com.regs
	r.lstrip()
	#this makes a problem with ++ operand, this is the easiest way i come up with (as a hack ofc)
	s = r.get(["++", "--"])
	if s: r.restore(s)
	if i and (s or not isregister):
		return Identifier(i, lvl, (address and "ptr") or "long")

	#number
	#in case of number (constant): adress is "*9999" (invalid), normal is "99999" (int), valat is "[9999]" (ptr)

	s = r.get(["+", "-"])
	r.lstrip()
	n = r.getWhile(nums)
	#todo this is a mess, should be fixed with "always post operand operation"
	if n or isregister:
		#if not n: n = i
		if valat:
			if s and n:
				if not i: i = "rsp"
				n = i+s+n
			else:
				n = i
		else: #not valat
			if i: #theres an ident, but this is not a @, so it must be an arithmetic
				r.restore(s+n)
				n = i
		return Identifier(n, lvl, (valat and "ptr") or "long")

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
		r.lstrip()
		tn = str(taip)
		if tn == "str":#todo use get_ident instead make val an ident
			if not r.get('"'): raise Exception("expected \"")
			val = r.getTill(['"'])
			if val[-1] == '"' : val = val[:-1]
		elif tn in com.tlit:
			val = get_ident(r) or 0
			#val = r.getWhile(nums) or 0
	#todo pass only Idents to Var
	v = Var(name, val, taip, lvl )
	return str(v)#para sacar cuando saque los vars a los funcs

def parse_exp(r, lvl=0): #expressions are separated by \n so one liners here only, level cares not
	print ("parsing expression", repr(r.l))
	l = r.level
	insts = []
	spaces = r.lstrip()#r.getWhile(blank)
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
	elif r.get(["??"]):
		insts.extend(comment(r, lvl))#todo, why comment returns a list?
	elif r.get(["asm"]):
		insts.extend(asm.parse_asm(r, lvl))#todo why returns list too (must be because of global)
	else:
		ret = r.get(["pop", "push"])
		if ret:
			insts.append(parsePushPop(r, ret == "pop", lvl))
		else:#todo put asm here too
			print ("is another thing ")
			t = parse_real_exp(r, lvl)
			insts.append(t)
	return insts

def parse_real_exp(r, lvl=0):
	"tries to parse an expression"
	#TODO this will need major refactoring when the expressions are done
	r.lstrip()
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
	return ident # needed to use real_exp in other expressions



#coding:utf-8
from parsers import asm, fun, com, exp

class Program:
	def __init__(self, f):
		self.f = f
	def writeAsm(self, l):
		self.f.write(l)
	def writeInst(self, ins):
		for i in ins:
			self.writeAsm(str(i))

class Reader:
	def __init__(self, f):
		self.f = f
		self.l = ""
		self.level = 0
		self._r()
		
	def _r(self):
		print("reading")
		if self.f.closed :
			print("reading a closed file! wtf no")
			self.level = -1
			return

		l = self.f.readline()
		level = 0
		#if (strip) and (l[-1]=="\n"): l = l[:-1]
		if l == "":
			self.f.close()
			print ("no moar to read")

			if self.l:
				if self.l[-1] != "\n": self.l += "\n"
			else:
				self.l = "\n"#shouldnt be a problem because f is closed now
			return
		
		print("readed final is", repr(l), "level", level)
		self.l += l

	def ensure(self, size=0):
		if len(self.l) < size:
			self._r()

	def consume(self, size=0):
		"""'eats' some chars of the buffer.
		it handles reading ahead,
		level, etc
		"""
		self.ensure(size)
		size = min(size, len(self.l))
		b = self.l[:size]
		self.l = self.l[size:]
		self.ensure(1)

		###tries level guessing. which has not much to do with actual consuming but we need to do it here
		#tries to ignore blanks at the end
		p=0
		while p<len(self.l) and self.l[p] == " ":
			p+=1

		level = 0
		#guess teh level
		#reads all the chars from the beginning, counts only the tabs,
		#stripping doesnt matter, if we are inside a multiline block it means that the normal separator (\n)
		#matters shit to that block and it uses another separator. we can mess with the level there,
		#because it means nothing.
		#fucking lvl fucks everything
		#ret = self.scanWhile("\t\n", consume=False)#consuming here will infinitely recurse (= curse and recure)
		#if ret[-1]: ret = ret[:-1]
		#len(ret.rsplit("\n", 1)[1])
		#i rather redefine
		toks = "\t\n"
		level = 0
		while p<len(self.l) and (self.l[p] in toks):
			level+=1
			if self.l[p] == "\n": level = 0
			p += 1
			self.ensure(p+1)

		if not self.l:
			print ("lol, nothing in the buf, level is -1")
			level = -1
		print("i guessed the level is", level)
		self.level = level
		return b
		#get level

	def lstrip(self, multy_line=False):
		"eats characters while they belong to a list, normally blanks"
		toks = (multy_line and com.blanknl) or com.blank
		return self.getWhile(toks, consume=True)

	def stripBlankLines(self):
		"""as i note it, the ones that needs to do "stripblanklines" are
			blocks, like the globa tokens
			because they contain many lines
			Multilines expressions should handle empty by themselves (maybe)
			and the other expressions are separated by newlines
			so, as far as the expression is on a line with something
			(which is responsibility of the callee (the blocks))
			everything is ok.
			this can also be used to clean the \n after an expression
			but be careful that doing that will skip any other character
			that might be there.
		"""
		while True:
			l = self.getTill("\n", False)
			if not l:
				break
			for i in l:
				if i not in com.blanknl:
					return
			self.consume(len(l))

	def get(self, toks=[], consume=True):
		"""allows to "check" if any token is ath the START"""
		#stripping should be explicit because it's destructive, i could makxe it not destructive but itll be confusing
		if type(toks) == str: toks = list(toks)
		toks.sort() # sorts normally by alphabetical order
		toks.sort(key=len)#sort, to avoid reading ahead if possible
		print("searching tokens=%s in s=%s"%(toks, repr(self.l)))
		for k in toks:
			lk = len(k)
			self.ensure(lk)
			if self.l.startswith(k):# i can do this because scan doesn't strip the data
				if consume:
					ret = self.consume(lk)
				return k
		return ""

	def getWhile(self, toks=[], consume=True):
		"checks if a string of possible tokens until one is different"
		p = 0
		b = ""
		while p<len(self.l) and (self.l[p] in toks):
			p += 1
			self.ensure(p+1)

		if consume:
			b = self.consume(p)
		else:
			b = self.peek(p)#we still have to inform what we scanned

		print ("scanned", p, "characters:", repr(b), " consumed?:", consume)
		return b
	'''use scanwhil(consume=true)
	def getWhile(self, toks=[]):
		"keeps consuming chars while its one of the possible"
		p = 0
		while p<len(self.l) and (self.l[p] in toks):
			p += 1
			self.ensure(p+1)
		b = self.consume(p)
		print ("stripped", p, "characters:", repr(b))
		return b
		"""t = ""
		while True:
			tt = self.scan(toks, consume=True)
			if not tt: break
			t += tt
		print("consumed", repr(t))
		return t"""
	'''

	def getTill(self, toks=[], consume=True, or_end=True):
		p = 0
		while p==0:
			ps = []
			for i in toks:
				pp = self.l.find(i)+1#notice +1
				if pp>0 : ps.append(pp)

			if ps : p = min(ps)

			if p==0:
				if self.f.closed :
					p = 0
					if or_end :
						p = len(self.l)
					break
				else:
					self._r()

		if consume:
			l = self.consume(p)
		else:
			l = self.peek(p)
		return l
			
	def peek(self, count):
		self.ensure(count)
		return self.l[:min(count, len(self.l))]

	def haveStuff(self):
		return self.l and not self.f.closed

def parse_def(l):
	print ("stub")
	return ""

parse_struct = parse_const= parse_import = parse_def

__global_tokens = {
	"asm": asm.parse_asm,
	"fun": fun.parse_proc,
	"import": parse_import,
	"struct": parse_struct,
	"const":parse_const,
	"var":exp.parse_var,#todo sacar de aca
	"·":exp.comment
	#"global":exp.parse_global_var#todo hacerlo

}

def parse_global(r, lvl=0):
	"""search for global elements
	asm:
	proc:
	import stuff
	struct:
	const:
	"""
	r.stripBlankLines()
	lv = r.level
	strip = r.lstrip()#kills level
	t = r.get(list(__global_tokens.keys()))
	if t not in __global_tokens:
		r.l = strip + r.l#restore the stuff
		r.level = lv#maybe instead of doing this shit, try to parse an expression here
		raise Exception("wtf? i don't know what to do, buffer is %s"%repr(r.l))
	instructions = []
	instructions.extend(
		__global_tokens[t](r, lv)
	)
	return instructions

def parse(r, p):
	while r.haveStuff():
		instructions = parse_global(r)
		print ("level=%s  buff='%s'" %(r.level, repr(r.l)))
		for i in instructions:
			p.writeAsm(i)


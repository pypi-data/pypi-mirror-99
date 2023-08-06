class INI:
	def __init__(self, filename, section=None, pass_section=True, trace=False, trace_verbose=1):
		self.filename = str(filename)
		self.section = section
		self.pass_section = pass_section
		self.trace = trace
		self.trace_verbose = trace_verbose

		if self.section != None:
			self.pass_section = False
		if self.pass_section == False and self.section == None:
			from .err import SectionError
			raise SectionError('`section` cannot be \'NoneType\' if `pass_section` is \'False\'')
		if self.trace == True:
			from .err import TraceError
			if self.trace_verbose < 1:
				raise TraceError('`trace_verbose` cannot be lower than 1 if `trace` is True')
			elif self.trace_verbose > 2:
				raise TraceError('`trace_verbose` cannot be higher than 2')
		elif self.trace == False and trace_verbose > 0:
			self.trace_verbose=0
		if self.section != None: self.section = str(section)

	def __enter__(self):
		return INI(self.filename, self.section, self.pass_section, self.trace, self.trace_verbose)

	def __exit__(*args,**kwargs):
		pass

	def get(self):
		"""get all keys and value by section"""
		from .utils import parse_section,parse_property,is_section,is_property

		ret = dict()
		if not self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:False')
			with open(self.filename,'r') as f:
				lines,point,anchor = f.readlines(),0,0
				for idx, line, in enumerate(lines):
					if parse_section(line.strip()) == self.section:
						point,anchor=idx+1,idx+1
						break
				for i in range(anchor,len(lines)):
					anchor += 1
					if is_section(lines[i].strip()):
						break
				for i in range(point,anchor):
					if is_property(lines[i].strip()):
						key, val = parse_property(lines[i].strip())
						ret.update({key: val})
			return ret
		elif self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:True')
			with open(self.filename,'r') as f:
				lines,point,anchor,fsec=f.readlines(),0,0,False
				for idx, line, in enumerate(lines):
					if is_section(line.strip()) or fsec:
						fsec=True
						_section = parse_section(line.strip())
						point,anchor=idx+1,idx+1
						for i in range(anchor,len(lines)):
							anchor += 1
							if is_section(lines[i].strip()):
								break
						if _section: ret.update({_section: {}})
						for i in range(point,anchor):
							if is_property(lines[i].strip()):
								key, val = parse_property(lines[i].strip())
								if _section != None: ret[_section].update({key:val})
					if not fsec:
						if is_property(line.strip()):
							key, val = parse_property(line.strip())
							ret.update({key: val})
			return ret

	def sections(self):
		"""get sections"""
		sec = list()
		data = INI(self.filename, self.section).get()
		if data == None: return data
		for d in data:
			if isinstance(data[d], dict): sec.append(d)

	def set_section(self):
		"""set section"""
		if not self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:False')
			if not INI(self.filename,self.section).isset_section():
				data = INI(self.filename).get()
				if data == None: data = dict()
				data.update({self.section: {}})
				from .utils import dump; dump(self.filename,data)
		elif self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: Couldn\'t set section, pass_section:True')

	def unset_section(self):
		"""unset section, the existing keys inside the section will get removed"""
		if not self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:False')
			if INI(self.filename,self.section).isset_section():
				data = INI(self.filename).get()
				if isinstance(data[self.section], dict): del data[self.section]; from .utils import dump; dump(self.filename,data); return True
				else: return False	
		elif self.pass_section: 
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: Couldn\'t unset section, pass_section:True')
			
	def isset_section(self):
		"""check if section was set or not"""
		if not self.pass_section:
			data = INI(self.filename).get()
			if data == None: return False
			if self.section in data:
				if isinstance(data[self.section],dict): return True
				else: return False
			else: return False
		elif self.pass_section: 
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: Couldn\'t check section, pass_section:True')

	def set(self,key,value):
		"""set new property or update existing property"""
		key = str(key)
		if self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:True')
			data = INI(self.filename).get()
			if data == None: data = dict()
			if key in data and not isinstance(data[key], dict):
				data[key] = value
				from .utils import dump; dump(self.filename,data)
			else:
				lines = list()
				with open(self.filename,'r') as f:
					lines = f.readlines()
					print(lines)
					lines.insert(0,f"{key}={value}\n")
				with open(self.filename,'w') as f:
					for l in lines:
						f.write(l)
			return True
		elif not self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:False')
			data = INI(self.filename).get()
			if data == None: data = dict()
			try:
				data[self.section][key] = value
			except KeyError:
				data[self.section].update({key: value})
			from .utils import dump; dump(self.filename,data)
			return True

	def sets(self,sets):
		"""set or update properties with sets or dictionary"""
		for ns in sets:
			if isinstance(sets[ns], dict) or isinstance(sets[ns], list): continue
			else:
				INI(self.filename,self.section).set(ns,sets[ns])

	def isset(self,key):
		"""check if property was set or not"""
		key = str(key)
		if self.pass_section:
			data = INI(self.filename).get()
			if data == None: return False
			if key in data:
				if not isinstance(data[key], dict): return True
				else: return False
			else: return False
		elif not self.pass_section:
			data = INI(self.filename).get()
			if data == None: return False
			if key in data:
				if INI(self.filename,self.section).isset_section():
					if not isinstance(data[self.section][key], dict): return True
					else: return False
				else: return False
			else: return False

	def unset(self,key):
		"""unset existing property by key"""
		key = str(key)
		if self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:True')
			if not INI(self.filename,self.section).isset(key): return False
			data = INI(self.filename).get(); del data[key]
			from .utils import dump; dump(self.filename,data)
			return True

		elif not self.pass_section:
			if self.trace_verbose >= 1: print(f'[iniparser2][TRACE]: parse mode = pass_section:False')
			if not INI(self.filename,self.section).isset(key): return False
			data = INI(self.filename).get(); del data[self.section][key]
			from .utils import dump; dump(self.filename,data)
			return True
			
	def exists(self):
		"""check whether the file is exists or not"""
		import os
		if os.path.exists(self.filename): return True
		else: return False

	def create(self):
		"""creates new file"""
		import os
		if not os.path.exists(self.filename):
			with open(self.filename,'x') as f:
				pass
			return True
		else: return False

	def flush(self,stream=False):
		"""flush file"""
		if not stream:
			import os
			if os.path.exists(self.filename):
				os.remove(self.filename)
				with open(self.filename,'x') as f:
					pass
				return True
			else: return False
		elif stream:
			with open(self.filename,'w') as f:
				f.write('')
			return True

	def remove(self):
		"""remove/deletes file"""
		import os
		if os.path.exists(self.filename):
			os.remove(self.filename)
			return True
		else: return False

class INI_TEMP:
	"""temporary parse method"""
	def __init__(self, section=None, pass_section=True, trace=False, trace_verbose=1):
		self.section = section
		self.pass_section = pass_section
		self.trace = trace
		self.trace_verbose = trace_verbose

		if self.section != None:
			self.pass_section = False
		if self.pass_section == False and self.section == None:
			from .err import SectionError
			raise SectionError('`section` cannot be \'NoneType\' if `pass_section` is \'False\'')
		if self.trace == True:
			from .err import TraceError
			if self.trace_verbose < 1:
				raise TraceError('`trace_verbose` cannot be lower than 1 if `trace` is True')
			elif self.trace_verbose > 2:
				raise TraceError('`trace_verbose` cannot be higher than 2')
		elif self.trace == False and trace_verbose > 0:
			self.trace_verbose=0
		if self.section != None: self.section = str(section)

	def __enter__(self):
		return INI_TEMP(self.section,self.pass_section,self.trace,self.trace_verbose)

	def __exit__(*args,**kwargs):
		pass

	def parse(self,string):
		import random
		char = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m',
				'Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M',
				'1','2','3','4','5','6','7','8','9','0']
		ret_char = list()
		for i in range(8):
			ret_char.append(random.choice(char))
		token = ''.join(ret_char)
		fname = f"{token}.ini.temp"
		x = INI(fname,self.section,self.pass_section,self.trace,self.trace_verbose)
		x.create()
		with open(fname,'w') as f:
			f.write(string)
		data = x.get()
		x.remove()
		return data
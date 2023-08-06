import re

def dump(filename,set):
	"""dump a dictionary or a set to INI file format"""
	with open(filename,'w+') as f:
		for ns in set:
			if isinstance(set[ns], dict):
				f.write(f'[{ns}]\n')
				for ps in set[ns]:
					if isinstance(set[ns][ps], dict) or isinstance(set[ns][ps], list): continue
					f.write(f'{ps}={set[ns][ps]}\n')
			else:
				f.write(f"{ns}={set[ns]}\n")

def parse_property(string):
	if check_comment(string): return
	prop = re.split(r'\s*(\=)\s*',string)
	if len(prop) < 3: return
	del prop[1]
	key, val = prop[0], prop[1]
	if key:
		val = ''.join(prop[1:])
		return key, val

def parse_section(string):
	if check_comment(string): return
	sec = re.split(r'^\[(.*)\]$',string)
	if sec[0] != string:
		for i,s in enumerate(sec):
			if not s: del sec[i]
		return sec[0]

def check_comment(string):
	sec = re.match(r'^[?!#|;]',string)
	if sec: return True
	return False

def is_property(string):
	if parse_property(string) != None: return True
	return False

def is_section(string):
	if parse_section(string) != None: return True
	return False

def is_ini(filename):
	return filename.endswith('.ini')
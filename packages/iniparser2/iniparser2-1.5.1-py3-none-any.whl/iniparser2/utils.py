def dump(filename,set):
	"""dump a dictionary or a set to INI file format"""
	with open(filename,'a+') as f:
		for ns in set:
			if isinstance(set[ns], dict):
				f.write(f'[{ns}]\r')
				for ps in set[ns]:
					if isinstance(set[ns][ps], dict) or isinstance(set[ns][ps], list): continue
					f.write(f'{ps}={set[ns][ps]}\r')
			else:
				f.write(f"{ns}={set[ns]}\r")

def is_ini(filename):
	return filename.endswith('.ini')
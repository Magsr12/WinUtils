#coding: utf-8

import os, shutil, time

temp_dir = os.getenv('temp') + '/'
files = []
dirs = []

def list_temp():
	print '[*] Procurando por arquivos temporarios...'
	time.sleep(0.9)
	temp_dir = os.getenv('temp') + '/'
	for x in os.listdir(temp_dir):
		if os.path.isfile(temp_dir + x):
			print '[*] Removido: ' + x
			files.append(x)
		elif os.path.isdir(temp_dir + x):
			print '[*] Removendo: ' + x
			dirs.append(x)
	if len(files) == 0 and len(dirs) == 0:
		pass
	else:
		for f in files:
			os.remove(temp_dir + f)
		for d in dirs:
			shutil.rmtree(temp_dir + d)


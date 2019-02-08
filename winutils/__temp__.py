#coding: utf-8
#Clean temp files and .pyc compiled files.

import os, shutil, time

temp_dir = os.getenv('temp') + '/'
files = []
dirs = []

def clean_temp():
	print '[*] Procurando por arquivos temporarios...'
	time.sleep(0.9)
	temp_dir = os.getenv('temp') + '/'
	for x in os.listdir(temp_dir):
		if os.path.isfile(temp_dir + x):
			print '[*] Removido: ' + x
			files.append(x)
			time.sleep(0.09)
		elif os.path.isdir(temp_dir + x):
			print '[*] Removido: ' + x
			dirs.append(x)
			time.sleep(0.09)
	if len(files) == 0 and len(dirs) == 0:
		pass
	else:
		for f in files:
			try:
				os.remove(temp_dir + f)
			except WindowsError:
				print '[*] {} esta sendo usado por outro processo.'.format(f)
		for d in dirs:
			shutil.rmtree(temp_dir + d)
		print '[*] {} arquivos temporarios apagados.'.format(len(files) + len(dirs))
def clean_pyc_files():
	os.system('del *.pyc')
	


#coding: utf-8

import argparse
import sys

from __extra__ import init
init()

from __temp__ import *
from __utils__ import *
from main import *
colorama.init()

start_lapse = time.time() # Initiate start_lapse

def main():
	info()
	w_utils = Utils()
	parser = argparse.ArgumentParser()
	parser.add_argument('--disk-usage', help='Verifica e corrige os possiveis erros que causam 100 uso do disco.', action='store_true', dest='disk', default=False)
	parser.add_argument('--enable-dism', help='Habilita o DISM para procurar por possiveis erros no HD', action='store_true', dest='dism_', default=False)
	parser.add_argument('--clean-apps', help='Limpa TODOS os aplicativos que vem por padrao no Windows 10, use --list-apps para listar os aplicativos.', action='store_true', dest='clean_apps', default=False)
	parser.add_argument('--list-apps', help='Lista os aplicativos a serem processados.', required=False, dest='list_apps', action='store_true')
	parser.add_argument('--force', help='Tenta a opcao --clean-apps mesmo se nao estiver numa versao compativel do windows.', dest='force', action='store_true')
	if len(sys.argv) < 2:
		usage = '''
usage: winutils.py [-h] [--disk-usage] [--enable-dism] [--clean-apps]
                   [--list-apps]

optional arguments:
  -h, --help     show this help message and exit
  --disk-usage   Verifica e corrige os possiveis erros que causam 100 uso do
                 disko.
  --enable-dism  Habilita o DISM para procurar por possiveis erros no HD
  --clean-apps   Limpa TODOS os aplicativos que vem por padrao no Windows 10,
                 use --list-apps para listar os aplicativos.
  --list-apps    Lista os aplicativos a serem processados.'''
  		exit(usage)


	args=parser.parse_args()
	disk_usage = args.disk
	enable_dism = args.dism_
	clean_apps_ = args.clean_apps
	list_apps = args.list_apps
	force = args.force
	if list_apps:
		for apps in w_utils.app_list:
			print apps
		exit()
	if clean_apps_:
		if '10.' not in platform.platform():
			if force:
				initiate_count('start') # Time start log
				w_utils.apps()
			else:
				print '[*] Esta versao do windows nao e compativel com a opcao --clean-apps, tente novamente com a opcao --force.'
				exit()
		else:
			initiate_count('start')
			w_utils.apps()
	if disk_usage:
		is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0 # Check if the user is Admin
		if is_admin is False:
			if force:
				pass
			else:
				exit('\n[*] Nao foi possivel prosseguir com a correcao de disko, esta opcao requer privilegios.\n\nIS_ADMIN: {}'.format(is_admin))
		w_utils.services_()
		w_utils.windows_defender()
		if enable_dism:
			w_utils.disk_usage(dism_=True)
		else:
			w_utils.disk_usage(dism_=False)
	if not disk_usage:
		if enable_dism is True:
			print '[*] A opcao --enable-dism deve ser atribuida junto com --disk-usage.'
			exit()


main()
clean_temp() # Functions in __temp__.py to clean %TEMP%
clean_pyc_files()
initiate_count('end', start_lapse) # Finalize the started_lapse
	

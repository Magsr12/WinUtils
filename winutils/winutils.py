#coding: utf-8

"""
WHAT IT DO:

[DISABLE SERVICES]

EXTERNAL COMMAND: sc config {service} start= {mode}

#demand = manual

#disable sysmain to start= disabled (superfetch)
#disable msiserver to start= demand ( Windows Installer )
#disable TrustedInstaller to start= demand ( Instalador de drivers )
#disable wuauserv to start= demand ( Windows update )

[TURN OFF WINDOWS DEFENDER]

(AUTO)
Turn_Off_Windows_Defender_Antivirus.reg

(MANUAL)
[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender]

"DisableAntiSpyware"=dword:00000001

[MORE]
      
If the schedule process is 100% consider to disable task scheduler. ( Agendador de tarefas )
"""
from __extra__ import init
init()

import os, ctypes, requests, sys, time, argparse, shutil, tempfile, colorama, platform
from clint.textui import progress
from __temp__ import *


colorama.init()

class bcolors:
	BOLD = '\033[1m'
	CYAN = '\033[36m'
	NORMAL = '\033[37m'
	YELLOW = '\033[33m'


class Utils:
	def __init__(self):
		self.app_list = ['3dbuilder', 'windowsalarms', 'windowscommunicationsapps', 'windowscamera'
        		, 'bingnews', 'nonenote', 'people', 'windowsphone', 'windowsstore', 'bingsports', 'soundrecorder'
        		, 'officehub', 'skypeapp', 'zunemusic', 'windowsmaps', 'solitairecollection', 'bingfinance', 'zunevideo']

		self.services = ['SysMain', 'TrustedInstaller', 'wuauserv', 'msiserver']

	def services_(self):		
        	print "[*] Desativando servico SysMain para otimizacao de disc_usage..."
        	sysmain_cmd = os.system('sc config sysmain start= disabled > NUL')
        	if sysmain_cmd != 0:
                	print "[*] Nao foi possivel desativar o servico SysMain (superfetch)"
        	else:
                	print "[*] Servico SysMain (superfetch) desabilitado "

        	print "[*] Desativando TrustedInstaller ( Instalador de Modulos )..."
        	trus_cmd = os.system('sc config TrustedInstaller start= demand > NUL') # Set TrustedInstaller to manual
        	if trus_cmd != 0:
                	print "[*] Nao foi possivel desativar o servico TrustedInstaller (Instalador de modulos)"
        	else:
                	print "[*] Servico TrustedInstaller (Instalador de modulos) desabilitado"
        	
        	wua_serv = os.system('sc config wuauserv start= demand > NUL') # Set wuauserv to manual
        	if wua_serv != 0:
                	print "[*] Nao foi possivel desativar o servico wuauserv (Windows Update)"
        	else:
                	print "[*] Servico wuauserv (Windows Update) desativado"
        	
        	msi_serv = os.system('sc config msiserver start= demand > NUL') # Set msiserver to manual
        	if msi_serv != 0:
                	print "[*] Nao foi possivel desativar o servico msiserver (Windows Installer)"
        	else:
                	print "[*] Servico msiserver (Windows Installer) desativado"
        	

	def apps(self):
		print '[*] Aguarde enquanto verificamos os aplicativos instalados...'
		time.sleep(1)
		for i in self.app_list:
			print '[*] Encontrado: {}'.format(i)
			time.sleep(0.08)
		print '[*] Carregando Powershell...'
		for app in self.app_list:
			try:
				apps_command = os.system('powershell "Get-AppxPackage *{}* | Remove-AppxPackage"'.format(app))
				if apps_command == 1:
					print "[*] Nao foi possivel desinstalar {}".format(app)
				else:
					print "[*] Removendo {}".format(app)
			except KeyboardInterrupt:
				time.sleep(2.9)
				exit()

	def windows_defender(self, func='disable'):
		if func == 'enable':
			print '[*] Habilitando Windows Defender...'
			os.system('start misc/Turn_On_Windows_Defender_Antivirus.reg')
			print '[*] Windows Defender habilitado.'
		elif func == 'disable':
			print '[*] Desabilitando Windows Defender...'
			os.system('start misc/Turn_Off_Windows_Defender_Antivirus.reg')
			print '[*] Windows defender desabilitado.'
		
	def disc_usage(self, dism_=False):
		if dism_:
			os.system('Dism /Online /Cleanup-Image /ScanHealth')
			os.system('Dism /Online /Cleanup-Image /RestoreHealth')
        	print  "[*] 1. Desabilite o arquivo de paginacao em: Avancado > Conf. Desempenho > Avancado > Alterar..."
        	print "[*] 2. Desative as configuracoes remotas do windows na aba Remoto"
		open_ = raw_input('[*] Abrir configuracoes [ENTER]')
		os.system('control sysdm.cpl')
		print '[*] Verificando se foram desabilitados...\n'
		for s in self.services:
			os.system('sc query {} | findstr  /i NOME_DO'.format(s))
			os.system('sc query {} | findstr  /i ESTADO'.format(s))
		print '\nFLAGS = STOPPED, RUNNING'
		print '\n[*] Caso haja algum servico em RUNNING, recomenda-se reiniciar o procedimento.'
		print '[*] Finalizado.'

class MainApp:
	def __init__(self):
		self.A = {'Driver Booster': 'http://update.iobit.com/dl/driver_booster_setup.exe',
		'Chrome': 'http://redirector.gvt1.com/edgedl/release2/chrome/AM4yMAx_dXd__69.0.3497.100/69.0.3497.100_chrome_installer.exe',
		'Winrar': 'https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-561.exe',
		'VLC': 'https://mirror.espoch.edu.ec/videolan/vlc/2.2.4/win32/vlc-2.2.4-win32.exe',
		}
		#self.app_list = ['Driver Booster', 'Chrome', 'Winrar', 'VLC']
		#self.app_path = ['C:\Program Files (x86)\IObit\Driver Booster', 'C:\Program Files (x86)\Google\Chrome', 'C:\Program Files\WinRAR', 'C:\Program Files\VideoLAN\VLC']
		#self.app_range = len(self.app_path)	
		#self.missing = []
		self.install_apps = []
		#Headers
		self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'en-US,en;q=0.8',
		'Connection': 'keep-alive'}

	def download_pkg(self, name, link):
		file_name = name + '.exe'
		r = requests.get(link, stream=True, headers=self.hdr)
		with open(file_name, 'wb') as f:
			total_length = int(r.headers.get('content-length'))
			for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
				if chunk:
					f.write(chunk)
					f.flush()

	def check_packages(self, force=False):
		if force is True:
			for i in self.app_list:
				self.missing.append(i)
		else:
			for i in range(self.app_range): # I am foda
				if os.path.isdir(self.app_path[i]):
					print '[*] {} encontrado.'.format(self.app_list[i])
				else:
					print '[*] {} nao encontrado.'.format(self.app_list[i])
					self.missing.append(self.app_list[i])

	def install_packages(self, post_execute=False):
		if len(self.missing) == 0:
			pass
		else:
			self.missing_range = len(self.missing)			
			for i in range(self.missing_range):
				try:
					print '[*] Baixando {} de: {} | Ctrl+C para pular a etapa'.format(self.missing[i], self.A.get(self.missing[i]))
					self.download_pkg(self.missing[i], self.A.get(self.missing[i]))
				except KeyboardInterrupt:
					pass
			for i in self.missing:
				if post_execute is True:
					print '[*] Executando {}'.format(i)
					os.system('{}'.format(i))
					ask_continue = raw_input('[*] Abrir o proximo instalador [ENTER]')

def info():
	_yellow_ = bcolors.BOLD + bcolors.YELLOW
	_cyan_ = bcolors.BOLD + bcolors.CYAN
	_normal_ = bcolors.NORMAL

	admin_is = ctypes.windll.shell32.IsUserAnAdmin()
	if admin_is == False:
		admin_is = 'NO'
	else:
		admin_is = 'YES'

	if platform.machine() == 'AMD64':
		platform_machine_bits = '64 Bits'
	else:
		platform_machine_bits = '32 Bits'
	print _cyan_ + '''
888       888 d8b                   888    d8b 888          
888   o   888 Y8P                   888    Y8P 888          
888  d8b  888                       888        888          
888 d888b 888 888 88888b.  888  888 888888 888 888 .d8888b  
888d88888b888 888 888 "88b 888  888 888    888 888 88K      
88888P Y88888 888 888  888 888  888 888    888 888 "Y8888b. 
8888P   Y8888 888 888  888 Y88b 888 Y88b.  888 888      X88 
888P     Y888 888 888  888  "Y88888  "Y888 888 888  88888P'
''' + _cyan_
	print _yellow_ + '[*] ' + platform.system() + ' ' + platform.version() + ' ' + platform_machine_bits
	print '[*] Admin privileges: ' + admin_is + _normal_ + '\n'

def main():
	info()
	w_utils = Utils()
	w_packages = MainApp()
	parser = argparse.ArgumentParser()
	parser.add_argument('--disc-usage', help='Verifica e corrige os possiveis erros que causam 100 uso do disco.', action='store_true', dest='disc', default=False)
	parser.add_argument('--enable-dism', help='Habilita o DISM para procurar por possiveis erros no HD', action='store_true', dest='dism_', default=False)
	parser.add_argument('--clean-apps', help='Limpa TODOS os aplicativos que vem por padrao no Windows 10, use --list-apps para listar os aplicativos.', action='store_true', dest='clean_apps', default=False)
	parser.add_argument('--list-apps', help='Lista os aplicativos a serem processados.', required=False, dest='list_apps', action='store_true')
	'''
	parser.add_argument('--download-apps', help='Somente baixa os aplicativos, forca o download se ja estiverem instalados.', action='store_true', dest='download_apps', default=False)
	parser.add_argument('--install-apps', help='Baixa e instala os aplicativos necessarios.', action='store_true', dest='install_apps', default=False)
	parser.add_argument('--check-apps', help='Somente verifica se os aplicativos necessarios estao instalados.', action='store_true', dest='check_apps', default=False)
	parser.add_argument('--list-apps', help='Lista os aplicativos configurados.', action='store_true', dest='list_apps', default=False)
	'''
	if len(sys.argv) < 2:
		usage = bcolors.NORMAL + '''
usage: winutils.py [-h] [--disc-usage] [--enable-dism] [--clean-apps]
                   [--list-apps]

optional arguments:
  -h, --help     show this help message and exit
  --disc-usage   Verifica e corrige os possiveis erros que causam 100 uso do
                 disco.
  --enable-dism  Habilita o DISM para procurar por possiveis erros no HD
  --clean-apps   Limpa TODOS os aplicativos que vem por padrao no Windows 10,
                 use --list-apps para listar os aplicativos.
  --list-apps    Lista os aplicativos a serem processados.''' + bcolors.NORMAL
  		exit(usage)


	args=parser.parse_args()
	disc_usage = args.disc
	enable_dism = args.dism_
	clean_apps_ = args.clean_apps
	list_apps = args.list_apps
	if list_apps:
		for apps in w_utils.app_list:
			print apps
		exit()
	if clean_apps_:
		w_utils.apps()
	if disc_usage:
		is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0 # Check if the user is Admin
		if is_admin is False:
			exit('\n[*] Nao foi possivel prosseguir com a correcao de disco, esta opcao requer privilegios.\n\nIS_ADMIN: {}'.format(is_admin))
		w_utils.services_()
		w_utils.windows_defender()
		if enable_dism:
			w_utils.disc_usage(dism_=True)
		else:
			w_utils.disc_usage(dism_=False)
	if not disc_usage:
		if enable_dism is True:
			print '[*] A opcao --enable-dism deve ser atribuida junto com --disc-usage.'
			exit()
main()
list_temp() # Function in temp.py to clean %TEMP%
	

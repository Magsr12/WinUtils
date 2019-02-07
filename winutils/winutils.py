#coding: utf-8
#Interative texts language: PT-BR

'''
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
'''

import argparse
import sys

from __extra__ import init
init()

from __temp__ import *
from __utils__ import *
colorama.init()

start_lapse = time.time() # Initiate start_lapse


class Utils:
	def __init__(self):
		self.app_list = ['3dbuilder', 'windowsalarms', 'windowscommunicationsapps', 'windowscamera'
        		, 'bingnews', 'nonenote', 'people', 'windowsphone', 'windowsstore', 'bingsports', 'soundrecorder'
        		, 'officehub', 'skypeapp', 'zunemusic', 'windowsmaps', 'solitairecollection', 'bingfinance', 'zunevideo']

		self.services = ['SysMain', 'TrustedInstaller', 'wuauserv', 'msiserver']

	def services_(self):		
        	print "[*] Desativando servico SysMain para otimizacao de disc_usage..."
        	sysmain_cmd = os.system('sc config sysmain start= disabled > NUL') # Disable superfetch
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
		print '[*] Aguarde enquanto verificamos os aplicativos a serem processados...'
		time.sleep(2.2)
		for i in self.app_list:
			print '[*] Enumerando: {}'.format(i) # Enumerate all apps in self.app_list
			time.sleep(0.05)
		print '[*] Carregando Powershell...'
		for app in self.app_list:
			try:
				apps_command = os.system('powershell "Get-AppxPackage *{}* | Remove-AppxPackage"'.format(app)) # Use this command to uninstall the apps
				if apps_command == 1:
					print "[*] Nao foi possivel desinstalar {}".format(app)
				else:
					print "[*] Removendo {}".format(app)
			except KeyboardInterrupt:
				print '[*] Pulando esta etapa...'; time.sleep(0.8)
				break

	def windows_defender(self, func='disable'):
		if func == 'enable':
			print '[*] Habilitando Windows Defender...'
			os.system('start misc/Turn_On_Windows_Defender_Antivirus.reg') # AUTO ENABLE WINDOWS DEFENDER
			print '[*] Windows Defender habilitado.'
		elif func == 'disable':
			print '[*] Desabilitando Windows Defender...'
			os.system('start misc/Turn_Off_Windows_Defender_Antivirus.reg') # AUTO DISABLE WINDOWS DEFENDER
			print '[*] Windows defender desabilitado.'
		
	def disc_usage(self, dism_=False):
		if dism_:
			os.system('Dism /Online /Cleanup-Image /ScanHealth')
			os.system('Dism /Online /Cleanup-Image /RestoreHealth')
        	print  "[*] 1. Desabilite o arquivo de paginacao em: Avancado > Conf. Desempenho > Avancado > Alterar..."
        	print "[*] 2. Desative as configuracoes remotas do windows na aba Remoto"
		open_ = raw_input('[*] Abrir configuracoes [ENTER]')
		os.system('control sysdm.cpl') # OPENING PAINEL
		print '[*] Verificando se foram desabilitados...\n'
		for s in self.services: # CHECK IF THE SERVICES HAS STOPPED
			os.system('sc query {} | findstr  /i NOME_DO'.format(s))
			os.system('sc query {} | findstr  /i ESTADO'.format(s))
		print '\nFLAGS = STOPPED, RUNNING'
		print '\n[*] Caso haja algum servico em RUNNING, recomenda-se reiniciar o procedimento.'
		print '[*] Finalizado.'

def main():
	info()
	w_utils = Utils()
	parser = argparse.ArgumentParser()
	parser.add_argument('--disc-usage', help='Verifica e corrige os possiveis erros que causam 100 uso do disco.', action='store_true', dest='disc', default=False)
	parser.add_argument('--enable-dism', help='Habilita o DISM para procurar por possiveis erros no HD', action='store_true', dest='dism_', default=False)
	parser.add_argument('--clean-apps', help='Limpa TODOS os aplicativos que vem por padrao no Windows 10, use --list-apps para listar os aplicativos.', action='store_true', dest='clean_apps', default=False)
	parser.add_argument('--list-apps', help='Lista os aplicativos a serem processados.', required=False, dest='list_apps', action='store_true')
	parser.add_argument('--force', help='Tenta a opcao --clean-apps mesmo se nao estiver numa versao compativel do windows.', dest='force', action='store_true')
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
	if disc_usage:
		is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0 # Check if the user is Admin
		if is_admin is False:
			exit('\n[*] Nao foi possivel prosseguir com a correcao de disco, esta opcao requer privilegios.\n\nIS_ADMIN: {}'.format(is_admin))
		initiate_count('start')
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
clean_temp() # Functions in __temp__.py to clean %TEMP%
clean_pyc_files()
initiate_count('end', start_lapse) # Finalize the started_lapse
	

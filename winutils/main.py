import os
import time



class Utils:
	def __init__(self):
		self.app_list = ['3dbuilder', 'windowsalarms', 'windowscommunicationsapps', 'windowscamera'
        		, 'bingnews', 'nonenote', 'people', 'windowsphone', 'windowsstore', 'bingsports', 'soundrecorder'
        		, 'officehub', 'skypeapp', 'zunemusic', 'windowsmaps', 'solitairecollection', 'bingfinance', 'zunevideo']

		self.services = ['SysMain', 'TrustedInstaller', 'wuauserv', 'msiserver']

	def services_(self):		
        	print "[*] Desativando servico SysMain para otimizacao de disk_usage..."
        	sysmain_cmd = os.system('sc config sysmain start= disabled > NUL') # Disable superfetch
        	time.sleep(1.3)
        	if sysmain_cmd != 0:
                	print "[*] Nao foi possivel desativar o servico SysMain (superfetch)"
        	else:
                	print "[*] Servico SysMain (superfetch) desabilitado "

        	print "[*] Desativando TrustedInstaller ( Instalador de Modulos )..."
        	trus_cmd = os.system('sc config TrustedInstaller start= demand > NUL') # Set TrustedInstaller to manual
        	time.sleep(1.3)
        	if trus_cmd != 0:
                	print "[*] Nao foi possivel desativar o servico TrustedInstaller (Instalador de modulos)"
        	else:
                	print "[*] Servico TrustedInstaller (Instalador de modulos) desabilitado"
        	
        	wua_serv = os.system('sc config wuauserv start= demand > NUL') # Set wuauserv to manual
        	time.sleep(1.3)
        	if wua_serv != 0:
                	print "[*] Nao foi possivel desativar o servico wuauserv (Windows Update)"
        	else:
                	print "[*] Servico wuauserv (Windows Update) desativado"
        	
        	msi_serv = os.system('sc config msiserver start= demand > NUL') # Set msiserver to manual
        	time.sleep(1.3)
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
			run = os.system('start misc/Turn_On_Windows_Defender_Antivirus.reg') # AUTO ENABLE WINDOWS DEFENDER
			if run == 1:
				print '[*] Nao foi possivel habilitar o Windows Defender.'
			else:
				print '[*] Windows Defender habilitado.'
		elif func == 'disable':
			print '[*] Desabilitando Windows Defender...'
			run = os.system('start misc/Turn_Off_Windows_Defender_Antivirus.reg') # AUTO DISABLE WINDOWS DEFENDER
			if run == 1:
				print '[*] Nao foi possivel desabilitar o Windows Defender.'
			else:
				print '[*] Windows defender desabilitado.'
		
	def disk_usage(self, dism_=False):
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


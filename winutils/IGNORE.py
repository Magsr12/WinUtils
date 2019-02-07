import requests
from clint.textui import progress

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
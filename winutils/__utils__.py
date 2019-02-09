#coding: utf-8

import colorama
import platform
import datetime
import ctypes
import time
from __colors__ import *

def info():
	admin_is = ctypes.windll.shell32.IsUserAnAdmin()
	if admin_is == False:
		admin_is = 'NO'
	else:
		admin_is = 'YES'

	if platform.machine() == 'AMD64':
		platform_machine_bits = '64 Bits'
	else:
		platform_machine_bits = '32 Bits'
	print CYAN + '''
888       888 d8b                   888    d8b 888          
888   o   888 Y8P                   888    Y8P 888          
888  d8b  888                       888        888          
888 d888b 888 888 88888b.  888  888 888888 888 888 .d8888b  
888d88888b888 888 888 "88b 888  888 888    888 888 88K      
88888P Y88888 888 888  888 888  888 888    888 888 "Y8888b. 
8888P   Y8888 888 888  888 Y88b 888 Y88b.  888 888      X88 
888P     Y888 888 888  888  "Y88888  "Y888 888 888  88888P'
''' + CYAN
	print YELLOW + '[*] ' + platform.platform() + ' ' + platform_machine_bits
	print '[*] Admin privileges: ' + admin_is + NORMAL + '\n'

def initiate_count(mode, start_lapse=False): # Time count func
	now = []
	now.append(datetime.datetime.now())
	init_hour = str(now[0])[11:19]
	if mode == 'start':		
		print YELLOW + '[*] Iniciando em: {}\n'.format(init_hour) + NORMAL	
	if mode == 'end':
		end_lapse = time.time()
		elapsed = end_lapse - start_lapse
		print YELLOW + '\n[*] Finalizado em {} segundos.'.format(int(elapsed)) + NORMAL




#coding: utf-8
#Check modules
import os

def init():
	try:
		import ctypes
	except ImportError:
		print 'module ctypes not found, trying to install it.'; os.system('pip install ctypes')
	try:
		import tempfile
	except ImportError:
		print 'module tempfile not found, trying to install it.'; os.system('pip install tempfile')

	try: 
		import colorama
	except ImportError:
		print 'module colorama not found, trying to install it.'; os.system('pip install colorama')

	try:
		import clint
	except ImportError:
		print 'module clint not found, trying to install it.'; os.system('pip install clint')

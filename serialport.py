from serial import Serial
import serial.tools.list_ports as list_ports
from colorama import Fore, Back, Style
from utils import *

class SerialPort(Serial):
	def __init__(self):
		selected_port = None
		baudrate = 115200

		for port in list_ports.comports():
			if 'usbserial' in port.device:
				selected_port = port.device
				break
		
		while True:
			print('selected', selected_port, '@', baudrate)
			ok = input('is it ok? [Y/n/baud] ').lower()
			if ok == 'n':
				i = 0
				for port in list_ports.comports():
					print(i, port.device)
					i += 1
				port_to_select = int(input('Input the port number: '))
				selected_port = list_ports.comports()[port_to_select].device
			elif ok == 'baud':
				baudrate = int(input('Enter the new baudrate: '))
			else:
				break
		print_std('OK')

		super().__init__(selected_port, baudrate, timeout=1)
	
	def readline(self):
		return super().readline().decode('utf8').strip()
	
	def readline_no_strip(self):
		return super().readline().decode('utf8')
	
	def wait_for_check(self, check):
		line = self.readline()
		print(Back.WHITE, end='', flush=True)
		last = False
		while not check(line):
			if line != '':
				if not last:
					print(Back.RESET)
				print(Fore.YELLOW + line + Fore.RESET + '\n', end='', flush=True)
				last=True
			else:
				if last:
					print('\n'+Back.WHITE, end='')
				print('.', end='', flush=True)
				last = False
			line = self.readline()
		
		print(Back.RESET)
		print(Fore.YELLOW + line + Fore.RESET)
	
	def wait_for_line(self, line):
		self.wait_for_check(lambda x: x == line)
	
	def write(self, data):
		super().write(data.encode('utf8'))
	
	def send(self, data):
		self.write(data + '\n')
	

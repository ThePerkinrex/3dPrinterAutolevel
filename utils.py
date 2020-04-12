from time import sleep
from colorama import Fore, Back, Style

def delay(secs):
	print(Back.WHITE, end='', flush=True)
	for i in range(0,secs):
		print('.', end='', flush=True)
		sleep(1)
	print(Back.RESET)

def print_serial(data):
	print(Fore.YELLOW + str(data) + Fore.RESET)

def bold(data):
	return Style.BRIGHT + str(data) + Style.RESET_ALL

def print_important(data):
	print(Fore.RED + bold(data) + Fore.RESET)

def print_std(data):
	print(Fore.CYAN + bold(data) + Fore.RESET)
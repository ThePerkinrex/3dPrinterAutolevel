
import colorama
from colorama import Fore, Back, Style
colorama.init()

from serialport import SerialPort
from utils import *

import matplotlib.pyplot as plt
import numpy as np

def autolevel(serialport):
	print_std('Enabling steppers')
	serialport.send('M17')
	serialport.wait_for_line('ok')

	print_std('Homing printer')
	serialport.send('G28')
	serialport.wait_for_line('ok')
	print_std('Printer homed')
	print_std('Autoleveling')

	serialport.send('G29')
	serialport.wait_for_line('Bilinear Leveling Grid:')
	lines = []
	while True:
		line = serialport.readline_no_strip()
		if line == '\n':
			break
		line = line.strip()
		lines.append(line.split())
	del lines[0]
	for line in lines:
		del line[0]
		for i in range(len(line)):
			line[i] = float(line[i])
	matrix_dim = (len(lines), len(lines[0]))

	Z = np.zeros(matrix_dim)
	Z[1][0] = 1
	
	for y in range(len(lines)):
		for x in range(len(lines[y])):
			Z[y][x] = lines[y][x]
	print_important(Z)
	x = np.linspace(1, matrix_dim[0], matrix_dim[0])
	y = np.linspace(1, matrix_dim[1], matrix_dim[1])

	X, Y = np.meshgrid(x, y)

	fig = plt.figure()
	ax = plt.axes(projection="3d")
	ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
					cmap='RdBu', edgecolor='black')

	serialport.reset_input_buffer()
	print_std('Disabling steppers')
	serialport.send('M17')
	serialport.wait_for_line('ok')

	plt.show()

with SerialPort() as serialport:
	print_important('Connected')
	serialport.wait_for_line('start')
	print_std('Printer starting up')
	serialport.wait_for_check(lambda x: 'M851' in x)

	while True:
		autolevel(serialport)

		again = input('Do it again? [Y/n] ').lower()

		if again == 'n':
			break
	
print_std('Done!')
	

	

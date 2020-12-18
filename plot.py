import sys, os
import configparser
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from itertools import cycle

# import functions for possible formulas evaluation in cfg
from math import pi, e
from math import exp, log
from math import cos, sin, tan
from math import acos, asin, atan
from math import cosh, sinh, tanh
from math import acosh, asinh, atanh
from math import degrees, radians

# set rc parameters
mpl.use('pgf')
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['pgf.texsystem'] = 'pdflatex'
mpl.rcParams['text.usetex'] = True
mpl.rcParams['pgf.preamble'] = "\\usepackage[T2A]{fontenc} \\usepackage[utf8]{inputenc} \\usepackage[english,russian]{babel} \\DeclareUnicodeCharacter{2212}{-}"
mpl.rcParams['figure.figsize'] = (6.69423, 4)

# define colors list
colors = [
	'#e6194b', '#3cb44b', '#0082c8', '#f58231', '#911eb4', '#46f0f0', 
	'#f032e6', '#d2f53c', '#fabebe', '#008080', '#e6beff', '#aa6e28',
	'#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000080',
	'#808080'
]

# get cfg files
if len(sys.argv) > 1:
	cfgfiles = [s + '.cfg' for s in sys.argv[1:]]
else:
	cfgfiles = ['plot.cfg']

for c in cfgfiles:
	print(f'------ CFG `{c}` ------', flush = True)

	# read cfg file
	cfg = configparser.ConfigParser(allow_no_value = True)
	cfg.read(c, encoding = 'utf-8')

	# save cfg lists into variables
	files = cfg.get('DATA', 'files', fallback = None)
	if not files:
		sys.exit('no input files are specified.')
	else:
		files = list(map(str.strip, files.split(',')))

	ycols = cfg.get('DATA', 'ycols', fallback = None)
	if not ycols:
		sys.exit('no input y-axis columns are specified.')
	else:
		ycols = list(map(str.strip, ycols.split(',')))

	xcols = cfg.get('DATA', 'xcols', fallback = None)
	if not xcols:
		sys.exit('no input x-axis columns are specified.')
	else:
		xcols = list(map(str.strip, xcols.split(',')))

	labels = cfg.get('PLOT', 'labels', fallback = None)
	if labels:
		labels = list(map(str.strip, labels.split(',')))

	# create cycle variables
	cycolors = cycle(colors)
	cyfiles = cycle(files)
	cyycols = cycle(ycols)
	cyxcols = cycle(xcols)
	if labels:
		cylabels = cycle(labels)
	
	# create plot
	for i in range(0, max(len(files), len(ycols))):
		file = next(cyfiles)
		xcol = int(next(cyxcols))
		ycol = int(next(cyycols))

		print(f'plot `{file}` file using ({xcol},{ycol})', flush = True)

		if xcol < 0:
			data = np.loadtxt(file, usecols = (ycol), skiprows = cfg.getint('DATA', 'skiprows', fallback = 0), delimiter = cfg.get('DATA', 'delim', fallback = None))
			y = data[eval(cfg.get('TRANSFORM', 'start', fallback = '0')):eval(cfg.get('TRANSFORM', 'end', fallback = str(len(data[:,1])))):eval(cfg.get('TRANSFORM', 'step', fallback = '1'))]
			x = np.arange(0, len(y))
		else:
			data = np.loadtxt(file, usecols = (xcol, ycol), skiprows = cfg.getint('DATA', 'skiprows', fallback = 0), delimiter = cfg.get('DATA', 'delim', fallback = None))
			x = data[eval(cfg.get('TRANSFORM', 'start', fallback = '0')):eval(cfg.get('TRANSFORM', 'end', fallback = str(len(data[:,1])))):eval(cfg.get('TRANSFORM', 'step', fallback = '1')),0]
			y = data[eval(cfg.get('TRANSFORM', 'start', fallback = '0')):eval(cfg.get('TRANSFORM', 'end', fallback = str(len(data[:,1])))):eval(cfg.get('TRANSFORM', 'step', fallback = '1')),1]

		if cfg.getboolean('FLAGS', 'subtract_x0', fallback = False):
			x = x - x[0]
		if cfg.getboolean('FLAGS', 'subtract_y0', fallback = False):
			y = y - y[0]

		x = x * eval(cfg.get('TRANSFORM', 'xscale', fallback = '1.0'))
		y = y * eval(cfg.get('TRANSFORM', 'yscale', fallback = '1.0'))

		color = next(cycolors)
		plt.plot(x, y, color, label = (None if not labels else next(cylabels)))

		if cfg.getboolean('FLAGS', 'add_max', fallback = False):
			pos = np.argmax(abs(y))
			plt.plot(x[pos], y[pos], color, label = '_hidden', marker = 'x')
			plt.annotate(
				text = ('%.2f' % (y[pos])), 
				xy = (x[pos], y[pos]),
				xycoords = 'data', 
				xytext = (3, 5), 
				textcoords = 'offset points', 
				fontsize = mpl.rcParams['font.size']*0.75
			)

	# add plot elements
	plt.title(cfg.get('PLOT', 'title', fallback = None))
	if labels:
		plt.legend()
	plt.xlabel(cfg.get('PLOT', 'xlabel', fallback = None))
	plt.ylabel(cfg.get('PLOT', 'ylabel', fallback = None))
	plt.xlim(cfg.getfloat('PLOT', 'xmin', fallback = None), cfg.getfloat('PLOT', 'xmax', fallback = None))
	plt.ylim(cfg.getfloat('PLOT', 'ymin', fallback = None), cfg.getfloat('PLOT', 'ymax', fallback = None))
	plt.grid(axis = 'both')

	# export
	plot_name = cfg.get('PLOT', 'plot_name', fallback = os.path.splitext(c)[0])
	plt.savefig(plot_name + '.pgf')
	plt.savefig(plot_name + '.png', dpi = 300)

	plt.clf()
	print()
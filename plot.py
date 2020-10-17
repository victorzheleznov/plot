import codecs
import re
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# open cfg file
cfg = codecs.open('plot.cfg', encoding = 'utf-8', mode = 'r')

# read first line — list of columns
line = cfg.readline().strip()
line = re.split(' = |, ', line)
columns = line[1:len(line)]

# read second line — list of files
line = cfg.readline().strip()
line = re.split(' = |, ', line)
files = line[1:len(line)]
if len(files) != len(columns):
    sys.exit("invalid number of files")

# read third line — list of labels
line = cfg.readline().strip()
line = re.split(' = |, ', line)
labels = line[1:len(line)]
if len(labels) != len(columns):
    sys.exit("invalid number of labels")

# read fourth line — x axis label
line = cfg.readline().strip()
line = re.split(' = ', line)
xlabel = line[1]

# read fifth line — y axis label
line = cfg.readline().strip()
line = re.split(' = ', line)
ylabel = line[1]

# read sixth line — max point flag
line = cfg.readline().strip()
line = re.split(' = ', line)
add_max = int(line[1])
add_max = bool(add_max)

# read seventh line — plot name
line = cfg.readline().strip()
line = re.split(' = ', line)
plot_name = line[1]

cfg.close()

# colors list
colors = [
    '#e6194b', '#3cb44b', '#0082c8', '#f58231', '#911eb4', '#46f0f0', 
    '#f032e6', '#d2f53c', '#fabebe', '#008080', '#e6beff', '#aa6e28',
    '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000080',
    '#808080'
]

# set rc parameters
mpl.use('pgf')
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['pgf.texsystem'] = 'pdflatex'
mpl.rcParams['text.usetex'] = True
mpl.rcParams['pgf.preamble'] = "\\usepackage[T2A]{fontenc} \\usepackage[utf8]{inputenc} \\usepackage[english,russian]{babel} \\DeclareUnicodeCharacter{2212}{-}"
mpl.rcParams["figure.figsize"] = (6.69423, 4)

# create plot
for i in range(0, len(columns)):
    data = np.loadtxt(files[i], skiprows = 1, usecols = (0, int(columns[i])))
    x = data[:,0]
    y = data[:,1]
    plt.plot(x, y, label = labels[i], color = colors[i])
    
    if add_max:
        pos = np.argmax(abs(y))
        plt.plot(x[pos], y[pos], marker = 'x', color = colors[i])
        plt.annotate(
            text = ('%.2f' % (y[pos])), 
            xy = (x[pos], y[pos]), xycoords = 'data', 
            xytext = (3, 5), textcoords = 'offset points', 
            fontsize = mpl.rcParams['font.size']*0.75
        )

plt.legend()
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.grid(axis = 'both')
plt.tight_layout()

# export pgf
plt.savefig(plot_name + '.pgf')

# export png
plt.savefig(plot_name + '.png', dpi = 300)
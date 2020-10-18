import codecs
import re
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# open cfg file
cfg = codecs.open('plot.cfg', encoding = 'utf-8', mode = 'r')

# read list of y axis columns
line = cfg.readline().strip()
line = re.split(' = |, ', line)
if len(line) == 1:
    sys.exit("ycolumns list is empty")
ycolumns = line[1:len(line)]

# read list of x axis columns
line = cfg.readline().strip()
line = re.split(' = |, ', line)
if len(line) == 1:
    sys.exit("xcolumns list is empty")
xcolumns = line[1:len(line)]
if len(xcolumns) == 1 and len(ycolumns) > 1:
    xcolumns = xcolumns * len(ycolumns)
if len(xcolumns) != 1 and len(xcolumns) != len(ycolumns):
    sys.exit("invalid number of xcolumns")

# read list of files
line = cfg.readline().strip()
line = re.split(' = |, ', line)
if len(line) == 1:
    sys.exit("files list is empty")
files = line[1:len(line)]
if len(files) == 1 and len(ycolumns) > 1:
    files = files * len(ycolumns)
if len(files) != 1 and len(files) != len(ycolumns):
    sys.exit("invalid number of files")

# read list of labels
line = cfg.readline().strip()
line = re.split(' = |, ', line)
if len(line) == 1:
    add_legend = False
else:
    add_legend = True
    labels = line[1:len(line)]

# read x axis label
line = cfg.readline().strip()
line = re.split(' = ', line)
xlabel = line[1]

# read y axis label
line = cfg.readline().strip()
line = re.split(' = ', line)
ylabel = line[1]

# read max point flag
line = cfg.readline().strip()
line = re.split(' = ', line)
add_max = int(line[1])
add_max = bool(add_max)

# read plot name
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
for i in range(0, len(ycolumns)):
    data = np.loadtxt(files[i], skiprows = 1, usecols = (int(xcolumns[i]), int(ycolumns[i])))
    x = data[:,0]
    y = data[:,1]
    plt.plot(x, y, color = colors[i])
    
    if add_max:
        pos = np.argmax(abs(y))
        plt.plot(x[pos], y[pos], marker = 'x', color = colors[i])
        plt.annotate(
            text = ('%.2f' % (y[pos])), 
            xy = (x[pos], y[pos]), xycoords = 'data', 
            xytext = (3, 5), textcoords = 'offset points', 
            fontsize = mpl.rcParams['font.size']*0.75
        )

if add_legend:
    plt.legend(labels)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.grid(axis = 'both')
plt.tight_layout()

# export pgf
plt.savefig(plot_name + '.pgf')

# export png
plt.savefig(plot_name + '.png', dpi = 300)
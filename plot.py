import sys
import configparser
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from itertools import cycle

# set rc parameters
mpl.use('pgf')
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['pgf.texsystem'] = 'pdflatex'
mpl.rcParams['text.usetex'] = True
mpl.rcParams['pgf.preamble'] = "\\usepackage[T2A]{fontenc} \\usepackage[utf8]{inputenc} \\usepackage[english,russian]{babel} \\DeclareUnicodeCharacter{2212}{-}"
mpl.rcParams["figure.figsize"] = (6.69423, 4)

# get cfg files
if len(sys.argv) > 1:
    cfgfiles = sys.argv[1:]
else:
    cfgfiles = 'plot.cfg'

for c in cfgfiles:
    print(f'------ CFG `{c}` ------', flush = True)
    
    # read cfg file
    cfg = configparser.ConfigParser(allow_no_value = True)
    cfg.read(c, encoding = 'utf-8')
    
    # save cfg lists into variables
    files = list(map(str.strip, cfg.get('DATA', 'files').split(',')))
    ycols = list(map(str.strip, cfg.get('DATA', 'ycols').split(',')))
    xcols = list(map(str.strip, cfg.get('DATA', 'xcols').split(',')))
    labels = list(map(str.strip, cfg.get('PLOT', 'labels', fallback = None).split(',')))
    
    # define colors list
    colors = [
        '#e6194b', '#3cb44b', '#0082c8', '#f58231', '#911eb4', '#46f0f0', 
        '#f032e6', '#d2f53c', '#fabebe', '#008080', '#e6beff', '#aa6e28',
        '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000080',
        '#808080'
    ]
    
    # create cycle variables
    cycolors = cycle(colors)
    cyycols = cycle(ycols)
    cyxcols = cycle(xcols)
    cylabels = cycle(labels)
        
    # create plot
    for f in files:
        print(f'plot `{f}` file', flush = True)
        
        data = np.loadtxt(f, usecols = (int(next(cyxcols)), int(next(cyycols))), skiprows = cfg.getint('DATA', 'skiprows', fallback = 0), delimiter = cfg.get('DATA', 'delim', fallback = None))
        x = data[:,0]
        y = data[:,1]
        
        if cfg.getboolean('FLAGS', 'subtract_x_start_point', fallback = False):
            x = x - x[0]
        if cfg.getboolean('FLAGS', 'subtract_y_start_point', fallback = False):
            y = y - y[0]
            
        x = x * cfg.getfloat('TRANSFORM', 'xscale', fallback = 1.0)
        y = y * cfg.getfloat('TRANSFORM', 'yscale', fallback = 1.0)
        
        col = next(cycolors)
        plt.plot(x, y, color = col, label = next(cylabels))
        
        if cfg.getboolean('FLAGS', 'add_max', fallback = False):
            pos = np.argmax(abs(y))
            plt.plot(x[pos], y[pos], color = col, label = '_hidden', marker = 'x')
            plt.annotate(
                s = ('%.2f' % (y[pos])), 
                xy = (x[pos], y[pos]),
                xycoords = 'data', 
                xytext = (3, 5), 
                textcoords = 'offset points', 
                fontsize = mpl.rcParams['font.size']*0.75
            )
    
    # add plot elements
    plt.title(cfg.get('PLOT', 'title', fallback = None))
    plt.legend()
    plt.xlabel(cfg.get('PLOT', 'xlabel', fallback = None))
    plt.ylabel(cfg.get('PLOT', 'ylabel', fallback = None))
    plt.xlim(cfg.getfloat('PLOT', 'xmin', fallback = None), cfg.getfloat('PLOT', 'xmax', fallback = None))
    plt.ylim(cfg.getfloat('PLOT', 'ymin', fallback = None), cfg.getfloat('PLOT', 'ymax', fallback = None))
    plt.grid(axis = 'both')
    
    # export
    plot_name = cfg.get('PLOT', 'plot_name', fallback = 'plot')
    plt.savefig(plot_name + '.pgf')
    plt.savefig(plot_name + '.png', dpi = 300)
    
    plt.clf()
    print()
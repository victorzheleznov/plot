# plot — simple script to plot data files

## Overview

`plot` script is used to plot data from text files with multiple columns. Plot parameters are defined in configuration file with extension `.cfg`. Configuration file name is passed to the script as command line argument. For `test.cfg` file:
```
py plot.py test
```
I suggest making executable file from this script and defining it as enviromental variable. Like that, script will be executable from any place in a computer using `plot` command and you will only need to create local configuration files. Process of doing so is described in [Suggested use case](#suggested-use-case) section.



If you want to create several figures with one execution, multiple configuration files can be passed to the script:
```
plot fig1 fig2
```
As a result script will produce for each configuration file two graphic files: `.png` for regular use and `.pgf` for LaTeX.

In pdfLaTeX you should use utf-8 encoding and define the following lines to avoid compile errors: 
```
\usepackage[utf8]{inputenc}
\DeclareUnicodeCharacter{2212}{-}
```
You can always fork this repo and define your own rc parameters for `matplotlib` (don't forget to change `plt.savefig` if you change backend) and colors list inside `plot.py`.

## Configuration parameters

Some remarks about configuration  parameters:
- if parameter is not needed, it should be removed from configuration  file;
- `files`, `xcols`, `ycols` parameters are mandatory;
- lists are comma separated (like in `files` example below);
- lengths of `files`, `xcols`, `ycols` lists are independent — so it's possible to plot different y-columns with respect to one x-column without defining `xcols = 0, 0, 0` etc.;
- number of plotted lines is equal to max of `files` and `ycols` lengths;
- if `xcols < 0`, then y-axis data will be plotted against data index;
- text parameters can be written as LaTeX math: `labels = $y_1$, $y_2$`.
- `step` can be used for large data files to reduce `.png` and `.pgf` files size.

Full list of configuration parameters is provided below.

Section | Parameter | Description | Example
------------ | ------------ | ------------- | ------------- 
`DATA` | `files` | paths to data files | `files = dir1/file1.txt, dir2/file2.txt` 
|| `ycols` | column numbers to be taken as y-axis data | `ycols = 1, 2` 
|| `xcols` | column numbers to be taken as x-axis data | `xcols = 0` 
|| `skiprows` | number of rows to skip at the beginning of files | `skiprows = 1` 
|| `delim` | delimiter (remove `delim` for whitespace delimiter) | `delim = ,` 
`PLOT` | `title` | plot title |  `title = test plot` 
|| `labels` | legend labels | `labels = first file, second file` 
|| `xlabel` | x-axis label | `xlabel = sec` 
|| `ylabel` | y-axis label | `ylabel = m` 
|| `xmin` | lower x-axis limit | `xmin = 300` 
|| `xmax` | upper x-axis limit | `xmax = 360` 
|| `ymin` | lower y-axis limit | `ymin = -100` 
|| `ymax` | upper y-axis limit | `ymax = 100` 
|| `plot_name` | output graphic files name | `plot_name = test` 
`FLAGS` | `add_max` | add absolute max of y-axis data | `add_max = 0` 
|| `subtract_x0` | subtract x-axis data start point | `subtract_x0 = 1` 
|| `subtract_y0` | subtract y-axis data start point | `subtract_y0 = 1` 
`TRANSFORM` | `xscale` | scale factor for x-axis | `xscale = 0.0005`
|| `yscale` | scale factor for y-axis | `yscale = 6378137.0`
|| `start` | start data index  | `start = 1000`
|| `end` | end data index | `end = 21000`
|| `step` | integer data index step | `step = 2000`

## Suggested use case
I'm working on windows machine and will be talking about this OS.

1. Using `pyinstaller` create executable file `plot.exe`:
```
pyinstaller plot.py
```
2. Add folder containing `plot.exe` to the [PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).

After that, you can create configuration files anywhere you want and plot data files using `plot` cmd command.

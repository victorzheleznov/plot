# plot — multipurpose script to plot data files

## Overview

## Config parameters
Section | Parameter | Description | Example | Default
------------ | ------------ | ------------- | ------------- | -------------
`DATA` | `files` | paths to data files | `files = dir1/file1.txt, dir2/file2.txt`
|| `ycols` | column numbers to be taken as y-axis data | `ycols = 1, 2`
|| `xcols` | column numbers to be taken as x-axis data | `xcols = 0`
|| `skiprows` | number of rows to skip at the beginning of files | `skiprows = 1`
|| `delim` | data delimiter (remove this parameter for whitespace delimiter) | `delim = ,`
`PLOT` | `title` | plot title |  `title = test plot`
|| `labels` | legend labels | `labels = first file, second file`
|| `xlabel` | x-axis label | `xlabel = sec`
|| `ylabel` | y-axis label | `ylabel = m`
|| `xmin` | lower x-axis limit | `xmin = 300`
|| `xmax` | upper x-axis limit | `xmax = 360`
|| `ymin` | lower y-axis limit | `ymin = -100`
|| `ymax` | upper y-axis limit | `ymax = 100`
|| `plot_name` | output files name | `plot_name = test`
`FLAGS` | `add_max` | show absolute max of y-axis data | `add_max = 0`
|| `subtract_x_start_point` | subtract x-axis data start point | `subtract_x_start_point = 1`
|| `subtract_y_start_point` | subtract y-axis data start point | `subtract_y_start_point = 1`
`TRANSFORM` | `xscale` | scale factor for x-axis | `xscale = 0.0005`
|| `yscale` | scale factor for y-axis | `yscale = 6378137.0`
|| `start` | start data index  | `start = 1000`
|| `end` | end data index | `end = 21000`
|| `step` | integer data index step | `step = 2000`

Remarks about config parameters:
- if parameter is not needed, it should be removed from cfg file;
- everything is comma separated;
- number of files is always equal to number of lines;
- `step` can be used for large data files to reduce files size.

## My use case
I'm working on windows machine and will be talking about this OS.

1. Using `pyinstaller` package i create executable file `plot.exe`:
```
pyinstaller plot.py
```
2. 


> Note: to hide warnings during execution follow [this answer](https://stackoverflow.com/a/57766145)

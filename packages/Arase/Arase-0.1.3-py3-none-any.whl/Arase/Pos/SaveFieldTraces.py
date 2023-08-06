import RecarrayTools as RT
from .. import Globals
from .TraceFieldDay import TraceFieldDay
import DateTimeTools as TT
from .GetPos import GetPos
import os
import numpy as np

def SaveFieldTraces(Model='T96',StartDate=20170101,EndDate=20191231,Verbose=True,Overwrite=False):
	'''
	Saves the Tsyganenko field trace footprints for RBSP within a range 
	of dates.
	
	'''
	#populate the list of dates to trace first
	date = StartDate
	dates = []
	while date <= EndDate:
		dates.append(date)
		date = TT.PlusDay(date)
	n = np.size(dates)
	
	#now to load the position data
	pos = GetPos()

	#set the output path
	outpath = Globals.DataPath + 'Traces/{:s}/'.format(Model)
	if not os.path.isdir(outpath):
		os.system('mkdir -pv '+outpath)
	
	#loop throught the dates doing the traces
	for i in range(0,n):
		fname = outpath + '{:08d}.bin'.format(dates[i])
		if Overwrite or (not os.path.isfile(fname)):
			print('Tracing date {:8d} ({:d} of {:d})'.format(dates[i],i+1,n))
			T = TraceFieldDay(dates[i],Model,Verbose)
			RT.SaveRecarray(T,fname)
		else:
			print('File {:s} exists'.format(fname))

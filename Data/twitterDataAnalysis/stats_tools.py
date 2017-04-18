
import math
import random

def find_bin_index(val, bins):
	returnIndex = None

	binIndex = None
	rightEdge = None
	i = 0
	while i<len(bins):
		
		if val<=bins[i]:
			rightEdge = bins[i]
			break

		i = i +1

	
	if rightEdge is not None:
		binIndex = bins.index(rightEdge)-1
	#------------------------------------

	returnIndex = binIndex

	return returnIndex

def values_for_bins(data, binEdges):
	returnList = []

	#Identify points in each bin
	#---------------------------
	pointsPerBin = []
	for i in xrange(1, len(binEdges)):
		lEdge = binEdges[i-1]
		rEdge = binEdges[i]

		pointsInThisBin = [item[1] for item in data if (item[0]>lEdge and item[0]<=rEdge)]

		pointsPerBin.append(pointsInThisBin)
	#---------------------------

	for binIndex in xrange(len(pointsPerBin)):
		
		valsInBin = pointsPerBin[binIndex]

		if len(valsInBin)>0:
			avgOfPoints = reduce(lambda x,y: x+y, valsInBin)/len(valsInBin)
		else:
			avgOfPoints = 0

		returnList.append(avgOfPoints)

	return returnList

def cond_exp(jpNumpyTable, xBins, yBins, y_bin_vals, xVal):
	''' 
		Given a joint probability table, compute the
		expectation value of the second variable,
		given the fixed value of the first.

		'a2DHist' is in Numpy Array form.

		returns: float

	'''
	
	returnFloat = 0

	xBinIndex = find_bin_index(xVal, xBins)

	#Compute Pr(X)
	pr_x = reduce(lambda x,y: x+y, [v for v in jpNumpyTable[xBinIndex]])

	accum = 0

	#Determine y-value for each bin
	#----------------------------
	yBinVals = None
	if y_bin_vals is not None:
		yBinVals = y_bin_vals
	else:
		#If values are not provided,
		#then use the "middle" of each bin
		yBinVals = []
		for i in range(1, len(yBins)):
			lEdge = yBins[i-1]
			rEdge = yBins[i]

			width = float(rEdge - lEdge)
			val = rEdge - (width/2)
			yBinVals.append(val)
	#------------------------------

	for yBinVal in yBinVals:
		#print "yBinVal: %s" % yBinVal

		yBinIndex = find_bin_index(yBinVal, yBins)
		
		#print "yBinIndex: %s" % yBinIndex
		#print "xBinIndex: %s" % xBinIndex

		pr_y_x = jpNumpyTable[xBinIndex][yBinIndex]
		pr_yval_given_xval = float(pr_y_x)/pr_x

		#print "Pr(Y|X): %s" % pr_yval_given_xval 

		accum+=yBinVal*pr_yval_given_xval


	returnFloat = accum

	return returnFloat
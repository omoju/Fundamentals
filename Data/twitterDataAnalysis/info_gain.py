
import os
import sys
import numpy as np
import math


def findBinIndexFor(aFloatValue, binsList):
	#print "findBinIndexFor: %s" % aFloatValue
	returnIndex = -1

	for i in range(len(binsList)):
		thisBin = binsList[i]
		if (aFloatValue >= thisBin[0]) and (aFloatValue < thisBin[1]):
			returnIndex = i
			break

	return returnIndex

def compute_joint_prob(joint_list, vals1, vals2, bins1=None, bins2=None, asFreq=False):

	returnDict = {}

	for rec in joint_list:
		val1 = rec[0]
		val2 = rec[1]

		#Find name by which first val should appear
		dictName1 = val1
		if bins1 is not None:
			dictName1 = findBinIndexFor(val1, bins1)

		#Find name by which second val should appear
		dictName2 = val2
		if bins2 is not None:
			dictName2 = findBinIndexFor(val2, bins2)

		#If first name is not present in dict,
		#then initialize it
		if dictName1 not in returnDict:
			returnDict[dictName1] = {}

			for val in vals2:

				#Determine name under which
				#y-values should appear (i.e. as bin names
				#or as given names)
				asDictName = val

				if bins2 is not None:
					asDictName = findBinIndexFor(val, bins2)

				returnDict[dictName1][asDictName] = 0

		returnDict[dictName1][dictName2]+=1

	if not asFreq:
		#Normalize values
		for key in returnDict:
			for secondKey in returnDict[key]:
				returnDict[key][secondKey] = float(returnDict[key][secondKey]) / len(joint_list)

	return returnDict

def getXForFixedY(joint_prob_dist, yVal):
	returnList = []

	for key in joint_prob_dist:
		returnList.append( joint_prob_dist[key][yVal])

	return returnList

def compute_h(floatsList):
	returnFloat = None

	acc = 0

	for f in floatsList:
		if f != 0:
			acc = acc - f * math.log(f, 2)


	returnFloat = acc

	return returnFloat


#	Computes Kullback-Leibler divergence between
#	P(X,Y) and P(X)
def conditional_entropy(joint_prob_dist, xVals, yVals):
	returnFloat = None

	h_acc = 0

	marginal_y_dist = getYMarginalDist(joint_prob_dist)

	for x in xVals:
		for y in yVals:
			joint_xy = 0
			marginal_y = 0

			if not x in joint_prob_dist or y not in joint_prob_dist[x]:
				joint_xy = 0
			else:
				joint_xy = joint_prob_dist[x][y]

			if not y in marginal_y_dist:
				marginal_y = 0
			else:
				marginal_y = marginal_y_dist[y]

			if joint_xy!=0 and marginal_y!=0:
				h_acc-=joint_xy*math.log(joint_xy/marginal_y, 2)


	# for yVal in yVals:
	# 	new_xDist = getXForFixedY(joint_prob_dist, yVal)

	# 	h_yVal = compute_h(new_xDist)

	# 	p_yVal = reduce(lambda x, y: x+y, new_xDist)

	# 	h_acc+=p_yVal * h_yVal

	returnFloat = h_acc

	return returnFloat

def getYMarginalDist(joint_prob_dist):
	returnDict = {}

	for xKey in joint_prob_dist:
		for yKey in joint_prob_dist[xKey]:

			if not yKey in returnDict:
				returnDict[yKey] = 0

			returnDict[yKey]+=joint_prob_dist[xKey][yKey]

	return returnDict

def getXMarginalDist(joint_prob_dist):
	returnDict = {}

	for key in joint_prob_dist:
		yVals = joint_prob_dist[key]
		marginalVal = reduce(lambda x,y: x+y, [yVals[e] for e in yVals])

		returnDict[key] = marginalVal


	return returnDict

def entropy_loss(joint_prob_dist, xVals, yVals):
	returnFloat = None

	priorsDict = getXMarginalDist(joint_prob_dist)

	priors = priorsDict.values()
	h_prior = compute_h(priors)
	h_conditional = conditional_entropy(joint_prob_dist, xVals, yVals)

	returnFloat = h_prior - h_conditional

	return returnFloat

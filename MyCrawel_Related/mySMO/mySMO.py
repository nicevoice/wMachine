import os
import re
import sys
import math
import random
reload(sys)
sys.setdefaultencoding('utf-8')

# target - desired output vector
target = None
# point - training point matrix
point = None
# sampleN - numbers of samples
sampleN = None
# sampleD - dimensions of samples
sampleD = None
# alpha - Lagrange Multipliers, initialized 0
alpha = None
# error cache
error_cache = None
# parameter b
b = None
# c - tolerance
c = None
# params - kernel function parameters list
params = None
# eps - LH tolerance
eps = None
# tol - KKT tolerance
tol = None
# delta_b - changes between two b-s
delta_b = None
# cache for eucldDistance
CACHE_EUCDIS = None
# cache for KenerlRBF Function
CACHE_KERNEL = None

def globalInit():
	global target,point,sampleN,sampleD,alpha,error_cache,b,c,params,eps,tol,delta_b
	global CACHE_EUCDIS,CACHE_KERNEL
	formatFile()
	# target
	# point
	sampleN = len(point)
	sampleD = len(point[0])
	alpha = [0]*sampleN
	error_cache = [0]*sampleN
	b = 0
	c = 1.0
	params = [2.0]
	eps = 1.0E-12
	tol = 0.001
	delta_b = 0
	CACHE_EUCDIS = {}
	CACHE_KERNEL = {}

# check avalibility of variables
# such as numbers of dimensions corresponding
def globalCheck():
	pass

# Euclidean Distance
def eucldDistance2(i1,i2):
	global point,sampleD
	global CACHE_EUCDIS
	# seek whether cache exists
	if CACHE_EUCDIS.has_key((i1,i2)):
		return CACHE_EUCDIS[(i1,i2)]
	if CACHE_EUCDIS.has_key((i2,i1)):
		return CACHE_EUCDIS[(i2,i1)]
	result = 0
	for k in range(0,sampleD):
		result += ( (point[i1][k] - point[i2][k]) * (point[i1][k] - point[i2][k]) )
	if i1 <= i2:
		CACHE_EUCDIS[(i1,i2)] = result
	else:
		CACHE_EUCDIS[(i2,i1)] = result
	return result

# Gaussian Kernel (RBF)
def KERNEL_RBF(i1,i2):
	global params
	global CACHE_KERNEL
	if CACHE_KERNEL.has_key((i1,i2)):
		return CACHE_KERNEL[(i1,i2)]
	if CACHE_KERNEL.has_key((i2,i1)):
		return CACHE_KERNEL[(i2,i1)]
	result = math.exp(-eucldDistance2(i1,i2)/2/params[0]/params[0])
	if i1 <= i2:
		CACHE_KERNEL[(i1,i2)] = result
	else:
		CACHE_KERNEL[(i2,i1)] = result
	return result

# Calculate Output U
# Normally Use KERNEL_RBF as Kernel Function
def calcOutputU(i):
	global target,point,alpha,sampleN
	result = 0
	for j in range(0,sampleN):
		result += target[j]*alpha[j]*KERNEL_RBF(j,i)
	result -= b
	return result

# Calculate PsiL
def calcPsiL(a1,a2,y1,y2,s,E1,E2,k11,k22,k12,L):
	global b
	f1 = y1*(E1+b)-a1*k11-s*a2*k12
	f2 = y2*(E2+b)-s*a1*k12-a2*k22
	L1 = a1+s*(a2-L)
	PsiL = L1*f1+L*f2+0.5*L1*L1*k11+0.5*L*L*k22+s*L*L1*k12
	return PsiL

# Calculate PsiH
def calcPsiH(a1,a2,y2,s,E2,k11,k22,k12,H):
	global b
	f1 = y1*(E1+b)-a1*k11-s*a2*k12
	f2 = y2*(E2+b)-s*a1*k12-a2*k22
	H1 = a1+s*(a2-H)
	PsiH = H1*f1+H*f2+0.5*H1*H1*k11+0.5*H*H*k22+s*H*H1*k12
	return PsiH

# Calculate b
def calcB(a1,a1_new_clipped,a2,a2_new_clipped,y1,y2,E1,E2,k11,k12,k22):
	global b,delta_b
	b1 = E1+y1*(a1_new_clipped-a1)*k11+y2*(a2_new_clipped-a2)*k12+b
	b2 = E2+y1*(a1_new_clipped-a1)*k12+y2*(a2_new_clipped-a2)*k22+b
	b_new = None
	j1 = 0 < a1_new_clipped and a1_new_clipped < c
	j2 = 0 < a2_new_clipped and a2_new_clipped < c
	if j1 and j2:
		b_new = b1 # also b2
	elif j1:
		b_new = b1
	elif j2:
		b_new = b2
	elif a1_new_clipped == a2_new_clipped and (a1_new_clipped == c or a1_new_clipped == 0):
		b_new = 0.5*(b1+b2)
	else:
		b_new = 0.5*(b1+b2)
		# raise Exception("calcB(): Undefined b, alpha out of range")
	delta_b = b_new-b
	return b_new

# update error_cache
def calcError_Cache():
	global alpha,point,error_cache,c,delta_b,sampleN
	t1 = y1*(a1_new_clipped-a1)
	t2 = y2*(a2_new_clipped-a2)
	for k in range(0,sampleN):
		if(alpha[k] > 0 and alpha[k] < c):
			error_cache[k] += t1*KERNEL_RBF(i1,k)+t2*KERNEL_RBF(i2,k)-delta_b
	error_cache[i1] = 0
	error_cache[i2] = 0

# Count numbers of non-zero and non-c alpha
def countAlpha():
	global alpha,c
	result = 0
	for k in alpha:
		if k > 0 and k < c:
			result += 1
	return result

# Calculate KS
def calcKS():
	global alpha,target,sampleN
	result = 0
	for k in range(0,sampleN):
		result = max(result,1-target[k]*calcOutputU(k))
	return result


# Calculate heuristic value
def calcGap(nth):
	global alpha,target,c
	ks = calcKS()
	Gap = [0]*sampleN
	for k in range(0,sampleN):
		tmp = 0
		for j in range(0,sampleN):
			tmp += alpha[j]*target[j]*KERNEL_RBF(k,j)
		Gap[k] = alpha[k]*(target[k]*tmp-1)+c*ks
	Gap.sort(reverse=True)
	return Gap[nth]


def takeStep(i1,i2):
	global alpha,point,target,error_cache,b,c,eps
	if i1 == i2:
		return 0
	a1 = alpha[i1]
	a2 = alpha[i2]
	x1 = point[i1] # vector
	x2 = point[i2] # vector
	y1 = target[i1]
	y2 = target[i2]
	E1 = None
	E2 = None
	if a1 > 0 and a1 < c:
		E1 = error_cache[i1]
	else:
		E1 = calcOutputU(i1) - y1
	if a2 > 0 and a2 < c:
		E2 = error_cache[i2]
	else:
		E2 = calcOutputU(i2) - y2
	s = y1 * y2
	# calculate L,H
	L = 0
	H = c
	if s < 0:
		L = max(0,a2-a1)
		H = min(c,c+a2-a1)
	else:
		L = max(0,a2+a1-c)
		H = min(c,a2+a1)
	if L == H:
		return 0
	# calculate eta
	k11 = KERNEL_RBF(i1,i1)
	k12 = KERNEL_RBF(i1,i2)
	k22 = KERNEL_RBF(i2,i2)
	eta = k11 + k22 - 2 * k12
	a1_new = None
	a2_new = None
	a2_new_clipped = a2
	if eta > 0:
		a2_new = a2 + y2 * (E1 - E2) / eta
		if a2_new < L:
			a2_new_clipped = L
		elif a2_new > H:
			a2_new_clipped = H
	else:
		Lobj = calcPsiL(a1,L,y1,y2,s,E1,E2,k11,k22,k12,H)
		Hobj = calcPsiH(a1,H,y1,y2,s,E2,E2,k11,k22,k12,H)
		if Lobj < Hobj - eps:
			a2_new_clipped = L
		elif Lobj > Hobj + eps:
			a2_new_clipped = H
		else:
			a2_new_clipped = a2
	if math.fabs(a2_new_clipped-a2) < eps*(a2_new_clipped+a2+eps):
		return 0
	a1_new = a1+s*(a2-a2_new_clipped)
	# adjust a1_new (shown in psudocode C++)
	a1_new_clipped = a1_new
	if a1_new < 0:
		a2_new_clipped += s*a1_new
		a1_new_clipped = 0
	elif a1_new > c:
		a2_new_clipped += s*(a1_new-c)
		a1_new_clipped = c
	b = calcB(a1,a1_new_clipped,a2,a2_new_clipped,y1,y2,E1,E2,k11,k12,k22)
	# if liner, update w
	# seems not linear
	# global w = calcW(a1,a1_new_clipped,a2,a2_new_clipped,x1,x2,y1,y2)
	# update error cache ?
	alpha[i1] = a1_new_clipped
	alpha[i2] = a2_new_clipped
	return 1

def examineExample(i2):
	global target,alpha,c,sampleN
	y2 = target[i2]
	a2 = alpha[i2]
	E2 = None
	if a2 > 0 and a2 < c:
		E2 = error_cache[i2]
	else:
		E2 = calcOutputU(i2) - y2
	r2 = E2*y2
	if (r2 < -tol and a2 < c) or (r2 > tol and a2 > 0):
		if countAlpha() > 1:
			i1 = calcGap(1)
			if takeStep(i1,i2):
				return 1

		rd = int(random.uniform(0,sampleN-1))
		for k in range(rd,sampleN):
			if alpha[k] > 0 and alpha[k] < c:
				if takeStep(k,i2):
					return 1
		for k in range(0,rd):
			if alpha[k] > 0 and alpha[k] < c:
				if takeStep(k,i2):
					return 1			

		rd = int(random.uniform(0,sampleN-1))
		for k in range(rd,sampleN):
			if takeStep(k,i2):
				return 1
		for k in range(0,rd):
			if takeStep(k,i2):
				return 1

	return 0

def main():
	global target,point,alpha,sampleN
	numChanged = 0
	examineAll = 1
	while numChanged > 0 or examineAll == 1:
		numChanged = 0
		if examineAll == 1:
			for I in range(0,sampleN):
				numChanged += examineExample(I)
		else:
			for I in range(0,sampleN):
				if alpha[I] != 0 and alpha[I] != c:
					numChanged += examineExample(I)
		if examineAll == 1:
			examineAll = 0
		elif numChanged == 0:
			examineAll = 1

def formatFile():
	global target,point
	f = open("heart_scale","r")
	s = f.read()
	g = re.split("\n",s)
	n = len(g) - 1
	p = {}
	label = {}
	dimen = {}
	for k in range(0,n):
		p[k] = re.split(" |:",g[k])
		n1 = len(p[k]) - 1
		# print "n1=%s"%n1
		label[k] = float(p[k][0])
		dimen[k] = {}
		i = 0
		for i in range(1,n1,2):
			# print "i=%s"%i
			dimen[k][int(p[k][i])] = float(p[k][i+1])
		# check missing dimemsions
		for j in range(0,int(p[k][i])):
			if not dimen[k].has_key(j):
				dimen[k][j] = 0
	target = label
	point = dimen

def testify():
	global target,point,sampleN
	rlist = []
	sac = 0
	pac = 0
	for k in range(0,sampleN):
		tar = calcOutputU(k)
		rlist.append(tar)
		if (tar > 0 and target[k] > 0) or (tar < 0 and target[k] < 0):
			sac += 1
		if tar == target[k]:
			pac +=1
	print "SgnAccuracy %s/%s=%s"%(sac,sampleN,(float)(sac/sampleN))
	print "PerfectAccuracy %s/%s=%s"%(pac,sampleN,(float)(pac/sampleN))
	print "rlist:"
	print rlist


if __name__ == "__main__":
	print "environment - Done."
	print "globalInit - Process"
	globalInit()
	print "sampleD=%s,sampleN=%s"%(sampleD,sampleN)
	print "globalInit - Done."
	print "main - Process"
	main()
	print "main - Done."
	print alpha
	print "b=%s"%b
	print "testify - Process"
	testify()
	print "testify - Done."
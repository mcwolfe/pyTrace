import pngcanvas
import math

def dotProd(a,b):
	sum = a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
	return sum
	
def differenceVector(a,b):
	return [a[0]-b[0],a[1]-b[1],a[2]-b[2]]


def mult(t,v):
	return [v[0]*t,v[1]*t,v[2]*t]
	
def addV(a,b):
	return [a[0]+b[0],a[1]+b[1],a[2]+b[2]]
	
def isParallell(l,n):
	d=dotProd(l,n)
	if d==0:
		return True
	else:
		return False
		
def checkSides (triangle,tv,p):
	for x in range(3):
		tempVekt = differenceVector(p,triangle[x])
		side = dotProd(tv[x],tempVekt)
		print("tempvekt:", tempVekt)
		print("tv: ",tv[x])
		print("Side",side)
		if side<0:	
			return False
	return True
	
def crossProduct(a,b):
	return [a[1]*b[2]-a[2]*b[1],
	a[2]*b[0]-a[0]*b[2],
	a[0]*b[1]-a[1]*b[0]
	]
	
def setTriangleVectors(a):
	tv={}
	tv['v01']=differenceVector(a[1],a[0])
	tv['v02']=differenceVector(a[2],a[0])
	tv['v12']=differenceVector(a[2],a[1])
	tv['v10']=differenceVector(a[0],a[1])
	tv['v20']=differenceVector(a[0],a[2])
	tv['v21']=differenceVector(a[1],a[2])
	return tv
	
def setTriangleObject(triangle,Color =(255,255,255,255)):
	p0 = triangle[0]
	tv=setTriangleVectors(triangle)
	n=crossProduct(tv['v01'],tv['v02'])
	n =normalise(n)
	triangleObject={
		'triangle':triangle,
		'p0':triangle[0],
		'vectors':tv,
		'n':n,
		'color':Color
	}
	return triangleObject

def calcT(triangleObject,ray):
	p0=triangleObject['p0']
	l0 = ray['l0']	
	n = triangleObject['n']	
	l = ray['l']
	pminl = differenceVector(p0,l0)
	upperdot = dotProd(pminl,n)
	lowerdot = dotProd(l,n)
	t=upperdot/lowerdot
	return t

def calcP (t,ray):
	distance = mult(t,ray['l'])
	p = addV(ray['l0'],distance)
	return p
	
def planeIntersect(triangleObject,ray):
	t = 0
	if not isParallell(ray['l'],triangleObject['n']):
		t = calcT(triangleObject,ray)
		if t>0:
			return {'intersect':True, 't':t}
		else:
			return {'intersect':False, 't':t}
	else:
		return {'intersect':False,'t':t}
		

def triangleIntersect(ray,triangleObject):
	t = planeIntersect(triangleObject,ray)
	result ={'intersect':False,'p':[0,0,0]}
	if t['intersect']:
		p = calcP(t['t'],ray)
		r = checkSidesCross(triangleObject,p)
		result['intersect']=r
		result['p']=p
	return result
	
def rotatePoint(x,y,z,point):
	return newPoint
	
def vectorLength(v):
	s = v[0]*v[0]+v[1]*v[1]+v[2]*v[2]
	s = math.sqrt(s)
	return s
	
def normalise(v):
	l = vectorLength(v)
	r = [0,0,0]
	for i in range(3):
		r[i]=v[i]/l
	return r
	
def compareCross(v1,v2,p):
	cp1 = crossProduct(v1,p)
	cp2 = crossProduct(v1,v2)
	dot = dotProd(cp1,cp2)
	return dot>=0

def checkSidesCross(triangleObject,p):
	tv = triangleObject['vectors']
	triangle=triangleObject['triangle']
	tv0 = differenceVector(p,triangle[0])
	t1 = compareCross(tv['v01'],tv['v02'],tv0)
	if not t1:
		return t1
	tv1 = differenceVector(p,triangle[1])
	t2 = compareCross(tv['v12'],tv['v10'],tv1)
	if not t2:
		return t2
	tv2 = differenceVector(p,triangle[2])
	t3 = compareCross(tv['v20'],tv['v21'],tv2)
	if not t3:
		return t3
	return True

def lambert(n,lr):
	return dotProd(normalise(lr),normalise(n))
	

def inIntervall(v,mi,ma):
	return (v<=ma) and (v>=mi)
	
def solveLinear(k,m,y):
	return (y-m)/k
	
def intersectSquare(p,vec,bb,choice,):
	hit = False
	if vec[choice]==0:
		return False
	UV = getUV(choice)
	u=UV[0]
	v=UV[1]
	t1 = solveLinear(vec[choice],p[choice],bb[choice*2])
	t2 = solveLinear(vec[choice],p[choice],bb[choice*2+1])
	t= min(t1,t2)
	umi = bb[UV[0]*2]
	uma = bb[UV[0]*2+1]
	vmi = bb[UV[1]*2]
	vma = bb[UV[1]*2+1]	
	p1 = calcP(t,{'l0':p, 'l':vec})
	hit = inIntervall(p1[u],umi,uma) and inIntervall(p1[v],vmi,vma)
	return hit

def getUV(choice):
	if choice==0:
		return [1,2]
	if choice==1:
		return [0,2]
	if choice==2:
		return [0,1]
		
def intersectBox(p,v,bb):
	hit = False
	for i in range(0,3):
		hit= intersectSquare(p,v,bb,i)
	return hit
	

def getTriangles(nPolys,nVertices,point,vertices):
	prev=0
	triangleList = []
	for i in range(nPolys):
		triangle=[]
		if nVertices[i]==3:
			for j in range(nVertices[i]):
				pointNumber=vertices[j+prev]
				triangle.append(point[pointNumber])
			prev+=nVertices[i]
			triangleList.append(triangle)
		if nVertices[i]==4:
			triangle.append(point[j+prev])
			triangle.append(point[j+prev+1])
			triangle.append(point[j+prev+2])
			triangleList.append(triangle)
			triangle.append(point[j+prev])
			triangle.append(point[j+prev+2])
			triangle.append(point[j+prev+3])
			triangleList.append(triangle)
			prev+=nVertices[i]
	return triangleList
		


		


	
	

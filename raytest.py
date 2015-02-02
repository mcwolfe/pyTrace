from raytracer import *
import io
print("Raytracer")

point=[
[-2,0,5],
[2,0,5],
[0,2,5],
[4,1,3],
]

bb=[-2,4,0,2,3,5]
nPolys = 2
nVertices = [3,3]
vertices=[0,1,2,2,1,3]
triangleObjectList = []

triangleList = getTriangles(nPolys,nVertices,point,vertices)

for i in triangleList:
	triangleObjectList.append(setTriangleObject(i))

print(triangleObjectList)

light = {
	'p':[0,1,4.5],
	'strength':1,
	'color':(255,255,255,255)
	}

#ray = {'l0':[1,-2,0], 'l':[0,0,1]}

WIDTH = 512
HEIGHT = 512
BGCOLOR = (0,0,0,255)
FGCOLOR = (255,255,255,255)
YMAX = 5
YMIN = -5
XMAX = 5
XMIN = -5

YRANGE = YMAX-YMIN
XRANGE = XMAX-XMIN
YSTEP = YRANGE/HEIGHT
XSTEP = XRANGE/WIDTH
startY = YMAX-(YSTEP/2)
startX = XMIN+(XSTEP/2)

canvas = pngcanvas.PNGCanvas(WIDTH,HEIGHT,color=(0xff,0,0,0xff))
CURRCOL = BGCOLOR
for yp in range(0,HEIGHT):
	for xp in range(0,WIDTH):
		xcoord=startX+xp*XSTEP
		ycoord=startY-yp*YSTEP
		ray = {'l0':[xcoord,ycoord,0], 'l':[0,0,1]}
		CURRCOL = BGCOLOR
		if intersectBox(ray['l0'],ray['l'],bb)==True:
			for triangleObject in triangleObjectList:
				trace = triangleIntersect(ray, triangleObject)
				if trace['intersect']==True:
					lr=differenceVector(trace['p'],light['p'])
					li = lambert(triangleObject['n'],lr)
					SCOL = triangleObject['color']
					CURRCOL = (round(SCOL[0]*li),round(SCOL[1]*li),round(SCOL[2]*li),255)
		canvas.point(xp,yp,CURRCOL)


minfil=io.open('trace.png','wb')
minfil.write(canvas.dump())





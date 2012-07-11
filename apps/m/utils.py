from math import *
#import wingdbstub

def dot(A,B,C):
    AB = []
    BC = []
    AB.append(B[0] - A[0])
    AB.append(B[1] - A[1])
    BC.append(C[0] - B[0])
    BC.append(C[1] - B[1])
    dot_product = AB[0] * BC[0] + AB[1] * BC[1]
    return dot_product

def cross(A,B,C):
    AB = []
    AC = []
    AB.append(B[0] - A[0])
    AB.append(B[1] - A[1])
    AC.append(C[0] - A[0])
    AC.append(C[1] - A[1])
    cross_product = AB[0] * AC[1] - AB[1] * AC[0]
    return cross_product

def distance(A,B):
    d1 = A[0] - B[0]
    d2 = A[1] - B[1]
    return sqrt(d1*d1 + d2*d2)

def linePointDist(A,B,C,isSegment):
    dist = cross(A,B,C) / distance(A,B)
    if isSegment:
        dot1 = dot(A,B,C)
        if dot1 > 0:
            return distance(B,C)
        dot2 = dot(B,A,C)
        if dot2 > 0:
            return distance(A,C)
    return fabs(dist)

def mostInLineWith(newPt, closestPt, prevPt, nextPt):
    distance_from_next = linePointDist(closestPt,nextPt,newPt,1)
    distance_from_prev = linePointDist(closestPt,prevPt,newPt,1)
    if distance_from_prev < distance_from_next :
        return 'prevPt'
    else:
    	return 'nextPt'
    
#nPt = [9.998245792289, -84.1363555191879]   # 4
#cPt = [9.99743788852093, -84.1372809378511]  # 3
#pPt = [9.99704694908875, -84.136368986786]  # 2
#xPt = [9.997849959306214, -84.1368920175438]  # x

#print mostInLineWith(xPt,cPt,nPt,pPt)
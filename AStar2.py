import time
import threading
import numpy as np

class point:
    x=0
    y=0
    g=0
    h=0
    parentX=0
    parentY=0
    #parent = point(x,y) #the previous points

    def __init__(self, x, y): #we create a gridpoint
        self.x = x
        self.y = y

    def f(self):
        return self.g+self.h

    def strPos(self):
        return str(self.x) + ", " + str(self.y)

    def __lt__(self, other): #comparison between 2 points
        return self.f() < other.f()
    def __gt__(self, other):
        return self.f() > other.f()
    def __le__(self, other):
        return self.f() <= other.f()
    def __ge__(self, other):
        return self.f() >= other.f()



#required each point has weight f
#this is broken down as f = g+h where g is move cost from starting point, h is estimated cost to target
#Note that Dijkstra pathfinding is the same as A* with h=0 for all nodes

#create a closed list which we have visited already
#create an open list which we have yet to visit
#put the starting point in the open list

# while the open list in non-empty take the smallest value from it and find its successors/neighbours

# for each successor calculate the distance from start and estimated distance from end
# set the values in the successor

#if the there exists the same point in the open list as the successor with lower value skip
# if there exists a point in closed list as the successor which has lower value skip, if it has higher value add the successor to the open list
#end for each

#put original point in the closed list

def InsertAt(list, val): #we want to insert val to the appropriate place
    for i in range(len(list)):
        if val < list[i]: 
            list.insert(i,val)
            return i
    list.append(val)
    return len(list)-1
        #print("list at " + str(i) + " = " + str(list[i].f()))
    for i in range(len(list)):
        print("list at " + str(i) + " = " + str(list[i].f()))

def FindInList(list, val): #find a point in the list by coordinate
    for i in range(len(list)):
        if val.x != list[i].x: continue
        if val.y != list[i].y: continue
        return i #if both coordinates are the same return index
    return -1 #it never matched indecies return -1


def OneNorm(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def Is_Valid(p):
    if p.x<0 or p.x>gridSize[0]-1: return False
    if p.y<0 or p.y>gridSize[1]-1: return False
    return True

def Is_Blocked(p):
    for a in blockedList:
        if p.x != a.x: continue
        if p.y != a.y: continue
        return True #both coordinates are the same => blocked
    return False #None of the blocked coordinates are the same => not blocked

gridSize = [10,10]
blockedList = []
for i in range(4):
    x= 2*i + 1
    r = i % 2
    for j in range(9):
        blockedList.append(point(x,j+r))

for b in blockedList:
    print("blocked list Coordinates = " + b.strPos())

openList = []
closedList = []
start = point(0,0) #starting point
end = point(gridSize[0]-1, gridSize[1]-1) #target end point
start.g = 0
start.h = OneNorm(start,end) #manhattan distance or more mathematically known as one-norm
openList.append(start) #we add the initial starting point

print("target is at " + end.strPos())
t=0
moveList = []
while len(openList) > 0: #as long as we have atleast one open element
    t +=1
    parent = openList.pop(0)#remove at get item at index 0
    successors = []
    successors.append(point(parent.x-1, parent.y))
    successors.append(point(parent.x+1, parent.y))
    successors.append(point(parent.x, parent.y-1))
    successors.append(point(parent.x, parent.y+1))
    #these are the potential successive points
    for a in successors:
        if not Is_Valid(a): continue #if a is not a valid point go for next successor
        if Is_Blocked(a): continue
        
        a.parentX=parent.x
        a.parentY=parent.y

        #for graphs should should be the edge length
        a.g = parent.g+1 #we took one more step than the previous point
        a.h = OneNorm(a,end)
        f = a.f()
        print("a.h = " + str(a.h))

        if a.h <= 0.001: #we check if the estimated stiance is less than some small delta
            #this is the target
            print("found path")
            moveList.append(a) #add the target
            pX = parent.parentX
            pY = parent.parentY
            moveList.append(parent)
            while pX != start.x or pY != start.y:
                #print("pX = " + str(pX) + ", pY = " + str(pY))
                pi = FindInList(closedList, point(pX, pY)) # try to find parent in closed list
                par = closedList[pi] #parent
                moveList.append(par)
                pX = par.parentX
                pY = par.parentY
            successors.clear()
            openList.clear()
            break #break from outer while loop as we have found the path to target

        #now we check if this successor is already in the open list
        index = FindInList(openList, a)
        #if the successor is not in the list we get -1 if it is in we get the index
        cindex = FindInList(closedList, a)
        #print("went past indecies")


        #we note that a point can't be in both open and closed lists at once
        if index >= 0:
            #the point is already in the openList
            if f >= openList[index].f(): continue
        if cindex >=0:
            if f >= closedList[cindex].f(): continue
            closedList.remove(a) #since it is in the closed list and it has lower f remove from the closed list

        at = InsertAt(openList, a)
        #print("inserted at " + str(at))
        continue

    closedList.append(parent) #once we have went through all the successors add the paprent to the closed / already visited points
    print("t="+str(t))
    #if t>5: break #for debugging we quit out of the while loop after 5 iterations

for a in moveList: # movelist has the target first and the first move in last index
    print(a.strPos()) # we print the positions

if len(openList)>0:
    p = openList[0] #the closest estimated point to target
    print("closest point position = " + str(p.x) + ", " + str(p.y))
    print("closest point estimated distance h = " + str(p.h))
    print("closest point distance from start g = " + str(p.g))








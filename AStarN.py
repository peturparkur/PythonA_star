import time
import threading
import numpy as np

class point:
    coord = [0,0] #array of the coordinates
    g=0
    h=0
    parentCoord = [0,0] #array of the parent coordinates
    #parent = point(x,y) #the previous points

    def __init__(self, _coord): #we create a gridpoint
        self.coord = _coord

    def f(self):
        return self.g+self.h

    def strPos(self):
        string = ""
        for i in range(len(self.coord)):
            string += str(self.coord[i]) + ", "
        return string

    def __lt__(self, other): #comparison between 2 points
        return self.f() < other.f()
    def __gt__(self, other):
        return self.f() > other.f()
    def __le__(self, other):
        return self.f() <= other.f()
    def __ge__(self, other):
        return self.f() >= other.f()
    def SameCoord(self, other):
        for i in range(len(self.coord)): # we assume that it's all the same and just check if some coordinates differs
            if self.coord[i] != other.coord[i]: return False
        return True




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
        if not val.SameCoord(list[i]): continue
        #failed = False
        #for j in range(len(list[i].coord)): #we check all coordnites
            #if val.coord[i] != list[i].coord[i]: 
                #failed = True
                #break
        #if val.x != list[i].x: continue
        #if val.y != list[i].y: continue
        #if failed == True: continue # atleast one coordinate is differe thus it's not at this index
        return i #if both coordinates are the same return index
    return -1 #it never matched indecies return -1


def OneNorm(p1, p2):
    #return abs(p1.x - p2.x) + abs(p1.y - p2.y)
    sum = 0
    for i in range(len(p1.coord)):
        sum = sum + abs(p1.coord[i] - p2.coord[i])
    return sum

def Is_Valid(p):
    for i in range(len(p.coord)):
        if p.coord[i] < 0 or p.coord[i] > gridSize[i] : return False
    return True

def Is_Blocked(p):
    for a in blockedList:
        #if p.x != a.x: continue
        #if p.y != a.y: continue
        if not p.SameCoord(a): continue
        return True #both coordinates are the same => blocked
    return False #None of the blocked coordinates are the same => not blocked

gridSize = [10,10, 10, 10] # the length of the gridSize is the number of dimensions we have
dimension = len(gridSize) # dimesnsion of the problem
blockedList = []
#for i in range(4):
#    x= 2*i + 1
#    r = i % 2
#    for j in range(9):
#        blockedList.append(point([x,j+r, 0, 0]))

for b in blockedList:
    print("blocked list Coordinates = " + b.strPos())

openList = []
closedList = []
start = point([0,0, 0, 0]) #starting point
end = point([gridSize[0]-1, gridSize[1]-1, 0, 0]) #target end point
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
    #print(f" length of parent coordinates {len(parent.coord)}")
    for i in range(len(parent.coord)):
        sc = parent.coord
        sc[i] += 1
        #print(f"sc = {sc}")
        successors.append(point(list(sc)))#we need this so we create a new list/array and copy in the values from sc
        sc[i] -= 2 #=parent.coord[i]-1
        #print(f"sc2 = {sc}")
        successors.append(point(list(sc)))
        sc[i] += 1
    #print(f" length of successors {len(successors)}")
    #successors.append(point([parent.coord[0], parent.coord[1], parent.coord[2], parent.coord[3]])) # this would depend on the dimension of the problem
    #successors.append(point([parent.x+1, parent.y]))
    #successors.append(point([parent.x, parent.y-1]))
    #successors.append(point([parent.x, parent.y+1]))
    #these are the potential successive points
    for a in successors:
        #print(f" for {a.strPos()} is valid = {Is_Valid(a)}, and isblocked = {Is_Blocked(a)}")
        if not Is_Valid(a): continue #if a is not a valid point go for next successor
        if Is_Blocked(a): continue
        
        a.parentCoord = parent.coord #array coordinates

        #for graphs should should be the edge length
        a.g = parent.g+1 #we took one more step than the previous point
        a.h = OneNorm(a,end)
        f = a.f()
        print("a.h = " + str(a.h))

        if a.h <= 0.001: #we check if the estimated stiance is less than some small delta
            #this is the target
            print("found path")
            moveList.append(a) #add the target
            #pX = parent.parentX
            #pY = parent.parentY
            #pC = parent.parentCoord #the parent coordinates
            pcp = point(parent.parentCoord) #create point with the parent's parent coordinates
            moveList.append(parent)
            while not pcp.SameCoord(start):#pX != start.x or pY != start.y: while parent coordinate is not the same as start
                #print("pX = " + str(pX) + ", pY = " + str(pY))
                pi = FindInList(closedList, pcp) #try to find parent in closed list
                par = closedList[pi] #parent
                moveList.append(par)
                #pX = par.parentX
                #pY = par.parentY
                pcp.coord = par.parentCoord
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


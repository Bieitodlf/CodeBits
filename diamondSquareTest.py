import time
import matplotlib.pyplot as plt
from matplotlib import interactive
import matplotlib
matplotlib.use('Qt5Agg')
from mpl_toolkits import mplot3d
import numpy as np

class terrain:
    def __init__(self):
        pass

    def newDSquare(self, depth, n=1, variation=5, stitchingPoints=None):
        #everything should be generated clockwise from top left
        self.variation = variation
        x0 = 0
        y0 = 0
        self.width = (2 ** n) + 1
        self.hMap = np.full((self.width, self.width), 0, dtype=float)
        if stitchingPoints == None:
            self.stitchingPoints = np.zeros((4, self.width), dtype=float)
        else:
            self.stitchingPoints = stitchingPoints
        mapEnd = self.width - 1
        self.framecount = 0
        self.generateDiamond(x0, y0, mapEnd, mapEnd, depth)
        print(self.framecount)

    def generateDiamond(self, x0, y0, xmax, ymax, depth):
        self.framecount += 1
        print("framecount: ", self.framecount)
        if depth > 0:
            print("depth: ", depth)
            depth -= 1
            print("depth: ", depth)
            subSquareHalfWidth = (xmax - x0) // 2
            #calculate center point for each sub-square
            centerX = subSquareHalfWidth + x0
            centerY = subSquareHalfWidth + y0
            if subSquareHalfWidth == 1:
                print("reached bottom")
            corners = ((x0, y0), (xmax, y0), (xmax, ymax), (x0, ymax))
            
            average = 0
            for corner in corners:
                average += self.hMap[corner[0]][corner[1]]
            average /= 4
            randomNumber = np.random.normal(0, self.variation * depth, size=1)
            self.hMap[centerX][centerY] = average + randomNumber
            print("diamond value was assigned")

            self.generateSquare(corners, subSquareHalfWidth, centerX, centerY, depth)


    def generateSquare(self, corners, subSquareHalfWidth, centerX, centerY, depth):
        edges = ((centerX, corners[0][1]), (corners[1][0], centerY), (centerX, corners[2][1]), (corners[0][0], centerY))
        average = 0
        for edge in edges:
            try:#each case checks if the point is at a map edge to see if we need to use stitching points. stitching points are stored in a 2d array where the x coord denotes which edge (clockwise from the top) it stores, and the second coordinate denotes the values to use (stored top to bottom and left to right
                if (edge[1] == 0):
                    average += self.stitchingPoints[0][edge[1]] + \
                        self.hMap[edge[0] + subSquareHalfWidth][edge[1]] + \
                        self.hMap[edge[0]][edge[1] + subSquareHalfWidth] + \
                        self.hMap[edge[0] - subSquareHalfWidth][edge[1]]
                elif(edge[0] == self.width - 1):
                    average += self.hMap[edge[0]][edge[1] - subSquareHalfWidth] + \
                        self.stitchingPoints[1][edge[0]] + \
                        self.hMap[edge[0]][edge[1] + subSquareHalfWidth] + \
                        self.hMap[edge[0] - subSquareHalfWidth][edge[1]]
                elif(edge[1] == self.width - 1):
                    average += self.hMap[edge[0]][edge[1] - (subSquareHalfWidth)] + \
                        self.hMap[edge[0] + (subSquareHalfWidth)][edge[1]] + \
                        self.stitchingPoints[2][edge[0]] + \
                        self.hMap[edge[0] - subSquareHalfWidth][edge[1]]
                elif(edge[0] == 0):
                    average += self.hMap[edge[0]][edge[1] - subSquareHalfWidth] + \
                        self.hMap[edge[0] + subSquareHalfWidth][edge[1]] + \
                        self.hMap[edge[0]][edge[1] + subSquareHalfWidth] + \
                        self.stitchingPoints[3][edge[1]]
                else:
                    average += self.hMap[edge[0]][edge[1] - subSquareHalfWidth] + \
                        self.hMap[edge[0] + subSquareHalfWidth][edge[1]] + \
                        self.hMap[edge[0]][edge[1] + subSquareHalfWidth] + \
                        self.hMap[edge[0] - subSquareHalfWidth][edge[1]]
            except:
                print("offending edge: (", edge[0], edge[1], ") at coords: (", centerX, centerY, ")")
                raise
            average /= 4
            randomNumber = np.random.normal(0, self.variation * depth, size=1)
            
            self.hMap[edge[0]][edge[1]] = average + randomNumber

        self.generateDiamond(corners[0][0], corners[0][1], centerX, centerY, depth)
        self.generateDiamond(edges[0][0], edges[0][1], edges[1][0], edges[1][1], depth)
        self.generateDiamond(centerX, centerY, corners[2][0], corners[2][1], depth)
        self.generateDiamond(edges[3][0], edges[3][1], edges[2][0], edges[2][1], depth)
        
        
def linearInterpolation(array):
    loops = 0
    print(len(array), (len(array[0])))
    for x in range(0, len(array) - 1):
        for y in range(0, len(array[x]) - 1):
            if array[x][y] == 0:
                average = 0
                for direction in range(0, 7):
                    average += searchNonZero(x, y, array, direction)                    
                array[x][y] = average / 4
                loops += 1
                print(loops) 


def searchNonZero(x0, y0, array, direction):
    if direction == 0:
        ystep = 1
        xstep = 0
    elif direction == 1:
        xstep = 1
        ystep = 0
    elif direction == 2:
        xstep = 0
        ystep = -1
    elif direction == 3:
        xstep = -1
        ystep = 0
    elif direction == 4:
        xstep = -1
        ystep = -1
    elif direction == 5:
        xstep = 1
        ystep = -1
    elif direction == 6:
        xstep = 1
        ystep = 1
    elif direction == 7:
        xstep = -1
        ystep = 1

    x = x0
    y = y0
    value = 0
    while value == 0:
        x += xstep
        y += ystep
        if x >= len(array) or y >= len(array[0]) or x < 0 or y < 0:
            return 0
        else:
            value = array[x][y]
    return value

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='generate heightmap by means of diamond square algorithm')
    parser.add_argument('--nsize', action='store', type=int, help='value to generate map size')
    parser.add_argument('--depth', action='store', type=int, help='depth of recursion')
    parser.add_argument('--variation', action='store', type=float, help='defines size of variation in each step')
    parser.add_argument('--interpolate', action='store', type=bool, help='use interpolation')

    args = parser.parse_args()
    nsize = args.nsize
    variation = args.variation
    depth = args.depth

    landscape = terrain()
    landscape.newDSquare(depth, n=nsize, variation=variation)
    width = landscape.width
    height = width

    if depth != nsize and args.interpolate == True:
        print("interpolation step")
        linearInterpolation(landscape.hMap)
   
    fig = plt.figure()

    axes = fig.add_subplot(111, projection='3d')
    X, Y = np.meshgrid(range(width), range(height))
    axes.plot_surface(X, Y, landscape.hMap)
#    fig.savefig('./test.svg', format='svg')
    interactive(True)
    fig.show()
    time.sleep(5)


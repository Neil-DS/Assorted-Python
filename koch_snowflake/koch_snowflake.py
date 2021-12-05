import tkinter as tk
import math
import numpy as np

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576

class App():
    def __init__(self):
        self.root = tk.Tk()
      
        self.root.configure(bg='gray75', borderwidth=0)
        self.frame = tk.Frame(self.root, borderwidth=0, relief=tk.RAISED, bg='gray75')
        self.frame.pack_propagate(False)
        self.root.geometry('{}x{}+100+100'.format(SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.frame.pack()
        self.canvas = tk.Canvas(self.frame, height=SCREEN_HEIGHT, width=SCREEN_WIDTH, borderwidth=0, bg='black', highlightbackground='gray75')
        self.canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.listOPoints = []

    def drawLine(self, pointList, color):
        for pair in pointList:
            self.canvas.create_line(pair[0][0], pair[0][1], pair[1][0], pair[1][1],  fill=color)
            #self.canvas.create_text(pair[0][0], pair[0][1]+10, text='x:{}, y:{}'.format(pair[0][0], pair[0][1]), fill='orange')

    def drawLine2(self, pointList, color):
        for i in range(len(pointList)-1):
            self.canvas.create_line(pointList[i][0], pointList[i][1], pointList[i+1][0], pointList[i+1][1],  fill=color)
            #self.canvas.create_text(pair[0][0], pair[0][1]+10, text='x:{}, y:{}'.format(pair[0][0], pair[0][1]), fill='orange')

    #need to rotate a point around another point and return the new point?
    def RotateAround(self, centre, point):        
        print('rotate....')       

        angle = np.deg2rad(60)

        #rotate point around centre.
        #move to origin
        new_point = (point[0] - centre[0], point[1] - centre[1])
        #rotate
        new_roate = (math.cos(angle) * new_point[0], math.sin(angle) * new_point[1])
        #move back
        new_point = (new_roate[0] + centre[0], new_roate[1] + centre[1])

        print('old_centre: {}\nold_point: {}'.format(centre, point))
        print('new_point: {}'.format(new_point))
        
        return new_point

    def Rotate_Line(self, line, angle):
        #print('rotate', line)

        angle = np.deg2rad(angle)

        centre = line[0][0], line[0][1]
        point = line[1][0], line[1][1]
        
        oldX = line[1][0] - centre[0]
        oldY = line[1][1] - centre[1]

        newX = (oldX * math.cos(angle)) - (oldY * math.sin(angle))
        newY = (oldX * math.sin(angle)) + (oldY * math.cos(angle))

        newX = newX + centre[0]
        newY = newY + centre[1] 
        new_point = (newX, newY)

        return new_point

    def turtleRecursion(self, line_list, repetitions):
        #get some rotation matrix action going.
        point_list = []

        #also need to think through how to loop through these points recursivley and eventually return the whole list I want

        new_line_list = []
        #this should create a list of points from the lines passed in, including making new points.
        for line in line_list:
            X1 = line[0][0]
            Y1 = line[0][1]
            X2 = line[1][0]
            Y2 = line[1][1]           
            
            k = 1/3
            newX1 = (X1+(k*(X2-X1)))
            newY1 = (Y1+(k*(Y2-Y1)))
            
            k=2/3
            newX2 = (X1+(k*(X2-X1)))
            newY2 = (Y1+(k*(Y2-Y1)))
            
            point_list.append(line[0])
            point_list.append((newX1, newY1))
            point_list.append((newX2, newY2))
            point_list.append(line[1])

            #making 4 lines out of those points
            new_line_list.append([line[0], (newX1, newY1)])
            new_line_list.append([(newX1, newY1), (newX2, newY2)])
            
            new_line_list[-1][1] = self.Rotate_Line(new_line_list[-1], 60)

            something_newX = new_line_list[-1][0]
            something_newY = new_line_list[-1][1]
            
            new_line_list.append([(something_newX, something_newY), (newX2, newY2)])
            new_line_list.append([(newX2, newY2), (line[1])])

            
        color_list = ['blue',  'green', 'red', 'pink', 'orange', 'yellow']
        for i in range(len(new_line_list)):
            self.drawLine(new_line_list[i:i+1], color_list[i%6])
            
        #print('point list: {} length: {}'.format(point_list, len(point_list)))
        print('line list: {} length: {}'.format(new_line_list, len(new_line_list)))


        '''
        #rotate lines now instead
        #every 2nd and 3rd line to be rotated? 0 +1 +2 3 4 +5 +6 7 8 +9 +10 11 12
        #start no, then it's a yes yes no no yes yes no no pattern
        yes_no = 1
        rotate_bool = False
        
        for x in range(len(new_line_list)):
            if(rotate_bool):
                #this changes the 2nd point in the line to be whatever is returned, which isn't accurate.               
                new_line_list[x][1] = self.Rotate_Line(new_line_list[x], 120)
                    
            yes_no += 1
        
            if(yes_no == 2):
                yes_no = 0
                rotate_bool = not rotate_bool

        self.canvas.delete('all')
        for i in range(len(new_line_list)):
            self.drawLine(new_line_list[i:i+1], color_list[(i%6)])

        return new_line_list
        '''
    
    '''            
        i = 0
        #rotate every 2nd point by 60 deg anti-clock       
        for point in point_list:
            print('[{}]points: {}'.format(i, point))
            #need to turn the 2nd point around the first point.
            if (i % 2):
                point_list[i] = self.RotateAround(point_list[i-1], point)                
            i += 1


        
        #turning it back into lines so I can draw them
        line_list = []
        for i in range(len(point_list)-1): 
            line_list.append(point_list[i])
            line_list.append(point_list[i+1])
            i = i + 2
    
        
        return point_list

    '''

        #a list should be thrown away if there's a new recursion call. should only keep the deepest list
        #if repetitions - 1:
            #turtleRecursion(new_list)
            
    def recursiveThing(self, pointList, repetitions):
        newSides = []        
      
        #should I do the recursion by line and not full list of points?
        #trying to figure out how to draw away from a center and when to change the center with a full list of points

        #in the situation where there is 4 lines first and last lines still need to decide based on the previous midpoint
        #while the 2 in the middle need a new mid point to make the decision on

        
        for line in pointList:           
            X1 = line[0][0]
            Y1 = line[0][1]
            X2 = line[1][0]
            Y2 = line[1][1]          
            
            #divide in 3 lines.
            #k = 1/2
            #midXa = (X1+(k*(X2-X1)))
            #midYa = (Y1+(k*(Y2-Y1)))
            
            k = 1/3
            newX1 = (X1+(k*(X2-X1)))
            newY1 = (Y1+(k*(Y2-Y1)))
            
            k=2/3
            newX2 = (X1+(k*(X2-X1)))
            newY2 = (Y1+(k*(Y2-Y1)))
            
            #print('new point 1: x:{}y:{} \nnew point 2: x:{}y:{}'.format(newX1, newY1, newX2, newY2))

            #cutting out the middle segment in the line
            midLines = [((newX1, newY1),(newX2, newY2))]                        

            #getting the point where the new lines would meet if kept at their orignal distance
            rootboys = self.findPeak((newX1, newY1), (newX2, newY2))

            #get back two possible answers for the root lines. for forming a triangle.
           
            possiblePoint1 = (rootboys[0][0], rootboys[0][1])
            possiblePoint2 = (rootboys[1][0], rootboys[1][1])

            #which one is futher from triangle center
            triangleCenter = (350,350)
            len1 = self.getLineLen(possiblePoint1, triangleCenter)
            len2 = self.getLineLen(possiblePoint2, triangleCenter)

            if(len1 > len2):
                newPoint = possiblePoint1
            else:
                newPoint = possiblePoint2
                
            rootlines = [((newX1, newY1),(rootboys[0][0], rootboys[0][1])), ((rootboys[0][0], rootboys[0][1]),(newX2, newY2))]            
            rootlines2 = [((newX1, newY1),(rootboys[1][0], rootboys[1][1])), ((rootboys[1][0], rootboys[1][1]),(newX2, newY2))]

            actualNewPoint = [((newX1, newY1), newPoint), (newPoint, (newX2, newY2))]
            
            newLine = [((X1, Y1), (newX1, newY1)), ((newX2, newY2), (X2, Y2))]
            #self.drawLine(newLine, 'red')
            
            #need to remove the line from the list and add the news ones.
            
            newLines = [((X1, Y1), (newX1, newY1))] + actualNewPoint + [((newX2, newY2), (X2, Y2))]
            #for every line add the new points to the empty list.
            newSides += newLines
        
        #after all lines check to see if you call the function again
        if(repetitions > 0):
            if(repetitions == 1):                
                self.listOPoints = self.recursiveThing(newSides, repetitions - 1)
            else:
                self.recursiveThing(newSides, repetitions - 1)     
                
        #return at the end
        return newSides
        

    def findPeak(self, a, b):        
        lengthAB = self.getLineLen(a, b)
        #print('length of AB', lengthAB)

        #print('a0{} a1{} b0{} b1{}'.format(a[0], a[1], b[0], b[1]))
       
        ACvalues = self.getValuesOfFormula(a[0], a[1]) #returns the values of length formula when AC is unknown. first is no#X 2nd is #Ys 3rd is constant value
        #print('AC formula: {}x + {}y + {}'.format(ACvalues[0], ACvalues[1], ACvalues[2]))


        BCvalues = self.getValuesOfFormula(b[0], b[1])
        #print('BC formula: {}x + {}y + {}'.format(BCvalues[0], BCvalues[1], BCvalues[2]))

        ACBCx = ACvalues[0] - BCvalues[0]
        ACBCy = ACvalues[1] - BCvalues[1]
        ACBCconst = (ACvalues[2] - BCvalues[2])

        #making x = y+const, by turning x into a 1
        ACBCyF = (ACBCy / -ACBCx) #moving to other side of equation
        ACBCconstF = (ACBCconst / -ACBCx) #moving to toher side with -AC

        #print('AC - BC => {}x = {}y + {}'.format(int(ACBCx/ACBCx), ACBCyF, ACBCconstF))        
        
        results = self.plugXintoLength(ACvalues[0], ACvalues[1], ACvalues[2], lengthAB, ACBCyF, ACBCconstF)

        #print('\n\n\n')       

        return results

    '''
        #i now have x = c + y
        #plugging back in AC
        xcubedconst = pow(ACminusBCconst, 2)
        xcubedy = (ACminusBCys * ACminusBCconst)+(ACminusBCys * ACminusBCconst)
        xcubedsquare = ACminusBCys * ACminusBCys
        y1frombefore = 1

        #
        beforexconst = ACvalues[0] * ACminusBCconst
        beforeys = ACvalues[1] * ACminusBCys

        #
        otheryfrombefore = ACvalues[1]
        theconstfrombefore = ACvalues[2] - lengthAB

        #these names are scary
        yToPower2 = y1frombefore + xcubedsquare        
        yFlat = xcubedy + beforeys + otheryfrombefore
        constTotal = xcubedconst + beforexconst + theconstfrombefore

        print('substituting x back into AC: {}y\u00B2 {}y + {}'.format(yToPower2, yFlat, constTotal))

        coeff = [yToPower2, yFlat, constTotal]

        #this only gets the y or x, can't remember
        y = np.roots(coeff)
        print('solving the quadratic gives: y={} or y={}'.format(y[0], y[1]))

        x = ((ACminusBCys*y[0] + ACminusBCconst), (ACminusBCys*y[1] + ACminusBCconst))


        a = (x[0], y[0])
        b = (x[1], y[1])
        print('x: {} or {}'.format(x[0], x[1]))

        
        return (a, b)
    '''

    #you get the 2 possible x and y here. test for distance from the center of the triangle to determine which x/y pair to use.
    def plugXintoLength(self, xConst, yConst, leftConstant, rightConstant, xycFormulasY, xycFormulasConstant):
        #multiplying out the first square
        theCubes = xycFormulasY * xycFormulasY
        theYs = (xycFormulasConstant * xycFormulasY) + (xycFormulasConstant * xycFormulasY)
        theConstants = xycFormulasConstant * xycFormulasConstant

        #print('first bit {}y\u00B2 {}y {}'.format(theCubes, theYs, theConstants))

        #second bit
        theCubes += 1
        theYs += (xConst * xycFormulasY) + yConst
        theConstants += (xConst * xycFormulasConstant) + leftConstant - rightConstant
        
        #print('plugging x back into AC gives: {}y\u00B2 + {}y + {} = 0'.format(theCubes, theYs, theConstants))

        coeff = [theCubes, theYs, theConstants]
        results  = np.roots(coeff)

        #print('y roots are: {}'.format(results))

        #now you have y roots, get the values of the corresponding x
        x = ((results[0] * xycFormulasY) + xycFormulasConstant, (results[1] * xycFormulasY) + xycFormulasConstant)
        #print('x1: {} x2: {}'.format(x[0], x[1]))

        a = (x[0], results[0])
        b = (x[1], results[1])
        
        return (a, b)
        
        #secondSeg = pow(a[1], 2)
        
    #expands the length formula and adds some stuff togethers, doesn't touch the length on other side
    def getValuesOfFormula(self, x, y):          
        amountOfXs= -x + -x        
        amountOfConstant1 = pow(x, 2)
        
        amountOfYs = -y + -y
        amountOfConstant2 = pow(y, 2)


        return (amountOfXs, amountOfYs, amountOfConstant1 + amountOfConstant2)
        
    def getLineLen(self, a, b):
        x1 = a[0]
        y1 = a[1]
        x2 = b[0]
        y2 = b[1]

        First1 = x2 * x2
        First2 = (x2 * -x1) + (x2 * -x1)
        First3 = -x1 * -x1
        firstSeg = First1 + First2 + First3

        Second1 = y2 * y2
        Second2 = (y2 * -y1) + (y2 * -y1)
        Second3 = -y1 * -y1
        secondSeg = Second1 + Second2 + Second3

        #print('FIRST SEG:{} \nSECOND SEG:{}'.format(firstSeg, secondSeg))

        return firstSeg+secondSeg
        
            
def main():
    app = App()

    x1 = 20
    x2 = 280
    y1 = 280
    y2 = 280

    #list of points for the starting traingle
    screen_centre = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))

    triangle_half_width = 75
    triangle_half_height = 75
    
    point_list = []

    #start from a point around the centre
    start_point = (screen_centre[0] - triangle_half_width, screen_centre[1] + triangle_half_height)
    end_point = (screen_centre[0] + triangle_half_width, screen_centre[1] + triangle_half_height)    
    point_list.append([start_point, end_point])

    start_point = end_point
    end_point = (screen_centre[0], screen_centre[1] - triangle_half_height)
    point_list.append([start_point, end_point])

    start_point = end_point
    end_point = (screen_centre[0] - triangle_half_width, screen_centre[1] + triangle_half_height)
    point_list.append([start_point, end_point])    
    
    #print(pointList[0])    
    #app.drawLine(point_list, 'white')        
    #mylist = app.recursiveThing(point_list, 3)
    #print(mylist)   

    something_else = app.turtleRecursion(point_list, 1)
    print('turtle stuff:\n', something_else)

    #app.drawLine(something_else, 'yellow')

    app.root.mainloop()

    #koch(win,iterations,x1,y1,x2,y2)
    
main()

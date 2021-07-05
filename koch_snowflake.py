import tkinter as tk
import math
import numpy as np

class App():
    def __init__(self):
        self.root = tk.Tk()
      
        self.root.configure(bg='gray75', borderwidth=0)
        self.frame = tk.Frame(self.root, borderwidth=0, relief=tk.RAISED, bg='gray75')
        self.frame.pack_propagate(False)
        self.root.geometry('1240x960+100+100')
        
        self.frame.pack()
        self.canvas = tk.Canvas(self.frame, height=960, width=960, borderwidth=0, bg='black', highlightbackground='gray75')
        self.canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.listOPoints = []

    def drawLine(self, pointList, color):
        for pair in pointList:
            self.canvas.create_line(pair[0][0], pair[0][1], pair[1][0], pair[1][1],  fill=color)
            #self.canvas.create_text(pair[0][0], pair[0][1]+10, text='x:{}, y:{}'.format(pair[0][0], pair[0][1]), fill='orange')

    def turtleRecursion(self, pointList, repetitions):
        #get some rotation matrix action going.

        #get line
        #advance by 1 unit
        #rotate by -60 degrees
        #advance one unit
        #rotate by 120 deg
        #advance 1 unit
        #rotate by -60deg
        #advance one unit
        for line in pointList:
            #1 unit = 1/3 of that line
            X1 = line[0][0]
            Y1 = line[0][1]
            X2 = line[1][0]
            Y2 = line[1][1]

            mag = self.getLineLen((X1, Y1), (X2, Y2))

            print(mag)
            
            
            
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

    pointList = [((200, 500), (500, 500)),((500, 500),(350, 235)),((350, 235),(200, 500))]

    #print(pointList[0])    
    #app.drawLine(pointList, 'white')
    
    mylist = app.recursiveThing(pointList, 2)

    #print(mylist)
    app.drawLine(app.listOPoints, 'yellow')

    app.turtleRecursion(pointList, 2)

    app.root.mainloop()

    #koch(win,iterations,x1,y1,x2,y2)
    
main()

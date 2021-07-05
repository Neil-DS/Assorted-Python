import tkinter as tk
import inspect
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
        self.canvas = tk.Canvas(self.frame, height=960, width=960, borderwidth=0, bg='grey', highlightbackground='gray75')
        self.canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.root.bind("<Escape>", self.escClose)
        self.canvas.bind("<Motion>", self.move)

        self.boundaryList = [
            [(0, 3), (960, 3)],
            [(0, 957), (960, 957)],
            [(3, 3), (3, 960)],
            [(960, 3), (960, 960)],
            [(300, 300), (400, 400)],
            [(900, 100), (100, 110)],
            [(100, 600), (300, 270)],
            [(200, 150), (132, 531)],
        ]
        
        self.ray_caster = Ray((150, 500), 2, 0)
        self.checkRay()
        self.listOPoints = []

    def drawLine(self, line, color, w=1):
        self.canvas.create_line(line[0][0], line[0][1], line[1][0], line[1][1], fill=color, width=w)
        
    def drawList(self, pointList, color):
        for pair in pointList:
            self.canvas.create_line(pair[0][0], pair[0][1], pair[1][0], pair[1][1],  fill=color)

    def escClose(self, event):
        self.root.destroy()       

    def move(self, event): 
        self.ray_caster.x = event.x
        self.ray_caster.y = event.y
        #should reorder the boundary list here based on distance from the ray.
        self.checkRay()

    def checkRay(self):
        self.canvas.delete('all')
        '''
        casts 62 rays out and checks all the boundaries in the list. 
        if the distance from the ray is smaller than previous one, make it the new collision point otherwise do nothing
        and at the end if there has been an intersection at all draw the line.
        '''        
        for i in range(0,360,1):
            ray_out = Ray((self.ray_caster.x, self.ray_caster.y), 2, np.radians(i))
            pointDistance = 1000000
            saved_intersection = 0
            for line in self.boundaryList:            
                ray_intersection = castRay(ray_out, line) #sees if there is an intersection, false if none otherwise returns intersection point.

                if ray_intersection:
                    a = np.array((self.ray_caster.x, self.ray_caster.y))
                    b = np.array(ray_intersection)
                    newDist = np.linalg.norm(a - b)

                    if(newDist < pointDistance):
                        pointDistance = newDist
                        saved_intersection = ray_intersection

                self.ray_caster.draw(self.canvas)
                self.drawLine(line, 'black', w=3)

            if saved_intersection:
                self.drawList([[(self.ray_caster.x, self.ray_caster.y), saved_intersection]], '#E1FF00')
                
class Ray():
    def __init__(self, position, radius, direction):
        self.x = position[0]
        self.y = position[1]
        self.r = radius
        self.direction = direction

    def draw(self, canvas):
        x0 = self.x - self.r
        y0 = self.y - self.r
        x1 = self.x + self.r
        y1 = self.y + self.r        
        #return canvas.create_oval(x0, y0, x1, y1, fill='#E1FF00')

    def move(self, newPos):
        self.x = newPos[0]
        self.y = newPos[1]
        

def castRay(ray, boundary):    
    x1 = boundary[0][0]
    y1 = boundary[0][1]
    x2 = boundary[1][0]
    y2 = boundary[1][1]

    #I'm using this as a line, but it should be a point with a direction? cause right now it's just a line extending in an infinite direction both ways.
    #I only want it to extend infinetly in the direction it is pointing.
    x3 = ray.x
    y3 = ray.y
    x4 = ray.x + math.cos(ray.direction)
    y4 = ray.y + math.sin(ray.direction)

    uNum = (x2 - x1)*(y1-y3)-(y2-y1)*(x1-x3)
    uDen = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
    #parrelel if den == 0
    if uDen == 0:
        return False
    
    u = uNum/uDen
        
    denominator = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)

    #lines are parralel and will never intersect if denominator is 0 so exit the cast.
    if(denominator == 0):
        return False

    numerator = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))

    t  = numerator / denominator
    #print("numerator: {}, denominator: {}, division: {}".format(numerator, denominator, t))
    Px = (x1 +t*(x2-x1))
    Py = (y1+t*(y2-y1))
        
    if 1 > t and t > 0:
        #print("numerator: {}, denominator: {}, division: {}".format(numerator, denominator, t))

        if(u >= 0): #infinite in 1 direction.
            return (Px, Py)
        else:
            return False
        
def main():
    app = App()
    print(inspect.signature(app.canvas.create_line))
    app.root.mainloop()


main()

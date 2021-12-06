import tkinter as tk
import math
import numpy as np
import time
from time import sleep

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

    
    def RotateLine(self, line, angle):
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
        new_point = newX, newY

        return new_point

    
    #this works a little differently than I think it should in general implementation?
    #mines splits each line into 3, 1st and 4th lines are unchanced
    #the program takes the 2nd line and rotates the 2nd point in that line by 60deg.
    #it then uses that new rotated point as the start for a new line to create the tip of the triangle
    #does this for every line in the list.
    #the function then calls itself recursivly.


    #I think normal implementations use a direction and a distance to walk in, this allows different shapes to be used as a base
    #and to issue different 'commands' instead of walking forward for x, walk forward for x*2 etc..
    def TurtleRecursion(self, line_list, repetitions):
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

            #immeditaly rotate the 2nd line and use it's ending point as the start for the 3rd line.
            new_point = self.RotateLine(new_line_list[-1], 60)
            new_line_list[-1][1] = new_point

            #I want the x,y of the previous point that got rotated

            #print('triangle', new_triangle_x, new_triangle_y)
            
            new_line_list.append([new_point, (newX2, newY2)])
            new_line_list.append([(newX2, newY2), (line[1])])            


        repetitions -= 1

        if(repetitions == 0):
            return new_line_list
        else:
            #print('\nline list: {} length: {}'.format(new_line_list, len(new_line_list)))
            new_line_list = self.TurtleRecursion(new_line_list, repetitions)
            return new_line_list

#creates the starting triangle for the koch algorithm
def CreateStartingTriangle(centre, width, height):    
    #centre of the triangle to draw
    triangle_centre = centre    
    triangle_half_width = width / 2
    triangle_half_height = height / 2

    point_list = []

    #start from a point around the centre
    start_point = (triangle_centre[0] - triangle_half_width, triangle_centre[1] + triangle_half_height)
    end_point = (triangle_centre[0] + triangle_half_width, triangle_centre[1] + triangle_half_height)    
    point_list.append([start_point, end_point])

    start_point = end_point
    end_point = (triangle_centre[0], triangle_centre[1] - triangle_half_height)
    point_list.append([start_point, end_point])

    start_point = end_point
    end_point = (triangle_centre[0] - triangle_half_width, triangle_centre[1] + triangle_half_height)
    point_list.append([start_point, end_point])       

    return point_list
        
'''
things I could do:
animate the rescursive steps based on a timer or keypress
create a new snowflake centred on mouse click
move all the snowflakes downwards while animating to creating a snowfall like effect
look into the square versions of the snowflake, or other versions in general
check the accuracy of my algo, inverse koch doesn't look the same on mine as it does on wiki

'''
def main():
    app = App()

    centre = ((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    width = 150
    height = 150
    
    point_list = CreateStartingTriangle(centre, width, height)        
    first_snowflake = app.TurtleRecursion(point_list, 2)

    centre = (150, 75)
    width = 100
    height = 100

    point_list = CreateStartingTriangle(centre, width, height)        
    second_snowflake = app.TurtleRecursion(point_list, 3)

    centre = (700, 125)
    width = 250
    height = 250

    point_list = CreateStartingTriangle(centre, width, height)        
    third_snowflake = app.TurtleRecursion(point_list, 4)
    
    color_list = ['blue',  'green', 'red', 'pink', 'orange', 'yellow']
    for i in range(len(first_snowflake)):
        app.drawLine(first_snowflake[i:i+1], 'white')

    for i in range(len(second_snowflake)):
        app.drawLine(second_snowflake[i:i+1], 'orange')

    for i in range(len(third_snowflake)):
        app.drawLine(third_snowflake[i:i+1], 'red')
    
    
    app.root.mainloop()
    
main()

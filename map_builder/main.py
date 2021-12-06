import tkinter as tk
import math as math
import numpy as np
import json
import random as rand

from PIL import Image, ImageTk

class display_block(tk.Label):
    def __init__(self, im, index, func, pos):
        tk.Label.__init__(self, image=im, bd=0)
        self.image = im
        self.indexValue = index
        self.position = pos

        self.place(x=pos[0], y=pos[1])
        self.bind("<Button-1>", lambda event, a=self.indexValue:func(event, a))

class App():
    def __init__(self):
        self.root = tk.Tk()

        #for making the map actual draw in the middle of the canvas.
        self.draw_entire_map_offset = 350
      
        self.root.configure(bg='gray75', borderwidth=0)
        self.frame = tk.Frame(self.root, borderwidth=0, relief=tk.RAISED, bg='gray75')
        self.frame.pack_propagate(False)
        self.root.geometry('1920x1080+100+100')        
        self.frame.pack()
        
        self.canvas = tk.Canvas(self.frame, width=1920, height=900, borderwidth=0, bg='black', highlightbackground='gray75')
        self.canvas.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.blockPickerCanvas = tk.Canvas(self.frame, width=250, height=250, borderwidth=0, bg='#ED5748', highlightbackground='gray75')
        self.blockPickerCanvas.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.root.bind("<Escape>", self.escClose)
        self.root.bind("<F1>", self.saveFile)
        self.canvas.bind("<Button-1>", self.clickedSquare)
        self.canvas.bind("<Key>", self.offchange)

        self.worldSquares = []
        self.blockSize = 10
        self.blockColor = 'white'
        self.drawingXOffset = 0
        self.drawingYOffset = 0

        self.im = Image.open('W:\\Work\\Assorted-Python\\map_builder\\backgrounds.png')
        print(self.im.format, self.im.size, self.im.mode)
        #self.im = self.im.resize((self.blockSize*4, self.blockSize*4), Image.ANTIALIAS)
        self.imageArray = []
        self.labelArray = []

        self.selectedIndex = 0.0
        self.imageSize = 25, 25

        #for how much of the image dims i want to load
        imageWidth = 40
        imageHeight = 8

        #fetches sprites off disk and resizes them
        for i in range(imageHeight):
            for j in range(imageWidth):
                cropDim = ((j*32), (i*32), (j*32)+32, (i*32)+32)
                self.test = ImageTk.PhotoImage(self.im.crop(cropDim).resize(self.imageSize))
                self.imageArray.append([self.test, j+(i*imageWidth)])

        #got through each image and put it on the bottom of the screen to allow for selecting sprites
        for i in range(imageHeight):
            for j in range(imageWidth):
                self.test = self.imageArray[j+(i*imageWidth)][0]
                position = ((j*26)+450, (i*26)+910)
                label = display_block(self.test, j+(i*imageWidth), self.pickedSquare, position)         
                self.labelArray.append(label)      

    def refresh(self):
        self.canvas.delete("all")
        self.drawSquare()

    def saveFile(self, event):
        with open('W:\Psychosis Defined\data\world_layout.pdmap', 'w+') as f:
            json.dump(self.worldSquares, f)
            f.close()
        print('SAVED')
        
    def escClose(self, event):
        self.root.destroy()

    def clickedSquare(self, event):
        xBlock = math.floor((event.x+self.drawingXOffset+12-self.draw_entire_map_offset)/self.imageSize[0])
        yBlock = math.floor((event.y+self.drawingYOffset+12)/self.imageSize[0])
        print("sprite placed at x: {}, y: {}".format(xBlock, yBlock))

        print(self.worldSquares[(xBlock)+(yBlock*100)])
        self.worldSquares[xBlock+(yBlock*100)][2] = int(self.selectedIndex)

        self.refresh()

    def pickedSquare(self, event, a):        
        print("sprite index: {}".format(self.imageArray[a][1]))
        self.selectedIndex = a

    def offchange(self, event):
        scrollSpeed = 25
        if(event.char == 'a'):
            self.drawingXOffset -= scrollSpeed
        elif(event.char == 'd'):
            self.drawingXOffset += scrollSpeed
        elif(event.char == 'w'):
            self.drawingYOffset -= scrollSpeed
        elif(event.char == 's'):
            self.drawingYOffset += scrollSpeed

        self.refresh()
       
    def drawSquare(self):
        for each in self.worldSquares:
            #this is so I can have small world blocks but still draw at a size I can see easily on screen.
            x = each[0] + ((self.imageSize[0]-self.blockSize)*(each[0]/self.blockSize)) #trying to scale the image
            y = each[1] + ((self.imageSize[0]-self.blockSize)*(each[1]/self.blockSize)) #
            #this is for only drawing world blocks within a certain range.
            if((x > self.drawingXOffset and x < (self.drawingXOffset+1225)) and
               (y > self.drawingYOffset and y < (self.drawingYOffset+900))):               
                self.canvas.create_image(x-self.drawingXOffset+self.draw_entire_map_offset, y-self.drawingYOffset, image=self.imageArray[each[2]][0])
        self.canvas.focus_set()
            

def main():
    app = App()

    with open('W:\Psychosis Defined\data\world_layout.pdmap', 'r') as f:
        app.worldSquares = json.load(f)
        f.close()

    '''
    #random 1-7 then add that to either 17, 57, or 97?
    sprites_to_pick_from = [40, 41, 42, 43, 120, 121, 122, 123]
    for i in range(10000):
        if(app.worldSquares[i][2] == 7):
            if(rand.randint(0,100) < 5):
                nicething  = rand.choice(somelist) + rand.randrange(15)
                app.worldSquares[i][2] = nicething
    '''

    '''
    #if you want to make a new one with different dimensions
    sprites_to_pick_from = [40, 41, 43]
    for i in range(100):
        for j in range(100):           
            app.worldSquares.append([j*app.blockSize, i*app.blockSize, sprites_to_pick_from[rand.randrange(len(sprites_to_pick_from))]])
    '''
    
    app.drawSquare()
    app.root.mainloop()

main()

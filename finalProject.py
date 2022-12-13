

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import numpy as np
import math
import os
from datetime import date
import imghdr

from numpy.lib.arraypad import pad
from numpy.lib.shape_base import column_stack

######################################
#drop-down menu 

def select():
    if clicked.get() == 'Error Diffusion':
        errorDiffusion(im)
    elif clicked.get() == 'Median Filter':
        medianFilter(im)

######################################
#recieves a list of 9 unsorted integers and sorts them using the bubble sort algorithm
#returns the median of the list

def median(unsortedList):

    values = unsortedList
    
    n = 9

    sorted = True

#bubble sort algorithm

    while (sorted == True) and (n>=0):
        sorted = False
        for i in range(n-2):
            if values[i] > values[i+1]:
                temp = values[i+1]
                values[i+1] = values[i]
                values[i] = temp
                sorted = True
        n = n-1
    
#returns the median value   

    return(values[4])

######################################
#applies the median filter to the image

def medianFilter(img):
    global imgLabel
    global im

    #converts image to grayscale then converts image to a numpy array

    img = img.convert('L')
    arrayA = np.array(img)
    rows, cols = np.shape(arrayA)

    arrayB = np.zeros((rows+2, cols+2))
    finalArray = np.zeros((rows, cols))

    arrayB[1:rows+1, 1:cols+1] = arrayA

    #loops through all values in array except boundary elements

    for i in range(1, rows+1):
        for j in range(1, cols+1):
             unsortedValues = []

             #loops for every surrounding pixel

             for l in range(-1, 2):
                 for k in range(-1, 2):
                    unsortedValues.append(arrayB[i+k, j+l])
                    
             finalArray[i-1,j-1] = median(unsortedValues)
               
    arrayC = (finalArray).astype(np.uint8)
    
    #converts the 2d array into a 3d array

    endArray = np.empty((rows, cols, 3), dtype=np.uint8)
    endArray[:, :, 0] = arrayC
    endArray[:, :, 1] = arrayC
    endArray[:, :, 2] = arrayC
   
    imgEdit = Image.fromarray(endArray)
    
    im = imgEdit  
    finalImg = ImageTk.PhotoImage(imgEdit)
    imgLabel.config(image = finalImg)
    root.update()
    imgLabel.displayImg = finalImg
                           
######################################
#applies the error diffusion effect to the image

def errorDiffusion(img):
    global imgLabel
    global im

    #converts the image to grayscale then converts the image to a numpy array

    img = img.convert('L')
    arrayA = np.array(img)
    rows, cols = np.shape(arrayA)

    arrayB = np.zeros((rows,cols))
    arrayC = np.zeros((rows+2, cols+2))
    

    arrayC[1:rows+1, 1:cols+1] = arrayA
    
    #loops through all values in array except boundary elements

    for i in range(1, rows+1):
        for j in range(1, cols+1):
            if arrayC[i,j] < 128:
                arrayB[i-1,j-1] = 0
                carry = arrayC[i,j]
            else:
                arrayB[i-1,j-1] = 255
                carry = arrayC[i,j] - 255
            
            arrayC[i,j+1] = arrayC[i,j+1] + 7*carry/16
            arrayC[i+1,j-1] = arrayC[i+1,j-1] + 3*carry/16     
            arrayC[i+1,j] = arrayC[i+1,j] + 5*carry/16
            arrayC[i+1,j+1] =arrayC[i+1,j+1] + carry/16

    
    arrayB = (arrayB).astype(np.uint8)
    
    endArray = np.empty((rows, cols, 3), dtype=np.uint8)
    
    #converts the 2d array into a 3d array

    endArray[:, :, 0] = arrayB
    endArray[:, :, 1] = arrayB
    endArray[:, :, 2] = arrayB

    imgEdit = Image.fromarray(endArray)
    
    im = imgEdit  

    finalImg = ImageTk.PhotoImage(imgEdit)
    imgLabel.config(image = finalImg)
    imgLabel.displayImg = finalImg
    root.update()
            
######################################
#validates the path selected by the user and passes it onto the main window

def endWindow():
    
    inputValue=imgLocation.get()

    #validation that ensures the path selected by the user is an existing image file
    if os.path.isfile(inputValue) == False :
        text1.config(text="Invalid path")
        return
    elif imghdr.what(inputValue) not in ("png", "jpeg", "bmp"):
        text1.config(text="Invalid file type")
        return
    
    root.deiconify()
    inputWindow1.destroy()
    openEditor(inputValue)


######################################
#creates the window for selecting a new image

def changeImage():
    global inputWindow2
    global tempImgLocation
    global tempText


    inputWindow2 = Toplevel(root)
    inputWindow2.geometry("+300+300")
    inputWindow2.title('')
    inputWindow2.resizable(width=False, height=False)
    tempText = Label(inputWindow2, text='Enter image path')
    tempText.grid(row=0, column = 0)
    tempImgLocation = Entry(inputWindow2, borderwidth=5)
    tempImgLocation.grid(row=1,column=0)
    tempEnter = Button(inputWindow2, text="Enter", command = lambda: updateImage())
    tempEnter.grid(row=2, column = 0)
    

######################################
#changes the image to the new selected image

def updateImage():
    
    global im

    location = tempImgLocation.get()

#validation that ensures the path selected by the user is an existing image file

    if os.path.isfile(location) == False:
        tempText.config(text="Invalid path")
        return
    elif imghdr.what(location) not in ("png", "jpeg", "bmp"):
        tempText.config(text="Invalid file type")
        return
        
    im = Image.open(location)
    updatedImg = ImageTk.PhotoImage(im)

 ##image is scaled down

    width, height = im.size

    while min(width, height) > 500:
       width = width/2
       height = height/2

    
    im = im.resize((int(width), int(height)))

    updatedImg = ImageTk.PhotoImage(im)
    
    imgLabel.config(image = updatedImg)
    imgLabel.dsiplayImg = updatedImg
    root.update()
    inputWindow2.destroy()
    

######################################
#creates the save image window

def openSaveWindow(img):
    global saveWindow
    global saveName
    saveWindow = Toplevel(root)
    saveWindow.geometry("+300+300")
    saveWindow.title('')
    saveWindow.resizable(width=False, height=False)
    
#creates save image window buttons

    text2 = Label( saveWindow, text='Enter save name')
    text2.grid(row=2, column = 0)
    saveName = Entry(saveWindow, borderwidth=5)
    saveName.grid(row=3,column=0)
    

    enter = Button(saveWindow, text="Enter", command =lambda: saveImg(img))
    enter.grid(row=4, column = 0)

#####################################
#saves the image under the given name

def saveImg(savedImg):
    fileName = saveName.get() + ".png"
    w2f(fileName)
    savedImg.save(fileName)
    saveWindow.destroy()


#####################################
#writes the saved image to the html page

def w2f(name):
    
    global w2fname

    #html code that is written to html file

    message = """<!DOCTYPE html> <html> <body> <img src='{location}' alt='{location}' ></body> </html>"""
    
    newMessage = message.format(location = name)
    f = open(w2fname, 'a+') 
    f.write(newMessage)
    f.close()

######################################
#main toolkit window

def openEditor(imLocation):
    global imgLabel
    global im
    global clicked

    #im stores the image that is currently displayed in the Main window

    root.deiconify()
    imgLabel=Label(root)
    im = Image.open(imLocation)

    #image is scaled down

    width, height = im.size

    while min(width, height) > 500:
        width = width/2
        height = height/2

    
    im = im.resize((int(width), int(height)))

    displayImg = ImageTk.PhotoImage(im)
    imgLabel.configure(image = displayImg)
    imgLabel.Image = displayImg
    
#creates Main window buttons

    options = [
    "Error Diffusion",
    "Median Filter"
    ]
    clicked = StringVar()
    clicked.set( "Error Diffusion" )
    drop = OptionMenu( root , clicked , *options )

    global sharpenSlider
    global enhanceSlider

    sharpen_image = Button(root, text="Sharpen", width = 15, command =  lambda: sharpen(im,numOfIter.get(),sharpenSlider.get()))
    apply = Button(root, text="Apply selected filter", command = select)
    enhance_image = Button(root, text="Low-Light Enhancement", width = 15, command =  lambda: enhance(im,numOfIter.get(),enhanceSlider.get()))
    quit = Button(root, text="Quit", command = lambda: (root.destroy()))
    save = Button(root, text="Save", command = lambda: openSaveWindow(im))
    change_image = Button(root, text="Update Image", command =  lambda: changeImage())
    sharpenSlider = Scale(root, from_=1, to=20, orient=HORIZONTAL)
    enhanceSlider = Scale(root, from_=1, to=20, orient=HORIZONTAL)
    numOfIter = Scale(root, from_=1, to=5, orient=HORIZONTAL)
    iterLabel = Label(root, text="Select number of iterations")
    sharpenLabel = Label(root, text="Select sharpening strength")
    enhanceLabel = Label(root, text="Select low-light enhancement strength")


    imgLabel.grid(columnspan=3, pady=20,padx=20)
    iterLabel.grid(column=2,row=2,padx=20)
    numOfIter.grid(column=2,row=3,padx=20)
    sharpenLabel.grid(column=0,row=2,padx=20)
    enhanceLabel.grid(column=1,row=2,padx=20)
    sharpen_image.grid(column=0,row=4,padx=20)
    sharpenSlider.grid(column=0, row=3,padx=20)
    enhance_image.grid(column=1, row=4,padx=20)
    enhanceSlider.grid(column=1, row=3,padx=20)
  
    drop.grid(column=0,row=6,pady=20,padx=40)
    apply.grid(column=2,row=6,pady=20,padx=20)

    change_image.grid(column=0,row=5,pady=20)
    save.grid(column=1,row=5,pady=20)
    quit.grid(column=2,row=5,pady=20)

    

######################################
#applies sharpening filter to the image

def sharpen(img,niter,scale):   

    #img - image to which filter is applied
    #niter - number of iterations
    #scale - filter strength

    global imgLabel
    global im

    cols, rows = img.size

    #converts image to an array
    img = img.convert('RGB')

    arrayA = np.array(img)/255
    endArray  = np.copy(arrayA)
    
    for l in range (0,3):
        
        for k in range(0, niter):
            arrayB = np.zeros((rows,cols))

            #loops through all values in array except boundary elements

            for x in range(1, rows-1):
                for y in range(1, cols-1):

                    #loops for every surrounding pixel
                    
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            arrayB[x,y] = arrayB[x,y] + arrayA[x+i,y+j,l]
                    
                    arrayB[x,y] = arrayB[x,y]/9

            arrayA[:,:,l] = arrayB
            


    
    endArray =  endArray + scale*(endArray-arrayA)
    endArray[endArray>1] = 1
    endArray[endArray<0] = 0    
   
    z = (endArray*255).astype(np.uint8)
    imgEdit = Image.fromarray(z)
    im = imgEdit
    finalImg = ImageTk.PhotoImage(imgEdit)
    imgLabel.config(image = finalImg)
    imgLabel.displayImg = finalImg
    root.update()

    
    
######################################
#applies low-light enhancement filter

def enhance(img,niter,scale):

    #img - image to which filter is applied
    #niter - number of iterations
    #scale - filter strength
    
    global imgLabel
    global im
    
    cols, rows = img.size

    img = img.convert('RGB')

    #converts image to a numpy array
    
    arrayA = np.array(img)/255
    
    for l in range(0,3):    
        for k in range (0, niter):
            
            arrayB= np.zeros((rows,cols))

            #loops through all values in array except boundary elements
            
            for x in range (1, rows-1):
                for y in range(1, cols-1):
                    
                    w = 0
                    wSum = 0

                    #loops for every surrounding pixel
                    
                    for i in range (-1,2):
                        for j in range(-1,2):
                            
                            w = math.exp(-scale*abs(arrayA[x+i,y+j,l]-arrayA[x,y,l]))
                            arrayB[x,y] = arrayB[x,y] + (arrayA[x+i,y+j,l])*w
                            wSum = wSum + w
            
                    arrayB[x,y] = arrayB[x,y]/wSum
            arrayA[:,:,l] = arrayB
    
    endArray = np.copy(arrayA)
    arrayA = np.array(img)/255
    endArray = arrayA/(endArray + 0.1)
    endArray[endArray>1] = 1
    endArray[endArray<0] = 0
    z = (endArray*255).astype(np.uint8)
    imgEdit = Image.fromarray(z)
    im = imgEdit
    finalImg = ImageTk.PhotoImage(imgEdit)
    imgLabel.config(image = finalImg)
    imgLabel.displayImg = finalImg
    root.update()

    

######################################

#creates the Main window then hides it

root = Tk() 
root.title('')
root.withdraw()

#creates Select Image window

inputWindow1 = Toplevel(root)
inputWindow1.geometry("+300+300")
inputWindow1.title('')
inputWindow1.resizable(width=False, height=False)
text1 = Label( inputWindow1, text='Enter image path')
text1.grid(row=0, column = 0)
imgLocation = Entry(inputWindow1, borderwidth=5)
imgLocation.grid(row=1,column=0)
enterButton = Button(inputWindow1, text="Enter", command = lambda: endWindow())
enterButton.grid(row=2, column = 0)

root.resizable(width=False, height=False)

#creates the webpage file and adds the date to it


today = date.today()

#file name of webpage

global w2fname
w2fname = 'webImg.html'

#html code that is written to hmtl file

title = """<!DOCTYPE html> <html> <body style="background-color:lightYellow;"> <h1> <center> Images from {todaysDate} </center> </h1> </body> </html>"""

newTitle = title.format(todaysDate = today)

f = open(w2fname, 'a') 
f.write(newTitle)
f.close()


root.mainloop()
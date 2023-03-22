
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import ImageProcessingAlgorithms as IP
import os


class GUI(Tk):

    def __init__(self):

        super(GUI, self).__init__()  # used to call constructor from super class as well, Tk in this case
        self.title("GUI for Image Processing")

        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight())) #Full Screen window size

        self.config(background="white")

        self.count = 0 # Counter to track undo option. This is used to update whenever an image is processed

        # All buttons, labels, scroll bar functions are added here,functions are defined outside this constructor


    # Canvas section

        #Creating Canvas for the left of the GUI, where all the Image Processing toolkit will be loaded
        self.frame_left = Canvas(self,height = 1000,width = 400, bd = 0, bg = "grey")
        self.frame_left.pack(side=LEFT, fill=Y, expand = NO)

        # Creating Canvas for the top of the GUI, where title will be loaded. Adding an image for better display purpose
        self.canvas_top = Canvas(self,height = 450,width = 1000, bd = 0, bg = "grey")
        self.canvas_top.pack(side = TOP, fill = X, expand = NO)

        #Image converted from given form into PhotoImage object supported for display by tkinter
        #Image will be used as background for the top canvas

        path = os.getcwd()
        path_cvi = path + "\\project_images\\i2.jpg"  #path for canvas image
        self.top_canvas_img = Image.open(path_cvi)
        self.top_canvas_img = ImageTk.PhotoImage(self.top_canvas_img)

        self.canvas_top.create_image(500,125,image = self.top_canvas_img)
        self.canvas_top.image = self.top_canvas_img

        #Same image used for left canvas as well
        self.frame_left.create_image(500,200,image = self.top_canvas_img)
        self.frame_left.image = self.top_canvas_img


    # Labels section :

        #Label for top canvas, to be displayed as the heading
        self.label_heading = Label(self.canvas_top,text = "Image Processing Algorithms",font = "Helvetica 25 bold",
                                   fg = "black",bg = "white", pady = 10, relief = SUNKEN, bd = 3)
        self.label_heading.pack(pady = 20, padx = 100)

    # Image Canvas Section

        #Here canvas is created so as to display the image to be processed, as well as successive processings
        self.canvas = Canvas(self, width=1000, height=1000, relief="sunken", bd=5, bg="white")
        self.canvas.pack(fill = BOTH, expand = True)

    # Select Image Button Section :

        #Button to Open the image from desired location of folder
        self.button1 = Button(self.frame_left, command=self.OpenFileBrowser, padx=0, pady=0,
                              relief="raised",borderwidth = 4,text = "Open Image",font = "Helvetica 18 bold")

        #grid option is used to visualize left canvas in terms for rows and columns
        #widgets are added using the grid option
        self.button1.grid(row = 1,column = 1, padx = 10, pady = 50, sticky = E)


    #Making a Drop Down Menu to select Algorithm
    #Drop down menu is used in place of buttons so that the code remains flexible in order to add new algorithm option

        #Making a label that reads "Algorithms". This label is besides a drop down menu which contains list of different algorithms
        self.label = Label(self.frame_left, text = "Algorithms", font = "Helvetica 18 bold", bg = "white", fg = "black")
        self.label.grid(row = 6, column = 1,padx = 5, pady= 60, sticky = NW)

        #Options of the drop down menu
        Options_Algo = [
            "None",
            "Histogram Equalization",
            "Gamma Correction",
            "Log Transform",
            "Blur Image",
            "Sharpen Image",
            "Sketch Image"
        ]

        #Variable that will hold the name of the Algorithm that will be selected to be applied to an image
        self.ChosenAlgorithm = StringVar()

        #Default value of the variable set to "None"
        self.ChosenAlgorithm.set("None")

        #Drop down menu, part of left canvas, value will be saved in self.ChosenAlgorithm, and options as list of values to be displayed
        self.DropMenu = OptionMenu(self.frame_left, self.ChosenAlgorithm, *Options_Algo)
        #Here *Options_Algo is written which basically conveys that each item of Options list is iterated and stored separate in drop down
        #If *Options_Algo is not used, entire list will be written in form of 1 variable

        #packing the DropMenu
        self.DropMenu.grid(row = 6, column = 2, ipadx = 20,ipady = 3, pady = 60, sticky = N)


    #Labels for Gamma, Smoothening and Sharpening

        #Labels displaying Gamma Value, Smooth Value and Sharpen Value are created
        #These labels are beside the control/ input mechanism necessary to apply respective algorithms
        self.label_gamma = Label(self.frame_left,text = "Gamma Value", bg = "white", fg = "black",font = "Helvetica 14 bold", bd = 5)
        self.label_gamma.grid(row = 7,column = 1, padx = 5, pady = 10, sticky = SW)
        self.label_smooth = Label(self.frame_left,text = "Smooth Value", bg = "white", fg = "black",font = "Helvetica 14 bold",bd = 5)
        self.label_smooth.grid(row=8, column=1, padx = 5, pady = 10, sticky = SW)

        self.label_sharpen = Label(self.frame_left,text = "Sharpen Value", bg = "white", fg = "black",font = "Helvetica 14 bold", bd = 5)
        self.label_sharpen.grid(row=9, column=1, padx = 5, pady = 10, sticky = SW)

    #Widgets for Gamma, Smoothening and Sharpening

        #Widgets below are created to control/provide input for the filter mechanism.
        #Gamma Correction uses an Entry widget to type in value of Gamma
        #Smoothening uses a slider bar to control the size of smoothing filter between 1 and 25
        #Sharpening uses a slider bar to control the extent of sharpening between 0 to 10



        #Scale widget to hold the value of smoothening
        self.smooth_slider = Scale(self.frame_left, from_ = 1, to = 25, tickinterval = 24,length = 120,
                                   orient = HORIZONTAL, relief = SUNKEN, bg = "white")


        #Scale widget to hold the value of Sharpening
        self.sharpen_slider = Scale(self.frame_left, from_=0, to= 10, tickinterval=5, length=120,
                                    orient=HORIZONTAL, relief = SUNKEN, bg = "white")

        #Entry widget to get the entry of Gamma value
        self.gamma_val = StringVar() #Variable to hold value of Gamma
        self.gamma_entry = Entry(self.frame_left, textvariable = self.gamma_val)



        #Packing all the three widgets on left canvas
        self.gamma_entry.grid(row = 7,column = 2, padx = 5, pady = 10,ipady = 8, sticky = SW)
        self.smooth_slider.grid(row=8, column=2, padx=5, pady=2,ipady = 0, sticky=SW)
        self.sharpen_slider.grid(row=9, column=2, padx=5, pady=2,ipady = 0, sticky=SW)

    #Buttons to use the Drop Menu

        #Following Buttons are present in the left canvas
        # 1. Apply Filter
        # 2. Save Image
        # 3. Undo Last Change
        # 4. Undo All Changes

        #Creating Apply Filter button
        #Calls ApplyFilter Function
        self.button_apply = Button(self.frame_left, text="Apply Filter", command=self.ApplyFilter, padx=30, pady=10,
                              relief="raised",borderwidth = 10)
        self.button_apply.grid(row=12, column=1,padx=5, pady=20,sticky = SW)

        #Creating Save Image button
        #Calls SaveImage Function
        self.button_save = Button(self.frame_left, text="Save Image", command=self.SaveImage, padx=30, pady=10,
                              relief="raised", borderwidth=10)
        self.button_save.grid(row=12, column=2,padx=0, pady=20, sticky = SW)

        #Creating Undo Last Change button
        #Calls UndoImage Function
        self.button_undo = Button(self.frame_left, text="Undo Last Change", command=self.UndoImage, padx=10, pady=10,
                              relief="raised", borderwidth=10)
        self.button_undo.grid(row=13, column=1,padx = 5, pady=0, sticky = NW)

        #Creating Undo All Changes button
        #Calls UndoAll Function
        self.button_undoall = Button(self.frame_left, text="Undo All Changes", command=self.UndoAll, padx=10, pady=10,
                              relief="raised", borderwidth=10)
        self.button_undoall.grid(row=13, column=2,padx=5, pady=0, sticky = NW)

    #Functions Section

    #This Sections contains all the functions that will be called when any of the button is pressed
    # List of Functions defined here :
    # 1. OpenFileBrowser
    # 2. ApplyFilter
    # 3. UndoAll
    # 4. SaveImage
    # 5. SharpenImage
    # 6. HistogramEqualization
    # 7. GammaCorrection
    # 8. LogarithmicTransformation
    # 9. BlurImage
    # 10. CartoonImage

    def OpenFileBrowser(self):
        self.file_name = filedialog.askopenfilename(initialdir="desktop", title="Select A File", filetype=
        (("all files", "*.*"),("jpeg files", "*.jpg") )) #Open file in desired format

        # Tkinter does not support few formats of images hence PILLOW library is used here

        #If file doesn't open correctly, then an exception is thrown along with an error message on screen
        try:
            img = Image.open(self.file_name)
        except:
            #If file is not an image
            tkinter.messagebox.showerror("Invalid File Format", "Select appropriate file to be opened")
        else:
            img.thumbnail((500,500))
            photo = ImageTk.PhotoImage(img)
            self.IMG = cv2.imread(self.file_name)
            self.IMG = cv2.cvtColor(self.IMG,cv2.COLOR_BGR2RGB) #All processed Images will be stored in self.IMG, after every process

            # A dictionary to pack and undo operations
            # Working of this setup is as follows:

            # 1. GUI is opened, self.count is set to 0
            # 2. Whenever ApplyFilter button is clicked, self.count is increased by 1 and currently Processed Image is stored.
            # 3. Image before applying filter is stored in dictionary with key "Image_{self.count}"
            # 4. After applying Filter, if Undo button is clicked, self.count already points to Previous Image.
            # 5. Undo button calls UndoLast function which calls the value of the key = "Image_{self.count}"
            # 6. UndoLast Function will respond till self.count doesn't become 0. After that, error message appears
            # 7. Again ApplyFilter button is clicked, self.count is increased by 1 and the process repeats

            self.Image_array = {} #initiate dictionary
            self.count = 0
            current_count = "Image_{}".format(self.count) #count keeps track of index for getting key to the last processed image
            self.Image_array[current_count] = self.IMG #storing image to a current counted image

            self.canvas.create_image(500,350, image=photo, anchor = CENTER) #Image centered at x = 500 and y = 350 of the canvas
            self.canvas.image = photo
            # The above line is very important, this will make sure that when the image variable leaves the function, its value is stored as a variable and not as a garbage

    def UndoImage(self):

        if self.count > 0: #Check if any image processing has been done until now or now

            current_count = "Image_{}".format(self.count) #Display
            self.IMG = self.Image_array[current_count]

            # Following code involves conversion of numpy 2D array representation of processed image to a thumbnail size of 500x500
            # This is done to display the image on canvas in a format supported by tkinter
            tempImage = Image.fromarray(self.IMG)
            tempImage.thumbnail((500, 500))
            phototempImage = ImageTk.PhotoImage(image=tempImage)

            self.canvas.create_image(500, 350, image=phototempImage)

            # temporary image stored as image attribute of canvas.
            # So that the image doesn't vanish after the execution of function
            self.canvas.image = phototempImage

            self.count = self.count - 1  # 1 subtracted to come back to image, 1 more subtracted for previous
        else: # can't do undo beyond this
            tkinter.messagebox.showerror("No More Undo", "Cannot perform any more undo operations")




    def UndoAll(self):

        #Original Image is stored at 0th key of dictionary so this function assigns that image to the current canvas
        self.count = 0
        self.IMG = self.Image_array["Image_0"]

        # Following code involves conversion of numpy 2D array representation of processed image to a thumbnail size of 500x500
        # This is done to display the image on canvas in a format supported by tkinter
        tempImage = Image.fromarray(self.IMG)
        tempImage.thumbnail((500, 500))
        phototempImage = ImageTk.PhotoImage(image=tempImage)

        self.canvas.create_image(500, 350, image=phototempImage)
        # temporary image stored as image attribute of canvas.
        # So that the image doesn't vanish after the execution of function
        self.canvas.image = phototempImage



    def SaveImage(self):
        #Box to confirm saving of the current Image
        value = tkinter.messagebox.askquestion("Save Image ?", "Do you want to save the current image")

        if value == "yes":
            To_be_saved = Image.fromarray(self.IMG) #convert to Image format from numpy array
            To_be_saved = To_be_saved.convert('RGB')
            filename_Save = filedialog.asksaveasfile(mode='w', defaultextension=".jpg") #extension by default is .jpg
            if not filename_Save: #If save box is closed or any other reason
                return
            To_be_saved.save(filename_Save) #Image saved at chosen location
             #Image saved at chosen location
        else:
            pass #if value no, then nothing

    def SharpenImage(self,extent):

        self.IMG = IP.Sharpen(self.IMG, extent)

        # Following code involves conversion of numpy 2D array representation of processed image to a thumbnail size of 500x500
        # This is done to display the image on canvas in a format supported by tkinter
        tempImage = Image.fromarray(self.IMG)
        tempImage.thumbnail((500,500))
        phototempImage = ImageTk.PhotoImage(image=tempImage)

        self.canvas.create_image(500,350,image=phototempImage)

        # temporary image stored as image attribute of canvas.
        # So that the image doesn't vanish after the execution of function
        self.canvas.image = phototempImage

    def HistogramEqualization(self):

        self.IMG = IP.HistogramEqualization(self.IMG)

        # Following code involves conversion of numpy 2D array representation of processed image to a thumbnail size of 500x500
        # This is done to display the image on canvas in a format supported by tkinter
        tempImage = Image.fromarray(self.IMG)
        tempImage.thumbnail((500,500))
        phototempImage = ImageTk.PhotoImage(image=tempImage)

        self.canvas.create_image(500,350,image=phototempImage)

        # temporary image stored as image attribute of canvas.
        # So that the image doesn't vanish after the execution of function
        self.canvas.image = phototempImage


    def GammaCorrection(self, Gamma):

        self.IMG = IP.Gamma_Correct(self.IMG, Gamma) #Applying Gamma Correction to the image, and storing it in self.IMG

        #Following code involves conversion of numpy 2D array representation of processed image to a thumbnail size of 500x500
        #This is done to display the image on canvas in a format supported by tkinter
        tempImage = Image.fromarray(self.IMG) #Image stored in temporary variable, of the form "Image"
        tempImage.thumbnail((500,500)) # setting the size of thumbnail to 500x500
        phototempImage = ImageTk.PhotoImage(image=tempImage) #Converting the desired thumbnail into PhotoImage object for display on canvas
        self.canvas.create_image(500,350,image=phototempImage)

        # temporary image stored as image attribute of canvas.
        # So that the image doesn't vanish after the execution of function
        self.canvas.image = phototempImage


    def LogarithmicTransformation(self):

        self.IMG = IP.LogarithmicTransformation(self.IMG)

        # Following code involves conversion of numpy 2D array representation of processed image to a thumbnail size of 500x500
        # This is done to display the image on canvas in a format supported by tkinter
        tempImage = Image.fromarray(self.IMG)
        tempImage.thumbnail((500,500))
        phototempImage = ImageTk.PhotoImage(image=tempImage)

        self.canvas.create_image(500,350,image=phototempImage)

        # temporary image stored as image attribute of canvas.
        # So that the image doesn't vanish after the execution of function
        self.canvas.image = phototempImage

    def BlurImage(self,Filter_size):
        self.IMG = IP.BlurImage(self.IMG,Filter_size)

        # Following code involves conversion of numpy 2D array representation of processed image to a thumbnail size of 500x500
        # This is done to display the image on canvas in a format supported by tkinter
        tempImage = Image.fromarray(self.IMG)
        tempImage.thumbnail((500,500))
        phototempImage = ImageTk.PhotoImage(image=tempImage)

        self.canvas.create_image(500,350,image=phototempImage)

        # temporary image stored as image attribute of canvas.
        # So that the image doesn't vanish after the execution of function
        self.canvas.image = phototempImage

    def SketchImage(self):

        self.IMG = IP.Sketch(self.IMG)

        # Following code involves conversion of numpy 2D array representation of processed image to a thumbnail size of 500x500
        # This is done to display the image on canvas in a format supported by tkinter
        tempImage = Image.fromarray(self.IMG)
        tempImage.thumbnail((500,500))
        phototempImage = ImageTk.PhotoImage(image=tempImage)

        self.canvas.create_image(500,350,image=phototempImage)

        # temporary image stored as image attribute of canvas.
        # So that the image doesn't vanish after the execution of function
        self.canvas.image = phototempImage

    # Apply Filter Function is called when Apply Filter button is pressed
    # This function is used to call various algorithms which are chosen for Image processing on the Image
    def ApplyFilter(self):
        Filter_2_use = self.ChosenAlgorithm.get() #Get name of Algorithm which is to be used

        self.count = self.count + 1 #Counter incremented by one states that current image will be processed now

        # Creating a dictionary key of the name "Image_1", "Image_2" etc.
        # Hold the currently processed Image in dictionary self.Image_array which will be used if Undo is pressed
        current_count = "Image_{}".format(self.count)
        self.Image_array[current_count] = self.IMG

        #else if ladder to call the appropriate function to Process the Image
        if Filter_2_use == "Sharpen Image":
            if self.sharpen_slider.get() == 0: #Mistakenly not changed sharpening extent value
                tkinter.messagebox.showerror("Extent of sharpening 0","Extent of Sharpening cannot be zero")
            self.SharpenImage(self.sharpen_slider.get()) #Call Sharpen Filter, passing value of sharpen scale taken as input from the user
        elif Filter_2_use == "Histogram Equalization":
            self.HistogramEqualization() #Call Histogram Equalization function
        elif Filter_2_use == "Gamma Correction":
            self.GammaCorrection(self.gamma_val.get()) #Call Gamma Correction function, passing value of gamma obtained from scale bar from user
        elif Filter_2_use == "Log Transform":
            self.LogarithmicTransformation() #Call Log transformation function
        elif Filter_2_use == "Blur Image":
            #Call smoothening function, pass value of scale bar obtained from function
            #The Value obtained is converted into odd value since Smoothing filter can only be of odd order and not even order
            self.BlurImage(2*self.smooth_slider.get()+1)
        elif Filter_2_use == "Sketch Image":
            #Call Cartoonizer
            self.SketchImage()
        elif Filter_2_use == "None":
            #If apply button clicked without selecting any filter, show the following error message
            tkinter.messagebox.showerror("No Filter Detected","Select appropriate filter to be applied")

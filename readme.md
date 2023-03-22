# GUI for Image Processing Algorithms

In this project, the GUI is developed to load any image, apply image processing algorithms on the image, and store the image. The folder present here consists of three python files, main.py GUI_class.py and ImageProcessingAlgorithms.py, also it contains report about the project in PDF format, and a folder called project images where the image for background of the GUI is stored. 

The main.py file should be executed on command terminal. The GUI_class.py consists of all the tkinter based GUI features. ImageProcessingAlgorithms.py consists of all the Image processing algorithms.

## How to run :

1. pip install -r requirements.txt
2. python main.py

If error arises in sklearn module installing, follow the following steps :

1. Type “regedit” in the Windows start menu to launch regedit.
2. Go to the Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem key.
3. Edit the value of the LongPathsEnabled property of that key and set it to 1.
4. Again run using the two shell commands mentioned in the text.


## GUI description :

Each and every feature of GUI is described with comments in the GUI_class.py file. Steps to use the GUI :

1. After execution of main.py, tkinter window covering the entire screen will open. Load an image using the 'Open Image' button. Select the algorithms using the Algorithms drop down menu,      which by default is set to None.
2. For Gamma correction, enter the value of Gamma.
3. For sharpening, if Apply Filter button is pressed when the sharpening slide is at 0, error message will pop up. The extent of sharpening can be varied on scale from 1 to 10, 10 being the    most sharpened image.
4. For Blurring, scale varies from 1 to 25 and correspondingly the averaging filter will vary as size 2*N + 1, where N is 1 to 25 as per the slider scale. Minimum 3x3 filter and maximum       49x49 filter can be used to blur the image
5. Saving the image will be by default in "jpeg" format.
6. Undo button can be applied as long as the user gets the original uploaded image.
7. Undo all button will remove all the changes made on existing image made by the user.


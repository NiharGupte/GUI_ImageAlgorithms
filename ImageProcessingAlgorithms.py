import numpy as np
import cv2
from sklearn import feature_extraction




#Image processing functions before applying transformations mentioned below are :
#1. RGB2HSV
#2. HSV2RGB
#3. ImagePreProcess
#4. ImagePostProcess


#Image in RGB format is converted to HSV format using opencv library builtin function
def RGB2HSV(Image_RGB):
    Image_HSV = cv2.cvtColor(Image_RGB,cv2.COLOR_RGB2HSV)
    return Image_HSV

#image in HSV format is converted to RBG format using opencv library builtin function
def HSV2RGB(Image_HSV):

    Image_RGB = cv2.cvtColor(Image_HSV,cv2.COLOR_HSV2RGB)
    return Image_RGB

def Image_Format(Image): #Used to determine if Image is Coloured or grayscale

    Colour = True if Image.ndim != 2 else False #Image dimension 3 = colour image, setting Boolean Colour variable to True
    return Colour

#Post processing of Image takes place here
#Parameters passed are Colour flag, processed V channel / grayscale channel, and Image which was needed to be filtered
def ImagePostProcess(Colour, Image_processed_channel, Image2Filter):


    #If the image is coloured, original Image is converted to HSV and the processed V channel is merged. Returns fully merged image

    if Colour == True:
        Image_HSV = RGB2HSV(Image2Filter)
        Image_HSV[:,:,2] = Image_processed_channel
        Image_processed = HSV2RGB(Image_HSV)
        return Image_processed

    #For grayscale image, the returned numpy array is the same channel itself

    else:
        return Image_processed_channel

#Pre Processing of Image is done here. Function will take the Colour flag, and the image.
# Return V channel if image is coloured or return image itself if it is in grayscale
def ImagePreProcess(Colour, Image):

    #Check Colour flag of image, if it is coloured, Image is converted from RGB to HSV using RGB2HSV function.
    # V channel is separated and returned for processing
    if Colour == True:
        Image_HSV = RGB2HSV(Image)
        PreProcessedImage = Image_HSV[:, :, 2]
        return PreProcessedImage
    #For grayscale image, the image itself is returned for processing
    else:
        return Image



#Filter Functions here are FilterFunction and FilterFunction2.
# Both these functions are written in order to convolute the passed filter with the Image itself using two separate algorithms
# Filter Function uses simple convolution using a for loop
#FilterFunction2 uses vectorization

#FilterFunction2 computes convolution faster than FilterFunction for smaller filters,for larger filter, space complexity is an issue
#FilterFunction is better for large sizer size filters, especially like 25x25, 35x35 etc, for small filters, time complexity is an issue
#Rule of thumb, use FilterFunction for filters size less than 20. Else use FilterFunction2


# Convolutes image with filter using vectorization
# Arguments passed : Filter itself, image with padding, original size of the image
def FilterFunction2(Filter_name, padded_image, original_size): #Arguments passed, padded image is passed here
    Filter_name = np.rot90(Filter_name,2) #Rotating filter by 180 degree for convolution

    #Patches of pixels of the Filter size are extracted, and are stacked together, one over each other
    #Example if Filter shape is 3x3, and Image size is 512x512, total 512*512 = 262144 3x3 matrices are generated
    #They are stacked one over each other to obtain a matrix of shape ( 262144, 3, 3)
    #Each element on axis = 0 of matrix corresponds to a 3x3 matrix of a given pixel with it's neighbour pixels

    patches = feature_extraction.image.extract_patches_2d(padded_image,
                                                                  (Filter_name.shape[0], Filter_name.shape[0]))

    #Reshaping the filter
    Filter = np.reshape(Filter_name, (1, Filter_name.shape[0], Filter_name.shape[0]))

    #Filter is repeated so that FILTER_MATRIX is of the shape same as patches matrix, say (262144,3,3)
    #FILTER_MATRIX is stacked on axis = 0 with 262144 Filters
    FILTER_MATRIX = np.repeat(Filter, patches.shape[0], axis=0)

    #Multiplication of Both Matrices is done here i.e. element wise multiplication of each patch with filter
    #Generated is a (262144,3,3) matrix again, now sum of all elements on axis 1 and 2 is taken (i.e. new shape = (262144,1))
    DOT = np.sum(np.multiply(patches, FILTER_MATRIX), axis=(1, 2))

    #the output of previous operation is a flattened matrix of original image matrix
    #reshaped to get final convoluted matrix
    DOT = DOT.reshape(original_size[0], original_size[1])

    return DOT

#Used normal convolution approach where a double for loop calculates dynamic 3x3 matrix patch of original image
# Thus consuming less space
def FilterFunction(Filter_name, padded_image):
    Filtered_IMG = np.zeros(padded_image.shape)  # Empty Image to store convoluted results
    W = Filter_name.shape[0]  # Shape of Window
    Filter_name = np.rot90(Filter_name,2)
    # Minimum and maximum values of rows and columns to be iterated during convolution
    # row_min and col_min represent the first true value of pixel at (x,y) of padded image
    # row_max and col_max represent the last true value of pixel at (x,y) of padded image

    # true value here means value which is not padded and was part of original image

    # Say, For 5x5 filter, 2 lines of pixels were padded on each side.
    # hence min value of row and col will be (3,3), Max will be (514,514) for an image (512x512)
    # which is padded to become (516,516) for 5x5 filter

    # In general, for WxW filter, these values will be given by :

    row_min = int(W / 2 + 1)
    col_min = int(W / 2 + 1)
    row_max = padded_image.shape[0] - int(W / 2 + 1) + 1
    col_max = padded_image.shape[1] - int(W / 2 + 1) + 1

    # Iterate over rows and columns to extract a patch of image of size WxW
    # Convolute the image and patch using np.multiply and using np.sum to get sum of all images
    for row in range(row_min, row_max + 1):
        for col in range(col_min, col_max + 1):
            patch = padded_image[int(row - (W / 2 + 1 / 2)): int(row + (W / 2 + 1 / 2) - 1),
                    int(col - (W / 2 + 1 / 2)): int(col + (W / 2 + 1 / 2) - 1)]

            Filtered_IMG[row][col] = np.sum(np.multiply(patch, Filter_name))

    # Filtered_IMG contains padding of zeros, to remove this padding, we use slicing operation

    x_min_op = int(W / 2 + 1)  # For 5x5 , this will be 3
    x_max_op = padded_image.shape[0] - int(W / 2 + 1) + 1  # For 5x5, this will be 514
    y_min_op = int(W / 2 + 1)  # For 5x5, this will be 3
    y_max_op = padded_image.shape[1] - int(W / 2 + 1) + 1  # For 5x5, this will be 514

    # hence we slice Filtered_IMG from 3 to 514 i.e. 512 pixels and eliminate padding

    Filtered_IMG = Filtered_IMG[x_min_op: x_max_op + 1, y_min_op: y_max_op + 1]

    return Filtered_IMG  # This will finally return non padded and filtered image




#Image transformations take place in the following functions.
#Architecture of each function :

#1. Colour Boolean variable of each image is obtained
#2. Preprocess the image based on Colour flag
#3. Apply necessary transformation
#4. Post Process the image channel and merge it will original image
#5. Return completely merged image

#Transformations mentioned here are:

#1. Logarithmic Transformation
#2. Gamma correction
#3. Histogram Equalization
#4. Blurring Image
#5. Sharpen the Image
#6. Sketcher


#Log transform of the image
def LogarithmicTransformation(Image2Filter):

    Colour = Image_Format(Image2Filter) #Colour Boolean

    Image2Filter_Channel = ImagePreProcess(Colour, Image2Filter) #Obtain necessary channel for filtering

    #Apply k*log(1 + r) where k = 45.96 to convert pixels back to range 0 to 255
    Image_logarithm = np.round((45.96 * (np.log(np.ones((Image2Filter_Channel.shape[0],
                                                         Image2Filter_Channel.shape[1])) + Image2Filter_Channel))))

    Image_logarithm_merged = ImagePostProcess(Colour, Image_logarithm, Image2Filter) #Merge the channel with original image

    return Image_logarithm_merged #return merged image

#Sharpening the Image
def Sharpen(Image2Filter,extent_of_sharpening): #Arguments passed
    Colour = Image_Format(Image2Filter) #Colour boolean calculated

    Image_channel = ImagePreProcess(Colour, Image2Filter) #Preprocess the Image

    #Use of Laplacian Filter
    Laplacian = np.array([[-1, -1, -1],
                          [-1,  8, -1],
                          [-1, -1, -1]])

    padded_img = np.pad(Image_channel, ((1, 1), (1, 1)), mode="reflect") #Padding the image with mirror padding

    Filtered_channel = FilterFunction2(Laplacian, padded_img, Image_channel.shape) # Using FilterFunction2 since only 3x3 Filter is there

    Blurred_Image = BlurImage(Image2Filter,5) #Blurring the Image before applying Laplacian

    #Extracting Blurred channel like any other channel
    Colour_blurred = Image_Format(Blurred_Image)
    Blurred_channel = ImagePreProcess(Colour_blurred, Blurred_Image)

    #Sharpening is controlled by using the extent of sharpening, i.e. addition to the original channel
    New_channel = Blurred_channel + extent_of_sharpening*Filtered_channel / 10

    New_channel = np.where(New_channel < 0, 0, New_channel) #Taking care of negative pixels
    New_channel = np.where(New_channel > 255, 255 , New_channel) #Taking care of over 255 pixels

    Filtered_IMG_merged = ImagePostProcess(Colour, New_channel, Image2Filter) #Final Postprocessing of image

    return Filtered_IMG_merged #returns the sharpened image




#Blurring function
def BlurImage(Image2Filter,Filter_size):

    Colour = Image_Format(Image2Filter)

    Image_channel = ImagePreProcess(Colour,Image2Filter)
    Smoothing_Filter = np.ones((Filter_size,Filter_size),dtype = float)/(Filter_size*Filter_size) #Averaging Filter

    x_pad = int((Filter_size - 1)/2) # padding value for rows e.g N = 5, 2 padded rows are needed
    y_pad = int((Filter_size - 1)/2) #padding value for columns e.g N = 5, 2 padded columns are needed

    padded_image = np.pad(Image_channel, ((x_pad,x_pad),(y_pad,y_pad)),mode="reflect") #reflect padding

    if Filter_size < 15:
        Filtered_Image = FilterFunction2(Smoothing_Filter,padded_image,Image_channel.shape) #Less time for low filter size
    else:
        Filtered_Image = FilterFunction(Smoothing_Filter, padded_image) #less memory for more filter size

    Filtered_Image_merged = ImagePostProcess(Colour,Filtered_Image, Image2Filter) #Merging image and the channel

    return Filtered_Image_merged #return final merged image


#Using Gamma Correct function

def Gamma_Correct(Image2Filter, Gamma):

    Gamma = float(Gamma) #convert the string var received from GUI into floating value

    Colour = Image_Format(Image2Filter) #Colour Boolean extracted
    Image2Filter_channel = ImagePreProcess(Colour,Image2Filter) #Image channel extracted

    Image_gamma = np.round((255 * (np.power(Image2Filter_channel/255, Gamma)))) #finding the Gamma value

    Image_gamma_merged = ImagePostProcess(Colour,Image_gamma,Image2Filter) #Image_merged

    return Image_gamma_merged #return merged Image

#Histogram Equalization
def HistogramEqualization(Image):

    Colour = Image_Format(Image) #Colour Boolean extracted
    Image_channel = ImagePreProcess(Colour,Image) #Image channel extracted

    unique, frequency = np.unique(Image_channel, return_counts=True) #Returns unique pixel values and number of pixels at that value


    #There may be few pixel values which might have never occured in the image, e.g. say 240 and 250 do not appear
    #so unique will contain a list of values from 0 to 255 without 240 and and 250
    #Thus to get the full frequency, we firstly add the remaining zeros for pixel values not occuring. e.g. 2 in this case

    full_frequency = np.append(frequency, np.zeros((256-frequency.shape[0],1),dtype = float))

    #now we iterate through the range 0 to 255, if a pixel value is not at a given i, we insert 0 at that place in full_frequency list

    for i in range(0,256):
        if i not in unique:
            full_frequency = np.insert(full_frequency,i,0)

    full_frequency = full_frequency[0:256] #Making sure that full_frequency has only 255 pixel values
    pixels = Image_channel.shape[0] * Image_channel.shape[1] #total no. of pixels
    PDF = full_frequency / pixels #dividing by total pixels to get PDF of the given image

    # Finding CDF of given PDF, multiplying it with 255 and converting it into integer to obtain the output
    #output here is S_k = (L-1)*CDF(R_k)

    s = np.array([int(255 * sum(PDF[0:i])) for i in range(0, 256)]) #Finding CDF of given PDF, multiplying it with 255 and converting

    #Now we map S to R
    #Iterating through the row and column of the image to obtain a pixel value.
    #Now finding the value corresponding to that pixel in S.
    # Since S naturally is an array which contains 255 values, indexing s at a given row and column will return the mapped value
    #E.g. in 1D : S = [0,0,0,1,1,4,5,6,7], index of S is from 0 to 8.
    #This automatically means that 0,1,2 are mapped to 0. 3,4 to 1. 4,5,6,7 to 4,5,6,7
    #The same concept is implemented below for the S array.
    #For S having constant values at an interval, it means pixel values in that interval would map to the same constant value.
    # S = [ ... 20,20,20,20,20,23, ... ], say S = 20 for index 3 to index 7. Means that the pixel values 3 4 5 6 7 get mapped to 20

    Equalized = np.array([s[Image_channel[row][col]] for row in range(0, Image_channel.shape[0]) for col in range(0, Image_channel.shape[1])])

    #the above operation gives a flattened vector of the image
    Equalized = np.reshape(Equalized, (Image_channel.shape[0], Image_channel.shape[1])) #Reshaping the equalized image

    Equalized_merged = ImagePostProcess(Colour,Equalized,Image) #Merging the equalized image

    return Equalized_merged #return fully equalized image

def Sketch(Image2Filter):

    Image2Filter = Sharpen(Image2Filter,10) #Sharpen image completely with c = 10
    Sobel_X = np.array([[ 1, 2, 1],
                        [ 0, 0, 0],
                        [-1,-2,-1]])
    Sobel_Y = np.array([[ 1, 0, -1],
                        [ 2, 0, -2],
                        [ 1, 0, -1]])

    Colour = Image_Format(Image2Filter)
    Image_channel = ImagePreProcess(Colour,Image2Filter)

    padded_image = np.pad(Image_channel,((1,1),(1,1)),mode = "reflect")

    Image_channel_processed_X = FilterFunction2(Sobel_X,padded_image,Image2Filter.shape)
    Image_channel_processed_Y = FilterFunction2(Sobel_Y, padded_image, Image2Filter.shape)

    Image_channel_processed = 255 - ((Image_channel_processed_X**2 + Image_channel_processed_Y**2)**0.5) #invert the edge detected image
    Image_channel_processed = np.where(Image_channel_processed < 0, 0, Image_channel_processed)

    Image_binarized_mask = np.where(Image_channel_processed < 50, 0, 255)

    #Binarizing the image to get a sketch effect, threshold = 50

    return Image_binarized_mask



import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random
import pickle 


class ImageLoader(object):
    def imageReader(dataDir, trainingDir, resultDir, resize,Crop):
        training_data = []
        for category in trainingDir:
            path = os.path.join(dataDir, category) # path to img/training or pixel-level-gt/training dir
            secondPath = os.path.join(dataDir,resultDir[trainingDir.index(category)])
            #class_num = CATEGORIES.index(category)
            newImg =  os.listdir(secondPath)
            i = 0;
            for img in os.listdir(path):
                try:
                    imgTraining_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_COLOR)
                    imgResult_array = cv2.imread(os.path.join(secondPath,newImg[i]),cv2.IMREAD_COLOR)
                    #first Resize
                    if resize[0] != 0:
                        imgTraining_array = cv2.resize(imgTraining_array, (resize[1],resize[2]))
                        imgResult_array = cv2.resize(imgResult_array, (resize[1],resize[2]))
                    if Crop[0] != 0:
                        #First Try to add a boarder
                        max_y,max_x = imgTraining_array.shape[:2] # this value is taken out from the original picture and used later for setting the max values
                        imgTraining_array = ImageLoader.addBorder(imgTraining_array,Crop[1],Crop[2],[0,0,0],max_x,max_y)
                        imgResult_array = ImageLoader.addBorder(imgResult_array,Crop[1],Crop[2],[0,0,0],max_x,max_y)
                        #Lets Split the images
                        imgTraining_array =ImageLoader.splitImage(imgTraining_array,Crop[1],Crop[2],max_x,max_y)
                        imgResult_array = ImageLoader.splitImage(imgResult_array,Crop[1],Crop[2],max_x,max_y)
                        training_data += list(zip(imgTraining_array,imgResult_array))
                    else:
                        training_data.append([imgTraining_array,imgResult_array])
                    i= i+1
                except Exception as e:
                    pass
        return training_data

    def saveImagesToPickle(dataDir, trainingDir, resultDir, resize,Crop,shuffleData,pickleOutX,pickleOutY,WheretosavePickleData):
        training_data = ImageLoader.imageReader(dataDir, trainingDir, resultDir, resize,Crop)
       # if(bool(shuffleData)):
        #    random.shuffle(training_data)
        x = [] #trainingdata
        y = [] #labels
        for features, label in training_data:
            x.append(features)
            y.append(label)

            
        if(resize[0]==1 and Crop[0] == 0):
            x = np.array(x).reshape(-1,resize[1],resize[2],3)
            y = np.array(y).reshape(-1,resize[1],resize[2],3)
        else:
            x = np.array(x)
            y = np.array(y)

        print(x.shape)
        im2 = x.copy()
        im2[:,:, :, 0] = x[:, :, :, 2]
        im2[:,:, :, 2] = x[:, :, :, 0]
        x = im2
        ANotherImg = y.copy()
        ANotherImg[:,:, :, 0] = y[:,:, :, 2]
        ANotherImg[:,:, :, 2] = y[:,:, :, 0]
        y = ANotherImg
        pickle_out = open(WheretosavePickleData+pickleOutX,"wb")
        pickle.dump(x,pickle_out)
        pickle_out.close()

        pickle_out = open(WheretosavePickleData+pickleOutY,"wb")
        pickle.dump(y,pickle_out)
        pickle_out.close()
        print("Finished saving images to pickle x for "+pickleOutX+"  y for "+pickleOutY)

    def loadSavedImage(WhereToload,inX,inY):
        pickle_in = open(WhereToload+inX,"rb")
        x_train = pickle.load(pickle_in)
        pickle_in = open(WhereToload+inY,"rb")
        y_train = pickle.load(pickle_in)
        return [x_train,y_train]

    def combine_images(imageArray, max_y: int, max_x: int) -> np.array:
        image = np.zeros((max_y,max_x,3),np.int)
        #np.array(x).reshape(-1,resize[1],resize[2],3)
        size_y, size_x,Nope = imageArray[0].shape
        curr_y = 0
        i = 0
        # TODO: rewrite with generators.
        while (curr_y + size_y) <= max_y:
            curr_x = 0
            while (curr_x + size_x) <= max_x:
                try:
                    image[curr_y:curr_y + size_y, curr_x:curr_x + size_x] = imageArray[i]
                except:
                    i -= 1
                i += 1
                curr_x += size_x
            curr_y += size_y
        return image


    def removingOnlyDarkpictures(picturesArray,Dimension):
        amountofblackpictures=0
        for i in range(len(picturesArray)):
            thisarray=np.asarray(picturesArray[i])
            arrayflow = np.all(thisarray < 0.1, Dimension)
            if(arrayflow.all()):
                amountofblackpictures = amountofblackpictures + 1
        print(amountofblackpictures)
    
    def addBorder(array,dimensionX,dimensionY,BoarderColor,max_x,max_y):
        #Takes in the prefer Images and adds a border if nessesary based on dimensions
        border_y = 0
        if max_y % dimensionY != 0:
            border_y = (dimensionY - (max_y % dimensionY) + 1) // 2
            array = cv2.copyMakeBorder(array,border_y,border_y,0,0, cv2.BORDER_CONSTANT, value=BoarderColor)
        border_x = 0
        if max_x % dimensionX != 0:
            border_x = (dimensionX - (max_x % dimensionX) + 1) // 2
            array = cv2.copyMakeBorder( array, 0, 0, border_x, border_x, cv2.BORDER_CONSTANT, value=BoarderColor)
        return array
        
    def splitImage(array,dimensionX,dimensionY,max_x,max_y):
        #Splits the images into smaller chunks based on the dimension entered returns an array of cut pictures
        smallerImages = []
        current_y = 0
        while(current_y + dimensionY)<= max_y:
            current_x = 0
            while(current_x + dimensionX) <= max_x:
                smallerImages.append(array[current_y:current_y+dimensionY,current_x:current_x + dimensionX])
                current_x += dimensionX
            current_y += dimensionY
        return smallerImages


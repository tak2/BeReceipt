#import
import os
import csv
import re
import cv2
import numpy as np
from scipy.ndimage import interpolation as inter


def start():
    #file input
    global inputdirectory
    inputdirectory =".\input"        #input directory
    #Initialazie the data dict and array
    global reciptdata
    reciptdata = {
            "Store": "",
            "Date": "",
            "Time": "",
            "Total": "",
            "ItemCount": ""
            }

    global itemlist 
    itemlist =[]
    global recipttext
    recipttext ="""Kauf land
        Münchener Straße 146
        85051 Ingolstadt
        Tel
        0841/12948130
        DE226350409
        Preis €
        Morra_ / Kasse / Eier
        KLC.Kaffeeweisser
        0,75 B
        Obst / Gemuese / Pflanzen
        Paprika grün
        0,164 kg
        0,65 B
        Paprika rot
        0,248 kg
        0,9 B
        Paprika gelb
        0,192 kg
        0,77 B
        Möhren
        0,336 kg
        0,50 B
        Champignon weiss
        0,62 B
        ==
        Summe
        4,28
        Bar
        4,30
        Rückseld
        0,02
        Steuer
        Brutto
        Netto
        Steuer
        B= 7,00%
        4,28
        ER
        0,28
        Datun:09.04.20 Uhrzeit:19:55:35 Bon: 00780
        Filiale
        13239 Kasse
        6 Bediener
        121
        Vielen Dank für Ihren Einkauf’!
        Ihr Kauf land-Tean.
        In nn NRUURN I IRIN N
        ‚421 2917599999996768989739.
        """
    pass

def main():
    #-------------initializantion and global variables 
    start()
    #---------loopthrough the input folder 
    for file in getinputfiles():
        #print(file)
        #-----------read image
        img = fileread(file) 
        #---------OCR preprossessing deskew then prepair
        #deskew(img)
        #showimg(deskew(img))
        imgdeskew = deskew(img)
        imgafter = ocrpre(imgdeskew)
        #showimg(imgafter)     
        #------------OCR output as text
    
    #--------------Get store
    
    #print(getstore(recipttext))
    #store = getstore(recipttext)
    #print(store)
    #-----------------Based on store use add data
    #getdata(store ,recipttext)

    #print (reciptdata)
    #print(itemlist)
    pass

def deskew(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255,	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    print(angle)
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    #print("[INFO] angle: {:.3f}".format(angle))
    return rotated

def fileread(file):
    img = cv2.imread(file)
    return img

def showimg(img):
    cv2.imshow('sample image',img)
    cv2.waitKey(0) # waits until a key is pressed
    cv2.destroyAllWindows() # destroys the window showing image
    return

def getinputfiles():
    inputfilesarry = []
    for filename in os.listdir(inputdirectory):
        if filename.endswith(".jpg") : 
            #print(os.path.join(inputdirectory, filename))
            inputfilesarry.append(os.path.join(inputdirectory, filename))
            continue
        else:
            continue

    return inputfilesarry

def ocrpre(img):
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,9,10)
    imgpre = th
    return imgpre

def getstore(recipttext): # input img gets the store name or retern genraic based on placelist.csv 
    with open('./setting/stores.csv') as csv_file:
        global storearry
        storearry = list(csv.reader(csv_file, delimiter=','))[0]
    for store in storearry:
        if store in recipttext.lower() : # it will break from first store name
            return store    
    return "gen"

def getdata(store ,recipttext): #gets the data from recipt 
    try:
        reciptdata.update({"Store": store})
        date_pattern = r'(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](19|20)'
        date = re.search(date_pattern, recipttext).group()
        reciptdata.update({"Date": date})
        time_pattern = r'([01][0-9]|2[0-4])[:]([0-6][0-9])[:]([0-6][0-9])'
        time = re.search(time_pattern, recipttext).group()
        reciptdata.update({"Time": time})
    except :
        pass
    if   store in ( storearry [0] , storearry [1] ): #kaufland
        kaufland(recipttext)
        pass
    elif store in storearry [2]: #lidl
        pass
    elif store in storearry [3]: #rewe
        pass
    elif store in storearry [4]: #edeka
        pass
    else:
        pass    
    pass

def kaufland(recipttext):
    reciptbody = False
    #price_pattern = r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])'
    for count,line in enumerate(recipttext.splitlines()):
        #print (line)
        if reciptbody :
            #print ("body",line)
            if (re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',line)) and (not('kg' in line) and not('kg' in recipttext.splitlines()[count -1 ]) )   :
                #print([recipttext.splitlines()[count -1 ] , re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',line).group()])
                #print ("price an d not kg ",line)
                itemlist.append([recipttext.splitlines()[count -1 ] , re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',line).group()])
                pass
            #print (line)
            elif (re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',line)) and not('kg' in line):
                #print([recipttext.splitlines()[count -2 ] , re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',line).group()])
                #print ("dddd",line)
                itemlist.append([recipttext.splitlines()[count -2 ] , re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',line).group()])
                pass
        if "Preis" in line :
            reciptbody = True
        elif "Summe" in line :
            reciptdata.update({"Total": re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',recipttext.splitlines()[count +1 ]).group()})
            reciptbody = False
    reciptdata.update({"ItemCount": len(itemlist)})
            

    pass

if __name__ == '__main__':
    main()
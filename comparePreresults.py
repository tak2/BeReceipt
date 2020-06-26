#.\input\7.jpg
from main import *

start()

# Rad the comapre text from the file 
with codecs.open('7.txt', 'r' , 'utf-8') as file:
    gt = file.read() #groundtruth

img = fileread(os.getcwd() + "/input/7ro.jpg")
#showimg(img)
#print(os.getcwd())

#init compare array 
comparry = []

#ocr raw print 
#print(OCR(img))
rawtext = OCR(img)
    #compare 
#print(cmprfiles(gt , rawtext))
comparry.append(["raw img                                  " , cmprfiles(gt , rawtext)] )

# ocr deskew img 
imgdeskew = deskew(img)
deskewtext = OCR(imgdeskew)
comparry.append(["deskew img                                " , cmprfiles(gt , deskewtext) ])

#flutating
for x in range(1, 20, 2):
    #print(x)
    for y in range(1, 30):
        #print (x , y)
        try:
            #print (x , y)
            imgafter = ocrpre(imgdeskew , x, y)
            pretext = OCR(imgafter)
            comparry.append([("preprossesing img with bloack size " + str(x) + " and c " + str(y)) , cmprfiles(gt , pretext) ])
            #print(("preprossesing img with bloack size " + x "and c" ))
        except:
            pass

        





# imge after pre and deskew 
# imgafter = ocrpre(imgdeskew)
# pretext = OCR(imgafter)
# comparry.append(["preprossesing img" , cmprfiles(gt , pretext) ])




#print (comparry)
import numpy as np
print(np.matrix(comparry))

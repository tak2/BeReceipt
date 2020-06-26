from main import *

start()

for file in getinputfiles():
    itemlist =[]
    reciptdata = {
        "Store": "",
        "Date": "",
        "Time": "",
        "Total": "",
        "ItemCount": ""
        }
    print(file)
    #get image from file 
    img = fileread(file)
    #showimg(img)
    imgdeskew = deskew(img)
    recipttext = OCR(imgdeskew)
    #fileoutput(file, recipttext )
    #fileoutput(file, recipttext )
    store = getstore(recipttext)
    print(store)
    getdata(store ,recipttext)
    print(reciptdata)
    print(itemlist)


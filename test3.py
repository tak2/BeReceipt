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
    reciptbody = False
    #price_pattern = r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])'
    for count,line in enumerate(recipttext.splitlines()):
        #print (line)
        if reciptbody :
            #print ("body",line)
            if (re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',line)) and (not('kg' in line) and not('kg' in recipttext.splitlines()[count -2 ]) )   :
                #print (recipttext.splitlines()[count -2 ])
                #print([recipttext.splitlines()[count -2 ] , re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',line).group()])
                #print ("price an d not kg ",line)
                itemlist.append([recipttext.splitlines()[count -2 ] , re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',line).group()])
                pass
            #print (line)
            elif (re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',line)) and not('kg' in line):
                #print([recipttext.splitlines()[count -2 ] , re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',line).group()])
                #print ("dddd",line)
                #print(recipttext.splitlines()[count -4 ])
                itemlist.append([recipttext.splitlines()[count -4 ] , re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',line).group()])
                pass
        if "Preis" in line :
            reciptbody = True
        elif "Summe" in line :
            try:
                reciptdata.update({"Total": re.search(r'([0-9][0-9]|[0-9])([,]|[.])([0-9][0-9]|[0-9])',recipttext.splitlines()[count +1 ]).group()})
            except:
                pass
            reciptbody = False
    reciptdata.update({"ItemCount": len(itemlist)})
    print(reciptdata)
    print(itemlist)


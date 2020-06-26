import main as mn
import codecs


mn.start()

for file in mn.getinputfiles():
    print(file)
    img = mn.fileread(file)
    mn.showimg(img)
    #mn.showimg(mn.deskew(img))
    #imgdeskew = mn.deskew(img)
    #imgafter = mn.ocrpre(imgdeskew)
    #mn.showimg(imgafter)
    #mn.fileoutput(file)

# with codecs.open('7.txt', 'r' , 'utf-8') as file:
#     data = file.read()
# print(data)

from PIL import Image
import PIL.ImageOps
import datetime as datetime
import math

#Sorts the pixels by row, by the color given, or by a summation of the colors
def HorizontalSort(image, color = 'RED', Descending = False):
    if Descending:
        image = PIL.ImageOps.invert(image)
    SortedPixels = []
    SortedImage = Image.new('RGB', image.size)
    Pixels = GetPixels(image)
    Pixels = [Pixels[i * image.size[0]:(i + 1) * image.size[0]] for i in range(image.size[1])]
    StartTime = datetime.datetime.now()
    for y in range(image.size[1]):
        for i in range(len(Colors)):
            color = NextColor(color)
            Pixels[y] = TestSort(Pixels[y], color, Descending)
        SortedPixels.extend(Pixels[y])
    EndTime = datetime.datetime.now()
    print("HORIZONTAL_SORT: %s (ms)" % ((EndTime - StartTime).total_seconds() * 1000))
    SortedImage.putdata(SortedPixels)
    if Descending:
        SortedImage = PIL.ImageOps.invert(SortedImage)
    SortedImage.save('TEST_HS.jpg')

def VerticalSort(image, color = 'RED', Descending = False):
    if Descending:
        image = PIL.ImageOps.invert(image)
    SortedPixels = []
    SortedImage = Image.new('RGB', image.size)
    RawPixels = GetPixels(image)
    Pixels = []
    for x in range(image.size[0]):
        temp = []
        for y in range(image.size[1]):
            temp.append(RawPixels[y * image.size[0] + x])
        Pixels.append(temp)
    StartTime = datetime.datetime.now()
    for x in range(image.size[0]):
        for i in range(len(Colors)):
            color = NextColor(color)
            Pixels[x] = TestSort(Pixels[x], color, Descending)
    for y in range(image.size[1]):
        PixelRow = [Pixels[i][y] for i in range(image.size[0])]
        SortedPixels.extend(PixelRow)
    EndTime = datetime.datetime.now()
    print("VERTICAL_SORT: %s (ms)" % ((EndTime - StartTime).total_seconds() * 1000))
    SortedImage.putdata(SortedPixels)
    if Descending:
        SortedImage = PIL.ImageOps.invert(SortedImage)
    SortedImage.save('TEST_VS.jpg')

def AllSort(image, color = 'RED', Descending = False):
    if Descending:
        image = PIL.ImageOps.invert(image)
    SortedImage = Image.new('RGB', image.size)
    Pixels = GetPixels(image)
    Colors = GetPixelColors(Pixels)
    StartTime = datetime.datetime.now()
    for i in range(len(Colors)):
        color = NextColor(color)
        Pixels = TestSort(Pixels, color, Descending)
    EndTime = datetime.datetime.now()
    print("All_SORT: %s (ms)" % ((EndTime - StartTime).total_seconds() * 1000))
    SortedImage.putdata(Pixels)
    if Descending:
        SortedImage = PIL.ImageOps.invert(SortedImage)

    SortedImage.save('TEST_AS.jpg')

def GetPixels(Image):
    return list(Image.getdata())

def GetPixelColors(Pixels):
    return list(zip(*Pixels))

def SumColors(Pixels):
    Sum = []
    for i in range(len(Pixels)):
        total = 0
        for j in range(len(Pixels[i])):
            total += Pixels[i][j]
        Sum.append(total)
    return Sum

def TestSort(Pixels, color = None, Descending = False):
    Size = 256 * 5
    if color == 'RED':
        ColorCalc = RedCalc
    elif color == 'GREEN':
        ColorCalc = GreenCalc
    elif color == 'BLUE':
        ColorCalc = BlueCalc
    counts = [[] for i in range(Size)]
    Sorted = []
    for i in range(len(Pixels)):
        counts[ColorCalc(Pixels[i])].append(Pixels[i])
    for i in range(len(counts)):
        Sorted.extend(counts[i])
    return Sorted

def RedCalc(Pixel):
    return Pixel[0] * 3 + Pixel[1] + Pixel[2]

def GreenCalc(Pixel):
    return Pixel[1] * 3 + Pixel[0] + Pixel[2]

def BlueCalc(Pixel):
    return Pixel[2] * 3 + Pixel[0] + Pixel[1]

def NextColor(Color):
    for i in range(len(Colors)):
        if(Color == Colors[i]):
            next = i - 1
            if next == -1:
                next = len(Colors) - 1
    return Colors[next]

def PixelSort(File):
    image = Image.open('File')
    return AllSort(image)

image = Image.open('image.jpg')
print(image.size[0] * image.size[1])

Colors = ['RED', 'GREEN', 'BLUE']
Sort = 'H'
if Sort == 'H':
    #Horizontal Sort
    HorizontalSort(image, 'RED')
    HorizontalSort(image, 'GREEN')
    HorizontalSort(image, 'BLUE')
    HorizontalSort(image)
elif Sort == 'V':
    #Vertical Sort
    VerticalSort(image, 'RED')
    VerticalSort(image, 'GREEN')
    VerticalSort(image, 'BLUE')
    VerticalSort(image, Descending = True)
elif Sort == 'A':
    #All Sort
    AllSort(image, 'RED')
    AllSort(image, 'GREEN')
    AllSort(image, 'BLUE')
    AllSort(image, Descending = True)

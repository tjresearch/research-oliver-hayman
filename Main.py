import PIL
import time 
import multiprocessing as mp
import random
import math
from PIL import Image
ROTNUM = 6
from google.colab import drive
from google.colab import files
'''uploaded = files.upload()
for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))'''
#sideScalar = 0.8
def scaleConvert(img, width, sideScale):
  t = float(width)/float(sideScale)
  a, b = img.size
  www = int(float(a)/float(t))
  if www > 0:
    return www
  return 1
def pix(s, img, n, theta, count):
  im2 = img.convert('RGBA')
  rot = im2.rotate(theta, expand=1)
  fff = Image.new('RGBA', rot.size, (255,)*4)
  out = Image.composite(rot, fff, rot)
  sav = out.convert('RGB')
  im = sav.load()
  a, b = sav.size
  wwww = color(im, n, a, b, count)
  #sav.save(s[:-4]+ "-"+str(theta)+".jpg")
  return wwww
def color(im, n, width, height, count):
  arr = []
  
  for i in range(0, int(width/n)):
    arr.append([])
    for j in range(0, int(height/n)):
      arr[i].append(0)
      label(im, i*n, j*n, n, arr, count)
  return arr
def label(im, a, b, c, arr, counttt):
  count = 0
  for i in range(c):
    for j in range(c):
      if im[a+i, b+j] == (255, 255, 255):
        count += 1
      #im[a+i, b+j] = (255, 255, 255)
  if float(count)/float(c*c) < 0.6:
    arr[int(a/c)][int(b/c)] = counttt
    '''for i in range(c):
      for j in range(c):
        im[a+i,b+j] = (0, 0, 0)'''
def pixelate(s, temp, theta, width, side, count):
  return pix(s, temp, scaleConvert(temp, width, side), theta, count)
def printer(x):
  for i in range(len(x[0])):
    s = ""
    for j in range(len(x)):
      s += str(x[j][i])
      s += "\t"
    print(s)
def truncate(x):
  t = True
  while t:
    try:
      if fullZero(x[0]):
        del x[0]
      else:
        t = False
    except:
      t = False
  t = True
  while t:
    try:
      if fullZero(x[-1]):
        del x[-1]
      else:
        t = False
    except:
      t = False
  t = True
  while t:
    try:
      if fullZeroCol(x, 0):
        x = delZero(x, 0)
      else:
        t = False
    except:
      t = False
  t = True
  while t:
    try:
      if fullZeroCol(x, len(x[0])-1):
        x = delZero(x, len(x[0])-1)
      else:
        t = False
    except:
      t = False
  return x
def fullZero(x):
  for i in x:
    if i != 0:
      return False
  return True
def fullZeroCol(x, n): 
  for i in x:
    if i[n] != 0:
      return False
  return True
def matBumperUp(x):
  ret = []
  for i in range(len(x)):
    ret.append(x[i][:])
  for k in range(len(x)):
    prev = 0
    current = 0
    count = 0
    for i in range(len(x[0])):
      prev = current
      current = x[k][i]
      ret[k][i] = 0
      if current != 0 and prev != 0:
          count += 1
      elif current == 0 and prev != 0:
          for j in range(count):
            ret[k][i-j-1] = j+1
          count = 0
      elif current != 0 and prev == 0:
          count += 1
    if current != 0:
      for j in range(count):
          ret[k][len(ret[0])-1-j] = j+1
  return ret
def matBumperDown(x):
  ret = []
  for i in range(len(x)):
    ret.append(x[i][:])
  for k in range(len(x)):
    prev = 0
    current = 0
    count = 0
    for i in range(len(x[0])):
      prev = current
      current = x[k][i]
      ret[k][i] = 0
      if current != 0 and prev != 0:
          count += 1
      elif current == 0 and prev != 0:
          for j in range(count):
            ret[k][i-1-j] = count - j
          count = 0
      elif current != 0 and prev == 0:
          count += 1
    if current != 0:
      for j in range(count):
          ret[k][len(ret[0])-1-j] = count - j
  return ret
def delZero(x, n):
  for i in x:
    del i[n]
  return x
def createContainer(widths, side):
  return pixelate("container.png", Image.open("container.png"), 0, widths[len(widths)-1], side, 1)
def widthFind(width, rot, rot2):
  a = abs(math.cos(rot+rot2)*width/math.sin(rot))
  b = abs(math.cos(rot-rot2)*width/math.sin(rot))
  return max(a, b)
def pixArr(widths, side, names):
  images = {}
  for i in range(len(widths)-1):
    images[i] = []
    u = Image.open(names[i])
    widthh, heightt = u.size
    for j in range(ROTNUM):
      v = u.rotate(j*360.0/ROTNUM)
      w, h = v.size
      images[i].append(truncate(pixelate(names[i]+".png", u, j*360.0/ROTNUM, w/widthh*widths[i], side, i+2)))
  return images
def size(x):
  count = 0
  for i in range(len(x)):
    for j in range(len(x[0])):
      if x[i][j] != 0:
        count += 1
  return count
def partition(arr,low,high): 
    i = ( low-1 )          
    pivot = size(arr[high])      
    for j in range(low , high): 
        if size(arr[j]) >= pivot: 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 
def quickSort(arr,low,high): 
    if low < high: 
        pi = partition(arr,low,high) 
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high)
def duplicate(name, amount, initial=1):
  im = Image.open(name)
  for i in range(amount):
    im.save(str(i+initial)+".png")
def sizeSort(arr):
  quickSort(arr, 0, len(arr)-1)
def imageCreator(arr):
  out = Image.new('RGB', (len(arr), len(arr[0])), color = (0, 0, 0))
  pixFin = out.load()
  pixCol = {0:(255, 255, 255)}
  for i in range(len(arr)):
      for j in range(len(arr[0])):
        temp = arr[i][j]
        if not (temp in pixCol):
          pixCol[temp] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pixFin[i, j] = pixCol[temp]
  out.save("final.jpg")
def imageCreator(arr, scale):
  out = Image.new('RGB', (len(arr)*scale, len(arr[0])*scale), color = 'white')
  pixFin = out.load()
  pixCol = {0:(255, 255, 255)}
  for i in range(len(arr)):
      for j in range(len(arr[0])):
        temp = arr[i][j]
        if not (temp in pixCol):
          pixCol[temp] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for k in range(scale*i, scale*(i+1)):
                  for l in range(scale*j, scale*(j+1)):
                      pixFin[k, l] = pixCol[temp]
  out.save("final.jpg")
def pack(widths, side, names):
  images = pixArr(widths, side, names)
  container = createContainer(widths, side)
  temp = []
  for i in range(len(widths)-1):
    temp.append((size(images[i][0]), i))
  temp.sort(reverse = True)
  bumperContainer = matBumperDown(container)
  bumperArr = {i:[matBumperUp(j) for j in images[i]] for i in range(len(widths)-1)}
  #print([size(images[0][i]) - size(bumperArr[0][i]) for i in range(len(images[0]))])
  #printer(container)
  #printer(bumperContainer)
  posRot = {}
  maxh = 0
  counthy = 0
  for aa in temp:
    counthy += 1
    print("Packing object", counthy)
    j, i = aa
    xxx, yyy, zzz = rotPlace(container, bumperContainer, images[i], bumperArr[i], side)
    maxh = max(len(container) - yyy, len(container) - maxh)
    posRot[i] = xxx
    bumperContainer = matBumperDown(container)
  print(maxh/len(container))
  return container
def minWidthFind(x, y, z):
   a, b = place(x, y)
   return (a, b, z)
def fileReader(fileName):
  widths = []
  names = []
  '''for i in open(fileName, "r").readlines():
    temp = i.replace("\n", "").strip().split(" ")
    if len(temp) > 2:
      for i in range(int(temp[2])-1):
        widths.append(float(temp[1]))
        names.append(temp[0])
    widths.append(float(temp[1]))
    names.append(temp[0])'''
  nn = int(input("How many objects do you want to pack?"))
  for i in range(nn):
    names.append(input("Enter an object file name:"))
    widths.append(float(input("Enter its width (in):")))
  names.append(input("Enter a container file name:"))
  widths.append(float(input("Enter its width (in):")))
  return widths, names
def rotPlace(container, bumperContainer, img, bumpImg, side):
  #minH, minW = place(bumperContainer, bumpImg[0])
  pool = mp.Pool(mp.cpu_count())
  results = pool.starmap(minWidthFind, [(bumperContainer, bumpImg[i], i) for i in range(ROTNUM)])
  print(results)
  b, a, c = max(results)
  pool.close()
  placeHelp(container, img[c], a, b)
  return (c, b, a)
def canPlace(x, y, a, b):
  maxx = 0
  try:
    for i in range(0, len(y)):
      for j in range(0, len(y[0])):
        if x[a+i][b+j] != 0 and y[i][j] != 0 and x[a+i][b+j] + y[i][j] > maxx:
          maxx = x[a+i][b+j] + y[i][j]
    return maxx
  except:
    return -1
def placeHelp(x, y, a, b):
  for i in range(0, len(y)):
    for j in range(0, len(y[0])):
      try: 
        x[a+i][b+j] = int(y[i][j])+int(x[a+i][b+j])
      except: print(a+i, " ", b+j)
def place(xx, yy):
  col = 0
  row = -1
  for i in range(len(xx)):
    count = len(xx[0])-len(yy[0])
    while(count >= col):
      temp = canPlace(xx, yy, i, count)
      if temp == 0: #or temp == 2:
        row = i
        col = count
        count -= 1
      elif temp == -1:
        count -= 1
      else:
        count -= temp - 1
  return (col, row)
time1 = time.time()
s = [[0, 0, 0, 0, 1], [1, 1, 1, 1, 1]]
#widths = [2, 2, 5]
widths, names = fileReader("objects.txt")
  #test.append(list(1 for x in range(100)))'''
#printer(matBumperUp(test))
#printer(matBumperUp(s))
#printer(matBumperUp(truncate(pixelate("1.png", 0, 2, 0.08, 1))))
print("Number of processors: ", mp.cpu_count())
imageCreator(pack(widths, 0.06, names), 3)
print("Completed!")
#print("Duration:", (time.time()-time1))
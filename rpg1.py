import os
from msvcrt import getch
import math
import random
print("~rpg~")
#setup
global w,h
w=int(input("Give screen width(>53): "))
while w<54:
	w=int(input("Give screen width(>53): "))
h=int(input("Give screen height:(>20): "))
while h<21:
	h=int(input("Give screen height(>20): "))
#global temps
posx,posy=int(h/2),0
stepping=' '
walkspeed=1
vd=29 #vsion distance (actual it is the diameter)
money=0
map = [[0 for x in range(w)] for y in range(h)] 
mapmask = [[0 for x in range(w)] for y in range(h)] 
#style
herochar='@'#chr(64)
emptychar=' '#chr(32)
mapborderchar='~'

def buildmap():
	buildobject("palace1_2.txt",random.randint(3,h-18),random.randint(2,w-52),1,1)
	#buildobject("palace1.txt",3,3,1,1)
	for i in range(random.randint(0,int(w/10))):
		buildobject("house1.txt",random.randint(3,h-10),random.randint(3,w-25),1,1)
	for i in range(random.randint(0,w)):
		buildobject("box1_1.txt",random.randint(0,h-1),random.randint(0,w-1),1,1)
	for i in range(random.randint(0,int(w/2))):
		buildobject("visionbox.txt",random.randint(0,h-2),random.randint(0,w-2),1,1)
	for i in range(random.randint(0,w)):
		buildobject("box2_2.txt",random.randint(0,h-2),random.randint(0,w-2),1,1)	
		
def buildobject(obj,x,y,spx,spy):
	with open(obj) as f:
		content = f.readlines()
	content = [n.strip() for n in content]
	f,objw=buildobjecttestspace(content,x,y,spx,spy)
	if f==0:
		for line in range(len(content)):
			for ch in range(objw):
				map[x+line][y+ch] = content[line][ch]
	return

def buildobjecttestspace(content,x,y,spx,spy):
	f=0
	objh = len(content)
	objw = 0
	for ch in content[0]:
		objw+=1	
	for i in range(-spx,objh+spx+1):
		for j in range(-spy,objw+spy+1):
			if x+i>=0 and x+i<h and y+j>=0 and y+j<w:
				if map[x+i][y+j]!=emptychar:
					f=1
	return f,objw

def starthero():
	global stepping
	stepping = map[posx][posy]
	map[posx][posy] = herochar
				
def move(posx,posy,relx,rely):
	flag=0
	if relx != 0:
		if posx+relx >= 0 and posx+relx < len(map):
			flag=1
	if rely != 0:
		if posy+rely >= 0 and posy+rely < len(map[0]):
			flag=1
	if flag==1:
		global stepping,money,vd
		m=map[posx+relx][posy+rely]
		if m!='-' and m!='|' and m!='+':
			map[posx][posy] = stepping
			if m=='O':
				money+=1
				stepping = emptychar
			elif m=='*':
				vd+=100
			else:
				stepping = m
			map[posx+relx][posy+rely] = herochar
			posx,posy = posx+relx,posy+rely
			printmap()
	return map,posx,posy

def updatemapmask(posx,posy):
	r = round(math.sqrt(vd+1/math.pi))
	for mx in range(-r+posx,r+posx+1):
		for my in range(-r+posy,r+posy+1):
			if mx>=0 and mx<h and my>=0 and my<w: 
				if abs(mx-posx)+abs(my-posy)<r*math.pi/math.sqrt(5):
					mapmask[mx][my]=1
	return mapmask
def printmap():
	os.system("cls")
	print(' MAP '.center(w, mapborderchar))
	mapmask = updatemapmask(posx,posy)
	for i in range(h):
		for j in range(w):
			if mapmask[i][j]==1: #mask=1
				print(map[i][j],end="")
			else:
				print(emptychar,end="")
		print("")
	print(' MAP '.center(w, mapborderchar))

def printstats():
	global money,vd,walkspeed
	os.system("cls")
	print(' STATS '.center(int(w/4)+10, mapborderchar))
	print(str((int(w/8)-6)*' ')+'Your hero : '+str(herochar))
	print(str((int(w/8)-2)*' ')+"Money : "+str(money))
	print(str((int(w/8)-3)*' ')+"Vision : "+str(vd))
	print(str((int(w/8)-2)*' ')+"Speed : "+str(walkspeed))
	print(' STATS '.center(int(w/4)+10, mapborderchar))

def startgame():
	mapmask = updatemapmask(posx,posy)
	for i in range(h):
		for j in range(w):
			if not(i==posx and j==posy): #not hero position
				map[i][j] = emptychar
				mapmask[i][j] = 0
	buildmap()
	starthero()
	printmap()
	return map,mapmask;

map,mapmask = startgame()
onpage=0
while True:#update
	#key input
	key = ord(getch())
	if key == 27:
		break
	elif key == 13: #Enter
		print("*Enter*")
	elif key == 115:
		if onpage==0:
			onpage=1
			printstats()
		elif onpage==1:
			onpage=0
			printmap()	
	elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
		key = ord(getch())
		if onpage==0:
			if key == 72:#up
				map,posx,posy = move(posx,posy,-walkspeed,0)
			elif key == 80:#down
				map,posx,posy = move(posx,posy,walkspeed,0)
			elif key == 75:#left
				map,posx,posy = move(posx,posy,0,-walkspeed)
			elif key == 77:#right
				map,posx,posy = move(posx,posy,0,walkspeed)		
	elif key != 255:
		print(key)
		
		
            
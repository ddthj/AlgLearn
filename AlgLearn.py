'''
Alglearn
By SquidFairy/ddthj
Version 1

Alglearn is a tool to help speedcubers learn sets of algorythms and help
them stay in practice.

Todo List:
-create algorythms [#] 
-create ability to change active sets []
-create practice mode [#]
-Have timer start on spacebar release []
-Ignore inverse on 180 turns []
-Make a better readme []

Requires:
Pygame on Python 3+
'''

import pygame
import time
import os
import random

global step
step = 0
global mode
mode = 0

pygame.init()
display = pygame.display.set_mode((500,200))
pygame.display.set_caption("AlgLearn")
MiniText = pygame.font.SysFont("courier",14)
Text = pygame.font.SysFont("courier",24)
#'freesansbold.ttf'

MiniText.set_bold(False)
white = (255,255,255)
black = (0,0,0)

display.fill(white)

def text(font,text,x,y):
    textsurf = font.render(text,True,black,white)
    textrect = textsurf.get_rect()
    textrect.x = x
    textrect.y = y
    display.blit(textsurf,textrect)

def getScramble(alg):
    a=alg.split(" ")
    #print(a)
    b = ""
    i = len(a) - 1
    while i >=0:
        c = a[i]
        if len(c) > 0:
            if c.find("'") != -1:
                b+=c[:-1] + " "
            else:
                b+=c + "' "
        i-=1
    return b

def pickWeak(algset):
    #print(algset)
    maxTime = float(0)
    useable = []
    for i in range(0,len(algset)):
        if algset[i].average < 0.0 or algset[i].average + 0.25 >= maxTime:
            useable.append(algset[i])
        if algset[i].average > maxTime:
            maxTime = algset[i].average
            useable = []
            useable.append(algset[i])
            for item in algset:
                if item.average < 0.0 or item.average + 0.25 > maxTime:
                    if item.name != algset[i].name:
                        useable.append(item)
    if len(useable) <=1:
        return useable[0]
    else:
        return useable[random.randint(0,len(useable)-1)]

def pickSlow(algset):
    lowest = 99.0
    index = 0
    useable = []
    for i in range(0,len(algset)):
        if algset[i].tps == 0:
            useable.append(algset[i])
        if algset[i].tps < lowest:
            lowest = algset[i].tps
            index = i
    if len(useable) > 2:
        return useable[random.randint(0,len(useable)-1)]
    else:
        return algset[index]

def pickCut(algset,setting):
    he = []
    for item in algset:
        if item.average > float(setting) or item.average < 0:
            he.append(item)
    if len(he) <= 0:
        return pickCut(algset,float(setting)-0.5)
    return he[random.randint(0,len(he)-1)]

class alg():
    def __init__(self,name,alg):
        self.name = name
        self.alg = alg
        self.scramble = getScramble(alg)
        self.solves = []
        self.average = float(-1)
        self.tps = 0
        self.t = self.turns(alg)
    def turns(self,alg):
        turns = 0
        for item in self.alg.split(" "):
            if item.find("2") != -1:
                turns +=2
            else:
                turns +=1
        return turns
        
    def update(self,time):
        self.solves.append(time)
        self.av()
    def av(self):
        x = 0.0
        for item in self.solves:
            x+=item
        if len(self.solves) > 0:
            self.average = x/len(self.solves)
            turns = 0
            for item in self.alg.split(" "):
                if item.find("2") != -1:
                    turns +=2
                else:
                    turns +=1
            self.tps = float(turns / self.average)
            #return (x/len(self.solves))
        else:
            self.average = -1.0
            #return -1

    def fakeAverage(self,time):
        x = 0.0
        x+=time
        for item in self.solves:
            x+=item
        return (x/(len(self.solves)+1))
    def fakeTPS(self,time):
        x = 0.0
        x+=time
        for item in self.solves:
            x+=item
        turns = 0
        for item in self.alg.split(" "):
            if item.find("2") != -1:
                turns +=2
            else:
                turns +=1
                
        return (float( turns / (x/(len(self.solves)+1))))
try:
    f = open("algset.txt","r")
    algset = []
    for line in f:
        #print(line)
        if not (line.find("#") != -1):
            line = line.replace("\n"," ")
            l = line.split(":")
            #print(str(l[1]))
            algset.append(alg(str(l[0]),str(l[1])))
        if line.find("!mode") != -1:
            line = line.replace("\n","")
            l = line.split(":")
            mode = int(l[1])
            if mode == 3:
                global setting
                setting = float(l[2])
    #print("algset length: "+str(len(algset)))
except Exception as e:
    print(e)
    algset = []
    algset.append(alg("algset.txt error reading file!","F"))
    
picked = False
space = False
while 1:
    display.fill(white)
    d = False
    #start = time.clock()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:        
            pygame.quit()
            os._exit(1)
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space = True
            if event.key == pygame.K_d:
                    d = True

    if step == 0 and space == False:
        dnf = False
        if picked == False:
            if mode == 1:
                current = pickWeak(algset)
            elif mode == 2:
                current = pickSlow(algset)
            elif mode ==3:
                current = pickCut(algset,setting)
            else:
                current = algset[random.randint(0,len(algset)-1)]
            picked = True
        text(MiniText,"Don't look at the cube",10,10)
        cText = "Scramble: " + str(current.scramble)
        text(MiniText,cText,10,40)
        text(MiniText,"Press Space to begin", 10,60)
    elif step == 0 and space == True:
        start = time.clock()
        ti = time.clock() - start
        text(Text,str(ti)[:5],180,20)
        step +=1
        space = False
    elif step == 1 and space == False:
        ti =time.clock() - start
        text(Text,str(ti)[:5],180,20)
        text(MiniText,("Solution: "+str(current.alg)),10,70)
        if ti > 0.0:
            h = str(current.t / ti)[:4] + " TPS"
        text(Text,h,320,20)
    elif step == 1 and space == True:
        text(MiniText,("Solution: "+str(current.alg)),10,70)
        stop = time.clock() - start
        text(Text,str(stop)[:5],180,20)
        if stop > 0.0:
            h = str(current.t / stop)[:4] + " TPS"
        text(Text,h,320,20)
        step += 1
        space = False
    elif step == 2:
        if d:
            dnf = True
        if dnf:
            text(MiniText,"DNF, this solve will not be recorded",10,150)
            z = 1
            y = current.average
            if mode == 2:
                y = str(current.tps)[:3]
        else:
            z = 0
            y = current.fakeAverage(stop)
            if mode == 2:
                y = str(current.fakeTPS(stop))[:3]
        text(Text,str(stop)[:5],180,20)
        if ti > 0.0:
            h = str(current.t / ti)[:4] + " TPS"
        text(Text,h,320,20)
        text(MiniText,"press 'd' to dnf or space to continue",10,120)
        if mode == 2:
            s = "" + current.name + ", " + str(len(current.solves) + 1 - z) + " Solves, " + str(y) + " Average TPS"
        else:
            s = "" + current.name + ", " + str(len(current.solves) + 1 - z) + " Solves, " + str(y)[:5] + " Average"
        text(MiniText,str(s),10,50)
        text(MiniText,("Solution: "+str(current.alg)),10,70)
        if space:
            step += 1
            space = False
    elif step == 3 and dnf == False:
        current.update(stop)
        space = False
        step=0
        picked = False
    elif step == 3 and dnf == True:
        dnf = False
        space = False
        step=0
        picked = False
    pygame.display.update()

        

import sys, pickle

import pygame
from pygame.locals import *

class _globals():
    pass

def updateScreen():
    factor = float(640) / g.viewport.w
    g.scaled = pygame.transform.scale(g.raw,(int(g.raw.get_width()*factor),
                                             int(g.raw.get_height()*factor)))
    cropbox = pygame.Rect(g.viewport.left*factor,g.viewport.top*factor,
                          g.viewport.w*factor,g.viewport.h*factor)
    screen.blit(g.scaled,(0,0),area=cropbox)

def output(screenpos):
    x = g.viewport.left + int((float(screenpos[0]) / 640) * g.viewport.w)
    y = g.viewport.top  + (float(screenpos[1]) / 480) * g.viewport.h
    
    t = x * g.dt
    f = (g.raw.get_height() - y) * g.df

    #look up the note:
    previous = g.note_table[0]
    note = g.note_table[-1][0]
    for row in g.note_table:
        if abs(row[1]-f) > abs(previous[1]-f):
            note = previous[0]
            break
        previous = row

    print "t: %f\tf: %d\t note: %s" % (t,f,note)

#SETUP
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Spectrogram")

#GLOBALS
g = _globals()
clock = pygame.time.Clock()

############################## - MAINLOOP - ##############################


g.viewport = pygame.Rect(0,0,320,240)
g.raw = pygame.image.load("out.bmp")
g.scaled = None

g.samplerate = 44100
g.dt = 0.125        #these have to be set manually for each piece, depending
g.df = 8            #on window length and samplerate

fin = open("notes_list.pickle")
g.note_table = pickle.load(fin)
fin.close()

updateScreen()

_END = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            _END = True
            break
        
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                g.viewport.left -= 16
            elif event.key == K_RIGHT:
                g.viewport.left += 16
            elif event.key == K_UP:
                g.viewport.top -= 16
            elif event.key == K_DOWN:
                g.viewport.top += 16
            elif event.key == K_i:
                if g.viewport.width > 120:
                    g.viewport.w -= 60
                    g.viewport.h -= 45
            elif event.key == K_o:
                if g.viewport.width < 640:
                    g.viewport.w += 60
                    g.viewport.h += 45

            g.viewport.clamp_ip(pygame.Rect(0,0,g.raw.get_width(),
                                            g.raw.get_height()))
            updateScreen()

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                #mouse wheel up
                if g.viewport.width > 120:
                    g.viewport.w -= 60
                    g.viewport.h -= 45
                g.viewport.clamp_ip(pygame.Rect(0,0,g.raw.get_width(),
                                            g.raw.get_height()))
                updateScreen()
            elif event.button == 5:
                #mouse wheel down
                if g.viewport.width < 640:
                    g.viewport.w += 60
                    g.viewport.h += 45
                g.viewport.clamp_ip(pygame.Rect(0,0,g.raw.get_width(),
                                            g.raw.get_height()))
                updateScreen()
            else:
                #a click
                output(event.pos)
    if _END:
        break
    
    pygame.display.flip()
    clock.tick(40)

pygame.quit()

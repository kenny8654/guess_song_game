from pygame import mixer
import pygame 
import threading
import time
from os import listdir
import random

def mask(word):
    output = ''
    for i,w in enumerate(word):
        if w != ' ':
            output += 'O'
        else:
            output += ' '
    return output

count = 0
text_status = True
path = "./music/"
music = listdir(path)
songNum = len(music)
f = open('songList.txt','r', encoding='UTF-8')
songList = {}
for i,line in enumerate(f.readlines()):
    songList[line.replace('\n', '').split(',')[0]] = line.replace('\n', '').split(',')[1]

print('songNum : '+ str(songNum))
randomList = list(range(0,songNum + 1 ))
random.shuffle(randomList)
pygame.init()
mixer.init()
screen = pygame.display.set_mode((960,480))
pygame.display.set_caption("猜歌猜起來")
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((204,204,204))
screen.blit(background,(0,0))
font = pygame.font.Font("msjh.ttc", 72)
text = font.render('Press Enter to Start', True, (225, 225, 228))


while True: 
 for event in pygame.event.get():
    screen.fill((0,0,0))
    screen.blit(text,(480 - text.get_width() // 2, 240 - text.get_height() // 2))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print('press enter  , text_status : ' + str(text_status))
        if text_status: # 猜歌
            while True: 
                if  music[randomList[count]].replace('.mp3','') in songList:
                    songName = songList[music[randomList[count]].replace('.mp3','')]
                    mixer.music.load('./music/' + music[randomList[count]])
                    play = mixer.music.play()
                    print('while if')
                    break
            text = font.render(mask(songName), True, (225, 225, 228))
            text_status = False
            print('text_status : mask' , mask(songName))
            # print('text ',text)
        else: # 公布答案
            count += 1
            text = font.render(songName, True, (225, 225, 228))
            text_status = True
            print('text_status : no mask' , songName)
    if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
        pygame.mixer.quit()
        pygame.quit()
    pygame.display.update() 


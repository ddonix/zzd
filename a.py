# -*- coding: UTF-8 -*-
import pygame  
  
pygame.mixer.init()  
pygame.mixer.music.load("auido.mp3")  
while True:  
	if pygame.mixer.music.get_busy()==False:  
		pygame.mixer.music.play()

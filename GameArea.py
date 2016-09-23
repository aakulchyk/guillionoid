#!/usr/bin/env python

import pygame

class Area:
    def __init__(self, scr):
        self.screen = scr
        
        size = w,h = scr.get_size()
        self.rect = pygame.Rect(10, 10, w-(w/4), h-20)
    def paint(self):
        pygame.draw.rect(self.screen, (100,100,100), self.rect, 3)
  
    

import pygame as pg
from color import *
from text_align import TEXT_ALIGN
class Label():
    def __init__(
        self,
        text:str, 
        size:int, 
        font_name,
        x:int,
        y:int,
        text_align:TEXT_ALIGN=TEXT_ALIGN.CENTER,
        color:(int,int,int)=WHITE
        ):
        self.__type__="label"
        self.text = text
        self.font = pg.font.Font(font_name, size)
        self.rect = (x, y)
        self.text_align = text_align
        self.color = color
       

    def draw(self, display): 
        self.text_surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surface.get_rect()       
        if self.text_align == TEXT_ALIGN.CENTER:
            self.text_rect.center = self.rect
        elif self.text_align == TEXT_ALIGN.LEFT:
            self.text_rect.midleft = self.rect
        elif self.text_align == TEXT_ALIGN.RIGHT:
            self.text_rect.midright = self.rect
        display.blit(self.text_surface,self.text_rect)

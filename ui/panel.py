import pygame as pg
class Panel():
    def __init__(
        self,        
        background_img=None,
        background_color:(int,int,int)=None,
        x:int=0,
        y:int=0,
        width:int=0,
        height:int=0
    ):
        self.__type__="panel"
        if background_color:
            self.rect = (x, y, width, height)
            self.color = background_color
            self.type = 0
    
    def draw(self,display):
        if self.type == 0:
            self.img_rect = pg.draw.rect(display,self.color,self.rect)
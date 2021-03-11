import pygame as pg
from game.color import *
from game.text_align import TEXT_ALIGN
from ui import Label, Cursor

class Select():
    def __init__(
        self,
        options, 
        size:int, 
        font_name,
        x:int,
        y:int,
        offset:int,
        text_align:TEXT_ALIGN=TEXT_ALIGN.CENTER,
        color:(int,int,int)=WHITE,
        horizontal:bool=False
        ):
        self.__type__="select"
        self.size = size
        self.font_name = font_name
        self.x = x
        self.y = y     
        self.offset = offset
        self.text_align = text_align
        self.color = color    
        self.options = []      
        self.cursor = Cursor(self.size,self.font_name,x=self.x,y=self.y)
        self.drawed = False
        self.horizontal = horizontal
        if len(options) > 0:
            self.create_options(options)

    def draw(self, display):
        for opt in self.options:
            opt['element'].draw(display)
        self.cursor.draw(display)
        self.drawed = True    

    def create_options(self,options):
        self.drawed = False
        _y=self.y
        _x=self.x
        for opt in options:
            self.options.append({
                "name":opt,
                "element":Label(
                    text=opt,
                    size=self.size,
                    font_name=self.font_name,
                    x=_x,
                    y=_y,
                    text_align= self.text_align,
                    color=self.color
                )
            })
            if self.horizontal:
                _x += self.offset
            else:
                _y += self.offset

    def set_cur(self, index):
        x, y =self.options[index]['element'].rect
        self.cursor.set_cur(x, y)
    
    def collidepoint(self, mx, my):
        for index, option in enumerate(self.options):
            if self.drawed and option["element"].text_rect.collidepoint((mx,my)):                        
                return index
        else:
            return None


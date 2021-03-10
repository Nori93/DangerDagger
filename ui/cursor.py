import pygame as pg
from color import *
from text_align import TEXT_ALIGN
from ui import Label

class Cursor():
    def __init__(
        self,
        size:int,
        font_name:str,
        cur_left_text:str="[",
        cur_right_text:str="]",
        x:int=0,
        y:int=0,
        offset_l:int=-115,   
        offset_r:int=115,             
        color:(int, int, int)=WHITE
    ):
        self.__type__="cursor"
        self.offset_l = offset_l
        self.offset_r = offset_r
        self.cur_l = Label(
            cur_left_text,
            size,
            font_name,
            x + self.offset_l,
            y,
            color=color)
        self.cur_r = Label(
            cur_right_text,
            size,
            font_name,
            x + self.offset_r,
            y,
            color=color)
        self.set_cur(x,y)
    
    def draw(self, display):
        self.cur_l.draw(display)
        self.cur_r.draw(display)

    def set_cur(self, x:int, y:int):
        self.cur_l.rect =(x + self.offset_l, y)
        self.cur_r.rect =(x + self.offset_r, y)
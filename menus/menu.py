import pygame as pg
from color import *
from input_handlers import handle_main_menu
from render_function import draw_text, draw_panel
from text_align import TEXT_ALIGN

from ui.label import Label
from ui.select import Select
from ui.panel import Panel

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.width / 2, self.game.height / 2
        self.run_display = True

        self.font_size = 20 
        
        self.cursor_rect_l = pg.Rect(0, 0, self.font_size , self.font_size)
        self.cursor_rect_r = pg.Rect(0, 0, self.font_size, self.font_size)
        
        self.offset_l = -100
        self.offset_r = 115
        self.offset_h = -0

    def draw_cursor(self):
        draw_text(self.game.display,"[",  self.font_size, self.game.font_name, self.cursor_rect_l.x, self.cursor_rect_l.y)
        draw_text(self.game.display,"]",  self.font_size, self.game.font_name, self.cursor_rect_r.x, self.cursor_rect_r.y)


    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pg.display.update()      

    def set_cur(self, x, y, offset_r=115,offset_l = -100,offset_h = 0):
        self.cursor_rect_l.midtop =(x + offset_l, y + offset_h)
        self.cursor_rect_r.midtop =(x + offset_r, y + offset_h)


    def handle_manu(self):
        action = handle_main_menu()
        self.act_start_key = action.get("start_key")
        self.act_back_key = action.get("back_key")
        self.act_down_key = action.get("down_key")
        self.act_up_key = action.get("up_key")
        self.act_left_key = action.get("left_key")
        self.act_right_key = action.get("right_key")
        self.act_esc = action.get("esc")
        self.act_mouse_left = action.get("mouse_left")
        self.act_quit = action.get("quit")

    
    def render_from_xml(self,xml):
        elements = []
        for element in xml:
            if element.tag =="label":
                elements.append({
                    'name': element.attrib["name"],
                    'element':self.create_label(element)
                })
            elif element.tag == "select":
                elements.append({
                    'name':element.attrib["name"],
                    'element':self.create_select(element)
                })
            elif element.tag == "panel":
                elements.append({
                    'name':element.attrib["name"],
                    'element':self.create_panel(element)
                })
        
        return elements
    
    def create_label(self,element):
        text_align = TEXT_ALIGN.CENTER
        if "text_aligne" in element.attrib:
            text_align = element.attrib['text_align']

        color = WHITE
        if "color" in element.attrib:
            color = element.attrib['color']

        return Label(
            text=element.attrib['text'],
            size=int(element.attrib['size']),
            font_name=element.attrib['font_name'],
            x=int(element.attrib['x']),
            y=int(element.attrib['y']),
            text_align=text_align,
            color=color
        )
    
    def create_select(self,element):
        options = []
        for child in element:
            options.append(child.attrib["text"])
        text_align = TEXT_ALIGN.CENTER
        if "text_aligne" in element.attrib:
            text_align = element.attrib['text_align']
        
        horizontal = False
        if "horizontal" in element.attrib:
            horizontal = bool(element.attrib['horizontal'])

        color = WHITE
        if "color" in element.attrib:
            color = element.attrib['color']
        return Select(
            options=options,
            size=int(element.attrib['size']),
            font_name=element.attrib['font_name'],
            x=int(element.attrib['x']),
            y=int(element.attrib['y']),
            offset=int(element.attrib['offset']),
            text_align=text_align,
            color=color,
            horizontal=horizontal
        )
    
    def create_panel(self, element):
        background_color=None
        if "background_color" in element.attrib:
            background_color = self.text_to_color(element.attrib['background_color'])
        return Panel(
            background_color = background_color,
            x=int(element.attrib['x']),
            y=int(element.attrib['y']),
            width=int(element.attrib['width']),
            height=int(element.attrib['height'])
            
        )

    def text_to_color(self,color):
        array = color.split(",")
        return (int(array[0]),int(array[1]),int(array[2]))
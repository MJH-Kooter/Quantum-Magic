import pygame as pg
import constants as c

class SpriteSheet():

    def __init__(self,image):
        self.sheet = image

    def get_image(self, frame, width, height):
        image = pg.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame*width),0,width,height))
        image.set_colorkey((0,0,0))
        return image

class Object():

    def get_image(self, frame, width, height):
        image = pg.Surface((width, height)).convert_alpha()
        image.blit(self.img, (0,0), ((frame*width),0,width,height))
        return image

    def __init__(self,image,id,gate,data):
        self.img = image
        self.id = id
        self.gate = gate
        self.data = data


class Line():

    def __init__(self,line_id,length):
        empty_obj = Object("","","","")
        self.line_id = line_id
        self.length = length
        self.circuit = list()
        for i in range(length):
            self.circuit.insert(i,empty_obj)

    def add_obj(self, incr,image, obj_id, gate, data):
        new_obj = Object(image, obj_id, gate, data)
        self.circuit[incr]=new_obj

    def rem_obj(self, incr):
        self.circuit[incr]=Object("","","","")

        
    

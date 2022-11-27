'''
@author Pedro Pablo Arriola Jimenez (20188)
@filename bmp_renderer.py
@description: BMP file renderer that works using concepts related
to framebuffers and low level code such as bytes.
'''

from random import randint
import struct


# Functions that will be needed to create low level structures.
def char(c):
    # 1 byte character
    c = struct.pack('=c', c.encode('ascii'))
    return c

def word(w):
    # 2 bytes character
    w = struct.pack('=h', w)   
    return w  


def dword(dw):
    # 4 bytes character
    dw = struct.pack('=l', dw)   
    return dw  

def color_select(r, g, b):
   return bytes([b, g, r]) 

# Class of type Render that will nest every function that will create a BMP file from scratch. 

class Render(object):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.pixels = 0
        self.clearColor = color_select(0, 0, 0)
        self.viewport_x = 0 
        self.viewport_y = 0
        self.viewport_height = 0
        self.viewport_width = 0
        self.texture = None
        
        # Constants for BMP files
        self.FILE_SIZE = (54)
        self.PIXEL_COUNT = 3
        self.PLANE = 1
        self.BITS_PER_PIXEL = 24
        self.DIB_HEADER = 40
        
    '''
    --- SR1: POINTS
  
    '''      
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        
        self.framebuffer = [[self.clearColor for x in range(self.width)]
                       for y in range(self.height)]
        
    def glViewPort(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_width = width
        self.viewport_height = height
    
    def glColor(self, r, g, b):
        self.clearColor = color_select(r, g, b)
    
    def glClearColor(self, r, g, b):
        self.clearColor = color_select(r, g, b)
        for x in range(self.viewport_x, self.viewport_x + self.viewport_width + 1):
            for y in range(self.viewport_y, self.viewport_y + self.viewport_height + 1):
                self.glPoint(x, y)
        
    def glVertex(self, x, y):
        if -1 <= x <= 1:
            if -1 <= y <= 1:
                pass
            else:
                y = 0
        else:
            x = 0
        self.pixel_X = int((x + 1) * self.viewport_width * 1/2 ) + self.viewport_x
        self.pixel_Y = int((y + 1) * self.viewport_height * 1/2) + self.viewport_y
        self.glPoint(self.pixel_X,self.pixel_Y)
        
    def glClear(self):
        for x in range(self.viewport_x, self.viewport_x + self.viewport_width + 1):
            for y in range(self.viewport_y, self.viewport_y + self.viewport_height + 1):
                self.glPoint(x, y)
        
    def glPoint(self, x, y):
        if(0 < x < self.width and 0 < y < self.height):
            self.framebuffer[y][x] = self.clearColor
    
    
        
    '''
    --- SR2: LINES
    
    '''
    
    # Line drawing function which implements Bresenham's algorithm
    def glLine(self, x0, y0, x1, y1):
    

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if  x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        
        threshold = dx
        
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x)
            else:
                self.glPoint(x, y)

            offset += dy * 2
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += dx * 2
        
    
    def glFinish(self, filename):
        with open(filename, 'bw') as file:
            # Header
            file.write(char('B'))
            file.write(char('M'))

            # file size
            file.write(dword(self.FILE_SIZE + self.height * self.width * self.PIXEL_COUNT))
            file.write(word(0))
            file.write(word(0))
            file.write(dword(self.FILE_SIZE))

            # Info Header
            file.write(dword(self.DIB_HEADER))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(self.PLANE))
            file.write(word(self.BITS_PER_PIXEL))
            file.write(dword(0))
            file.write(dword(self.width * self.height * self.PIXEL_COUNT))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
    
            # Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.framebuffer[y][x])
            file.close()
            
    def draw_poly(self, polygon):
        for i in range(len(polygon)):
            self.glPoint(polygon[i][0], polygon[i][1])
            if i < len(polygon) - 1:
                self.glLine(polygon[i][0], polygon[i][1], polygon[i+1][0], polygon[i + 1][1])
            else:
                self.glLine(polygon[i][0], polygon[i][1], polygon[0][0], polygon[0][1])
    
    def fill_poly(self, polygon):
        x_pos = []
        y_pos = []
        x_m = 0
        y_m = 0

        for i in range(len(polygon)):
            x_pos.append(polygon[i][0])
            y_pos.append(polygon[i][1])

        for i in x_pos:
            x_m += i
        x_m = int(x_m / len(x_pos))
        
        for i in y_pos:
            y_m += i
        y_m = int(y_m / len(y_pos))
        
        distance = int(( (x_pos[0] - x_m) ** 2 + (y_pos[0] - y_m) ** 2 ) ** (1 / 2))
        
        for i in range(distance + 1):
            for j in range(len(x_pos)):
                #revisa la posicion en x
                if x_pos[j] < x_m:
                    x_pos[j] += 1
                elif x_pos[j] == x_m:
                    pass
                else:
                    x_pos[j] -= 1
                #revisa la posicion en y
                if y_pos[j] < y_m:
                    y_pos[j] += 1
                elif y_pos[j] == y_m:
                    pass 
                else:
                    y_pos[j] -= 1
            
            # Revisa el largo del poligon y compara para comenzar a dibujar lineas que hagan el rellenado
            for i in range(len(polygon)):
                
                if i < len(polygon) - 1:
                    self.glLine(x_pos[i], y_pos[i], x_pos[i + 1], y_pos[i + 1])
                    
                    self.glLine(x_pos[i], y_pos[i], x_pos[i + 1], y_pos[i + 1] + 1)
                    self.glLine(x_pos[i], y_pos[i], x_pos[i + 1] + 1,y_pos[i + 1])
                    self.glLine(x_pos[i], y_pos[i], x_pos[i + 1] - 1,y_pos[i + 1])
                    self.glLine(x_pos[i], y_pos[i], x_pos[i + 1], y_pos[i + 1] - 1)
                    
                    self.glLine(x_pos[i], y_pos[i] + 1, x_pos[i + 1], y_pos[i + 1])
                    self.glLine(x_pos[i], y_pos[i] - 1, x_pos[i + 1], y_pos[i + 1])
                    self.glLine(x_pos[i] + 1,y_pos[i], x_pos[i+1], y_pos[i + 1])
                    self.glLine(x_pos[i] - 1,y_pos[i], x_pos[i+1], y_pos[i + 1])
                    
                    self.glLine(x_pos[i],y_pos[i]+1,x_pos[i+1],y_pos[i+1]+1)
                    self.glLine(x_pos[i],y_pos[i]-1,x_pos[i+1],y_pos[i+1]+1)
                    self.glLine(x_pos[i]+1,y_pos[i],x_pos[i+1],y_pos[i+1]+1)
                    self.glLine(x_pos[i]-1,y_pos[i],x_pos[i+1],y_pos[i+1]+1)
                    
                    self.glLine(x_pos[i],y_pos[i]+1,x_pos[i+1],y_pos[i+1]-1)
                    self.glLine(x_pos[i],y_pos[i]-1,x_pos[i+1],y_pos[i+1]-1)
                    self.glLine(x_pos[i]+1,y_pos[i],x_pos[i+1],y_pos[i+1]-1)
                    self.glLine(x_pos[i]-1,y_pos[i],x_pos[i+1],y_pos[i+1]-1)
                    
                    self.glLine(x_pos[i],y_pos[i]+1,x_pos[i+1]+1,y_pos[i+1])
                    self.glLine(x_pos[i],y_pos[i]-1,x_pos[i+1]+1,y_pos[i+1])
                    self.glLine(x_pos[i]+1,y_pos[i],x_pos[i+1]+1,y_pos[i+1])
                    self.glLine(x_pos[i]-1,y_pos[i],x_pos[i+1]+1,y_pos[i+1])
                    
                    self.glLine(x_pos[i], y_pos[i] + 1, x_pos[i + 1] - 1, y_pos[i + 1])
                    self.glLine(x_pos[i], y_pos[i] - 1, x_pos[i + 1] - 1, y_pos[i + 1])
                    self.glLine(x_pos[i] + 1, y_pos[i], x_pos[i+1] - 1, y_pos[i + 1])
                    self.glLine(x_pos[i] - 1, y_pos[i], x_pos[i+1] - 1, y_pos[i + 1])

                else:
                    self.glLine(x_pos[i], y_pos[i], x_pos[0], y_pos[0])
                    self.glLine(x_pos[i], y_pos[i], x_pos[0], y_pos[0] + 1)
                    self.glLine(x_pos[i], y_pos[i], x_pos[0] + 1, y_pos[0])
                    self.glLine(x_pos[i], y_pos[i], x_pos[0] - 1,y_pos[0])
                    self.glLine(x_pos[i], y_pos[i], x_pos[0], y_pos[0] - 1)
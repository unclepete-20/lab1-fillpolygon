from bmp_renderer import Render

frame = Render()

'''
LAB 1 FILLING POLYGONS

'''

frame.glCreateWindow(800, 800)

polygon1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330),
        (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]

polygon2 = [(321, 335), (288, 286), (339, 251), (374, 302)]

polygon3 = [(377, 249), (411, 197), (436, 249)]

polygon4 = [(413, 177), (448, 159), (502, 88),
            (553, 53), (535, 36), (676, 37), (660, 52),
            (750, 145), (761, 179), (672, 192), (659, 214),
            (615, 214), (632, 230), (580, 230),
            (597, 215), (552, 214), (517, 144), (466, 180)]

polygon5 = [(682, 175), (708, 120), (735, 148), (739, 170)]

# Draws and fills a STAR
frame.glColor(255, 255, 0)
frame.draw_poly(polygon1)
frame.fill_poly(polygon1)

# Draws and fills a SQUARE
frame.glColor(0, 255, 0)
frame.draw_poly(polygon2)
frame.fill_poly(polygon2)

# Draws and fills a TRIANGLE
frame.glColor(0, 0, 255)
frame.draw_poly(polygon3)
frame.fill_poly(polygon3)

# Draws and fills a KETTLE
frame.glColor(192, 192, 192)
frame.draw_poly(polygon4)
frame.fill_poly(polygon4)

# Draws and fills a HOLE INSIDE THE KETTLE
frame.glColor(0, 0, 0)
frame.draw_poly(polygon5)
frame.fill_poly(polygon5)

# LAB 1 FINISHED
frame.glFinish('lab1.bmp')
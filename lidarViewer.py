'''
@author: ryu_cz

Simple lidar point cloud data viewer
'''
from pyglet.gl import *
from pyglet.window import key, mouse
from primitives.vec3 import Vec3
from primitives.controls import Camera
import struct
import copy
        
try:
    # Try and create a window with extra setting
    config = Config(double_buffer=True,)
    window = pyglet.window.Window(resizable=True, config=config, vsync=True)
except pyglet.window.NoSuchConfigException:
    window = pyglet.window.Window(resizable=True)
        
        
class Keyboard(object):
    "Keyboard state holder"
    TIME_STEP = 0.02
    def __init__(self):
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False
        self.PAGEDOWN = False
        self.PAGEUP = False
        self.W = False
        self.A = False
        self.S = False
        self.D = False
        self.moveSize = 0.2
    def scheduleCallback(self, dt, *args, **kwargs):
        """ Shedulable task to bind movement to time 
        @param dt: time, in seconds, since the last clock tick"""
        distance = self.moveSize * dt/self.TIME_STEP 
        if self.UP or self.W:
            cam.move(0,distance)
        if self.RIGHT or self.D:
            cam.move(distance,0)
        if self.LEFT or self.A:
            cam.move(-distance,0)
        if self.DOWN or self.S:
            cam.move(0,-distance)  
        if self.PAGEUP:
            cam.up(distance)  
        if self.PAGEDOWN:
            cam.up(-distance)          
      
def parseLidarData(file_path):
    """Reads and parse binary file into points
    @param file_path: adrress of binary lidar data file
    """
    file_lid = open(file_path, 'rb')
    byte_f = file_lid.read(4)
    lidar_points=[]
    minimal = Vec3( float("inf") ,float("inf")  ,float("inf") )
    maximal = Vec3( float("-inf") ,float("-inf")  ,float("-inf") )
    x = 0.0
    y = 0.0
    z = 0.0
    print "Reading file"
    while byte_f:
        x = struct.unpack('f', byte_f)[0]
        y, z =  struct.unpack('f'*2, file_lid.read(8))
        file_lid.read(4)
        byte_f = file_lid.read(4)
        minimal.x = min(minimal.x, x)
        minimal.y = min(minimal.y, y)
        minimal.z = min(minimal.z, z)
        maximal.x = max(maximal.x, x)
        maximal.y = max(maximal.y, y)
        maximal.z = max(maximal.z, z)
        lidar_points.append(x)
        lidar_points.append(y)
        lidar_points.append(z)  
    file_lid.close()
    print "Info:"
    print "\tmin", minimal
    print "\tmax", maximal
    print "\tdelta", maximal-minimal
    print "lidar file read(",len(lidar_points),"points )"
    print "proccesing data..."
    drawlist = copy.copy(lidar_points)
    for i in xrange(len(drawlist)/3):
        drawlist[3*i] -=  minimal.x
        drawlist[3*i+1] -=  minimal.y
        drawlist[3*i+2] -=  minimal.z
        if( i*3 % 100000 == 0):
            print i * 3 ,"/", len(lidar_points)
    print len(lidar_points),"/", len(lidar_points),"..finished"
    return drawlist


@window.event
def on_resize(width, height):
    # Override the default on_resize handler to create a 3D projection
    cam.focus(width, height)
    return pyglet.event.EVENT_HANDLED

@window.event
def on_key_press(symbol, modifiers):
    keyboard.RIGHT |= symbol == key.RIGHT
    keyboard.LEFT |= symbol == key.LEFT
    keyboard.UP |= symbol == key.UP
    keyboard.DOWN |= symbol == key.DOWN
    keyboard.PAGEUP |= symbol == key.PAGEUP
    keyboard.PAGEDOWN |= symbol == key.PAGEDOWN
    keyboard.W |= symbol == key.W
    keyboard.A |= symbol == key.A
    keyboard.S |= symbol == key.S
    keyboard.D |= symbol == key.D
    if symbol == key.R:
        cam.reset()

@window.event
def on_key_release(symbol, modifiers):
    keyboard.RIGHT &= not symbol == key.RIGHT
    keyboard.LEFT &= not symbol == key.LEFT
    keyboard.UP &= not symbol == key.UP
    keyboard.DOWN &= not symbol == key.DOWN
    keyboard.PAGEUP &= not symbol == key.PAGEUP
    keyboard.PAGEDOWN &= not symbol == key.PAGEDOWN
    keyboard.W &= not symbol == key.W
    keyboard.A &= not symbol == key.A
    keyboard.S &= not symbol == key.S
    keyboard.D &= not symbol == key.D
    
@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    cam.zoom(scroll_x, scroll_y)
    
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & mouse.LEFT:
        cam.rotate(dx, dy)
    
@window.event
def on_draw():
        # clear canvas
        window.clear()#glClear(GL_COLOR_BUFFER_BIT)py
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glPushMatrix();
        glMultMatrixf(cam.modelview);
        """Light and other seting"""
        glPopMatrix();
        
        cam.zoomAndRotate()
        cam.pan()
        
        glPolygonMode(GL_BACK, GL_LINE)
        vertex_list.draw(pyglet.gl.GL_POINTS)
               

######################main############################
cam = Camera(x=250, y=250, z=30)
keyboard = Keyboard()

#schedule keybard move task
pyglet.clock.schedule_interval( keyboard.scheduleCallback, keyboard.TIME_STEP)

file_path = "/home/ryu_cz/gis_lidar/pt000023.bin"
points = parseLidarData(file_path)
colors = [ 200 for _ in xrange(len(points))]
points = tuple(points)
colors = tuple(colors)

vertex_list = pyglet.graphics.vertex_list(len(points)/3,
    ('v3f', points),
    ('c3B', colors))
        
pyglet.app.run()

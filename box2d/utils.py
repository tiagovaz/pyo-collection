# pyglet.utils.py
# www.akeric.com - 2011-03-17
# utils to make pyglet easier to work with, help my learning of it.

import pyglet
from pyglet.gl import *

def screenshot(name='screenshot'):
    """
    Take a screenshot

    Parameters:
    name : string : Default 'screenshot'.  Name of the saved image.  Will
        always save as .png
    """
    # Get the 'the back-left color buffer'
    pyglet.image.get_buffer_manager().get_color_buffer().save('%s.png'%name)

def getPixelValue(x, y):
    """
    Return the RGBA 0-255 color value of the pixel at the x,y position.
    """
    # BufferManager, ColorBufferImage
    color_buffer = pyglet.image.get_buffer_manager().get_color_buffer()
    # AbstractImage, ImageData, sequece of bytes
    pix = color_buffer.get_region(x,y,1,1).get_image_data().get_data("RGBA", 4)
    return pix[0], pix[1], pix[2], pix[3]

def drawPoint(x, y, color):
    """
    Based on the (r,g,b) color passed in, draw a point at the given x,y coord.
    """
    pyglet.graphics.draw(1, GL_POINTS,
                         ('v2i', (x, y)),
                         ('c3B', (color[0], color[1], color[2]) ) )

def getSmoothConfig():
    """
    Sets up a configuration that allows of smoothing\antialiasing.
    The return of this is passed to the config parameter of the created window.
    """
    try:
        # Try and create a window config with multisampling (antialiasing)
        config = Config(sample_buffers=1, samples=4,
                        depth_size=16, double_buffer=True)
    except pyglet.window.NoSuchConfigException:
        print "Smooth contex could not be aquiried."
        config = None
    return config

def printEvents(window):
    """
    Debug tool that will print the events to the console.

    window is an instance of a Window object receiving the events.
    """
    window.push_handlers(pyglet.window.event.WindowEventLogger())

def playMusic(music):
    """
    Simple wrapper to play a music (mp3) file.

    music : music file relative to application.
    """
    music = pyglet.resource.media(music)
    music.play()

def setBackgroundColor(color):
    """
    Color is a list of four values, [r,g,b,a], each from 0 -> 1
    """
    pyglet.gl.glClearColor(*color)

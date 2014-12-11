# primitivesTest01.py
# www.akeric.com - 2011-03-17

import sys
import random
import pyglet
from pyglet.gl import *
import primitives # module discussed above
import utils # module from above

FPS = 60
smoothConfig = utils.getSmoothConfig()

class PrimWin(pyglet.window.Window):

    def __init__(self):
        super(PrimWin, self).__init__(fullscreen=False, caption='Primitives Test!', config=smoothConfig)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.p = primitives.Pixel(10,10)
        self.c = primitives.Circle(200,100,width=100,color=(0.,.9,0.,1.))
        self.a = primitives.Arc(150,150,radius=100,color=(1.,0.,0.,1.),sweep=90,style=GLU_FILL)
        self.P = primitives.Polygon([(0, 0), (50, 200), (80, 200),(60,100),(100,5)],color=(.3,0.2,0.5,.7))
        self.l = primitives.Line((10,299),(100,25),stroke=8,color=(0,0.,1.,1.))
        # Setup debug framerate display:
        self.fps_display = pyglet.clock.ClockDisplay()
        # Schedule the update of this window, so it will advance in time at the
        # defined framerate.  If we don't, the window will only update on events
        # like mouse motion.
        pyglet.clock.schedule_interval(self.update, 1.0/FPS)

    def on_draw(self):
        # Window event
        self.clear()
        self.c.render()
        self.p.render()
        self.a.render()
        self.P.render()
        self.l.render()
        self.fps_display.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        # Window event
        self.c.x = x
        self.c.y = y

    def update(self, dt):
        # Scheduled event
        self.a.rotation+=1
        self.c.color = [random.random() for i in xrange(3)]+[1]

if __name__ == '__main__':
    PrimWin()
    sys.exit(pyglet.app.run())

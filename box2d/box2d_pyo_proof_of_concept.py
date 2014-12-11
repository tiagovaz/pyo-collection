import pyglet
from pyglet import gl
from Box2D import (
    b2Vec2, b2PolygonDef, b2World,
    b2BodyDef, b2AABB, b2MouseJointDef, b2CircleDef
)

from audio import *

s = Server(audio='jack').boot()
s.start()


FPS = 60

W = 100
H = 72

SCALE = 0.1    # World units - screen units conversion factor

world = None  # let's keep world as a global for now

# List of blocks that have been created
blocks = []

def screen_to_world(pos):
    sx, sy = pos
    return b2Vec2(sx * SCALE, sy * SCALE)


def world_to_screen(pos):
    wx, wy = pos
    return (wx / SCALE, wy / SCALE)


def sprite_scale(self):
    return 0.1 / SCALE

W = 100
H = 72

def setup_world():
    world_bounds = b2AABB()
    world_bounds.lowerBound = (-200, -1000)
    world_bounds.upperBound = (200, 200)
    world = b2World(
        world_bounds,
        b2Vec2(0, -40.0),  # Gravity vector
        True  # Use "sleep" optimisation
    )

    wallsdef = b2BodyDef()
    walls = world.CreateBody(wallsdef)
    walls.userData = 'Blocks'

    WALLS = [
        (W / 2, 1, (W / 2, -1), 0),  # floor
        (W / 2, 1, (W / 2, H + 1), 0),  # ceiling
        (1, 600, (-1, -500), 0),  # left wall
        (1, 600, (W + 1, -500), 0),  # right wall
    ]

    for wall in WALLS:
        shape = b2PolygonDef()
        shape.SetAsBox(*wall)
        walls.CreateShape(shape)

    return world

class Block:
    def __init__(self, pos, audio_mod):

        self.BOX_SIZE = 2
        self.POINTS = [
            (-self.BOX_SIZE, self.BOX_SIZE),
            (self.BOX_SIZE, self.BOX_SIZE),
            (self.BOX_SIZE, -self.BOX_SIZE),
            (-self.BOX_SIZE, -self.BOX_SIZE),
        ]

        self.audio = audio_mod

        bodydef = b2BodyDef()
        bodydef.position = pos
        self.body = world.CreateBody(bodydef)
        shape = b2PolygonDef()
        shape.SetAsBox(self.BOX_SIZE, self.BOX_SIZE, (0, 0), 0)
        shape.density = 0.1
        shape.restitution = 0.2
        shape.friction = 0.5

        self.body.CreateShape(shape)
        self.body.SetMassFromShapes()

    def set_audio_freq(self):
        self.audio.setfreq([i+self.body.linearVelocity.y for i in self.audio.freq])

    def get_body(self):
        return self.body

    def get_position(self):
        return self.body.position

    def draw(self):
        transformed = [world_to_screen(self.body.GetWorldPoint(p)) for p in self.POINTS]
        gl.glColor3f(1.0, 0.1, 0)
        gl.glBegin(gl.GL_LINE_LOOP)
        for p in transformed:
            gl.glVertex2f(*p)
        gl.glEnd()


def on_mouse_press(x, y, button, modifiers):
    p = screen_to_world((x, y))
    a = BG()
    b = Block(p, a)
    blocks.append(b)


def update(dt):
    world.Step(1.0 / FPS, 10, 8)
    for block in blocks:
        print block.body.linearVelocity.x
        block.set_audio_freq()
    #   if block.get_body().isSleeping is True:
    #       block.audio.tail()
        #else:
        #    block.audio.play()

def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()

    for block in blocks:
        block.draw()

if __name__ == '__main__':
    world = setup_world()
    window = pyglet.window.Window(
        width=int(W / SCALE),
        height=int(H / SCALE)
    )
    window.event(on_mouse_press)
    window.event(on_draw)

    pyglet.clock.schedule(update)

    pyglet.app.run()


#### body parameters to explore ####

#b2Body(
#       allowSleep        = True,
#       angle             = 4.71391630173,
#       angularDamping    = 0.0,
#       angularVelocity   = 0.0,
#       fixedRotation     = False,
#       isBullet          = False,
#       isSleeping        = True,
#       linearDamping     = 0.0,
#       linearVelocity    = b2Vec2(0,0),
#       massData          = b2MassData(
#       I      = 4.26666688919,
#       center = b2Vec2(0,0),
#       mass   = 1.60000002384),
#       position          = b2Vec2(36.4606,13.9873),
#       userData          = None,
#       GetInertia()      = 4.26666688919,
#       GetLocalCenter()  = b2Vec2(0,0),
#       GetMass()         = 1.60000002384,
#       GetWorldCenter()  = b2Vec2(36.4606,13.9873),
#       GetXForm()        = b2XForm(
#       R        = b2Mat22(
#       col1       = b2Vec2(0.00152732,-0.999999),
#       col2       = b2Vec2(0.999999,0.00152732),
#       GetAngle() = -1.56926906109),
#       position = b2Vec2(36.4606,13.9873)),
#       IsBullet()        = False,
#       IsDynamic()       = True,
#       IsFrozen()        = False,
#       IsFixedRotation() = False,
#       IsSleeping()      = True,
#       IsStatic()        = False)
#

import pyglet
from pyglet import gl

from Box2D import (
    b2Vec2, b2PolygonDef, b2World,
    b2BodyDef, b2AABB, b2MouseJointDef,
    b2CircleDef
)
import primitives
import random
import mapper

# TODO:
# - draw ball - OK!
# - add objects from keyboard - OK!
# - connect to libmapper - OK!
# - draw lines

#FIXME:
# - lock from device creation

# GLOBALS
FPS = 60

W = 100
H = 72

SCALE = 0.1    # World units - screen units conversion factor

TEX_COORDS = [
    (0, 1),
    (1, 1),
    (1, 0),
    (-0, 0),
]

class Main:
    def __init__(self):
        world_bounds = b2AABB()
        world_bounds.lowerBound = (-200, -1000)
        world_bounds.upperBound = (200, 200)
        self.world = b2World(
            world_bounds,
            b2Vec2(0, -0),  # Gravity vector
            True  # Use "sleep" optimisation
        )

        # blocks, balls etc
        self.objs = []
        wallsdef = b2BodyDef()
        walls = self.world.CreateBody(wallsdef)
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

        self.mouse_joint = None

    def screen_to_world(self, pos):
        sx, sy = pos
        return b2Vec2(sx * SCALE, sy * SCALE)


    def world_to_screen(self, pos):
        wx, wy = pos
        return (wx / SCALE, wy / SCALE)

    def sprite_scale(self):
        return 0.1 / SCALE

    def on_mouse_press(self, x, y, button, modifiers):
        if self.mouse_joint:
            return

        p = surface.screen_to_world((x, y))

        # Create a mouse joint on the selected body (assuming it's dynamic)

        # Make a small box.
        aabb = b2AABB()
        aabb.lowerBound = p - (0.001, 0.001)
        aabb.upperBound = p + (0.001, 0.001)

        # Query the world for overlapping shapes.
        body = None
        k_maxCount = 10  # maximum amount of shapes to return

        (count, shapes) = world.Query(aabb, k_maxCount)
        for shape in shapes:
            shapeBody = shape.GetBody()
            if not shapeBody.IsStatic() and shapeBody.GetMass() > 0.0:
                if shape.TestPoint(shapeBody.GetXForm(), p):  # is it inside?
                    body = shapeBody
                    break

        if body:
            # A body was selected, create the mouse joint
            md = b2MouseJointDef()
            md.body1 = world.GetGroundBody()
            md.body2 = body
            md.target = p
            md.maxForce = 100000.0
            self.mouse_joint = world.CreateJoint(md).getAsType()
            body.WakeUp()

    def on_mouse_release(self, x, y, button, modifiers):
        if self.mouse_joint:
            world.DestroyJoint(self.mouse_joint)
            self.mouse_joint = None

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.mouse_joint:
            p = surface.screen_to_world((x, y))
            self.mouse_joint.SetTarget(p)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key._1:
            self.objs.append(Block(random.uniform(1,5)))
        if symbol == pyglet.window.key._2:
            self.objs.append(Ball(random.uniform(1,5)))
        #FIXME: doesn't update current objs
        if symbol == pyglet.window.key.G:
            self.set_gravity((0,-40))

    def set_gravity(self, gravity):
        # gravity is a tuple
        self.world.SetGravity(b2Vec2(gravity))

    def on_draw(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        for obj in self.objs:
            obj.draw()

    def update(self, dt):
        self.world.Step(1.0 / FPS, 20, 16)
        for obj in self.objs:
            obj.poll()

class Block():
    def __init__(self, box_size):
        self.points = [
            (-box_size, box_size),
            (box_size, box_size),
            (box_size, -box_size),
            (-box_size, -box_size)
        ]

        bodydef = b2BodyDef()
        bodydef.position = (W / 2, H / 2)
        self.body = world.CreateBody(bodydef)
        shape = b2PolygonDef()
        shape.SetAsBox(box_size, box_size, (0, 0), 0)
        shape.density = 0.4
        shape.restitution = 0.5
        shape.friction = 0.5

        self.body.CreateShape(shape)
        self.body.SetMassFromShapes()
        surface.objs.append(self)
        self.r, self.g, self.b = random.random(), random.random(), random.random()

        self.map_block = mapper.device("Block")
        #self.av = self.map_angularVelocity.add_output(abs(self.body.angularVelocity), 1, 'f', None, 0, 10)
        self.av = self.map_block.add_output('/angularVelocity', 1, 'f', None, 0, 15)
        self.angle = self.map_block.add_output('/angle', 1, 'f', None, 0, 300)
        self.lvx = self.map_block.add_output('/linearVelocity.x', 1, 'f', None, 0, 50)
        self.lvy = self.map_block.add_output('/linearVelocity.y', 1, 'f', None, 0, 50)
        self.px = self.map_block.add_output('/position.x', 1, 'f', None, 2, 80)
        self.py = self.map_block.add_output('/position.y', 1, 'f', None, 2, 60)

    def draw(self):
        transformed = [surface.world_to_screen(self.body.GetWorldPoint(p)) for p in self.points]
        gl.glColor3f(self.r,self.g,self.b)
        gl.glBegin(gl.GL_QUADS)
        for p in transformed:
            gl.glVertex2f(*p)
        gl.glEnd()

    def poll(self):
#        print self.body
        self.av.update(abs(self.body.angularVelocity))
        self.angle.update(abs(self.body.angle))
        self.lvx.update(abs(self.body.linearVelocity.x))
        self.lvy.update(abs(self.body.linearVelocity.y))
        self.px.update(self.body.position.x)
        self.py.update(self.body.position.y)
        self.map_block.poll(0)

class Ball():
    def __init__(self, box_size):
        self.box_size = box_size
        self.points = [
            (-self.box_size, self.box_size),
            (self.box_size, self.box_size),
            (self.box_size, -self.box_size),
            (-self.box_size, -self.box_size)
        ]
        bodydef = b2BodyDef()
        bodydef.position = b2Vec2(W * 0.33, H * 0.7)
        self.body = world.CreateBody(bodydef)
        self.cdef = b2CircleDef()
        self.cdef.radius = self.box_size
        self.cdef.density = 0.4
        self.cdef.restitution = 0.7
        self.cdef.friction = 0.2
        self.body.CreateShape(self.cdef)
        self.body.SetMassFromShapes()
        surface.objs.append(self)
        self.r, self.g, self.b = random.random(), random.random(), random.random()

    def draw(self):
        center = ((-self.box_size + self.box_size) / 2, (self.box_size + -self.box_size) / 2)
        m = surface.world_to_screen(self.body.GetWorldPoint(center))
        self.c = primitives.Circle(m[0],m[1],width=self.cdef.radius*20,color=(self.r,self.g,self.b,1.),stroke=0)
#        self.c.style = gl.GLU_POINT
        self.c.render()

    def poll(self):
        pass
#        print self.body

surface = Main()
world = surface.world

if __name__ == '__main__':
    config = pyglet.gl.Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True)
    window = pyglet.window.Window(
        width=int(W / SCALE),
        height=int(H / SCALE),
        config=config,
        resizable=True
    )
    window.event(surface.on_mouse_press)
    window.event(surface.on_mouse_release)
    window.event(surface.on_mouse_drag)
    window.event(surface.on_draw)
    window.event(surface.on_key_press)

    pyglet.clock.schedule(surface.update)
    pyglet.app.run()

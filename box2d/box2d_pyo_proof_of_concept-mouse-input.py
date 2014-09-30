import pyglet
from pyglet import gl
from Box2D import (
    b2Vec2, b2PolygonDef, b2World,
    b2BodyDef, b2AABB, b2MouseJointDef
)


# GLOBALS
FPS = 60

W = 100
H = 72

SCALE = 0.1    # World units - screen units conversion factor


class Main:
    def __init__(self):
        world_bounds = b2AABB()
        world_bounds.lowerBound = (-200, -1000)
        world_bounds.upperBound = (200, 200)
        self.world = b2World(
            world_bounds,
            b2Vec2(0, -30),  # Gravity vector
            True  # Use "sleep" optimisation
        )

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
            print "Block clicked"
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

    def on_draw(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        transformed = [surface.world_to_screen(block_body.GetWorldPoint(p)) for p in block.points]
        gl.glColor3f(1.0, 0.1, 0)
        gl.glBegin(gl.GL_QUADS)
        for p in transformed:
            gl.glVertex2f(*p)
        gl.glEnd()

    def update(self, dt):
        self.world.Step(1.0 / FPS, 20, 16)

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
        shape.density = 0.1
        shape.restitution = 0.2
        shape.friction = 0.5

        self.body.CreateShape(shape)
        self.body.SetMassFromShapes()


surface = Main()
world = surface.world

block = Block(2)
block_body = block.body



if __name__ == '__main__':
    window = pyglet.window.Window(
        width=int(W / SCALE),
        height=int(H / SCALE)
    )
    window.event(surface.on_mouse_press)
    window.event(surface.on_mouse_release)
    window.event(surface.on_mouse_drag)
    window.event(surface.on_draw)

    pyglet.clock.schedule(surface.update)
    pyglet.app.run()

import pyglet
from pyglet import gl
from Box2D import (
    b2Vec2, b2PolygonDef, b2World,
    b2BodyDef, b2AABB, b2MouseJointDef,
    b2CircleDef
)

FPS = 60

W = 100
H = 72

SCALE = 0.1    # World units - screen units conversion factor

world = None  # let's keep world as a global for now
mouse_joint = None


def screen_to_world(pos):
    sx, sy = pos
    return b2Vec2(sx * SCALE, sy * SCALE)


def world_to_screen(pos):
    wx, wy = pos
    return (wx / SCALE, wy / SCALE)


def sprite_scale(self):
    return 0.1 / SCALE


def setup_world():
    world_bounds = b2AABB()
    world_bounds.lowerBound = (-200, -1000)
    world_bounds.upperBound = (200, 200)
    world = b2World(
        world_bounds,
        b2Vec2(0, -30),  # Gravity vector
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


BOX_SIZE = 4
POINTS = [
    (-BOX_SIZE, BOX_SIZE),
    (BOX_SIZE, BOX_SIZE),
    (BOX_SIZE, -BOX_SIZE),
    (-BOX_SIZE, -BOX_SIZE),
]
TEX_COORDS = [
    (0, 1),
    (1, 1),
    (1, 0),
    (-0, 0),
]


def setup_bear():
    bodydef = b2BodyDef()
    bodydef.position = (W * 0.66, H * 0.7)
    body = world.CreateBody(bodydef)
    shape = b2PolygonDef()
    shape.SetAsBox(BOX_SIZE, BOX_SIZE, (0, 0), 0)
    shape.density = 0.3
    shape.restitution = 0.5
    shape.friction = 0.5

    body.CreateShape(shape)
    body.SetMassFromShapes()
    return body


def setup_ball():
    bodydef = b2BodyDef()
    bodydef.position = b2Vec2(W * 0.33, H * 0.7)
    body = world.CreateBody(bodydef)
    cdef = b2CircleDef()
    cdef.radius = BOX_SIZE
    cdef.density = 0.01
    cdef.restitution = 0.3
    cdef.friction = 0.3
    body.CreateShape(cdef)
    body.SetMassFromShapes()
    return body


def on_mouse_press(x, y, button, modifiers):
    global mouse_joint
    if mouse_joint:
        return

    p = screen_to_world((x, y))

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
        mouse_joint = world.CreateJoint(md).getAsType()
        body.WakeUp()


def on_mouse_release(x, y, button, modifiers):
    global mouse_joint
    if mouse_joint:
        world.DestroyJoint(mouse_joint)
        mouse_joint = None


def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global mouse_joint
    if mouse_joint:
        p = screen_to_world((x, y))
        mouse_joint.SetTarget(p)


def update(dt):
    world.Step(1.0 / FPS, 20, 16)
    ball.ApplyForce(b2Vec2(0, 5), ball.position)


bear_tex = pyglet.image.load('textures/bear-cube.png').get_mipmapped_texture()
ball_tex = pyglet.image.load('textures/beach-ball.png').get_mipmapped_texture()


def draw_obj(body, tex):
    gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP)
    gl.glBindTexture(gl.GL_TEXTURE_2D, tex.id)
    transformed = [world_to_screen(body.GetWorldPoint(p)) for p in POINTS]
    gl.glBegin(gl.GL_QUADS)
    for p, tc in zip(transformed, TEX_COORDS):
        gl.glTexCoord2f(*tc)
        gl.glVertex2f(*p)
    gl.glEnd()


def on_draw():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()

    draw_obj(bear, bear_tex)
    draw_obj(ball, ball_tex)


if __name__ == '__main__':
    world = setup_world()
    bear = setup_bear()
    ball = setup_ball()
    window = pyglet.window.Window(
        width=int(W / SCALE),
        height=int(H / SCALE)
    )
    window.event(on_mouse_press)
    window.event(on_mouse_release)
    window.event(on_mouse_drag)
    window.event(on_draw)

    pyglet.clock.schedule(update)
    pyglet.app.run()

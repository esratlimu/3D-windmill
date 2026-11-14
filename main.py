
import sys
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# ======================================
# GLOBAL SETTINGS
# ======================================

angle = 0.0
speed = 1.0
paused = False
lighting = True
cloud_move = 0.0
camera_index = 0

quadric = None

windmills = [
    (-8, -2),
    (0, -6),
    (8, -2)
]

cameras = [
    (19, 13, 27),
    (0, 12, 29),
    (22, 10, 8),
    (0, 25, 0)
]


# ======================================
# LIGHTING AND MATERIAL
# ======================================

def setup_lighting():

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glLightfv(
        GL_LIGHT0, GL_AMBIENT,
        [0.38, 0.38, 0.38, 1]
    )

    glLightfv(
        GL_LIGHT0, GL_DIFFUSE,
        [1.0, 0.95, 0.82, 1]
    )

    glLightfv(
        GL_LIGHT0, GL_SPECULAR,
        [1, 1, 1, 1]
    )

    glEnable(GL_COLOR_MATERIAL)

    glColorMaterial(
        GL_FRONT_AND_BACK,
        GL_AMBIENT_AND_DIFFUSE
    )

    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)


# ======================================
# SPHERE HELPER
# ======================================

def sphere(x, y, z, sx, sy, sz, color):

    glPushMatrix()

    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)

    glColor3f(*color)

    glutSolidSphere(1, 24, 24)

    glPopMatrix()


# ======================================
# SKY AND SUN
# ======================================

def draw_sky():

    glDisable(GL_LIGHTING)

    # Sun
    sphere(
        12, 15, -20,
        1.7, 1.7, 1.7,
        (1.0, 0.85, 0.15)
    )

    # Clouds
    clouds = [
        (-12, 13, -13),
        (-2, 15, -17),
        (10, 13, -12),
        (18, 15, -18)
    ]

    for x, y, z in clouds:

        x += cloud_move

        if x > 28:
            x -= 56

        sphere(
            x, y, z,
            1.6, 0.65, 0.7,
            (0.98, 0.99, 1.0)
        )

        sphere(
            x + 1.1, y + 0.25, z,
            1.1, 0.85, 0.7,
            (1.0, 1.0, 1.0)
        )

        sphere(
            x - 1.1, y + 0.1, z,
            1.0, 0.65, 0.7,
            (0.95, 0.98, 1.0)
        )

    if lighting:
        glEnable(GL_LIGHTING)


# ======================================
# GREEN LANDSCAPE
# ======================================

def draw_ground():

    glColor3f(0.22, 0.57, 0.20)

    glBegin(GL_QUADS)

    glNormal3f(0, 1, 0)

    glVertex3f(-45, 0, -45)
    glVertex3f(-45, 0, 35)
    glVertex3f(45, 0, 35)
    glVertex3f(45, 0, -45)

    glEnd()


# ======================================
# ROLLING HILLS
# ======================================

def draw_hills():

    hills = [
        (-17, -0.4, -16, 12, 4, 5),
        (0, -0.5, -20, 15, 5, 5),
        (18, -0.5, -15, 12, 4, 5),
        (-24, -0.5, 3, 9, 3, 5),
        (25, -0.5, 7, 10, 3, 6)
    ]

    colors = [
        (0.16, 0.43, 0.16),
        (0.20, 0.50, 0.18),
        (0.13, 0.39, 0.15),
        (0.23, 0.55, 0.20),
        (0.17, 0.46, 0.17)
    ]

    for hill, color in zip(hills, colors):

        x, y, z, sx, sy, sz = hill

        sphere(x, y, z, sx, sy, sz, color)


# ======================================
# CURVED ROAD
# ======================================

def draw_road():

    glDisable(GL_LIGHTING)

    glColor3f(0.48, 0.43, 0.35)

    glBegin(GL_QUAD_STRIP)

    for i in range(101):

        t = i / 100.0

        z = 10 - t * 29

        x = 3.0 * math.sin(t * math.pi * 2)

        glVertex3f(x - 1.0, 0.025, z)
        glVertex3f(x + 1.0, 0.025, z)

    glEnd()

    if lighting:
        glEnable(GL_LIGHTING)


# ======================================
# TREE
# ======================================

def draw_tree(x, z, scale=1.0):

    glPushMatrix()

    glTranslatef(x, 0, z)
    glScalef(scale, scale, scale)

    # Trunk
    glColor3f(0.35, 0.17, 0.07)

    glPushMatrix()

    glRotatef(-90, 1, 0, 0)

    gluCylinder(
        quadric,
        0.22, 0.15,
        2.0,
        20, 20
    )

    glPopMatrix()

    # Leaves
    sphere(
        0, 2.5, 0,
        1.0, 1.1, 1.0,
        (0.04, 0.34, 0.08)
    )

    sphere(
        -0.45, 2.9, 0,
        0.65, 0.75, 0.65,
        (0.08, 0.48, 0.10)
    )

    sphere(
        0.45, 2.9, 0,
        0.65, 0.75, 0.65,
        (0.05, 0.40, 0.07)
    )

    glPopMatrix()


def draw_forest():

    trees = [
        (-13, 0, 1.1),
        (-15, 5, 0.9),
        (-11, 8, 1.2),
        (13, 2, 1.0),
        (15, 7, 1.2),
        (11, 9, 0.9),
        (-6, 12, 0.8),
        (7, 12, 0.8),
        (-20, -5, 1.0),
        (20, -7, 1.0)
    ]

    for x, z, scale in trees:
        draw_tree(x, z, scale)


# ======================================
# FLOWERS
# ======================================

def draw_flowers():

    glDisable(GL_LIGHTING)

    for i in range(90):

        x = math.sin(i * 12.5) * 17
        z = math.cos(i * 7.2) * 12 - 2

        glPointSize(4)

        if i % 3 == 0:
            glColor3f(1, 0.8, 0.15)
        elif i % 3 == 1:
            glColor3f(1, 0.35, 0.55)
        else:
            glColor3f(1, 1, 1)

        glBegin(GL_POINTS)
        glVertex3f(x, 0.06, z)
        glEnd()

    if lighting:
        glEnable(GL_LIGHTING)


# ======================================
# WINDMILL TOWER
# ======================================

def draw_tower():

    glColor3f(0.84, 0.87, 0.91)

    glPushMatrix()

    glRotatef(-90, 1, 0, 0)

    gluCylinder(
        quadric,
        0.48, 0.20,
        7.5,
        32, 32
    )

    glPopMatrix()


# ======================================
# WINDMILL BLADE
# ======================================

def draw_blade():

    points = [
        (-0.20, 0.20),
        (0.20, 0.20),
        (0.34, 1.2),
        (0.28, 2.3),
        (0.16, 3.2),
        (-0.16, 3.2),
        (-0.28, 2.3),
        (-0.34, 1.2)
    ]

    thickness = 0.10

    # Front face
    glColor3f(0.92, 0.95, 0.98)

    glBegin(GL_POLYGON)

    glNormal3f(0, 0, 1)

    for x, y in points:
        glVertex3f(x, y, thickness)

    glEnd()

    # Back face
    glBegin(GL_POLYGON)

    glNormal3f(0, 0, -1)

    for x, y in reversed(points):
        glVertex3f(x, y, -thickness)

    glEnd()

    # Side faces
    glColor3f(0.58, 0.65, 0.72)

    glBegin(GL_QUADS)

    for i in range(len(points)):

        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]

        glVertex3f(x1, y1, thickness)
        glVertex3f(x2, y2, thickness)
        glVertex3f(x2, y2, -thickness)
        glVertex3f(x1, y1, -thickness)

    glEnd()


# ======================================
# WINDMILL HUB
# ======================================

def draw_hub():

    glColor3f(0.25, 0.29, 0.35)

    glutSolidSphere(0.48, 32, 32)


# ======================================
# COMPLETE WINDMILL
# ======================================

def draw_windmill(x, z):

    glPushMatrix()

    glTranslatef(x, 0, z)

    # Tower
    draw_tower()

    # Nacelle
    glPushMatrix()

    glTranslatef(0, 7.5, 0)

    glColor3f(0.72, 0.76, 0.81)

    glPushMatrix()

    glScalef(0.65, 0.38, 0.55)

    glutSolidCube(1)

    glPopMatrix()

    # Rotor blades
    glPushMatrix()

    glTranslatef(0, 0, 0.55)

    glRotatef(angle, 0, 0, 1)

    for i in range(3):

        glPushMatrix()

        glRotatef(i * 120, 0, 0, 1)

        draw_blade()

        glPopMatrix()

    glPopMatrix()

    draw_hub()

    glPopMatrix()

    glPopMatrix()


# ======================================
# WINDMILL GROUND SHADOW
# ======================================

def draw_shadows():

    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    for x, z in windmills:

        glColor4f(0.04, 0.08, 0.04, 0.22)

        glPushMatrix()

        glTranslatef(x, 0.035, z)
        glScalef(1.2, 1, 2.0)

        glBegin(GL_TRIANGLE_FAN)

        glVertex3f(0, 0, 0)

        for i in range(33):

            a = 2 * math.pi * i / 32

            glVertex3f(
                math.cos(a),
                0,
                math.sin(a)
            )

        glEnd()

        glPopMatrix()

    glDisable(GL_BLEND)

    if lighting:
        glEnable(GL_LIGHTING)


# ======================================
# DISPLAY SCENE
# ======================================

def display():

    glClear(
        GL_COLOR_BUFFER_BIT |
        GL_DEPTH_BUFFER_BIT
    )

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    cx, cy, cz = cameras[camera_index]

    gluLookAt(
        cx, cy, cz,
        0, 4, -2,
        0, 1, 0
    )

    if lighting:

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glLightfv(
            GL_LIGHT0,
            GL_POSITION,
            [10, 18, 8, 1]
        )

    else:

        glDisable(GL_LIGHTING)

    draw_sky()
    draw_hills()
    draw_ground()
    draw_road()
    draw_shadows()
    draw_forest()
    draw_flowers()

    for x, z in windmills:
        draw_windmill(x, z)

    glutSwapBuffers()


# ======================================
# KEYBOARD CONTROL
# ======================================

def keyboard(key, x, y):

    global angle, speed, paused
    global lighting, camera_index

    if key == b'\x1b':
        sys.exit(0)

    elif key == b' ':
        paused = not paused

    elif key == b'w':
        speed += 0.5

    elif key == b's':
        speed = max(0, speed - 0.5)

    elif key == b'r':
        angle = 0
        speed = 1
        paused = False

    elif key == b'l':
        lighting = not lighting

    elif key == b'c':
        camera_index = (camera_index + 1) % len(cameras)

    glutPostRedisplay()


# ======================================
# ANIMATION
# ======================================

def update(value):

    global angle, cloud_move

    if not paused:

        angle = (angle + speed) % 360

        cloud_move += 0.025

        if cloud_move > 56:
            cloud_move = 0

    glutPostRedisplay()

    glutTimerFunc(16, update, 0)


# ======================================
# WINDOW RESIZE
# ======================================

def reshape(w, h):

    if h == 0:
        h = 1

    glViewport(0, 0, w, h)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(
        45,
        w / h,
        0.1,
        150
    )

    glMatrixMode(GL_MODELVIEW)


# ======================================
# MAIN
# ======================================

def main():

    global quadric

    glutInit(sys.argv)

    glutInitDisplayMode(
        GLUT_DOUBLE |
        GLUT_RGB |
        GLUT_DEPTH
    )

    glutInitWindowSize(1200, 800)

    glutInitWindowPosition(80, 40)

    glutCreateWindow(
        b"Advanced 3D Windmill Farm"
    )

    glClearColor(
        0.48, 0.73, 0.94, 1
    )

    glEnable(GL_DEPTH_TEST)

    glEnable(GL_NORMALIZE)

    setup_lighting()

    quadric = gluNewQuadric()

    gluQuadricNormals(
        quadric,
        GLU_SMOOTH
    )

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    glutTimerFunc(16, update, 0)

    glutMainLoop()


if __name__ == "__main__":
    main()

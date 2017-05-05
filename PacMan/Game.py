from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import cos, sin, pi as PI
from PacMan.Maze import Maze, Direction
from PacMan.Characters import Hero, Enemy


class Game(object):
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600
    NAME = b'PacMan'

    def __init__(self):
        self.__init_logic()
        self.__init_glut()

    def __init_logic(self):
        self.grid_size = 100
        self.grid_unit_size = 10
        self.maze = Maze(self.grid_unit_size, self.grid_size)
        self.hero = Hero(0, 0, 3)
        self.enemy1 = Enemy(1, 1)
        self.enemy2 = Enemy(2, 2)

    def __init_glut(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
        self.width = glutGet(GLUT_SCREEN_WIDTH) if glutGet(GLUT_SCREEN_WIDTH) > 0 else Game.DEFAULT_WIDTH
        self.height = glutGet(GLUT_SCREEN_HEIGHT) if glutGet(GLUT_SCREEN_HEIGHT) > 0 else Game.DEFAULT_HEIGHT
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(int(self.width / 2), int(self.height / 2))
        glutCreateWindow(Game.NAME)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0.0, self.grid_size, 0.0, self.grid_size)

        glutDisplayFunc(self.MyDisplayFunc)
        # glutIdleFunc(self.MyIdleFunc)
        glutKeyboardFunc(self.MyKeyboardFunc)
        glutMouseFunc(self.MyMouseFunc)
        glutReshapeFunc(self.MyReshapeFunc)
        glutMainLoop()

    def MyDisplayFunc(self):
        print("MyDisplayFunc")
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color to black and opaque
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the color buffer (background)

        self.draw_walls(self.maze.get_maze_wall_list())
        self.draw_hero()
        self.draw_enemy(self.enemy1)
        self.draw_enemy(self.enemy2)
        self.draw_enemy(Enemy(3, 3))
        self.draw_enemy(Enemy(4, 4))
        self.draw_enemy(Enemy(5, 5))
        # self.draw_enemy(Enemy(6,6))
        # self.draw_enemy(Enemy(7,7))
        # self.draw_enemy(Enemy(8,8))
        # self.draw_enemy(Enemy(9,9))



        glFlush()
        glutSwapBuffers()  # Swap the front and back frame buffers (double buffering)

    def draw_walls(self, walls):
        glBegin(GL_LINES)
        glColor3f(1, 1, 1)
        for wall in walls:
            glVertex2i(wall[0][0], wall[0][1])
            glVertex2i(wall[1][0], wall[1][1])
        glEnd()

    def draw_hero(self):
        posX = self.hero.posX * self.grid_unit_size
        posY = self.hero.posY * self.grid_unit_size
        cell_center = self.grid_unit_size / 2
        radius = 3
        triangle_amount = 10
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1, 1, 0)
        for i in range(triangle_amount):
            glVertex2f(
                cell_center + posX + (radius * cos(2 * PI * i / triangle_amount)),
                cell_center + posY + (radius * sin(2 * PI * i / triangle_amount))
            )
        glEnd()

    def draw_enemy(self, enemy):
        glColor3f(1, 0, 0)
        center_x = enemy.posX * self.grid_unit_size + self.grid_unit_size / 2
        center_y = enemy.posY * self.grid_unit_size + self.grid_unit_size / 2
        print(center_x, center_y)
        enemy_size = 4
        glBegin(GL_QUADS)
        glVertex2f(center_x, center_y + enemy_size)
        glVertex2f(center_x + enemy_size, center_y)
        glVertex2f(center_x, center_y - enemy_size)
        glVertex2f(center_x - enemy_size, center_y)
        glEnd()

    @staticmethod
    def MyIdleFunc():
        print("MyIdleFunc")

    def MyKeyboardFunc(self, key_byte, mouse_x, mouse_y):
        print("MyKeyboardFunc : ", key_byte, mouse_x, mouse_y)

        if key_byte == b'w':
            self.hero.move(Direction.NORTH)
        elif key_byte == b's':
            self.hero.move(Direction.SOUTH)
        elif key_byte == b'd':
            self.hero.move(Direction.EAST)
        elif key_byte == b'a':
            self.hero.move(Direction.WEST)
        glutPostRedisplay()

    @staticmethod
    def MyMouseFunc(button_number, is_pressed, mouse_x, mouse_y):
        print("MyMouseFunc : ", button_number, is_pressed, mouse_x, mouse_y)

    @staticmethod
    def MyReshapeFunc(width, height):
        print("MyReshapeFunc : ", width, height)
        # Set the viewport to cover the new window
        glViewport(0, 0, width, height)
        # Set the aspect ratio of the clipping volume to match the viewport
        glMatrixMode(GL_PROJECTION)  # To operate on the Projection matrix
        glLoadIdentity()
        gluOrtho2D(0.0, 100.0, 0.0, 100.0)


if __name__ == "__main__":
    Game()
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

class Object3D:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.position = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 0.0]

    def translate(self, dx, dy, dz):
        self.position[0] += dx
        self.position[1] += dy
        self.position[2] += dz

    def rotate(self, rx, ry, rz):
        self.rotation[0] += rx
        self.rotation[1] += ry
        self.rotation[2] += rz

class Cube(Object3D):
    def __init__(self):
        super().__init__()
        # Vertices kubus
        self.vertices = [
            [-1, -1, -1],  # 0
            [ 1, -1, -1],  # 1
            [ 1,  1, -1],  # 2
            [-1,  1, -1],  # 3
            [-1, -1,  1],  # 4
            [ 1, -1,  1],  # 5
            [ 1,  1,  1],  # 6
            [-1,  1,  1]   # 7
        ]

        # Faces kubus (urutan harus counter-clockwise jika dilihat dari luar)
        self.faces = [
            [0, 1, 2, 3],  # Belakang (z = -1)
            [4, 5, 6, 7],  # Depan (z = +1)
            [0, 4, 5, 1],  # Bawah (y = -1)
            [3, 2, 6, 7],  # Atas (y = +1)
            [0, 3, 7, 4],  # Kiri (x = -1)
            [1, 5, 6, 2]   # Kanan (x = +1)
        ]
class Pyramid(Object3D):
    def __init__(self):
        super().__init__()
        # Vertices piramida
        self.vertices = [
            [0, 2, 0],     # 0 - puncak
            [-1, -1, 1],   # 1 - base
            [1, -1, 1],    # 2 - base
            [1, -1, -1],   # 3 - base
            [-1, -1, -1]   # 4 - base
        ]

        # Faces piramida
        self.faces = [
            [1, 2, 3, 4],  # base
            [0, 1, 2],     # sisi 1
            [0, 2, 3],     # sisi 2
            [0, 3, 4],     # sisi 3
            [0, 4, 1]      # sisi 4
        ]

class Camera:
    def __init__(self):
        self.position = [0.0, 0.0, 10.0]
        self.target = [0.0, 0.0, 0.0]
        self.up = [0.0, 1.0, 0.0]

    def setup_perspective(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width/height, 0.1, 100.0)

    def setup_view(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.position[0], self.position[1], self.position[2],
                  self.target[0], self.target[1], self.target[2],
                  self.up[0], self.up[1], self.up[2])

class Lighting:
    def __init__(self):
        self.ambient_enabled = True
        self.diffuse_enabled = True
        self.specular_enabled = True

    def setup_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)

        # Ambient light
        if self.ambient_enabled:
            ambient_light = [0.2, 0.2, 0.2, 1.0]
            glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_light)

        # Directional light (Light 0)
        glEnable(GL_LIGHT0)
        light_position = [2.0, 2.0, 2.0, 0.0]  # directional light

        if self.diffuse_enabled:
            diffuse_light = [0.8, 0.8, 0.8, 1.0]
            glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)

        if self.specular_enabled:
            specular_light = [1.0, 1.0, 1.0, 1.0]
            glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)

        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

class Graphics3D:
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D Graphics Demo - Cube & Pyramid")

        # Objek 3D
        self.cube = Cube()
        self.pyramid = Pyramid()
        self.current_object = "cube"

        # Camera dan lighting
        self.camera = Camera()
        self.lighting = Lighting()

        # Kontrol
        self.mouse_dragging = False
        self.last_mouse_pos = (0, 0)

        # Setup OpenGL
        self.setup_opengl()

    def setup_opengl(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)  # Gouraud shading

        # Material properties untuk Phong lighting
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)

        self.camera.setup_perspective(self.width, self.height)
        self.lighting.setup_lighting()

    def calculate_normal(self, v1, v2, v3):
        """Hitung normal vector untuk face"""
        edge1 = [v2[i] - v1[i] for i in range(3)]
        edge2 = [v3[i] - v1[i] for i in range(3)]

        # Cross product
        normal = [
            edge1[1] * edge2[2] - edge1[2] * edge2[1],
            edge1[2] * edge2[0] - edge1[0] * edge2[2],
            edge1[0] * edge2[1] - edge1[1] * edge2[0]
        ]

        # Normalize
        length = math.sqrt(sum(n*n for n in normal))
        if length > 0:
            normal = [n/length for n in normal]

        return normal

    def draw_object(self, obj):
        glPushMatrix()

        # Transformasi
        glTranslatef(obj.position[0], obj.position[1], obj.position[2])
        glRotatef(obj.rotation[0], 1, 0, 0)
        glRotatef(obj.rotation[1], 0, 1, 0)
        glRotatef(obj.rotation[2], 0, 0, 1)

        # Gambar faces
        for face in obj.faces:
            if len(face) == 4:  # Quad
                glBegin(GL_QUADS)
            else:  # Triangle
                glBegin(GL_TRIANGLES)

            # Hitung normal untuk face
            v1 = obj.vertices[face[0]]
            v2 = obj.vertices[face[1]]
            v3 = obj.vertices[face[2]]
            normal = self.calculate_normal(v1, v2, v3)
            glNormal3f(normal[0], normal[1], normal[2])

            # Gambar vertices
            for vertex_index in face:
                vertex = obj.vertices[vertex_index]
                glVertex3f(vertex[0], vertex[1], vertex[2])

            glEnd()

        glPopMatrix()

    def draw_wireframe(self, obj):
        glPushMatrix()
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 1.0)

        # Transformasi
        glTranslatef(obj.position[0], obj.position[1], obj.position[2])
        glRotatef(obj.rotation[0], 1, 0, 0)
        glRotatef(obj.rotation[1], 0, 1, 0)
        glRotatef(obj.rotation[2], 0, 0, 1)

        # Gambar wireframe
        for face in obj.faces:
            glBegin(GL_LINE_LOOP)
            for vertex_index in face:
                vertex = obj.vertices[vertex_index]
                glVertex3f(vertex[0], vertex[1], vertex[2])
            glEnd()

        glEnable(GL_LIGHTING)
        glPopMatrix()

    def handle_keyboard(self, keys):
        # Translasi dengan WASD
        if keys[K_w]:
            if self.current_object == "cube":
                self.cube.translate(0, 0.1, 0)
            elif self.current_object == "pyramid":
                self.pyramid.translate(0, 0.1, 0)
        if keys[K_s]:
            if self.current_object == "cube":
                self.cube.translate(0, -0.1, 0)
            elif self.current_object == "pyramid":
                self.pyramid.translate(0, -0.1, 0)
        if keys[K_a]:
            if self.current_object == "cube":
                self.cube.translate(-0.1, 0, 0)
            elif self.current_object == "pyramid":
                self.pyramid.translate(-0.1, 0, 0)
        if keys[K_d]:
            if self.current_object == "cube":
                self.cube.translate(0.1, 0, 0)
            elif self.current_object == "pyramid":
                self.pyramid.translate(0.1, 0, 0)

        # Rotasi dengan arrow keys
        if keys[K_LEFT]:
            if self.current_object == "cube":
                self.cube.rotate(0, -2, 0)
            elif self.current_object == "pyramid":
                self.pyramid.rotate(0, -2, 0)
        if keys[K_RIGHT]:
            if self.current_object == "cube":
                self.cube.rotate(0, 2, 0)
            elif self.current_object == "pyramid":
                self.pyramid.rotate(0, 2, 0)
        if keys[K_UP]:
            if self.current_object == "cube":
                self.cube.rotate(-2, 0, 0)
            elif self.current_object == "pyramid":
                self.pyramid.rotate(-2, 0, 0)
        if keys[K_DOWN]:
            if self.current_object == "cube":
                self.cube.rotate(2, 0, 0)
            elif self.current_object == "pyramid":
                self.pyramid.rotate(2, 0, 0)

        # Kontrol kamera
        if keys[K_q]:
            self.camera.position[2] -= 0.2
        if keys[K_e]:
            self.camera.position[2] += 0.2

    def handle_mouse(self, mouse_pos, mouse_pressed):
        if mouse_pressed[0]:  # Left click
            if not self.mouse_dragging:
                self.mouse_dragging = True
                self.last_mouse_pos = mouse_pos
            else:
                dx = mouse_pos[0] - self.last_mouse_pos[0]
                dy = mouse_pos[1] - self.last_mouse_pos[1]

                if self.current_object == "cube":
                    self.cube.rotate(dy * 0.5, dx * 0.5, 0)
                elif self.current_object == "pyramid":
                    self.pyramid.rotate(dy * 0.5, dx * 0.5, 0)

                self.last_mouse_pos = mouse_pos
        else:
            self.mouse_dragging = False

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Setup camera
        self.camera.setup_view()

        # Set material color
        if self.current_object == "cube":
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.8, 0.2, 0.2, 1.0])  # Merah
            self.draw_object(self.cube)
        elif self.current_object == "pyramid":
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.2, 0.8, 0.2, 1.0])  # Hijau
            self.draw_object(self.pyramid)
        elif self.current_object == "both":
            # Cube merah
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.8, 0.2, 0.2, 1.0])
            self.cube.position = [-2, 0, 0]
            self.draw_object(self.cube)

            # Pyramid hijau
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.2, 0.8, 0.2, 1.0])
            self.pyramid.position = [2, 0, 0]
            self.draw_object(self.pyramid)

        pygame.display.flip()

    def print_controls(self):
        print("=== KONTROL ===")
        print("WASD: Translasi objek")
        print("Arrow Keys: Rotasi objek")
        print("Mouse Drag: Rotasi dengan mouse")
        print("Q/E: Zoom kamera")
        print("1: Tampilkan Cube")
        print("2: Tampilkan Pyramid")
        print("3: Tampilkan Both")
        print("L: Toggle Lighting")
        print("ESC: Keluar")
        print("================")

    def run(self):
        clock = pygame.time.Clock()
        running = True

        self.print_controls()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_1:
                        self.current_object = "cube"
                        print("Menampilkan Cube")
                    elif event.key == pygame.K_2:
                        self.current_object = "pyramid"
                        print("Menampilkan Pyramid")
                    elif event.key == pygame.K_3:
                        self.current_object = "both"
                        print("Menampilkan Both")
                    elif event.key == pygame.K_l:
                        if glIsEnabled(GL_LIGHTING):
                            glDisable(GL_LIGHTING)
                            print("Lighting OFF")
                        else:
                            glEnable(GL_LIGHTING)
                            print("Lighting ON")

            # Handle continuous input
            keys = pygame.key.get_pressed()
            self.handle_keyboard(keys)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            self.handle_mouse(mouse_pos, mouse_pressed)

            # Render
            self.render()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    print("Memulai aplikasi 3D Graphics...")
    print("Pastikan PyOpenGL dan Pygame terinstall:")
    print("pip install PyOpenGL PyOpenGL_accelerate pygame")
    print()

    try:
        app = Graphics3D()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        print("Pastikan semua library terinstall dengan benar!")
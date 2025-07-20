import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

class Shape:

    def _init_(self, color, thickness):
        self.color = color
        self.thickness = thickness

        self.translation = [0, 0]
        self.rotation_angle = 0.0
        self.scale_factors = [1.0, 1.0]
        self.pivot_point = [0, 0]

    def set_pivot_to_center(self):

        pass

    def apply_transformations(self):

        glPushMatrix()

        glTranslatef(self.translation[0], self.translation[1], 0)

        glTranslatef(self.pivot_point[0], self.pivot_point[1], 0)

        glRotatef(self.rotation_angle, 0, 0, 1)

        glScalef(self.scale_factors[0], self.scale_factors[1], 1.0)

        glTranslatef(-self.pivot_point[0], -self.pivot_point[1], 0)

    def draw(self, clipping_window=None, inside_color=None):

        pass

class Point(Shape):

    def _init_(self, pos, color, thickness):
        super()._init_(color, thickness)
        self.pos = pos
        self.set_pivot_to_center()

    def set_pivot_to_center(self):
        self.pivot_point = list(self.pos)

    def draw(self, clipping_window=None, inside_color=None):
        is_inside = clipping_window.is_point_inside(self.pos[0], self.pos[1]) if clipping_window else False

        self.apply_transformations()

        glPointSize(self.thickness * 2)
        glColor3fv(inside_color if is_inside else self.color)

        glBegin(GL_POINTS)
        glVertex2fv(self.pos)
        glEnd()

        glPopMatrix()

class Line(Shape):

    def _init_(self, start_pos, end_pos, color, thickness):
        super()._init_(color, thickness)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.set_pivot_to_center()

    def set_pivot_to_center(self):
        self.pivot_point = [
            (self.start_pos[0] + self.end_pos[0]) / 2,
            (self.start_pos[1] + self.end_pos[1]) / 2
        ]

    def draw(self, clipping_window=None, inside_color=None):
        self.apply_transformations()

        glLineWidth(self.thickness)

        if clipping_window:

            accepted, x1, y1, x2, y2, is_fully_inside = clipping_window.clip_line(self.start_pos[0], self.start_pos[1], self.end_pos[0], self.end_pos[1])
            if accepted:
                glColor3fv(inside_color if is_fully_inside else self.color)
                glBegin(GL_LINES)
                glVertex2f(x1, y1)
                glVertex2f(x2, y2)
                glEnd()
        else:

            glColor3fv(self.color)
            glBegin(GL_LINES)
            glVertex2fv(self.start_pos)
            glVertex2fv(self.end_pos)
            glEnd()

        glPopMatrix()

class Rectangle(Shape):

    def _init_(self, corner1, corner2, color, thickness):
        super()._init_(color, thickness)

        self.min_x = min(corner1[0], corner2[0])
        self.min_y = min(corner1[1], corner2[1])
        self.max_x = max(corner1[0], corner2[0])
        self.max_y = max(corner1[1], corner2[1])
        self.vertices = [
            (self.min_x, self.min_y),
            (self.max_x, self.min_y),
            (self.max_x, self.max_y),
            (self.min_x, self.max_y)
        ]
        self.set_pivot_to_center()

    def set_pivot_to_center(self):
        self.pivot_point = [
            (self.min_x + self.max_x) / 2,
            (self.min_y + self.max_y) / 2
        ]

    def draw(self, clipping_window=None, inside_color=None):
        self.apply_transformations()
        glLineWidth(self.thickness)


        lines = [
            (self.vertices[0], self.vertices[1]),
            (self.vertices[1], self.vertices[2]),
            (self.vertices[2], self.vertices[3]),
            (self.vertices[3], self.vertices[0])
        ]

        if clipping_window:
            for line in lines:
                accepted, x1, y1, x2, y2, is_fully_inside = clipping_window.clip_line(line[0][0], line[0][1], line[1][0], line[1][1])
                if accepted:
                    glColor3fv(inside_color if is_fully_inside else self.color)
                    glBegin(GL_LINES)
                    glVertex2f(x1, y1)
                    glVertex2f(x2, y2)
                    glEnd()
        else:
            glColor3fv(self.color)
            glBegin(GL_LINE_LOOP)
            for vertex in self.vertices:
                glVertex2fv(vertex)
            glEnd()

        glPopMatrix()

class Ellipse(Shape):

    def _init_(self, center, radius_x, radius_y, color, thickness, segments=100):
        super()._init_(color, thickness)
        self.center = center
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.segments = segments
        self.set_pivot_to_center()

    def set_pivot_to_center(self):
        self.pivot_point = list(self.center)

    def draw(self, clipping_window=None, inside_color=None):
        self.apply_transformations()
        glLineWidth(self.thickness)


        vertices = []
        for i in range(self.segments + 1):
            angle = 2 * math.pi * i / self.segments
            x = self.center[0] + self.radius_x * math.cos(angle)
            y = self.center[1] + self.radius_y * math.sin(angle)
            vertices.append((x, y))

        if clipping_window:
            for i in range(self.segments):
                accepted, x1, y1, x2, y2, is_fully_inside = clipping_window.clip_line(
                    vertices[i][0], vertices[i][1], vertices[i+1][0], vertices[i+1][1]
                )
                if accepted:
                    glColor3fv(inside_color if is_fully_inside else self.color)
                    glBegin(GL_LINES)
                    glVertex2f(x1, y1)
                    glVertex2f(x2, y2)
                    glEnd()
        else:
            glColor3fv(self.color)
            glBegin(GL_LINE_LOOP)
            for vertex in vertices:
                glVertex2fv(vertex)
            glEnd()

        glPopMatrix()



class ClippingWindow:

    INSIDE = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8

    def _init_(self, xmin, ymin, xmax, ymax):
        self.set_bounds(xmin, ymin, xmax, ymax)
        self.color = (0.8, 0.8, 0.0)
        self.thickness = 1.5

    def set_bounds(self, xmin, ymin, xmax, ymax):

        self.xmin = min(xmin, xmax)
        self.ymin = min(ymin, ymax)
        self.xmax = max(xmin, xmax)
        self.ymax = max(ymin, ymax)

    def _compute_outcode(self, x, y):

        code = self.INSIDE
        if x < self.xmin:
            code |= self.LEFT
        elif x > self.xmax:
            code |= self.RIGHT
        if y < self.ymin:
            code |= self.BOTTOM
        elif y > self.ymax:
            code |= self.TOP
        return code

    def is_point_inside(self, x, y):
        return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax

    def clip_line(self, x1, y1, x2, y2):

        outcode1 = self._compute_outcode(x1, y1)
        outcode2 = self._compute_outcode(x2, y2)
        original_outcode1 = outcode1
        original_outcode2 = outcode2

        accepted = False

        while True:
            if not (outcode1 | outcode2):
                accepted = True
                break
            elif outcode1 & outcode2:
                break
            else:
                x, y = 0, 0
                outcode_out = outcode1 if outcode1 else outcode2


                if outcode_out & self.TOP:
                    x = x1 + (x2 - x1) * (self.ymax - y1) / (y2 - y1)
                    y = self.ymax
                elif outcode_out & self.BOTTOM:
                    x = x1 + (x2 - x1) * (self.ymin - y1) / (y2 - y1)
                    y = self.ymin
                elif outcode_out & self.RIGHT:
                    y = y1 + (y2 - y1) * (self.xmax - x1) / (x2 - x1)
                    x = self.xmax
                elif outcode_out & self.LEFT:
                    y = y1 + (y2 - y1) * (self.xmin - x1) / (x2 - x1)
                    x = self.xmin


                if outcode_out == outcode1:
                    x1, y1 = x, y
                    outcode1 = self._compute_outcode(x1, y1)
                else:
                    x2, y2 = x, y
                    outcode2 = self._compute_outcode(x2, y2)

        is_fully_inside = not (original_outcode1 | original_outcode2)
        return accepted, x1, y1, x2, y2, is_fully_inside

    def draw(self):

        glColor3fv(self.color)
        glLineWidth(self.thickness)
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.xmin, self.ymin)
        glVertex2f(self.xmax, self.ymin)
        glVertex2f(self.xmax, self.ymax)
        glVertex2f(self.xmin, self.ymax)
        glEnd()

    def translate(self, dx, dy):
        self.xmin += dx
        self.xmax += dx
        self.ymin += dy
        self.ymax += dy

    def scale(self, factor):
        center_x = (self.xmin + self.xmax) / 2
        center_y = (self.ymin + self.ymax) / 2
        width = (self.xmax - self.xmin) * factor
        height = (self.ymax - self.ymin) * factor
        self.xmin = center_x - width / 2
        self.xmax = center_x + width / 2
        self.ymin = center_y - height / 2
        self.ymax = center_y + height / 2


class Editor2D:
    def _init_(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.is_running = True


        self.objects = []
        self.drawing_mode = 'line' # 'point', 'line', 'rect', 'ellipse'
        self.temp_points = []
        self.selected_object_index = -1


        self.colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]
        self.color_index = 0
        self.current_color = self.colors[self.color_index]
        self.thicknesses = [1.0, 2.0, 3.0, 5.0, 8.0]
        self.thickness_index = 0
        self.current_thickness = self.thicknesses[self.thickness_index]


        self.clipping_window = None
        self.setting_window_mode = False
        self.inside_color = (0.1, 1.0, 0.1) # Warna hijau terang untuk objek di dalam window

        self.init_pygame()
        self.init_opengl()
        self.print_instructions()

    def init_pygame(self):
        pygame.init()
        pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Editor Grafis 2D - OpenGL")

    def init_opengl(self):

        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glOrtho(0.0, self.width, 0.0, self.height, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def print_instructions(self):
        """Menampilkan instruksi penggunaan ke konsol."""
        print("\n--- Selamat Datang di Editor Grafis 2D ---")
        print("Mode Menggambar (Ganti dengan F1-F4):")
        print(f"  [F1] Titik  [F2] Garis (Aktif)  [F3] Persegi  [F4] Elips")
        print("\nKontrol Dasar:")
        print("  Klik Kiri Mouse : Menentukan titik untuk menggambar objek.")
        print("  [C]             : Ganti Warna Objek (Saat ini: Merah)")
        print("  [T]             : Ganti Ketebalan Garis (Saat ini: 1.0)")
        print("\nTransformasi Objek (Pilih objek dulu dengan TAB):")
        print("  [TAB]           : Pilih objek berikutnya.")
        print("  [W/A/S/D]       : Translasi (Geser) objek terpilih.")
        print("  [Q/E]           : Rotasi objek terpilih.")
        print("  [Z/X]           : Scaling (Ubah ukuran) objek terpilih.")
        print("\nWindowing & Clipping:")
        print("  [V]             : Aktifkan mode set window (lalu klik 2 titik).")
        print("  Panah           : Geser window kliping.")
        print("  [+/-]           : Ubah ukuran window kliping.")
        print("  [B]             : Hapus window kliping.")
        print("\nLain-lain:")
        print("  [DELETE]        : Hapus objek terpilih.")
        print("  [ESC]           : Keluar.")
        print("--------------------------------------------------")

    def run(self):

        clock = pygame.time.Clock()
        while self.is_running:
            self.handle_events()
            self.render()
            clock.tick(60)
        pygame.quit()

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_key_press(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Klik kiri
                    self.handle_mouse_click(event.pos)

    def handle_key_press(self, key):

        if key == K_ESCAPE:
            self.is_running = False

        # Ganti mode gambar
        elif key == K_F1: self.drawing_mode = 'point'; print("Mode: Titik")
        elif key == K_F2: self.drawing_mode = 'line'; print("Mode: Garis")
        elif key == K_F3: self.drawing_mode = 'rect'; print("Mode: Persegi")
        elif key == K_F4: self.drawing_mode = 'ellipse'; print("Mode: Elips")


        elif key == K_c:
            self.color_index = (self.color_index + 1) % len(self.colors)
            self.current_color = self.colors[self.color_index]
            print(f"Warna diubah ke: {self.current_color}")
        elif key == K_t:
            self.thickness_index = (self.thickness_index + 1) % len(self.thicknesses)
            self.current_thickness = self.thicknesses[self.thickness_index]
            print(f"Ketebalan diubah ke: {self.current_thickness}")


        elif key == K_TAB:
            if len(self.objects) > 0:
                self.selected_object_index = (self.selected_object_index + 1) % len(self.objects)
                print(f"Objek ke-{self.selected_object_index} dipilih.")
            else:
                self.selected_object_index = -1


        elif key == K_DELETE and self.selected_object_index != -1:
            print(f"Objek ke-{self.selected_object_index} dihapus.")
            del self.objects[self.selected_object_index]
            self.selected_object_index = -1


        elif key == K_v:
            self.setting_window_mode = True
            self.temp_points = []
            print("Mode Set Window Aktif: Klik 2 titik untuk menentukan batas window.")
        elif key == K_b:
            self.clipping_window = None
            print("Window kliping dihapus.")
        elif self.clipping_window:
            if key == K_UP: self.clipping_window.translate(0, 10)
            elif key == K_DOWN: self.clipping_window.translate(0, -10)
            elif key == K_LEFT: self.clipping_window.translate(-10, 0)
            elif key == K_RIGHT: self.clipping_window.translate(10, 0)
            elif key == K_EQUALS or key == K_PLUS: self.clipping_window.scale(1.1)
            elif key == K_MINUS: self.clipping_window.scale(0.9)



        if self.selected_object_index != -1:
            obj = self.objects[self.selected_object_index]
            if key == K_d: obj.translation[0] += 5
            elif key == K_a: obj.translation[0] -= 5
            elif key == K_w: obj.translation[1] += 5
            elif key == K_s: obj.translation[1] -= 5
            elif key == K_e: obj.rotation_angle -= 5
            elif key == K_q: obj.rotation_angle += 5
            elif key == K_x: obj.scale_factors = [s * 1.1 for s in obj.scale_factors]
            elif key == K_z: obj.scale_factors = [s * 0.9 for s in obj.scale_factors]

    def handle_mouse_click(self, pos):

        gl_pos = (pos[0], self.height - pos[1])

        if self.setting_window_mode:
            self.temp_points.append(gl_pos)
            if len(self.temp_points) == 2:
                self.clipping_window = ClippingWindow(
                    self.temp_points[0][0], self.temp_points[0][1],
                    self.temp_points[1][0], self.temp_points[1][1]
                )
                self.setting_window_mode = False
                self.temp_points = []
                print("Window kliping berhasil dibuat.")
            return

        self.temp_points.append(gl_pos)


        if self.drawing_mode == 'point':
            self.objects.append(Point(gl_pos, self.current_color, self.current_thickness))
            self.temp_points = []
        elif self.drawing_mode == 'line' and len(self.temp_points) == 2:
            self.objects.append(Line(self.temp_points[0], self.temp_points[1], self.current_color, self.current_thickness))
            self.temp_points = []
        elif self.drawing_mode == 'rect' and len(self.temp_points) == 2:
            self.objects.append(Rectangle(self.temp_points[0], self.temp_points[1], self.current_color, self.current_thickness))
            self.temp_points = []
        elif self.drawing_mode == 'ellipse' and len(self.temp_points) == 2:
            center = self.temp_points[0]
            edge = self.temp_points[1]
            radius_x = abs(center[0] - edge[0])
            radius_y = abs(center[1] - edge[1])
            self.objects.append(Ellipse(center, radius_x, radius_y, self.current_color, self.current_thickness))
            self.temp_points = []

    def render(self):

        glClearColor(0.05, 0.05, 0.15, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        for i, obj in enumerate(self.objects):
            obj.draw(self.clipping_window, self.inside_color)

            if i == self.selected_object_index:
                self.draw_selection_box(obj)


        if self.clipping_window:
            self.clipping_window.draw()


        if len(self.temp_points) > 0:
            glPointSize(5)
            glColor3f(1,1,1) # Warna putih
            glBegin(GL_POINTS)
            for p in self.temp_points:
                glVertex2fv(p)
            glEnd()

        pygame.display.flip()

    def draw_selection_box(self, obj):

        if isinstance(obj, Point):
            min_x, max_x = obj.pos[0] - 5, obj.pos[0] + 5
            min_y, max_y = obj.pos[1] - 5, obj.pos[1] + 5
        elif isinstance(obj, Line):
            min_x = min(obj.start_pos[0], obj.end_pos[0]) - 5
            max_x = max(obj.start_pos[0], obj.end_pos[0]) + 5
            min_y = min(obj.start_pos[1], obj.end_pos[1]) - 5
            max_y = max(obj.start_pos[1], obj.end_pos[1]) + 5
        elif isinstance(obj, Rectangle):
            min_x, max_x = obj.min_x - 5, obj.max_x + 5
            min_y, max_y = obj.min_y - 5, obj.max_y + 5
        elif isinstance(obj, Ellipse):
            min_x = obj.center[0] - obj.radius_x - 5
            max_x = obj.center[0] + obj.radius_x + 5
            min_y = obj.center[1] - obj.radius_y - 5
            max_y = obj.center[1] + obj.radius_y + 5


        obj.apply_transformations()

        glColor3f(0.8, 0.8, 0.8) # Warna abu-abu
        glLineWidth(1)
        glEnable(GL_LINE_STIPPLE)
        glLineStipple(1, 0x00FF) # Pola garis putus-putus

        glBegin(GL_LINE_LOOP)
        glVertex2f(min_x, min_y)
        glVertex2f(max_x, min_y)
        glVertex2f(max_x, max_y)
        glVertex2f(min_x, max_y)
        glEnd()

        glDisable(GL_LINE_STIPPLE)
        glPopMatrix()


if __name__ == '__main__':
    try:
        editor = Editor2D()
        editor.run()
    except Exception as e:
        print(f"Terjadi error: {e}")
        pygame.quit()
import pygame
import random
import math
import abc
 
SCREEN_DIM = (800, 600)
 
 
class Vec2d:
 
 
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
 
    def __repr__(self):
        return 'Vector({x}, {y})'.format(x=self.__x, y=self.__y)
 
    def __add__(self, other):
        """сумма двух векторов"""  # TODO лучше не комент, а докстринг тогда
        return Vec2d(self.__x + other.x, self.__y + other.y)
 
    def __sub__(self, other):  # разность двух векторов
        return Vec2d(self.__x - other.x, self.__y - other.y)
 
    def __mul__(self, k):  # умножение вектора на число
        return Vec2d(self.__x * k, self.__y * k)
 
    def scal_mul(self, other):  # скалярное умножение векторов
        return self.__x * other.x + self.__y * other.y
 
    def __len__(self):
        raise NotImplementedError()  # TODO рейзить надо обьект!
 
    @property
    def length(self):  # длина вектора
        return (self.__x ** 2 + self.__y ** 2) ** .5  # TODO можно так
 
    @property
    def x(self):
        return self.__x
 
    @property
    def y(self):
        return self.__y
 
    @x.setter
    def x(self, value):
        self.__x = value
 
    @y.setter
    def y(self, value):
        self.__y = value
    # TODO кмк излишне скрывать __x и __y, если ты практически полный доступ дал
    # TODO но можно
 
    @property
    def int_pair(self):
        return int(self.__x), int(self.__y)
 
    def vec(self, other):  # создание вектора по началу (x) и концу (y) направленного отрезка
        return other - self
 
 
class Polyline:
 
    # TODO тут стандартная бага новичка - нельзя дефолтом ставить изменяемый обьект
    # TODO надо так:
    def __init__(self, points=None, speeds=[]):
        self.points = [] if points is None else points
        self.speeds = speeds
 
    def add_to_polyline(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)
 
    # Пересчитывание координат опорных точек
    def set_points(self):
        # TODO используй силу, Люк! for i, point in enumerate(self.points):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(-self.speeds[p].x, self.speeds[p].y)
            if self.points[p].x > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)
 
    def draw_points(self, style='points', width=3, color=(255, 255, 255)):
        if style == 'line':
            for p_n in range(-1, len(self.points) - 1):
                pygame.draw.line(
                    gameDisplay,
                    color,
                    self.points[p_n].int_pair,
                    self.points[p_n + 1].int_pair,
                    width)
        elif style == 'points':
            for p in self.points:
                pygame.draw.circle(
                    gameDisplay,
                    color,
                    p.int_pair,
                    width)
 
 
class Knot(Polyline):
 
    # TODO переопределять конструктор, если ничего не добавляешь - не надо
    def __init__(self):
        super().__init__()
 
    def set_points(self):
        self.__get_knot(steps)
        super().set_points()
 
    def draw_points(self, steps, style, color):
        self.__get_knot(steps)
        super().draw_points(style=style, color=color)
 
    def __get_knot(self, count):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.__get_points(ptn, count))
        return res
 
    def __get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.__get_point(points=base_points, alpha=i * alpha))  # TODO вызовы лучше делать именованные
        return res
 
    def __get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.__get_point(points, alpha, deg - 1) * (1 - alpha)
 
 
# Основная программа
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
 
    steps = 35
    working = True
    polyline = Polyline()
    knot = Knot()
 
    pause = True
 
    hue = 0
    color = pygame.Color(0)
 
    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
 
            if event.type == pygame.MOUSEBUTTONDOWN:
                polyline.add_to_polyline(
                    point=Vec2d(*event.pos),
                    speed=Vec2d(random.random() * 2, random.random() * 2))
                knot.add_to_polyline(
                    point=Vec2d(*event.pos),
                    speed=Vec2d(random.random() * 2, random.random() * 2))
                print(random.random() * 2)
 
        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        polyline.draw_points()
        knot.draw_points(steps, 'line', color)
 
        if not pause:
            polyline.set_points()
            knot.set_points()
 
        pygame.display.flip()
 
    pygame.display.quit()
    pygame.quit()
    exit(0)
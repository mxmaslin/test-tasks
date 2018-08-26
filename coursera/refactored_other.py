import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, pos):
        self.pos = pos

    def __getitem__(self, item):
        return self.pos[item]

    def __add__(self, other):
        res = self.pos[0] + other.pos[0], self.pos[1] + other.pos[1]
        return Vec2d(res)

    def __sub__(self, other):
        res = self.pos[0] - other.pos[0], self.pos[1] - other.pos[1]
        return Vec2d(res)

    def __mul__(self, other):
        if isinstance(other, Vec2d):
            res = self.pos[0] * other.pos[0], self.pos[1] * other.pos[1]
        else:
            res = self.pos[0] * other, self.pos[1] * other
        return Vec2d(res)

    def __len__(self):
        """Ð´Ð¾Ð±Ð°Ð²Ð¸Ñ‚ÑŒ Ð²Ð¾Ð·Ð¼Ð¾Ð¶Ð½Ð¾ÑÑ‚ÑŒ Ð²Ñ‹Ñ‡Ð¸ÑÐ»ÑÑ‚ÑŒ Ð´Ð»Ð¸Ð½Ñƒ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð° a Ñ‡ÐµÑ€ÐµÐ· len(a)"""
        return int(
            math.sqrt(self.pos[0] * self.pos[0] + self.pos[1] * self.pos[1])
        )

    def vec(self, other):
        """ÑÐ¾Ð·Ð´Ð°Ð½Ð¸Ðµ Ð²ÐµÐºÑ‚Ð¾Ñ€Ð° Ð¿Ð¾ Ð½Ð°Ñ‡Ð°Ð»Ñƒ (x) Ð¸ ÐºÐ¾Ð½Ñ†Ñƒ (y) Ð½Ð°Ð¿Ñ€Ð°Ð²Ð»ÐµÐ½Ð½Ð¾Ð³Ð¾ Ð¾Ñ‚Ñ€ÐµÐ·ÐºÐ°"""
        return other.__sub__(self)

    def int_pair(self):
        """Ð´Ð¾Ð±Ð°Ð²Ð¸Ñ‚ÑŒ Ð¼ÐµÑ‚Ð¾Ð´ int_pair Ð´Ð»Ñ Ð¿Ð¾Ð»ÑƒÑ‡ÐµÐ½Ð¸Ðµ Ð¿Ð°Ñ€Ñ‹ (tuple) Ñ†ÐµÐ»Ñ‹Ñ… Ñ‡Ð¸ÑÐµÐ»"""
        return int(self.pos[0]), int(self.pos[1])


class BaseSequence:
    """Ð‘Ð°Ð·Ð¾Ð²Ñ‹Ð¹ ÐºÐ»Ð°ÑÑ Ð´Ð»Ñ Points, Speeds"""
    def __init__(self, unit_cls, unit=None):
        self.__unit_cls = unit_cls
        self.sequence = []
        if unit:
            self.sequence.append(self.__unit_cls(unit))

    def __getitem__(self, item):
        return self.sequence[item]

    def __len__(self):
        return len(self.sequence)

    def __setitem__(self, key, value):
        self.sequence[key] = value

    def __iter__(self):
        return iter(self.sequence)

    def add(self, unit):
        self.sequence.append(self.__unit_cls(unit))

    def reset(self, unit=None):
        self.__init__(unit)


class Sequence(BaseSequence):
    __unit_cls = Vec2d

    def __init__(self, point=None):
        super().__init__(self.__unit_cls, point)


class SpeedSequence(BaseSequence):
    __unit_cls = Vec2d

    def __init__(self, point=None):
        super().__init__(self.__unit_cls, point)

    def __setitem__(self, key, value):
        self.sequence[key] = self.__unit_cls(value)


class Polyline:
    """ÐšÐ»Ð°ÑÑ Ð·Ð°Ð¼ÐºÐ½ÑƒÑ‚Ñ‹Ñ… Ð»Ð¾Ð¼Ð°Ð½Ñ‹Ñ… Polyline, Ñ Ð²Ð¾Ð·Ð¼Ð¾Ð¶Ð½Ð¾ÑÑ‚ÑÐ¼Ð¸: Ð´Ð¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð²
    Ð»Ð¾Ð¼Ð°Ð½ÑƒÑŽ Ñ‚Ð¾Ñ‡ÐºÐ¸ (Vec2d) c ÐµÑ‘ ÑÐºÐ¾Ñ€Ð¾ÑÑ‚ÑŒÑŽ; Ð¿ÐµÑ€ÐµÑÑ‡Ñ‘Ñ‚ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ Ñ‚Ð¾Ñ‡ÐµÐº
    (set_points); Ð¾Ñ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ° Ð»Ð¾Ð¼Ð°Ð½Ð¾Ð¹ (draw_points).
    """

    def __init__(self):
        self.points = Sequence()
        self.speeds = SpeedSequence()

    # ÐŸÐµÑ€ÑÑ‡Ð¸Ñ‚Ñ‹Ð²Ð°Ð½Ð¸Ðµ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ Ð¾Ð¿Ð¾Ñ€Ð½Ñ‹Ñ… Ñ‚Ð¾Ñ‡ÐµÐº
    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p][0] > SCREEN_DIM[0] or self.points[p][0] < 0:
                self.speeds[p] = (- self.speeds[p][0], self.speeds[p][1])
            if self.points[p][1] > SCREEN_DIM[1] or self.points[p][1] < 0:
                self.speeds[p] = (self.speeds[p][0], -self.speeds[p][1])

    def draw_points(self, points=None, width=3, color=(255, 255, 255)):
        if points is None:
            points = self.points

        for p in points:
            pygame.draw.circle(gameDisplay, color, (int(p[0]), int(p[1])),
                               width)

    def draw_line(self, points=None, width=3, color=(255, 255, 255)):
        if points is None:
            points = self.points

        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(
                gameDisplay, color, (int(points[p_n][0]), int(points[p_n][1])),
                (int(points[p_n + 1][0]), int(points[p_n + 1][1])), width
            )

    def add_point(self, point):
        self.points.add(point)

    def add_speed(self, speed):
        self.speeds.add(speed)

    def reset(self):
        self.points.reset()
        self.speeds.reset()


class Knot(Polyline):
    """Ð ÐµÐ°Ð»Ð¸Ð·Ð¾Ð²Ð°Ñ‚ÑŒ ÐºÐ»Ð°ÑÑ Knot â€” Ð¿Ð¾Ñ‚Ð¾Ð¼Ð¾Ðº ÐºÐ»Ð°ÑÑÐ° Polyline â€” Ð² ÐºÐ¾Ñ‚Ð¾Ñ€Ð¾Ð¼
    Ð´Ð¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð¸ Ð¿ÐµÑ€ÐµÑÑ‡Ñ‘Ñ‚ ÐºÐ¾Ð¾Ñ€Ð´Ð¸Ð½Ð°Ñ‚ Ð¸Ð½Ð¸Ñ†Ð¸Ð¸Ñ€ÑƒÑŽÑ‚ Ð²Ñ‹Ð·Ð¾Ð² Ñ„ÑƒÐ½ÐºÑ†Ð¸Ð¸ get_knot
    Ð´Ð»Ñ Ñ€Ð°ÑÑ‡Ñ‘Ñ‚Ð° Ñ‚Ð¾Ñ‡ÐµÐº ÐºÑ€Ð¸Ð²Ð¾Ð¹ Ð¿Ð¾ Ð´Ð¾Ð±Ð°Ð²Ð»ÑÐµÐ¼Ñ‹Ð¼ Ð¾Ð¿Ð¾Ñ€Ð½Ñ‹Ð¼.
    """

    def __init__(self, steps=35):
        super().__init__()
        self.steps = steps
        self.knot_line = self.get_knot()

    def add_point(self, point):
        super().add_point(point)
        self.set_knot()

    def add_speed(self, speed):
        self.speeds.add(speed)
        self.set_knot()

    def set_points(self):
        super().set_points()
        self.set_knot()

    def set_knot(self):
        self.knot_line = self.get_knot()

    # Ð¡Ð³Ð»Ð°Ð¶Ð¸Ð²Ð°Ð½Ð¸Ðµ Ð»Ð¾Ð¼Ð°Ð½Ð¾Ð¹
    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        res = points[deg] * alpha + \
            self.get_point(points, alpha, deg-1) * (1-alpha)
        return res

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        count = self.steps
        points = self.points
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append((points[i] + points[i + 1]) * 0.5)
            ptn.append(points[i + 1])
            ptn.append((points[i + 1] + points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn, count))
        return res

    def draw_line(self, points=None, width=3, color=(255, 255, 255)):
        if points is None:
            points = self.knot_line
        super().draw_line(points, width=width, color=color)

    # ÐžÑ‚Ñ€Ð¸ÑÐ¾Ð²ÐºÐ° ÑÐ¿Ñ€Ð°Ð²ÐºÐ¸
    def draw_help(self):
        gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(self.steps), "Current points"])

        pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                          (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def reset(self):
        super().reset()
        self.knot_line = self.get_knot()


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    controller = Knot(steps=steps)

    working = True
    show_help = False
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
                    controller.reset()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    controller.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    controller.steps -= 1 if controller.steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                controller.add_point(event.pos)
                controller.add_speed((random.random()*2, random.random()*2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        controller.draw_points()
        controller.draw_line(width=3, color=color)

        if not pause:
            controller.set_points()
        if show_help:
            controller.draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
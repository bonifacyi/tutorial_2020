from random import randrange as rnd, choice
import tkinter as tk
import math
import time

WIDTH = 800
HEIGHT = 600
TARGETS = 10


class Ball:
    def __init__(self, x=40, y=450, vx=0, vy=0):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.number = 0
        self.x = x
        self.y = y
        self.r = 15
        self.vx = vx
        self.vy = vy
        self.s_air = 0.02
        self.g = 3
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canvas.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canvas.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        fx_drag = self.s_air * abs(self.vx) ** 1.2
        fy_drag = self.s_air * abs(self.vy) ** 1.2
        if self.vx > 1:
            self.vx = self.vx - fx_drag
        elif self.vx < -1:
            self.vx = self.vx + fx_drag
        else:
            self.vx = 0

        if self.x + self.r >= WIDTH and self.vx > 0:
            self.x = WIDTH - self.r
            self.vx = -self.vx
        elif self.x - self.r <= 0 and self.vx < 0:
            self.x = self.r
            self.vx = -self.vx

        if self.vy > 0:
            self.vy = self.vy + self.g - fy_drag
        elif self.vy < 0:
            self.vy = self.vy + self.g + fy_drag

        self.y += self.vy

        if self.y + self.r >= HEIGHT and self.vy > 0:
            self.y = HEIGHT - self.r
            self.vy = self.vy / 1.4
            if abs(self.vy) > self.g:
                self.vy = -self.vy
            else:
                self.vx, self.vy = 0, 0
        elif self.y - self.r <= 0 and self.vy < 0:
            self.y = self.r
            self.vy = -self.vy

        self.x += self.vx

        if self.vx == 0 and self.vy == 0:
            self.live -= 1

        self.set_coords()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        delta = ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5
        if delta <= self.r + obj.r:
            canvas.delete(self.id)
            return True
        else:
            return False

    def ball_delete(self):
        if self.live == 0:
            canvas.delete(self.id)
            return self.number


class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.x = 20
        self.y = 450
        self.id = canvas.create_line(20, 450, 50, 420, width=7)
        self.balls = dict()
        self.bullet = 0

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        self.bullet += 1
        self.angle = math.atan((event.y - self.y) / (event.x - self.x))
        x = 20 + max(self.f2_power, 20) * math.cos(self.angle)
        y = 450 + max(self.f2_power, 20) * math.sin(self.angle)
        vx = self.f2_power * math.cos(self.angle)
        vy = self.f2_power * math.sin(self.angle)
        new_ball = Ball(x, y, vx, vy)
        new_ball.number = self.bullet
        self.balls[self.bullet] = new_ball
        self.f2_on = 0
        self.f2_power = 10

    def ball_cleaner(self):
        for_del = []
        for ball in self.balls.values():
            delete = ball.ball_delete()
            if delete:
                for_del.append(delete)
        for i in for_del:
            del self.balls[i]

    def targeting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan((event.y - 450) / (event.x - 20)) if event.x - 20 != 0 else -math.pi
        if self.f2_on:
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')
        canvas.coords(self.id, 20, 450,
                      20 + max(self.f2_power, 20) * math.cos(self.angle),
                      450 + max(self.f2_power, 20) * math.sin(self.angle)
                      )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canvas.itemconfig(self.id, fill='orange')
        else:
            canvas.itemconfig(self.id, fill='black')


class Target:
    def __init__(self):
        """ Инициализация новой цели. """
        self.live = 1
        self.color = 'red'
        self.r = rnd(5, 50)
        self.x = rnd(WIDTH // 2, WIDTH - self.r)
        self.y = rnd(self.r, HEIGHT - self.r)
        self.dx, self.dy = rnd(-2, 2), rnd(-2, 2)
        self.color = 'red'
        self.id = canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )

    def set_coords(self):
        canvas.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move_target(self):
        self.x += self.dx
        self.y += self.dy
        if self.x + self.r > WIDTH or self.x - self.r <= WIDTH / 3:
            self.dx = -self.dx
        if self.y + self.r > HEIGHT or self.y - self.r <= 0:
            self.dy = -self.dy
        self.set_coords()


class MainBlock:
    def __init__(self):
        global canvas
        self.root = tk.Tk()
        self.root.geometry(str(WIDTH) + 'x' + str(HEIGHT))
        canvas = tk.Canvas(self.root, bg='white')
        canvas.pack(fill=tk.BOTH, expand=1)

        self.point = 0
        self.points = 0
        self.id_points = canvas.create_text(30, 30, text=self.points, font='28')
        self.screen = canvas.create_text(400, 300, text='', font='28')
        self.targets = []
        self.game_round()

    def game_round(self):
        self.gun = Gun()
        self.gen_target(TARGETS)

        self.gun.bullet = 0
        self.gun.balls = dict()
        canvas.bind('<Button-1>', self.gun.fire2_start)
        canvas.bind('<ButtonRelease-1>', self.gun.fire2_end)
        canvas.bind('<Motion>', self.gun.targeting)

        self.move_target()
        self.time_handler()

    def time_handler(self):
        if self.targets or self.gun.balls:
            for ball in self.gun.balls.values():
                ball.move()
                hit_id = self.hit_target(ball)
                if hit_id:
                    self.hit()
                    print(self.points)
                    if not self.targets:
                        canvas.bind('<Button-1>', '')
                        canvas.bind('<ButtonRelease-1>', '')
                        canvas.itemconfig(self.screen, text='Вы уничтожили цель за ' + str(self.gun.bullet) + ' выстрелов')
            self.gun.ball_cleaner()
            canvas.update()
            self.gun.targeting()
            self.gun.power_up()
            self.root.after(30, self.time_handler)
        else:
            canvas.itemconfig(self.screen, text='')
            canvas.delete(self.gun.id)
            self.game_round()

    def gen_target(self, n):
        for i in range(n):
            target = Target()
            self.targets.append(target)

    def move_target(self):
        for target in self.targets:
            target.move_target()
        self.root.after(10, self.move_target)

    def hit_target(self, ball):
        for i in range(len(self.targets)):
            if ball.hittest(self.targets[i]):
                canvas.delete(self.targets[i].id)
                self.targets.pop(i)

                return True

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points
        canvas.itemconfig(self.id_points, text=self.points)


def main():
    MainBlock()
    tk.mainloop()


if __name__ == '__main__':
    main()


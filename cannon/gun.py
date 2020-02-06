from random import randrange as rnd, choice
import tkinter as tk
import math
import time

WIDTH = 800
HEIGHT = 600
DT = 0.03


def main():
    global root, canvas, gun, target, screen1, bullet, balls
    root = tk.Tk()
    root.geometry(str(WIDTH) + 'x' + str(HEIGHT))
    canvas = tk.Canvas(root, bg='white')
    canvas.pack(fill=tk.BOTH, expand=1)

    target = Target()
    screen1 = canvas.create_text(400, 300, text='', font='28')
    gun = Gun()


class Ball:
    def __init__(self, x=40, y=450, vx=0, vy=0):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
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

        if self.y + self.r >= HEIGHT and self.vy > 0:
            self.y = HEIGHT - self.r
            self.vy = self.vy / 1.3
            if self.vy > self.g:
                self.vy = -self.vy
            else:
                self.vx, self.vy = 0, 0
        elif self.y - self.r <= 0 and self.vy < 0:
            self.y = self.r
            self.vy = -self.vy

        self.x += self.vx
        self.vy = self.vy + self.g
        self.y += self.vy
        print(self.vx, fx_drag, self.vy)
        self.set_coords()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        return False


class Gun:
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.x = 20
        self.y = 450
        self.id = canvas.create_line(20, 450, 50, 420, width=7)   # FIXME: don't know how to set it...

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        r = 5
        self.angle = math.atan((event.y - self.y) / (event.x - self.x))
        x = 20 + max(self.f2_power, 20) * math.cos(self.angle)
        y = 450 + max(self.f2_power, 20) * math.sin(self.angle)
        vx = self.f2_power * math.cos(self.angle)
        vy = self.f2_power * math.sin(self.angle)
        new_ball = Ball(x, y, vx, vy)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targeting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan((event.y - 450) / (event.x - 20))
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
        self.points = 0
        self.live = 1
        # FIXME: don't work!!! How to call this functions when object is created?
        self.id = canvas.create_oval(0, 0, 0, 0)
        self.id_points = canvas.create_text(30, 30, text=self.points, font='28')
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        canvas.coords(self.id, x - r, y - r, x + r, y + r)
        canvas.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canvas.coords(self.id, -10, -10, -10, -10)
        self.points += points
        canvas.itemconfig(self.id_points, text=self.points)


def time_handler(event=''):
    global Gun, target, screen1, balls, bullet
    bullet = 0
    balls = []
    canvas.bind('<Button-1>', gun.fire2_start)
    canvas.bind('<ButtonRelease-1>', gun.fire2_end)
    canvas.bind('<Motion>', gun.targeting)

    target.live = 1
    while target.live or balls:
        for ball in balls:
            ball.move()
            if ball.hittest(target) and target.live:
                target.live = 0
                target.hit()
                canvas.bind('<Button-1>', '')
                canvas.bind('<ButtonRelease-1>', '')
                canvas.itemconfig(screen1, text='Вы уничтожили цель за ' + str(bullet) + ' выстрелов')
        canvas.update()
        time.sleep(DT)
        gun.targeting()
        gun.power_up()
    canvas.itemconfig(screen1, text='')
    canvas.delete(Gun)
    root.after(750, time_handler)


main()
time_handler()
root.mainloop()

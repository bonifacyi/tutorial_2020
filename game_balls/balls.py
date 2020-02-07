#!/usr/bin/env python

import tkinter as tk
from random import randint, choice

WIDTH = 1000
HEIGHT = 800
COLOR = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']


class Ball:
    def __init__(self, canvas, x, y, other_balls):
        self.canvas = canvas
        self.other_balls = other_balls
        self.R = randint(20, 50)
        self.x = x
        self.y = y
        self.dx = randint(-3, 3)
        self.dy = randint(-3, 3)
        self.color = choice(COLOR)
        self.ball_id = self.create_ball()
        self.level = 50 * (self.dx ** 2 + self.dy ** 2) // self.R
        print(self.dx, self.dy)

    def create_ball(self):
        if self.x < self.R:
            x = self.R
        elif self.x > WIDTH - self.R:
            x = WIDTH - self.R
        else:
            x = self.x
        if self.y < self.R:
            y = self.R
        elif self.y > HEIGHT - self.R:
            y = HEIGHT - self.R
        else:
            y = self.y

        return self.canvas.create_oval(x - self.R, y - self.R, x + self.R, y + self.R, fill=self.color)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        if self.x + self.R > WIDTH or self.x - self.R <= 0:
            self.dx = -self.dx
        if self.y + self.R > HEIGHT or self.y - self.R <= 0:
            self.dy = -self.dy

    def show(self):
        self.canvas.move(self.ball_id, self.dx, self.dy)

    def check_inside(self, balls):
        for ball in balls:
            delta = ((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2) ** 0.5
            if delta < self.R + ball.R and self != ball:
                # print(self.dx, self.dy, ball.dx, ball.dy)
                self.dx, ball.dx = ball.dx, self.dx
                self.dy, ball.dy = ball.dy, self.dy
                # print(self.dx, self.dy, ball.dx, ball.dy)

    def check_collision(self):
        for ball in self.other_balls:
            delta = ((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2) ** 0.5
            # if delta < self.R + ball.R:

    def check_destroy(self, check_x, check_y):
        if (check_x - self.x) ** 2 + (check_y - self.y) ** 2 <= self.R ** 2:
            self.canvas.delete(self.ball_id)
            return True
        else:
            return False


class Block:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(str(WIDTH) + 'x' + str(HEIGHT))
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.canvas_click_handler)
        self.balls = []
        self.tick()

    def canvas_click_handler(self, event):
        for ball in self.balls:
            if ball.check_destroy(event.x, event.y):
                return
        self.balls.append(Ball(self.canvas, event.x, event.y, self.balls))

    def tick(self):
        for ball in self.balls:
            ball.move()
            ball.check_inside(self.balls)
            ball.show()
        self.root.after(10, self.tick)


def main():
    Block()
    tk.mainloop()


if __name__ == '__main__':
    main()

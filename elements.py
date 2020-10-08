#!/usr/bin/env python

from graph import *
from random import randint
from math import pi, sin, cos, sqrt


def background(width, height, horizon, up_color, bottom_color):
    """ generate base field """
    windowSize(width, height)
    canvasSize(width, height)
    penColor(up_color)
    brushColor(up_color)
    rectangle(0, 0, width, horizon)
    penColor(bottom_color)
    brushColor(bottom_color)
    rectangle(0, horizon, width, height)


def stolb(x, width, height, color):
    """ x - left border """
    penColor(color)
    brushColor(color)
    rectangle(x, 0, x + width, height)


def spine(x, y, width, color, corner=0):
    """x, y - center of base"""
    corner = (corner * 2 * pi) / 360
    height = width * 8
    penColor(0, 0, 0)
    brushColor(color)
    x1 = x - width * cos(corner) / 2
    y1 = y - width * sin(corner) / 2
    x2 = x + width * cos(corner) / 2
    y2 = y + width * sin(corner) / 2
    x3 = x + height * sin(corner)
    y3 = y - height * cos(corner)
    polygon([(x1, y1), (x2, y2), (x3, y3)])


def ellipse(x, y, width, height, color, corner=0):
    """Print ellipse. x, y - center; width, height - size;"""
    corner = (corner * 2 * pi) / 360
    penColor(150, 150, 150)
    brushColor(color)
    coord = []
    for i in range(360):
        alfa = (i * 2 * pi) / 360
        dx = (width / 2) * cos(alfa)
        dy = (height / 2) * sin(alfa)
        dx_corner = dx * cos(corner) - dy * sin(corner)
        dy_corner = dx * sin(corner) + dy * cos(corner)
        coord.append((x + dx_corner, y + dy_corner))
    polygon(coord)


def grib(x, y, size, corner=0):
    corner_rad = (corner * 2 * pi) / 360
    prop = 0.35
    ellipse(x, y, size * prop, size, 'white', corner)
    x_head = x + size * sin(corner_rad) / 2
    y_head = y - size * cos(corner_rad) / 2
    ellipse(x_head, y_head, size, size * prop, 'red', corner)

    x_limit = size * 4 // 10
    point_count = randint(4, 8)
    array = [i for i in range(-3, 4)]
    for i in array:
        xi = x_limit * i / 3
        y_limit = int(sqrt(x_limit ** 2 - xi ** 2) * prop)
        yi = randint(-y_limit, y_limit)
        x_point = x_head + xi * cos(corner_rad) - yi * sin(corner_rad)
        y_point = y_head + xi * sin(corner_rad) + yi * cos(corner_rad)
        width_point = randint(size // 12, size // 7)
        height_point = randint(size // 18, size // 12)
        ellipse(x_point, y_point, width_point, height_point, 'white', corner)


def gen_spine(x, y, size, color, prop, count, corner=None):
    for i in range(count):
        x_limit = size // 2
        spine_x = x + randint(-x_limit, x_limit)
        y_limit = int(sqrt((size / 2) ** 2 - (spine_x - x) ** 2) * prop)
        spine_y = y + randint(-y_limit, y_limit)
        if corner is None:
            spine_corner = randint(0, 30) if spine_x >= x else -randint(0, 30)
        else:
            spine_corner = corner
        spine_width = size * 0.04
        spine(spine_x, spine_y, spine_width, color, spine_corner)


def hedgehog_position(x, y, size):
    position = dict()
    position['prop'] = 0.5

    position['head_size'] = size * 0.25
    position['head_x'] = x + size * 0.6
    position['head_y'] = y + size * 0.04

    position['nose_size'] = position['head_size'] * 0.12
    position['nose_x'] = position['head_x'] + position['head_size'] // 2
    position['nose_y'] = position['head_y']

    position['eye_size'] = position['head_size'] * 0.17
    position['eye_left_x'] = position['head_x']
    position['eye_left_y'] = position['head_y'] - position['head_size'] * 0.1
    position['eye_right_x'] = position['head_x'] + position['head_size'] // 4
    position['eye_right_y'] = position['head_y'] - position['head_size'] * 0.15

    position['leg1_size'] = size * 0.13
    position['leg2_size'] = size * 0.11
    position['leg3_size'] = size * 0.15
    position['leg4_size'] = size * 0.15
    position['leg1_x'] = x - size // 2
    position['leg1_y'] = y + size * 0.1
    position['leg2_x'] = x + size * 0.46
    position['leg2_y'] = y + size * 0.1
    position['leg3_x'] = x - size * 0.37
    position['leg3_y'] = y + size * 0.2
    position['leg4_x'] = x + size * 0.37
    position['leg4_y'] = y + size * 0.2

    position['grib_size'] = size * 0.4
    position['grib_x'] = x
    position['grib_y'] = y - size * position['prop'] * 0.8
    position['grib_corner'] = 15
    position['apple1_color'] = (252, 148, 3)
    position['apple2_color'] = (252, 148, 3)
    position['apple3_color'] = 'red'
    position['apple1_size'] = size * 0.25
    position['apple2_size'] = size * 0.25
    position['apple3_size'] = size * 0.3
    position['apple1_x'] = x - size * 0.4
    position['apple1_y'] = y - size * 0.25
    position['apple2_x'] = x - size * 0.3
    position['apple2_y'] = y - size * 0.3
    position['apple3_x'] = x + size * 0.35
    position['apple3_y'] = y - size * 0.3
    position['spine_color'] = (60, 45, 23)

    return position


def hedgehog(x, y, size):
    color = (105, 87, 77)
    pos = hedgehog_position(x, y, size)

    ellipse(pos['leg1_x'], pos['leg1_y'], pos['leg1_size'], pos['leg1_size'] * 0.5, color)  # left rear leg
    ellipse(pos['leg2_x'], pos['leg2_y'], pos['leg2_size'], pos['leg2_size'] * 0.9, color)  # left fore leg
    ellipse(x, y, size, size * pos['prop'], color)  # body
    ellipse(pos['leg3_x'], pos['leg3_y'], pos['leg3_size'], pos['leg3_size'] * 0.4, color)  # right rear leg
    ellipse(pos['leg4_x'], pos['leg4_y'], pos['leg4_size'], pos['leg4_size'] * 0.5, color)  # left fore leg

    gen_spine(x, y, size, pos['spine_color'], pos['prop'], 100)

    ellipse(pos['head_x'], pos['head_y'], pos['head_size'], pos['head_size'] * 0.6, color)  # head
    ellipse(pos['nose_x'], pos['nose_y'], pos['nose_size'], pos['nose_size'], 'black')  # nose
    ellipse(pos['eye_left_x'], pos['eye_left_y'], pos['eye_size'], pos['eye_size'], 'black')    # left eye
    ellipse(pos['eye_right_x'], pos['eye_right_y'], pos['eye_size'], pos['eye_size'], 'black')  # right eye

    gen_spine(x, y, size, pos['spine_color'], pos['prop'], 100)

    ellipse(pos['apple1_x'], pos['apple1_y'], pos['apple1_size'] * 0.8, pos['apple1_size'], pos['apple1_color'])
    ellipse(pos['apple2_x'], pos['apple2_y'], pos['apple2_size'] * 0.9, pos['apple2_size'], pos['apple2_color'])
    grib(pos['grib_x'], pos['grib_y'], pos['grib_size'], pos['grib_corner'])
    ellipse(pos['apple3_x'], pos['apple3_y'], pos['apple3_size'], pos['apple3_size'], pos['apple3_color'])

    gen_spine(x, y, size, pos['spine_color'], pos['prop'], 70)
    gen_spine(x, y, size, pos['spine_color'], pos['prop'], 30, 0)


if __name__ == '__main__':
    width = 800
    height = 1000
    horizon = 600

    up_color = (120, 190, 120)
    bottom_color = (145, 90, 60)
    background(width, height, horizon, up_color, bottom_color)
    stolb_color = (227, 177, 50)

    """stolb_width = randint(width // 50, width // 7)
    stolb_height = randint(horizon, height)
    stolb(300, stolb_width, stolb_height, stolb_color)"""

    stolb(0, 70, 650, stolb_color)
    hedgehog(0, 900, 150)
    hedgehog(300, 650, 150)
    stolb(150, 140, 950, stolb_color)
    stolb(500, 90, 680, stolb_color)
    stolb(700, 60, 750, stolb_color)
    hedgehog(500, 800, 250)
    hedgehog(750, 620, 170)
    grib(360, 990, 100)
    grib(420, 995, 60, -10)

    run()

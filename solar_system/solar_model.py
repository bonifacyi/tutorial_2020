import math


def cosmic_body_motion(x, y, r, pivot_x, pivot_y, dt, period_of_rotation):
    if r == 0:
        return x, y
    regarding_x = x - pivot_x
    regarding_y = y - pivot_y
    count = period_of_rotation * 100 / dt
    ds = 2 * math.pi * r / count
    dx = ds * regarding_y / r
    dy = ds * regarding_x / r
    x += dx
    y += dy
    print(dx, dy)
    return x, y


def convert_color(array):
    new_array = []
    for color in array:
        new = str(hex(color))
        new_array.append(new[2:])
    new_color = '#{0:0^2x}{1:0^2x}{2:0^2x}'.format(*array)
    return new_color


if __name__ == '__main__':
    c = convert_color((255, 255, 0))
    print(c)

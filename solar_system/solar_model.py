import math


def calculate_new_angle(alpha, dt, period_of_rotation):
    count = period_of_rotation * 1000 / dt
    delta_alpha = 2 * math.pi / count
    alpha_new = alpha + delta_alpha
    if alpha_new > 2 * math.pi:
        alpha_new -= 2 * math.pi
    return alpha_new


def circular_cosmic_body_motion(alpha, r, axis_x, axis_y, dt, period_of_rotation):
    if r == 0:
        return axis_x, axis_y, 0
    alpha_new = calculate_new_angle(alpha, dt, period_of_rotation)
    x = r * math.cos(alpha_new) + axis_x
    y = axis_y - r * math.sin(alpha_new)
    return x, y, alpha_new


def point_on_ellipse(alpha, a, b, alpha_a, axis_x, axis_y):
    x_norm = a * math.cos(alpha)
    y_norm = -b * math.sin(alpha)
    x = axis_x + x_norm * math.cos(alpha_a) - y_norm * math.sin(alpha_a)
    y = axis_y - x_norm * math.sin(alpha_a) - y_norm * math.cos(alpha_a)
    return x, y


def ellipse_cosmic_body_motion(alpha_start, a, b, alpha_a, axis_x, axis_y, dt, period_of_rotation):
    if a * b == 0:
        return axis_x, axis_y, 0
    alpha_new = calculate_new_angle(alpha_start, dt, period_of_rotation)
    x, y = point_on_ellipse(alpha_new, a, b, alpha_a, axis_x, axis_y)
    return x, y, alpha_new


def calculate_speed(x_start, y_start, x_end, y_end, dt):
    delta = ((x_start - x_end) ** 2 + (y_start - y_end) ** 2) ** 0.5
    speed = delta * 1000 / dt   # pix/sec
    return speed


def calculate_remoteness(x, y, axis_x, axis_y):
    r = ((x - axis_x) ** 2 + (y - axis_y) ** 2) ** 0.5
    return r


if __name__ == '__main__':
    pass
import math


def circular_cosmic_body_motion(alpha, r, pivot_x, pivot_y, dt, period_of_rotation):
    if r == 0:
        return pivot_x, pivot_y, 0
    count = period_of_rotation * 1000 / dt
    delta_alpha = 2 * math.pi / count
    alpha_new = alpha + delta_alpha
    x = r * math.cos(alpha_new) + pivot_x
    y = pivot_y - r * math.sin(alpha_new)
    return x, y, alpha_new


def ellipse_cosmic_body_motion(alpha_start, a, b, alpha_a, pivot_x, pivot_y, dt, period_of_rotation):
    if a * b == 0:
        return pivot_x, pivot_y, 0
    count = period_of_rotation * 1000 / dt
    delta_alpha = 2 * math.pi / count
    alpha_new = alpha_start + delta_alpha
    x = a * math.cos(alpha_new) + pivot_x
    y = pivot_y + b * math.sin(alpha_new)
    return x, y, alpha_new



if __name__ == '__main__':
    pass
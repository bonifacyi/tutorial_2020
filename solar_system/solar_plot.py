import matplotlib.pyplot as mp


def plot_solar_stats(stat_x, stat_y, name='', name_x='', name_y='', title=''):
    if len(stat_y) != len(stat_x):
        min_len = min(len(stat_x), len(stat_y))
        stat_x = stat_x[:min_len]
        stat_y = stat_y[:min_len]

    mp.plot(stat_x, stat_y, label=name)
    mp.title(title)
    mp.xlabel(name_x)
    mp.ylabel(name_y)

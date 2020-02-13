import tkinter as tk
from abc import ABC, abstractmethod
from random import choice
import os, math, copy, numpy
from solar_system.solar_input import *
from solar_system.solar_model import *
from solar_system.solar_objects import *
from solar_system.solar_plot import *


class Agent(ABC):
    def __init__(self):
        self.job = None
        self.canvas = None

    @abstractmethod
    def start(self):
        self.job = self.canvas.after(DT, self.update)

    @abstractmethod
    def play(self):
        if self.job == 'pause':
            self.job = self.canvas.after(DT, self.update)

    @abstractmethod
    def stop(self):
        if self.job is not None:
            self.canvas.after_cancel(self.job)
            self.job = None

    @abstractmethod
    def pause(self):
        if self.job is not None and self.job != 'pause':
            self.canvas.after_cancel(self.job)
            self.job = 'pause'

    @abstractmethod
    def update(self):
        pass


class CosmicBody(Agent):
    def __init__(
            self,
            canvas,
            name,
            alpha_start,
            size_r,
            rotation_a,
            rotation_b,
            alpha_a,
            period_of_rotation,
            color=None,
            job_init=None,
            parent=None
    ):
        super().__init__()
        self.job = job_init
        self.canvas = canvas
        self.name = name
        self.alpha = alpha_start
        self.size_r = size_r
        self.pivot_x = WINDOW_SHAPE[0] / 2
        self.pivot_y = WINDOW_SHAPE[1] / 2
        self.rotation_a = rotation_a
        self.rotation_b = rotation_b
        self.alpha_a = alpha_a
        self.period_of_rotation = period_of_rotation
        self.parent = parent
        if color is None:
            self.color = choice(['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple'])
        else:
            self.color = color

        self.x, self.y = point_on_ellipse(
            self.alpha, self.rotation_a, self.rotation_b, self.alpha_a, self.pivot_x, self.pivot_y)
        self.speed = 0
        self.remoteness = 0
        self.time = 0

        self.stats = {
            'x': [self.x],
            'y': [self.y],
            'speed': [],
            'remoteness': [],
            'time': [self.time],
        }

        self.id = self.canvas.create_oval(
            self.x - self.size_r,
            self.y - self.size_r,
            self.x + self.size_r,
            self.y + self.size_r,
            fill=self.color
        )

    def start(self):
        super().start()

    def play(self):
        super().play()

    def stop(self):
        super().stop()

    def pause(self):
        super().pause()

    def update(self):
        x_start, y_start = self.x, self.y

        self.x, self.y, self.alpha = ellipse_cosmic_body_motion(
            self.alpha,
            self.rotation_a,
            self.rotation_b,
            self.alpha_a,
            self.pivot_x,
            self.pivot_y,
            DT,
            self.period_of_rotation
        )

        self.time += DT / 1000
        self.speed = calculate_speed(x_start, y_start, self.x, self.y, DT)
        self.remoteness = calculate_remoteness(self.x, self.y, self.pivot_x, self.pivot_y)
        self.add_parameters_to_stats()

        self.set_coord()
        self.job = self.canvas.after(DT, self.update)

    def set_coord(self):
        self.canvas.coords(
            self.id,
            self.x - self.size_r,
            self.y - self.size_r,
            self.x + self.size_r,
            self.y + self.size_r,
        )

    def destroy(self):
        self.stop()
        self.canvas.delete(self.id)

    def get_state(self):
        state = {
            'name': self.name,
            'alpha_start': self.alpha,
            'size_r': self.size_r,
            'rotation_a': self.rotation_a,
            'rotation_b': self.rotation_b,
            'alpha_a': self.alpha_a,
            'period_of_rotation': self.period_of_rotation,
            'color': self.color,
            'job': self.job is not None,
        }
        return state

    def add_parameters_to_stats(self):
        self.stats['x'].append(self.x)
        self.stats['y'].append(self.y)
        self.stats['speed'].append(self.speed)
        self.stats['remoteness'].append(self.remoteness)
        self.stats['time'].append(self.time)

    def get_parameters_from_stats(self):
        return self.stats


class SolarField(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, background='white')
        self.cosmic_objects = STATE_OBJECTS['solar_field']['cosmic_objects']
        self.planets = dict()

    def create_cosmic_objects(self):
        for value in self.cosmic_objects:
            name = value['name']
            size_r = value['r']
            alpha_start = 2 * math.pi * value['alpha_start'] / 360
            rotation_a = value['rotation_a']
            rotation_b = value['rotation_b']
            alpha_a = 2 * math.pi * value['alpha_a'] / 360
            period_of_rotation = NORMAL_PERIOD * value['period_of_rotation_in_days'] / 365
            color = '#{0:0^2x}{1:0^2x}{2:0^2x}'.format(*value['color'])
            parent = value['parent']
            if parent in None:
                obj = CosmicBody(
                    self, name, alpha_start, size_r, rotation_a, rotation_b, alpha_a, period_of_rotation, color
                )
                self.planets[obj.id] = obj

    def get_state(self):
        state = {
            'cosmic_objects': [pl.get_state() for pl in self.planets.values()]
        }
        return state

    def set_state(self, state, job_init):
        self.remove_planets()
        self.create_planets_from_state(state['cosmic_objects'], job_init)

    def create_planets_from_state(self, states, job_init):
        states = copy.deepcopy(states)
        for state in states:
            job_active = state.pop('job')
            obj = CosmicBody(self, **state, job_init=job_init if job_active else None)
            self.planets[obj.id] = obj

    def restart(self):
        self.stop()
        self.remove_planets()
        self.create_cosmic_objects()
        self.start()

    def start(self):
        for planet in self.planets.values():
            planet.start()

    def pause(self):
        for planet in self.planets.values():
            planet.pause()

    def play(self):
        for planet in self.planets.values():
            planet.play()

    def stop(self):
        for planet in self.planets.values():
            planet.stop()

    def remove_planets(self, planets_to_remove=None):
        if planets_to_remove is None:
            keys = list(self.planets)
        else:
            keys = list(planets_to_remove)
        for key in keys:
            self.planets[key].destroy()
            del self.planets[key]

    def get_history_stats(self):
        history_stats = dict()
        for planet in self.planets.values():
            stats = planet.get_parameters_from_stats()
            history_stats[planet.name] = dict()
            history_stats[planet.name]['x'] = stats['x']
            history_stats[planet.name]['y'] = stats['y']
            history_stats[planet.name]['speed'] = stats['speed']
        return history_stats

    def plot_speed_from_time(self):
        for planet in self.planets.values():
            stats = planet.get_parameters_from_stats()
            stat_x = stats['time']
            stat_y = stats['speed']
            name_x = 't, sec'
            name_y = 'V, pix/sec'
            title = 'Speed'
            plot_solar_stats(stat_x, stat_y, planet.name, name_x, name_y, title)
        mp.legend()
        mp.show()

    def plot_remoteness_from_time(self):
        for planet in self.planets.values():
            stats = planet.get_parameters_from_stats()
            stat_x = stats['time']
            stat_y = stats['remoteness']
            name_x = 't, sec'
            name_y = 'R, pix'
            title = 'Remoteness'
            plot_solar_stats(stat_x, stat_y, planet.name, name_x, name_y, title)
        mp.legend()
        mp.show()

    def plot_speed_from_remoteness(self):
        for planet in self.planets.values():
            stats = planet.get_parameters_from_stats()
            stat_x = stats['remoteness']
            stat_y = stats['speed']
            name_x = 'R, pix'
            name_y = 'V, pix/sec'
            title = 'Speed-Remoteness'
            plot_solar_stats(stat_x, stat_y, planet.name, name_x, name_y, title)
        mp.legend()
        mp.show()


class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.solar_field = SolarField(self)
        self.solar_field.pack(fill=tk.BOTH, expand=1)

    def get_state(self):
        state = {'solar_field': self.solar_field.get_state()}
        return state

    def set_state(self, state, job_init):
        self.solar_field.set_state(state['solar_field'], job_init)

    def new_solar_system(self):
        self.solar_field.restart()

    def pause(self):
        self.solar_field.pause()

    def play(self):
        self.solar_field.play()

    def stop(self):
        self.solar_field.stop()

    def plot_speed_from_time(self):
        self.solar_field.plot_speed_from_time()

    def plot_remoteness_from_time(self):
        self.solar_field.plot_remoteness_from_time()

    def plot_speed_from_remoteness(self):
        self.solar_field.plot_speed_from_remoteness()

    def get_history_stats(self):
        history_stats = self.solar_field.get_history_stats()
        return history_stats


class Menu(tk.Menu):
    def __init__(self, master):
        super().__init__(master)

        self.file_menu = tk.Menu(self)
        self.file_menu.add_command(label='save', command=self.master.save)
        self.file_menu.add_command(label='load', command=self.master.load)
        self.file_menu.add_command(label='save history', command=self.master.save_history)
        self.file_menu.add_command(label='exit', command=self.master.quit)
        self.add_cascade(label='file', menu=self.file_menu)

        self.main_menu = tk.Menu(self)
        self.main_menu.add_command(label='new', command=self.master.new_solar_system)
        self.main_menu.add_command(label='play', command=self.master.play)
        self.main_menu.add_command(label='pause', command=self.master.pause)
        self.main_menu.add_command(label='stop', command=self.master.stop)
        self.add_cascade(label="main menu", menu=self.main_menu)

        self.plot = tk.Menu(self)
        self.plot.add_command(label='plot speed-time', command=self.master.plot_speed_from_time)
        self.plot.add_command(label='plot remoteness-time', command=self.master.plot_remoteness_from_time)
        self.plot.add_command(label='plot speed-remoteness', command=self.master.plot_speed_from_remoteness)
        self.add_cascade(label='plot', menu=self.plot)


class SolarApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('{}x{}'.format(*WINDOW_SHAPE))

        self.save_dir = os.path.join(os.path.split(__file__)[0], 'save')

        self.main_frame = MainFrame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.menu = Menu(self.master)
        self.config(menu=self.menu)
        self.bind("<Control-s>", self.save)

    def save(self):
        self.pause()
        solar_system_state = self.get_state()
        write_space_objects_data_to_file(solar_system_state, self.save_dir)
        self.play()

    def load(self):
        self.pause()
        state = read_space_objects_data_from_file(self.save_dir)
        self.set_state(state)
        self.play()

    def save_history(self):
        self.pause()
        history_stats = self.main_frame.get_history_stats()
        write_space_objects_data_to_file(history_stats, self.save_dir)
        self.play()

    def get_state(self):
        return {'main_frame': self.main_frame.get_state()}

    def set_state(self, state, job_init='pause'):
        self.main_frame.set_state(state['main_frame'], job_init)

    def new_solar_system(self):
        self.main_frame.new_solar_system()

    def pause(self):
        self.main_frame.pause()

    def play(self):
        self.main_frame.play()

    def stop(self):
        self.main_frame.stop()

    def plot_speed_from_time(self):
        self.main_frame.plot_speed_from_time()

    def plot_remoteness_from_time(self):
        self.main_frame.plot_remoteness_from_time()

    def plot_speed_from_remoteness(self):
        self.main_frame.plot_speed_from_remoteness()

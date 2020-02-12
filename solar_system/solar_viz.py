import tkinter as tk
from abc import ABC, abstractmethod
from random import choice
import os, math
from solar_system.solar_input import *
from solar_system.solar_model import *
from solar_system.solar_objects import *


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
            alpha_start,
            size_r,
            rotation_a,
            rotation_b,
            alpha_a,
            period_of_rotation,
            color=None,
            job_init=None,

    ):
        super().__init__()
        self.job = job_init
        self.canvas = canvas
        self.alpha = alpha_start
        self.size_r = size_r
        self.pivot_x = WINDOW_SHAPE[0] / 2
        self.pivot_y = WINDOW_SHAPE[1] / 2
        self.rotation_a = rotation_a
        self.rotation_b = rotation_b
        self.alpha_a = alpha_a
        self.period_of_rotation = period_of_rotation
        if color is None:
            self.color = choice(['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple'])
        else:
            self.color = color

        self.x = rotation_a * math.cos(self.alpha) + self.pivot_x
        self.y = self.pivot_y - rotation_b * math.sin(self.alpha)
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
        self.x, self.y, self.alpha = ellipse_cosmic_body_motion(
            self.alpha,
            self.rotation_a,
            self.rotation_b,
            self.alpha_a,
            self.pivot_x, self.pivot_y,
            DT, self.period_of_rotation
        )
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


class SolarField(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, background='white')
        self.cosmic_objects = STATE_OBJECTS['solar_field']['cosmic_objects']
        self.planets = dict()

    def create_cosmic_objects(self):
        for key, value in self.cosmic_objects.items():
            size_r = value['r']
            alpha_start = 2 * math.pi * value['alpha_start'] / 360
            rotation_a = value['rotation_a']
            rotation_b = value['rotation_b']
            alpha_a = 2 * math.pi * value['alpha_a'] / 360
            period_of_rotation = SPEED * value['period_of_rotation_in_days'] / 365
            color = '#{0:0^2x}{1:0^2x}{2:0^2x}'.format(*value['color'])

            obj = CosmicBody(self, alpha_start, size_r, rotation_a, rotation_b, alpha_a, period_of_rotation, color)
            self.planets[key] = obj

    def get_state(self):
        return dict()

    def set_state(self, state, job_init):
        pass

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


class Menu(tk.Menu):
    def __init__(self, master):
        super().__init__(master)

        self.file_menu = tk.Menu(self)
        self.file_menu.add_command(label='save', command=self.master.save)
        self.file_menu.add_command(label='load', command=self.master.load)
        self.add_cascade(label='file', menu=self.file_menu)

        self.main_menu = tk.Menu(self)
        self.main_menu.add_command(label='new', command=self.master.new_solar_system)
        self.main_menu.add_command(label='play', command=self.master.play)
        self.main_menu.add_command(label='pause', command=self.master.pause)
        self.main_menu.add_command(label='stop', command=self.master.stop)
        self.main_menu.add_command(label='exit', command=self.master.quit)
        self.add_cascade(label="main menu", menu=self.main_menu)


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

WINDOW_SHAPE = (1000, 1000)     # pix
DT = 30         # milli sec
NORMAL_ROTATION_TIME = 30   # sec
STATE_OBJECTS = {
    'solar_field': {
        'cosmic_objects': {
            'solar': {
                'name': 'Solar',
                'alpha': 0,
                'r': 50,
                'rotation_r': 0,
                'period_of_rotation_in_days': 0,
                'color': (255, 255, 0),
            },
            'mercury': {
                'name': 'Mercury',
                'alpha': 0,
                'r': 4,
                'rotation_r': 70,
                'period_of_rotation_in_days': 88,
                'color': (237, 200, 100),
            },
            'venus': {
                'name': 'Venus',
                'alpha': 0,
                'r': 9,
                'rotation_r': 100,
                'period_of_rotation_in_days': 225,
                'color': (123, 235, 237),
            },
            'earth': {
                'name': 'Earth',
                'alpha': 0,
                'r': 10,
                'rotation_r': 130,
                'period_of_rotation_in_days': 365,
                'color': (5, 150, 180),
            },
            'mars': {
                'name': 'Mars',
                'alpha': 0,
                'r': 7,
                'rotation_r': 170,
                'period_of_rotation_in_days': 687,
                'color': (230, 140, 70),
            },
            'jupiter': {
                'name': 'Jupiter',
                'alpha': 0,
                'r': 30,
                'rotation_r': 230,
                'period_of_rotation_in_days': 4332,
                'color': (145, 130, 110),
            },
            'saturn': {
                'name': 'Saturn',
                'alpha': 0,
                'r': 25,
                'rotation_r': 300,
                'period_of_rotation_in_days': 10759,
                'color': (195, 185, 95),
            },
            'uranium': {
                'name': 'Uranium',
                'alpha': 0,
                'r': 18,
                'rotation_r': 350,
                'period_of_rotation_in_days': 30685,
                'color': (140, 200, 220),
            },
            'neptune': {
                'name': 'Neptune',
                'alpha': 0,
                'r': 18,
                'rotation_r': 400,
                'period_of_rotation_in_days': 60190,
                'color': (120, 133, 224),
            },
            'pluto': {
                'name': 'Pluto',
                'alpha': 0,
                'r': 3,
                'rotation_r': 440,
                'period_of_rotation_in_days': 90553,
                'color': (120, 133, 224),
            },
        }
    }
}

WINDOW_SHAPE = (1300, 1000)     # pix
AXIS_X = WINDOW_SHAPE[0] / 2
AXIS_Y = WINDOW_SHAPE[1] / 2
DT = 30         # milli sec
NORMAL_PERIOD = 10      # sec, real time for full rotation of earth
"""  """
STATE_OBJECTS = {
    'solar_field': {
        'cosmic_objects': {
            'Solar1': {
                'name': 'Solar',
                'alpha_start': 0,
                'r': 20,
                'rotation_a': 40,
                'rotation_b': 40,
                'alpha_a': 0,
                'period_of_rotation_in_days': 80,
                'color': (255, 255, 0),
                'parent': None,
                'sputnik': [],
            },
            'Solar2': {
                'name': 'Solar',
                'alpha_start': 180,
                'r': 20,
                'rotation_a': 40,
                'rotation_b': 40,
                'alpha_a': 0,
                'period_of_rotation_in_days': 80,
                'color': (255, 255, 0),
                'parent': None,
                'sputnik': [],
            },
            'Mercury': {
                'name': 'Mercury',
                'alpha_start': 0,
                'r': 6,
                'rotation_a': 200,
                'rotation_b': 100,
                'alpha_a': 45,
                'period_of_rotation_in_days': 150,
                'color': (237, 200, 100),
                'parent': None,
                'sputnik': [],
            },
            'Venus': {
                'name': 'Venus',
                'alpha_start': 0,
                'r': 9,
                'rotation_a': 160,
                'rotation_b': 150,
                'alpha_a': 0,
                'period_of_rotation_in_days': 225,
                'color': (123, 235, 237),
                'parent': None,
                'sputnik': [],
            },
            'Earth': {
                'name': 'Earth',
                'alpha_start': 0,
                'r': 10,
                'rotation_a': 190,
                'rotation_b': 180,
                'alpha_a': 0,
                'period_of_rotation_in_days': 365,
                'color': (5, 150, 180),
                'parent': None,
                'sputnik': ['Luna'],
            },
            'Mars': {
                'name': 'Mars',
                'alpha_start': 0,
                'r': 8,
                'rotation_a': 225,
                'rotation_b': 220,
                'alpha_a': 0,
                'period_of_rotation_in_days': 450,
                'color': (230, 140, 70),
                'parent': None,
                'sputnik': [],
            },
            'Jupiter': {
                'name': 'Jupiter',
                'alpha_start': 0,
                'r': 20,
                'rotation_a': 290,
                'rotation_b': 270,
                'alpha_a': 0,
                'period_of_rotation_in_days': 600,
                'color': (145, 130, 110),
                'parent': None,
                'sputnik': [],
            },
            'Saturn': {
                'name': 'Saturn',
                'alpha_start': 0,
                'r': 18,
                'rotation_a': 330,
                'rotation_b': 320,
                'alpha_a': 0,
                'period_of_rotation_in_days': 700,
                'color': (195, 185, 95),
                'parent': None,
                'sputnik': [],
            },
            'Uranium': {
                'name': 'Uranium',
                'alpha_start': 0,
                'r': 16,
                'rotation_a': 375,
                'rotation_b': 370,
                'alpha_a': 0,
                'period_of_rotation_in_days': 900,
                'color': (140, 200, 220),
                'parent': None,
                'sputnik': [],
            },
            'Neptune': {
                'name': 'Neptune',
                'alpha_start': 0,
                'r': 14,
                'rotation_a': 425,
                'rotation_b': 420,
                'alpha_a': 0,
                'period_of_rotation_in_days': 1000,
                'color': (120, 133, 224),
                'parent': None,
                'sputnik': [],
            },
            'Pluto': {
                'name': 'Pluto',
                'alpha_start': 0,
                'r': 5,
                'rotation_a': 530,
                'rotation_b': 470,
                'alpha_a': 30,
                'period_of_rotation_in_days': 1100,
                'color': (120, 133, 224),
                'parent': None,
                'sputnik': [],
            },
            'Luna': {
                'name': 'Luna',
                'alpha_start': 0,
                'r': 4,
                'rotation_a': 20,
                'rotation_b': 20,
                'alpha_a': 0,
                'period_of_rotation_in_days': 30,
                'color': (120, 133, 133),
                'parent': 'Earth',
                'sputnik': [],
            },
        },
    },
}

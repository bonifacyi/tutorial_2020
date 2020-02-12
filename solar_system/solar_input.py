from tkinter import filedialog
import os
import json


def write_space_objects_data_to_file(state, save_dir):
    file_name = get_save_file_name(save_dir)
    if file_name is not None:
        with open(file_name, 'w') as file:
            json.dump(state, file, indent=2)


def read_space_objects_data_from_file(save_dir):
    file_name = get_load_file_name(save_dir)
    if file_name is not None:
        with open(file_name, 'r') as file:
            state = json.load(file)
        return state


def get_save_file_name(save_dir):
    os.makedirs(save_dir, exist_ok=True)
    file_name = filedialog.asksaveasfilename(
        initialdir=save_dir,
        title='Save state',
        filetypes=(("json files", "*.json"), ("all files", "*.*"))
    )
    if file_name in [(), '']:
        return None
    return file_name


def get_load_file_name(save_dir):
    file_name = filedialog.askopenfilename(
        initialdir=save_dir,
        title='Load state',
        filetypes=(("json files", "*.json"), ("all files", "*.*"))
    )
    if file_name in [(), '']:
        return None
    return file_name

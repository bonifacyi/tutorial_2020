#!/usr/bin/env python

import tkinter as tk


def canvas_click_handler(event):
    print('Coordinates: x=', event.x, 'y=', event.y)


def main():
    global root, canvas
    global x, y, z
    root = tk.Tk()
    canvas = tk.Canvas(root)
    canvas.pack()
    canvas.bind('<Button-1>', canvas_click_handler)



    root.mainloop()


if __name__ == '__main__':
    main()
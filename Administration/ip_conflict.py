#!/usr/bin/env python

import openpyxl
import sys


def file_parse(path):
    table = openpyxl.load_workbook(filename=path)
    sheet = table.worksheets[0]
    array = dict()
    for row in sheet:
        for elem in row:
            if elem.value:
                array[elem.coordinate] = elem.value
    return array


def check_double(arr, exc):
    array = dict(arr)
    for key, element in array.items():
        i = 0
        for val in array.values():
            if element == val:
                i += 1
        if i > 1 and element not in exc:
            print(key, ':', element)


if len(sys.argv) == 1:
    print('xls or xlsx file necessary.')
    exit()
else:
    file_path = sys.argv[1]
file = file_parse(file_path)
exception = list()
if len(sys.argv) > 2:
    for i in range(2, len(sys.argv)):
        exception.append(sys.argv[i])


check_double(file, exception)

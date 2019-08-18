#! /usr/bin/env python
# Usage: py.exe spreadsheet_to_text_files.py <workbook>

from openpyxl.utils import get_column_letter as gcl
import openpyxl
import sys


if len(sys.argv) == 2:
    file = sys.argv[1]
else:
    file = input('Enter workbook path:\n> ')

wb = openpyxl.load_workbook(file)
ws = wb.active


for index, col in enumerate(ws.columns, start=1):
    with open(f'Column {gcl(index)}.txt', 'w') as file:
        for cell in col:
            file.write(f'{cell.value}\n')
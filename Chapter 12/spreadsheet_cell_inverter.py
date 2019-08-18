#! /usr/bin/env python
# Usage: py.exe spreadsheet_cell_inverter.py <workbook>

import openpyxl
import sys


if len(sys.argv) == 2:
    file = sys.argv[1]
else:
    file = input('Enter Workbook path:\n> ')


wb = openpyxl.load_workbook(file)
ws = wb.active
ws2 = wb.create_sheet()  # create empty worksheet

\
for row in range(1, ws.max_row + 1):
    for col in range(1, ws.max_column + 1):
        # copy inverted rows and columns to new worksheet
        ws2.cell(row=col, column=row,
                 value=ws.cell(row=row, column=col).value)

# delete old worksheet
wb.remove(ws)
# rename new worksheet with old worksheet's title
ws2.title = ws.title

wb.save(file)

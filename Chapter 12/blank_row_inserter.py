#! /usr/bin/env python
# Usage: py.exe blank_row_inserter.py <index row> <number of rows> <.xlsx file>

import openpyxl
import sys


if len(sys.argv) == 4:
    file = sys.argv[3]
    index_row = int(sys.argv[1])
    num_rows = int(sys.argv[2])

    print('Selecting file...')
    wb = openpyxl.load_workbook(file)
    ws = wb.active
    print('Adding rows...')
    for _ in range(num_rows):
        ws.insert_rows(index_row)

    print('Saving file...')
    wb.save(sys.argv[3])
    print('Done.')
else:
    raise Exception('Not enough arguments.')
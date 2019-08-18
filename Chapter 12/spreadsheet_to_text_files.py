#! /usr/bin/env python

from openpyxl.utils import get_column_letter as gcl
import openpyxl


wb = openpyxl.load_workbook('(inverted).xlsx')
ws = wb.active


for index, col in enumerate(ws.columns, start=1):
    with open(f'Column {gcl(index)}.txt', 'w') as file:
        for cell in col:
            print(cell.value)
            file.write(f'{cell.value}\n')
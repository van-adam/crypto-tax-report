from openpyxl.styles import Font, Alignment
from openpyxl.worksheet.dimensions import ColumnDimension
from openpyxl.worksheet.worksheet import Worksheet


def add_row(sheet: Worksheet, row_num: int, bold: bool, alignment: str, *cell_values: object) -> None:
    col_num = 1
    for value in cell_values:
        cell = sheet.cell(row_num, col_num, value)
        cell.font = Font(bold=bold)
        cell.alignment = Alignment(horizontal=alignment)
        col_num += 1


def autosize_columns(ws: Worksheet):
    dim_holder = ws.column_dimensions

    for column_cells in ws.columns:
        width = max(len(str(column_cell.value)) for column_cell in column_cells)
        dim_holder[column_cells[0].column] = ColumnDimension(ws, index=column_cells[0].column_letter, width=width)

    ws.column_dimensions = dim_holder

from openpyxl.cell import Cell
from openpyxl.styles import Font, Alignment
from openpyxl.worksheet.dimensions import ColumnDimension
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import numbers


def add_row(sheet: Worksheet, row_num: int, bold: bool, alignment: str, *cell_values: object) -> None:
    """
    Adds a row of contents to the passed worksheet.

    :param sheet: the sheet to add the row to
    :param row_num: the row number to add the row at
    :param bold: whether the content should be bold
    :param alignment: whether the content should be right-left or left-aligned
    :param cell_values: the contents
    """
    col_num = 1
    for value in cell_values:
        cell: Cell = sheet.cell(row_num, col_num, value)
        cell.font = Font(bold=bold)
        cell.alignment = Alignment(horizontal=alignment)

        if isinstance(value, float):
            cell.number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1
        col_num += 1


def autosize_columns(sheet: Worksheet) -> None:
    """
    Resizes the columns of the passed worksheet to fit the content inside the cells of the columns.
    
    :param sheet: the worksheet to autosize
    """
    dim_holder = sheet.column_dimensions

    for column_cells in sheet.columns:
        width = max(len(str(column_cell.value)) for column_cell in column_cells)
        dim_holder[column_cells[0].column] = ColumnDimension(sheet, index=column_cells[0].column_letter, width=width)

    sheet.column_dimensions = dim_holder

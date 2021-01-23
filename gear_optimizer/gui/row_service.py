import tkinter as tk


def show_row(title, fields, row_number, root):
    entries = {}
    column = 1
    tk.Label(root, text=title).grid(row=row_number)

    for field in fields:
        tk.Label(root, text=f'{field}:').grid(row=row_number, column=column)
        entry = tk.Entry(root)
        entry.grid(row=row_number, column=column + 1)
        entry.insert(0, fields[field])
        entries[field] = entry
        column += 2
    return entries


def read_fields(user_input_fields):
    return _read_and_transform_field(user_input_fields, _get_as_string)


def read_int_fields(user_input_fields):
    return _read_and_transform_field(user_input_fields, _get_as_integer)


def _read_and_transform_field(user_input_fields, transformation):
    values = {}
    for field in user_input_fields:
        values[field] = transformation(user_input_fields[field])
    return values


def _get_as_string(field):
    return field.get()


def _get_as_integer(field):
    return int(field.get())

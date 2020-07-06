import os
import sys
import pprint

pp = pprint.PrettyPrinter(indent=4)

# def search_tables(s):

tables = []
max_qty = 0

def init():
    global tables
    global max_qty

    tables = []
    max_qty = 0

def search_var(var):
    # 後ろからsearchするべき説
    global tables
    global max_qty

    for col in tables:
        if col["op"] == var:
            return col

    max_qty += 1
    new_col = {}
    new_col["Qty"] = max_qty
    new_col["op"] = var
    tables.append(new_col)

    return new_col;

def search_num(num):
    global tables
    global max_qty

    for col in tables:
        if col["op"] == "lit" and col["opd1"] == num:
            return col

    max_qty += 1
    new_col = {}
    new_col["Qty"] = max_qty
    new_col["op"] = "lit"
    new_col["opd1"] = num
    tables.append(new_col)

    return new_col;

def search_str(some_str):
    if some_str.isdecimal():
        col = search_num(some_str)
    else:
        col = search_var(some_str)
    return col

def search_col(target_col):
    global tables
    global max_qty

    for col in tables:
        if col["op"] == target_col["op"] and \
                col["opd1"] == target_col["opd1"] and \
                col["opd2"] == target_col["opd2"]:
            return col


def do_mov(args):
    global tables
    global max_qty

    print("mov", args[0], args[1])

    col1 = search_str(args[0])

    new_col = {}
    new_col["Qty"] = col1["Qty"]
    new_col["op"] = args[1]
    new_col["opd1"] = col1["Qty"]
    tables.append(new_col)

def do_add(args):
    global tables
    global max_qty

    print("add", args[0], args[1], args[2])

    col1 = search_str(args[0])
    col2 = search_str(args[1])

    col_for_calc = {}
    col_for_calc["op"] = "Add"
    col_for_calc["opd1"] = col1["Qty"]
    col_for_calc["opd2"] = col2["Qty"]

    col_for_calc = search_col(col_for_calc)
    if not col_for_calc:
        max_qty += 1
        col_for_calc = {}
        col_for_calc["Qty"] = max_qty
        col_for_calc["op"] = "Add"
        col_for_calc["opd1"] = col1["Qty"]
        col_for_calc["opd2"] = col2["Qty"]
        tables.append(col_for_calc)
    else:
        print("Common subexpression elimination")
        tables.append(col_for_calc)
        pass

    col_for_opd3 = {}
    col_for_opd3["Qty"] = col_for_calc["Qty"]
    col_for_opd3["op"] = args[2]
    col_for_opd3["opd1"] = col_for_calc["Qty"]

    tables.append(col_for_opd3)

def print_tables():
    print("=" * 26 + " tables " + "=" * 26)
    for col in tables:
        print(col)
    print("=" * 60)

def main(args):
    global tables
    global max_qty

    init()

    filename = args[0]
    with open(filename) as f:
        lines = f.readlines()

    print(lines)

    for line in lines:
        if line.startswith("mov"):
            do_mov(line.rstrip("\n").split(" ")[1:])
        if line.startswith("add"):
            do_add(line.rstrip("\n").split(" ")[1:])
        print_tables()
        

if __name__ == "__main__":
    main(sys.argv[1:])

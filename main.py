import os
import sys
import pprint

pp = pprint.PrettyPrinter(indent=4)

# def search_tables(s):

tables = []
max_qty = 0

def init():
    tables = []
    max_qty = 0

def search_col_for_target_var(var):
    for col in reversed(tables):
        if col["op"] == var:
            return col

    return None;

def search_col_for_target_num(num):
    for col in reversed(tables):
        if col["op"] == "lit" and col["opd1"] == num:
            return col

    return None;

def search_or_newly_create_col(some_str):
    global max_qty

    if some_str.isdecimal():
        col = search_col_for_target_num(some_str)
        if not col:
            max_qty += 1
            new_col = {}
            new_col["Qty"] = max_qty
            new_col["op"] = "lit"
            new_col["opd1"] = some_str
            tables.append(new_col)
            col = new_col
    else:
        col = search_col_for_target_var(some_str)
        if not col:
            max_qty += 1
            new_col = {}
            new_col["Qty"] = max_qty
            new_col["op"] = some_str
            tables.append(new_col)
            col = new_col

    return col

def search_col(target_col, op):
    for col in reversed(tables):
        if col["op"] == target_col["op"] and \
                col["opd1"] == target_col["opd1"] and \
                col["opd2"] == target_col["opd2"]:
            return col
        # For commutativity
        if op in ["add", "mul"] and \
                col["op"] == target_col["op"] and \
                col["opd1"] == target_col["opd2"] and \
                col["opd2"] == target_col["opd1"]:
            return col
    
    return None

def do_mov(args):
    global tables
    global max_qty

    print("mov", args[0], args[1])

    col1 = search_or_newly_create_col(args[0])

    new_col = {}
    new_col["Qty"] = col1["Qty"]
    new_col["op"] = args[1]
    new_col["opd1"] = col1["Qty"]
    tables.append(new_col)

def do_arithmetic(args, op):
    global tables
    global max_qty

    print(op, args[0], args[1], args[2])

    col1 = search_or_newly_create_col(args[0])
    col2 = search_or_newly_create_col(args[1])

    col_for_calc = {}
    col_for_calc["op"] = op
    col_for_calc["opd1"] = col1["Qty"]
    col_for_calc["opd2"] = col2["Qty"]

    col_for_calc = search_col(col_for_calc, op)
    if not col_for_calc:
        max_qty += 1
        col_for_calc = {}
        col_for_calc["Qty"] = max_qty
        col_for_calc["op"] = op
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
        elif line.startswith("add"):
            do_arithmetic(line.rstrip("\n").split(" ")[1:], "add")
        elif line.startswith("sub"):
            do_arithmetic(line.rstrip("\n").split(" ")[1:], "sub")
        elif line.startswith("mul"):
            do_arithmetic(line.rstrip("\n").split(" ")[1:], "mul")
        print_tables()
        

if __name__ == "__main__":
    main(sys.argv[1:])

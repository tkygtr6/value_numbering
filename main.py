import os
import sys
import pprint

pp = pprint.PrettyPrinter(indent=4)

OPS = ["mov", "add", "sub", "mul"]

Qty_dict = {}
tables = []
max_qty = 0

def init():
    tables = []
    max_qty = 0

def append_tables(col):
    tables.append(col)
    if not col["Qty"] in Qty_dict.keys():
        if col["op"] == "lit":
            Qty_dict[col["Qty"]] = col["opd1"]
        elif col["op"] not in OPS:
            Qty_dict[col["Qty"]] = col["op"]

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
            append_tables(new_col)
            col = new_col
    else:
        col = search_col_for_target_var(some_str)
        if not col:
            max_qty += 1
            new_col = {}
            new_col["Qty"] = max_qty
            new_col["op"] = some_str
            append_tables(new_col)
            col = new_col

    return col

def search_col(op, opd1, opd2):
    for col in reversed(tables):
        if col["op"] == op and \
                col["opd1"] == opd1 and \
                col["opd2"] == opd2:
            return col
        # For commutativity
        if op in ["add", "mul"] and \
                col["op"] == op and \
                col["opd1"] == opd2 and \
                col["opd2"] == opd1:
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
    append_tables(new_col)

def do_arithmetic(args, op):
    global tables
    global max_qty

    is_CSE = False

    col1 = search_or_newly_create_col(args[0])
    col2 = search_or_newly_create_col(args[1])

    col_for_calc_result = search_col(op, col1["Qty"], col2["Qty"])
    if col_for_calc_result:
        print("Common subexpression elimination")
        is_CSE = True
        append_tables(col_for_calc_result)
    else:
        max_qty += 1
        col_for_calc_result = {}
        col_for_calc_result["Qty"] = max_qty
        col_for_calc_result["op"] = op
        col_for_calc_result["opd1"] = col1["Qty"]
        col_for_calc_result["opd2"] = col2["Qty"]
        append_tables(col_for_calc_result)

    col_for_opd3 = {}
    col_for_opd3["Qty"] = col_for_calc_result["Qty"]
    col_for_opd3["op"] = args[2]
    col_for_opd3["opd1"] = col_for_calc_result["Qty"]
    append_tables(col_for_opd3)

    if is_CSE:
        for col in reversed(tables):
            if col["Qty"] == col_for_opd3["opd1"] and \
                    col["op"] not in OPS:
                print("mov", Qty_dict[col["opd1"]], args[2])
                return
    print(op, args[0], args[1], args[2])


def print_tables():
    print("=" * 26 + " tables " + "=" * 26)
    for col in tables:
        print(col)
    print("=" * 60)

def main(args):
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

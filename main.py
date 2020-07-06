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
    var_dict = {}
    var_dict["Qty"] = max_qty
    var_dict["op"] = var
    tables.append(var_dict)

    return var_dict;

def search_num(num):
    global tables
    global max_qty

    for col in tables:
        if col["op"] == "lit" and col["opd1"] == num:
            return col

    max_qty += 1
    var_dict = {}
    var_dict["Qty"] = max_qty
    var_dict["op"] = "lit"
    var_dict["opd1"] = num
    tables.append(var_dict)

    return var_dict;

def search_col(some_str):
    if some_str.isdecimal():
        col = search_num(some_str)
    else:
        col = search_var(some_str)
    return col


def do_mov(args):
    global tables
    global max_qty

    print(args[0], args[1])

    col1 = search_col(args[0])

    var_dict = {}
    var_dict["Qty"] = col1["Qty"]
    var_dict["op"] = args[1]
    var_dict["opd1"] = col1["Qty"]
    tables.append(var_dict)

def print_tables():
    print("=" * 26 + " tables " + "=" * 26)
    for col in tables:
        print(col)
    print("=" * 60)

def main(args):
    global tables
    global max_qty

    init()

    filename = os.path.join("inputs", args[0])
    with open(filename) as f:
        lines = f.readlines()

    print(lines)

    for line in lines:
        if line.startswith("mov"):
            do_mov(line.rstrip("\n").split(" ")[1:])
        print_tables()
        

if __name__ == "__main__":
    main(sys.argv[1:])

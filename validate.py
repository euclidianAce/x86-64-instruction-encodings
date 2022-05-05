#!/usr/bin/env python3

import csv
from sys import argv

class tsv(csv.Dialect):
    delimiter = '\t'
    doublequote = None
    escapechar = None
    lineterminator = '\n'
    quotechar = None
    quoting = csv.QUOTE_NONE
    skipinitialspace = None

first_row = ['Opcode', 'Operand1', 'Operand2', 'Operand3', 'Operand4', 'Modifier', 'ForcedPrefix']

exit_code = 0
errors = []

# TODO: check mutual exclusivity for groups
valid_prefixes = [
    # group 1
    0xF0,
    0xF2,
    0xF3,

    # group 2
    0x2E,
    0x36,
    0x3E,
    0x26,
    0x64,
    0x65,

    # group 3
    0x66,

    # group 4
    0x67,
]

valid_registers = [
    'al', 'ax', 'eax', 'rax',
    'cl', 'cx', 'ecx', 'rcx',
    'dl', 'dx', 'edx', 'rdx',
    'bl', 'bx', 'ebx', 'rbx',
    'ah', 'sp', 'esp', 'rsp',
    'ch', 'bp', 'ebp', 'rbp',
    'dh', 'si', 'esi', 'rsi',
    'bh', 'di', 'edi', 'rdi',
    'r8l', 'r8w', 'r8d', 'r8',
    'r9l', 'r9w', 'r9d', 'r9',
    'r10l', 'r10w', 'r10d', 'r10',
    'r11l', 'r11w', 'r11d', 'r11',
    'r12l', 'r12w', 'r12d', 'r12',
    'r13l', 'r13w', 'r13d', 'r13',
    'r14l', 'r14w', 'r14d', 'r14',
    'r15l', 'r15w', 'r15d', 'r15',
]

valid_addressing_methods = [
    'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S',
    'U', 'V', 'W', 'X', 'Y',
    '%',
]

valid_operand_types = [
    'a', 'b', 'c', 'd', 'dq',
    'p', 'pd', 'pi', 'ps', 'q',
    'qq', 's', 'sd', 'ss', 'si',
    'v', 'w', 'x', 'y', 'z',
]

valid_modifiers = ['0', '1', '2', '3', '4', '5', '6', '7', 'r']

def add_error(file_name, msg):
    global exit_code
    global errors
    exit_code = 1
    errors += [file_name + ": " + msg]

def validate_operand(file_name, operand):
    if operand == None:
        add_error(file_name, "Missing an Operand field")
        return
    elif operand == '':
        return

    if operand[0] == '$':
        register_name = operand[1:]
        if register_name not in valid_registers:
            add_error(file_name, "Invalid register name '%s'" % register_name)
        return
    addr_method = operand[0]
    if addr_method not in valid_addressing_methods:
        add_error(file_name, "Invalid addressing method '%s'" % addr_method)

    if len(operand) < 2:
        if addr_method != 'M':
            add_error(file_name, "Missing operand type")
        return

    op_type = operand[1:]
    if op_type not in valid_operand_types:
        add_error(file_name, "Invalid operand type '%s'" % op_type)

def validate_modifier(file_name, modifier):
    if modifier == None:
        add_error(file_name, "Missing field 'Modifier'")
        return
    elif modifier == '':
        return

    if modifier[0] != '/':
        add_error(file_name, "modifier (%s) should begin with a slash" % modifier)
        return
    if len(modifier) != 2:
        add_error(file_name, "modifier (%s) should only be 2 characters" % modifier)
        return
    if modifier[1] not in valid_modifiers:
        add_error(file_name, "modifier should be one of " + repr(valid_modifiers))
        return

def validate_forced_prefix(file_name, prefix_str):
    if prefix_str == None:
        add_error(file_name, "Missing field 'ForcedPrefix'")
        return
    elif prefix_str == '':
        return

    try:
        prefix = int(prefix_str, 16)
        if prefix not in valid_prefixes:
            add_error(file_name, "Invalid ForcedPrefix: %s is not a valid prefix, should be one of " + repr(valid_prefixes));
    except ValueError:
        add_error(file_name, "ForcedPrefix %s is not a valid hex number" % op)

def validate_file(file_name):
    with open(file_name, "r") as file:
        reader = csv.DictReader(file, first_row, dialect=tsv)
        head = reader.__next__()

        global errors
        initial_len = len(errors)

        for key, val in head.items():
            if val == None:
                add_error(file_name, "Missing header '%s'" % key)
            elif key != val:
                add_error(file_name, "Expected header '%s', got '%s'" % (key, val))

        if initial_len != len(errors):
            return

        for row in reader:
            if row['Opcode'] == None:
                add_error(file_name, "Opcode is missing")
            for op in row['Opcode'].split(','):
                try: int(op, 16)
                except ValueError:
                    add_error(file_name, "Opcode %s is not a valid hex number" % op)
            validate_operand(file_name, row['Operand1'])
            validate_operand(file_name, row['Operand2'])
            validate_operand(file_name, row['Operand3'])
            validate_operand(file_name, row['Operand4'])
            validate_modifier(file_name, row['Modifier'])
            validate_forced_prefix(file_name, row['ForcedPrefix'])

if __name__ == '__main__':
    for file_name in argv[1:]:
        if file_name.startswith("encodings/") and file_name.endswith(".tsv"):
            l = len(errors)
            validate_file(file_name)
            if l == len(errors):
                print(file_name + ": Ok!")
    for e in errors:
        print(e)
    exit(exit_code)

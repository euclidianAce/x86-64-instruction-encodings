#!/usr/bin/env python3

import csv
import re
from sys import argv
from typing import Optional, Tuple

class tsv(csv.Dialect):
    delimiter = '\t'
    doublequote = True
    escapechar = None
    lineterminator = '\n'
    quotechar = None
    quoting = csv.QUOTE_NONE
    skipinitialspace = False

first_row = ["Opcode", "Operand1", "Operand2", "Operand3", "Operand4", "OperandEncoding", "Extra", "ForcedPrefix", "Support"]
exit_code = 0
errors = []

def add_error(prefix: str, msg: str):
    global exit_code
    global errors
    exit_code = 1
    errors += [prefix + ": " + msg]

def is_hex_byte(field: str) -> Tuple[bool, str]:
    try:
        value = int(field, 16)
        if value < 0 or value > 255:
            return (False, "Value out of range [0,FF]")
        return (True, "")
    except:
        return (False, "Not a valid hex integer")

def validate_opcode(error_prefix: str, field: str):
    if field == "":
        add_error(error_prefix, "Missing Opcode")
        return

    extension = None

    if field[-1] == '+':
        field = field[0:-1]

    slash_index = field.find('/')
    if slash_index != -1:
        extension = field[slash_index + 1:]
        field = field[0:slash_index]

    for n in field.split(","):
        ok, reason = is_hex_byte(n)
        if not ok:
            add_error(error_prefix, f"Invalid Opcode '{n}': {reason}")

    if extension:
        try:
            value = int(extension, 10)
            if value < 0 or value > 7:
                add_error(error_prefix, f"Opcode extension must be within [0,7], got {value}")
        except ValueError:
            add_error(error_prefix, f"Invalid Opcode extension {extension}")

def validate_operand(error_prefix: str, field: str):
    if field == "":
        return

    valid_operands = [
        "m",
        "rm8",
        "rm16",
        "rm32",
        "rm64",
        "r8",
        "r16",
        "r32",
        "r64",
        "Sreg",
        "cl",
        "cx",
        "ecx",
        "rcx",
        "al",
        "ax",
        "eax",
        "rax",
        "cs",
        "ss",
        "ds",
        "es",
        "fs",
        "gs",
        "moffs8",
        "moffs16",
        "moffs32",
        "moffs64",
        "imm8",
        "imm16",
        "imm32",
        "imm64",
        "ptr16:16",
        "ptr16:32",
        "m16:16",
        "m16:32",
        "m16:64",
        "rel8",
        "rel16",
        "rel32",
        "1",
    ]

    valid_attributes = [ "Signed", "Unsigned" ]

    xs = [x for x in field.split(',')]
    if len(xs) > 2:
        add_error(error_prefix, "Too many fields in operand")

    if xs[0] not in valid_operands:
        add_error(error_prefix, f"Invalid operand '{xs[0]}'")

    if len(xs) > 1 and xs[1] not in valid_attributes:
        add_error(error_prefix, f"Invalid operand attribute '{xs[1]}'")

def validate_operand_encoding(error_prefix: str, field: str):
    valid_operand_encodings = [
        "RMI",
        "RM", "MR", "FD", "TD", "OI", "MI", "MC", "M1",
        "O", "M", "I", "D", "S",
        "ZO"
    ]
    if field not in valid_operand_encodings:
        add_error(error_prefix, f"'{field}' is not a valid operand encoding")

def validate_extra(error_prefix: str, field: str):
    valid_extras = [ "OperandSizeOverride", "REX", "REX.W" ]

    if field == "":
        return

    for ex in field.split(','):
        if ex not in valid_extras:
            add_error(error_prefix, f"Invalid Extra '{ex}'")

def validate_forced_prefix(error_prefix: str, field: str):
    if field == "":
        return

    ok, reason = is_hex_byte(field)
    if not ok:
        add_error(error_prefix, f"Invalid ForcedPrefix '{field}': {reason}");

def validate_support(error_prefix: str, field: str):
    xs = [x for x in field.split(',')]
    if len(xs) != 2:
        add_error(error_prefix, f"Invalid Support: expected exactly 2 fields, got {len(xs)}")
        return

    valid_64 = [ "V", "I", "NE", "NP", "NI", "NS" ]
    valid_legacy = [ "V", "I", "NE" ]

    if xs[0] not in valid_64:
        add_error(error_prefix, f"Invalid 64-bit Support field: {xs[0]}")

    if xs[1] not in valid_legacy:
        add_error(error_prefix, f"Invalid legacy Support field: {xs[1]}")

def validate_file(file_name: str):
    with open(file_name, "r") as file:
        # TODO: report line numbers in errors
        reader = csv.DictReader(file, first_row, dialect=tsv)
        head = reader.__next__()

        global errors

        initial_len = len(errors)

        for key, val in head.items():
            if val is None:
                add_error(file_name, f"Missing header '{key}'")
            elif key != val:
                add_error(file_name, f"Expected header '{key}', got '{val}'")

        if initial_len != len(errors):
            return

        for row in reader:
            if row['Opcode'] is None:
                add_error(file_name, "Opcode is missing")
                continue

            validate_opcode(file_name, row['Opcode'])
            validate_operand(file_name, row['Operand1'])
            validate_operand(file_name, row['Operand2'])
            validate_operand(file_name, row['Operand3'])
            validate_operand(file_name, row['Operand4'])
            validate_operand_encoding(file_name, row['OperandEncoding'])
            validate_extra(file_name, row['Extra'])
            validate_forced_prefix(file_name, row['ForcedPrefix'])
            validate_support(file_name, row['Support'])

if __name__ == '__main__':
    for file_name in argv[1:]:
        l = len(errors)
        validate_file(file_name)
        if l == len(errors):
            print(file_name + ": Ok!")
    for e in errors:
        print(e)
    exit(exit_code)

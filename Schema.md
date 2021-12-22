In the `encodings` folder there are `tsv` files named for each (currently transcribed) instruction encoding.

The first row contains the names of the fields
---
 - Opcode
   The hexadecimal opcode for the instruction. May be up to 3 comma separated bytes.


 - Operand1, Operand2, Operand3, Operand4
   The encodings of the operands to the instruction.

   Unused operands will be encoded with an empty cell. (This can be used to count the number of operands an instruction has)

   The format of these encodings is the same as described in the `Intel® 64 and IA-32 Architectures Software Developer’s Manual`, Volume 2, Appendix A.2.1 and A.2.2, but with the following additional notation:
    - `%`: The operand is a general register and the lower 3 bits of the register id (given in `registers.tsv`) is added to the opcode. For registers with id >=8 (i.e. `r8`-`r15`) the 4th bit is encoded in the `REX` prefix.
    - `$`: Followed by a specific register name means that this instruction only operates on this register for this encoding

 - Modifier
    Additional encoding information not present in the Opcode nor Operands.

    The format is the same as described in the `Intel® 64 and IA-32 Architectures Software Developer’s Manual Volume 2` in Chapter `3.1.1.1`. A summary is provided here for convenience.
     - `/0`, `/1`, `/2`, `/3`, `/4`, `/5`, `/6` `/7`: The 3 `reg` bits of the ModRM byte are an extension of the opcode, rather than an operand. The extension is given by the digit after the slash. i.e. `/3` -> `reg = 0b011`.

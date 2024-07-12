# Conditional Instructions (`Jcc`, `SETcc`, `MOVcc`, etc.)

Conditional instruction mnemonics will often describe the same underlying
instruction (e.g. `jnbe` (jump if not below or equal) is the same as `ja` (jump
if above)). This document enumerates each condition that is tested and each
mnemonic that tests it.

# `above` vs `greater` etc.
Certain flags will be described with words that appear to mean the same thing,
such as `above` and `greater`, or `below` and `less`. These refer to the signed
and unsigned comparisons as outlined in the table below:

| word    | signedness |
|---------|------------|
| above   | unsigned   |
| below   | unsigned   |
| greater | signed     |
| less    | signed     |

# Flags

| Abbreviation | Meaning       |
|--------------|---------------|
| `CF`         | Carry Flag    |
| `ZF`         | Zero Flag     |
| `SF`         | Sign Flag     |
| `OF`         | Overflow Flag |
| `PF`         | Parity Flag   |

# Conditions

## Mnemonics with corresponding `encodings/*.tsv` files

Conditional instructions will only have `encodings/*.tsv` files for the first column in this table.

| Instruction Suffix and Meaning | Alternative 1              | Alternative 2              | Offset Added to Opcode |
| -----------------------------  | -------------------------  | -------------------------- | ---------------------- |
| `o`   Overflow                 |                            |                            | 0                      |
| `no`  Not Overflow             |                            |                            | 1                      |
| `c`   Carry                    | `b`   Below                | `nae` Not Above or Equal   | 2                      |
| `nc`  Not Carry                | `nb`  Not Below            | `ae`  Above or Equal       | 3                      |
| `z`   Zero                     | `e`   Equal                |                            | 4                      |
| `nz`  Not Zero                 | `ne`  Not Equal            |                            | 5                      |
| `be`  Below or Equal           | `na`  Not Above            |                            | 6                      |
| `a`   Above                    | `nbe` Not Below or Equal   |                            | 7                      |
| `s`   Sign                     |                            |                            | 8                      |
| `ns`  Not Sign                 |                            |                            | 9                      |
| `p`   Parity                   | `pe`  Parity Even          |                            | 10                     |
| `np`  Not Parity               | `po`  Parity Odd           |                            | 11                     |
| `l`   Less                     | `nge` Not Greater or Equal |                            | 12                     |
| `ge`  Greater or Equal         | `nl`  Not Less             |                            | 13                     |
| `le`  Less or Equal            | `ng`  Not Greater          |                            | 14                     |
| `g`   Greater                  | `nle` Not Less or Equal    |                            | 15                     |

## Conditions with mnemonics
 - `CF` = 0
   - `nc` (not carry)
   - `nb` (not below)
   - `ae` (above or equal)

 - `CF` = 1
   - `c` (carry)
   - `b` (below)
   - `nae` (not above or equal)

 - `ZF` = 0
   - `nz` (not zero)
   - `ne` (not equal)

 - `ZF` = 1
   - `z` (zero)
   - `e` (equal)

 - `SF` = 0
   - `ns` (not sign)

 - `SF` = 1
   - `s` (sign)

 - `OF` = 0
   - `no` (not overflow)

 - `OF` = 1
   - `o` (overflow)

 - `PF` = 0
   - `np` (not parity)
   - `po` (parity odd)

 - `PF` = 1
   - `p` (parity)
   - `pe` (parity even)

 - `CF` = 0 and `ZF` = 0
   - `a` (above)
   - `nbe` (not below or equal)

 - `CF` = 1 or `ZF` = 1
   - `be` (below or equal)
   - `na` (not above)

 - `ZF` = 0 and `SF` = `OF`
   - `g` (greater)
   - `nle` (not less or equal)

 - `SF` = `OF`
   - `ge` (greater or equal)
   - `nl` (not less)

 - `SF` ≠ `OF`
   - `l` (less)
   - `nge` (not greater or equal)

 - `ZF` = 1 or `SF` ≠ `OF`
   - `le` (less or equal)
   - `ng` (not greater)

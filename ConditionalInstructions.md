# Conditional Instructions (`Jcc`, `SETcc`, `MOVcc`, etc.)

Conditional instruction mnemonics will often describe the same underlying
instruction (e.g. `jnbe` (jump if not below or equal) is the same as `ja` (jump
if above)). This document enumerates each condition that is tested and each
mnemonic that tests it.

# `above` vs `greater` etc.
Certain flags will be describe with words that appear to mean the same thing,
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

Only the first of each of the listed conditions mnemonics has a corresponding `encodings/*.tsv` file. For quick reference, they are listed here:

| Short Name/Instruction Suffix | Offset added to opcode | Meaning |
| ----- | ---- | ------------ |
| `o`   | `0`  | Overflow |
| `no`  | `1`  | Not Overflow |
| `c`   | `2`  | Carry |
| `nc`  | `3`  | Not Carry |
| `z`   | `4`  | Zero |
| `nz`  | `5`  | Not Zero |
| `be`  | `6`  | Below or Equal (Unsigned) |
| `a`   | `7`  | Above (Unsigned) |
| `s`   | `8`  | Sign |
| `ns`  | `9`  | Not Sign |
| `p`   | `10` | Parity (Even) |
| `np`  | `11` | Not Parity (Odd) |
| `l`   | `12` | Less (Signed) |
| `ge`  | `13` | Greater or Equal (Signed) |
| `le`  | `14` | Less or Equal (Signed)  |
| `g`   | `15` | Greater (Signed) |

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

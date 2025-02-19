# Encoding Schema

## `Opcode`

A comma separated list of 2 digit hexadecimal digits. The digits `A` through `F` will always be capitalized.

May end with:
 - `+`: to indicate that a register id must be added to the Opcode
 - `/0`, `/1`, `/2`, `/3`, `/4`, `/5`, `/6`, `/7`: an extension of the opcode to be encoded in the `R` field of the ModRM byte

## `Operand1`, `Operand2`, `Operand3`, `Operand4`

The operands of the instruction, maybe followed by a comma and a `Signed` or `Unsigned` attribute.

 - `al`, `ax`, `eax`, `rax`: The a register
 - `cl`, `cx`, `ecx`, `rcx`: The c register
 - `r8`, `r16`, `r32`, `r64`: A general-purpose register of the given bit width
 - `rm8`, `rm16`, `rm32`, `rm64`: Either a general-purpose register or memory operand of the given bit width
 - `Sreg`: A segment register
 - `moffs8`, `moffs16`, `moffs32`, `moffs64`: A memory offset of the given bit width (TODO: Elaborate on this)
 - `imm8`, `imm16`, `imm32`, `imm64`: An immediate of the given bit width


The `Signed` or `Unsigned` attribute documents things such as implicit sign/zero extension e.g. in `C7 mov rm64, imm32`

## `OperandEncoding`

Indicates how the operands of the instruction are encoded. Corresponds to the table after the opcodes in the intel manual.

 - `RM`: the ModRM byte is needed to encode this instruction and the `R` field is the first operand and the `M` field is the second
 - `MR`: the ModRM byte is needed to encode this instruction and the `M` field is the first operand and the `R` field is the second
 - `FD`: (TODO)
 - `TD`: (TODO)
 - `OI`: The register id of the first operand is added to the Opcode and immediate follows
 - `MI`: the ModRM byte is needed to encode this instruction and the `M` field is the first operand. The `R` field is given by the `Opcode` extension field. Immediate data follows.
 - `M`: the ModRM byte is needed to encode this instruction and the `M` field is the operand. The `R` field is given by the `Opcode` extension field.
 - `O`: The register id of the operand is added to the Opcode
 - `ZO`: No operands

## `Extra`

Additional data needed to encode the instruction or additional information about what the operation will do

 - `OperandSizeOverride`: the "operand-size override" prefix `66H` is needed to encode this instruction in 64 bit mode
 - `AddressSizeOverride`: the "address-size override" prefix `67H` is needed to encode this instruction in 64 bit mode
 - `REX.W`: the "W" bit of the REX prefix should be present

## `ForcedPrefix`

A prefix that if present goes before any REX prefix

## `Support`

64-bit and Legacy mode support

The first item indicates 64-bit support:

 - `V`: Valid, supported
 - `I`: Invalid, not supported
 - `NE`: Not encodable
 - `NP`: REX prefix does not affect the legacy instruction
 - `NI`: This encoding is a different instruction in 64-bit mode
 - `NS`: "Indicates an instruction syntax that requires an address override prefix in 64-bit mode and is not supported. Using an address override prefix in 64-bit mode may result in model-sepcific execution behavior"

The second item indicates Compatability/Legacy mode support
 - `V`: Valid, supported
 - `I`: Invalid, not supported
 - `NE`: "Indicates an Intel 64 instruction mnemonics/syntax that is not encodable; the opcode sequence is not applicable as an individual instruction in compatibility mode or IA-32 mode. The opcode may represent a valid sequence of legacy IA-32 instructions"

# Per instruction data (instructions.tsv)

## Instruction

The name of the instruction

## `OSZAPCTIDNR`

The effect this instruction has on the eflags register

Each letter corresponds to the following flags: `OF`, `SF`, `ZF`, `AF`, `PF`, `CF`, `TF`, `IF`, `DF`, `NT`, `RF`

And each ascii character in the column has the following meaning for the corresponding flag:

 - `.`: The flag is unaffected (Corresponds to a blank space in the intel manual)
 - `T`: The flag is tested
 - `M`: The flag is modified
 - `U`: The flag is tested and modified (Corresponds to `TM` in the intel manual)
 - `0`: The flag is cleared (i.e. set to 0)
 - `1`: The flag is set     (i.e. set to 1)
 - `?`: Undefined. (i.e. its value should not be relied upon) (Corresponds to `-` in the intel manual)
 - `R`: A prior value is restored

## `Lock`, `Rep`, `Repx`

`Lock` Describes if a `LOCK` prefix may be used

`Rep` Describes if a `REP` prefix may be used

`Repx` Describes if a `REPZ` or `REPNZ` prefix may be used

Valid values:

 - `true`
 - `false`

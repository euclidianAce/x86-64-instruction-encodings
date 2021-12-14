#/bin/sh
set -xe
touch encodings/$1.tsv
echo -e "Opcode\tOperand1\tOperand2\tOperand3\tOperand4\tModifier" > encodings/$1.tsv

#/bin/sh
set -e

name="new-encodings/$1.tsv"

if [ -e "$name" ]; then
	echo "$name already exists!" 1>&2
	exit 1
fi

touch $name
echo -e "Opcode\tOperand1\tOperand2\tOperand3\tOperand4\tOperandEncoding\tExtra\tForcedPrefix\tSupport" > $name
echo "Wrote $name"

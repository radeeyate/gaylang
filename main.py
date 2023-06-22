import re
from os import system
from sys import argv

# Token types
TOKEN_PRIDE = "PRIDE"
TOKEN_VARIABLE = "VARIABLE"
TOKEN_VALUE = "VALUE"
TOKEN_YAAAS = "YAAAS"
TOKEN_SAY = "SAY"
TOKEN_TELL = "TELL"
TOKEN_END = "END"
TOKEN_TERMINATION = "TERMINATION"
TOKEN_CLEAR = "CLEAR"

# Token regular expressions
TOKEN_REGEX = [
    (TOKEN_PRIDE, r"🌈\s*pride\s*🏳️‍🌈"),
    # (TOKEN_VARIABLE, r'💃([^💃🌈🏳️‍🌈]+)\s+is\s+"([^"]+)"💃'),
    (TOKEN_VARIABLE, r"💃([^💃🌈🏳️‍🌈]+)\s+is\s+([^💃🌈🏳️‍🌈]+)💃"),
    (TOKEN_YAAAS, r"🔥yaaaas💃"),
    (TOKEN_SAY, r"🌈say\s+([^🌈🎉]+)🎉"),
    (TOKEN_TELL, r"🌈tell\s+💃([^💃🌈🏳️‍🌈]+)🌈🎉"),
    (TOKEN_END, r"🔥end💃"),
    (TOKEN_TERMINATION, r"🌈end🏳️‍🌈"),
    (TOKEN_CLEAR, r"🌈clear🌈"),
]

# Tokenize input code
def tokenize(code):
    tokens = []
    code = code.strip()
    lines = code.split("\n")  # Split code into lines
    line_number = 1  # Initialize line number

    for line in lines:
        line = line.strip()

        while line:
            matched = False
            for token_type, regex in TOKEN_REGEX:
                match = re.match(regex, line)
                if match:
                    token_value = match.group(0)
                    tokens.append((token_type, token_value))
                    line = line[len(token_value) :].strip()
                    matched = True
                    break
            if not matched:
                raise SyntaxError(
                    f"Invalid Gaylang syntax at line {line_number}, token: {line}"
                )

        line_number += 1  # Increment line number

    return tokens


# Parse tokens and execute code
def execute(code):
    tokens = tokenize(code)
    variables = {}

    def get_variable_value(variable_name):
        if variable_name in variables:
            return variables[variable_name]
        else:
            raise NameError(f'Variable "{variable_name}" is not defined')

    i = 0
    while i < len(tokens):
        token_type, token_value = tokens[i]

        if token_type == TOKEN_PRIDE:
            i += 1
        elif token_type == TOKEN_VARIABLE:
            # match = re.match(r'💃([^💃🌈🏳️‍🌈]+)\s+is\s+"([^"]+)"💃', token_value)
            match = re.match(r"💃([^💃🌈🏳️‍🌈]+)\s+is\s+([^💃🌈🏳️‍🌈]+)💃", token_value)
            variable_name = match.group(1)
            variable_value = match.group(2)
            if (
                not variable_value.startswith('"')
                and not variable_value.endswith('"')
                and variable_value.isdigit()
            ):
                variable_value = int(variable_value)
            else:
                if not variable_value.startswith('"') or not variable_value.endswith(
                    '"'
                ):
                    raise SyntaxError(
                        f"EOL while scanning string literal: {variable_value}"
                    )
                else:
                    variable_value = re.sub(r'^"|"$', "", variable_value)
            variables[variable_name] = variable_value
            # print(variables)
            i += 1
        elif token_type == TOKEN_YAAAS:
            i += 1
            while i < len(tokens):
                token_type, token_value = tokens[i]
                if token_type == TOKEN_TELL:
                    match = re.match(r"🌈tell\s+💃([^💃🌈🏳️‍🌈]+)🌈🎉", token_value)
                    variable_name = match.group(1)
                    print(get_variable_value(variable_name))
                    i += 1
                elif token_type == TOKEN_SAY:
                    match = re.match(r"🌈say\s+([^🌈🎉]+)🎉", token_value)
                    string_value = match.group(1)
                    string_value = re.sub(r'^"|"$', "", string_value)
                    print(string_value)
                    i += 1
                elif token_type == TOKEN_CLEAR:
                    system("cls" if os.name == "nt" else "clear")
                    i += 1
                elif token_type == TOKEN_END:
                    break
                else:
                    raise SyntaxError(f"Invalid token inside code block: {token_value}")
            i += 1
        elif token_type == TOKEN_TERMINATION:
            break
        else:
            raise SyntaxError(f"Invalid token: {token_value}")

    if i == len(tokens):
        raise SyntaxError("Program did not terminate correctly")


if len(argv) > 1:
    with open(argv[1], encoding="utf-8") as file:
        lines = file.read()
    execute(lines)
else:
    print("Gaylang Shell Coming Soon...")

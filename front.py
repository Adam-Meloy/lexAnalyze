# This a re-written version of the lexical analyzer provided, in python.
# front.py: a lexical analyzer system for simple arithmetic expressions
# Team Members: Adam Meloy, Megan Lesmeister

# Variables
char_class: int = None
lexeme: str = ""  # char -> string
next_char: str = None  # char
lex_len: int = 0
next_token: int = None
in_fp = open("front.in", "r").read()


# Character classes
class CharClass:
    EOF: int = -1
    LETTER: int = 0
    DIGIT: int = 1
    UNKNOWN: int = 99


# Token codes
class Tokens:
    INT_LIT: int = 10
    IDENT: int = 11
    DEF = -2  # DEF, or default, is the value used when no token is a match for the given input.

    # Task 1 Operators
    MULT_OP: int = 20
    DIV_OP: int = 21
    MOD_OP: int = 22
    ADD_OP: int = 23
    SUB_OP: int = 24
    LESS_OP: int = 25
    LESSEQ_OP: int = 26
    GREAT_OP: int = 27
    GREATEQ_OP: int = 28
    EQUAL_OP: int = 29
    NOTEQ_OP: int = 30
    NOT_OP: int = 31
    ASSIGN_OP: int = 32
    AND_OP: int = 33
    OR_OP: int = 34

    # Task 2 Symbols
    LEFT_PAREN: int = 40
    RIGHT_PAREN: int = 41
    LEFT_BRACE: int = 42
    RIGHT_BRACE: int = 43
    SEMICOL: int = 44
    COMMA: int = 45

    # Task 3 Reserved Words
    FOR_CODE: int = 50
    IF_CODE: int = 51
    ELSE_CODE: int = 52
    WHILE_CODE: int = 53
    DO_CODE: int = 54
    SWITCH_CODE: int = 55
    INT_CODE: int = 56
    FLOAT_CODE: int = 57
    PRINT_CODE: int = 58


# Function definitions
#######################################################
# lookup_simple - a function to lookup operators and parentheses of length 1 and return the token
def lookup_simple(ch):
    global next_token

    match ch:
        # Task 1 Operations
        case '+':
            next_token = Tokens.ADD_OP
        case '-':
            next_token = Tokens.SUB_OP
        case '*':
            next_token = Tokens.MULT_OP
        case '/':
            next_token = Tokens.DIV_OP
        case '%':
            next_token = Tokens.MOD_OP
        case '<':
            next_token = Tokens.LESS_OP
        case '>':
            next_token = Tokens.GREAT_OP
        case '!':
            next_token = Tokens.NOT_OP
        case '=':
            next_token = Tokens.ASSIGN_OP

        # Task 2 Symbols
        case '(':
            next_token = Tokens.LEFT_PAREN
        case ')':
            next_token = Tokens.RIGHT_PAREN
        case '{':
            next_token = Tokens.LEFT_BRACE
        case '}':
            next_token = Tokens.RIGHT_BRACE
        case ';':
            next_token = Tokens.SEMICOL
        case ',':
            next_token = Tokens.COMMA

        # Special cases
        case '\n':
            pass
        case _:
            next_token = Tokens.DEF
    return next_token


# Function definitions
#######################################################
# lookup_complex - a function to lookup operators and parentheses of length 2+ and return the token
def lookup_complex(ch):
    global next_token

    match ch:
        # Task 1 Operations cont.
        case '<=':
            next_token = Tokens.LESSEQ_OP
        case '>=':
            next_token = Tokens.GREATEQ_OP
        case '==':
            next_token = Tokens.EQUAL_OP
        case '!=':
            next_token = Tokens.NOTEQ_OP
        case '&&':
            next_token = Tokens.AND_OP
        case '||':
            next_token = Tokens.OR_OP

        # Special cases
        case '\n':
            pass
        case _:
            next_token = Tokens.DEF
    return next_token


# Function definitions
#######################################################
# lookup_reserved - a function to lookup reserved words and return the token
def lookup_reserved(ch):
    global next_token
    match ch.lower():
        # Task 3 Reserved Words
        case "for":
            next_token = Tokens.FOR_CODE
        case "if":
            next_token = Tokens.IF_CODE
        case "else":
            next_token = Tokens.ELSE_CODE
        case "while":
            next_token = Tokens.WHILE_CODE
        case "do":
            next_token = Tokens.DO_CODE
        case "switch":
            next_token = Tokens.SWITCH_CODE
        case "int":
            next_token = Tokens.INT_CODE
        case "float":
            next_token = Tokens.FLOAT_CODE
        case "print":
            next_token = Tokens.PRINT_CODE
        case _:
            next_token = Tokens.IDENT


#######################################################
# addChar - a function to add nextChar to lexeme
def add_char():  # void
    global lexeme
    global next_char
    global lex_len

    if lex_len <= 98:
        lexeme += next_char
        lex_len += 1
    else:
        print("Error - lexeme is too long \n")


#######################################################
# getChar - a function to get the next character of input and determine its character class
def get_char():  # void
    global char_class
    global next_char
    global in_fp

    try:
        next_char = in_fp[0]
        in_fp = in_fp[1:]
    except IndexError:
        next_char = CharClass.EOF

    if next_char != CharClass.EOF:
        if next_char.isalpha():
            char_class = CharClass.LETTER
        elif next_char.isdigit():
            char_class = CharClass.DIGIT
        else:
            char_class = CharClass.UNKNOWN
    else:
        char_class = CharClass.EOF


#######################################################
# getNonBlank - a function to call getChar until it returns a non-whitespace character
def get_non_blank():  # void
    global next_char

    while next_char.isspace():
        get_char()
        if next_char == CharClass.EOF:
            break


#######################################################
# lex - a simple lexical analyzer for arithmetic expressions
def lex():  # int
    global char_class
    global lexeme
    global next_char
    global lex_len
    global next_token

    while next_token != CharClass.EOF:
        lex_len = 0

        get_non_blank()

        match char_class:
            # Parse strings and reserved words
            case CharClass.LETTER:
                while char_class == CharClass.LETTER or char_class == CharClass.DIGIT:
                    add_char()
                    get_char()
                lookup_reserved(lexeme)

            # Parse integer literals
            case CharClass.DIGIT:
                while char_class == CharClass.DIGIT:
                    add_char()
                    get_char()
                next_token = Tokens.INT_LIT

            # Parse parentheses and operators
            case CharClass.UNKNOWN:
                add_char()
                get_char()
                if lookup_complex(lexeme + next_char) != Tokens.DEF:
                    add_char()
                    get_char()
                    lookup_complex(lexeme)
                elif lookup_simple(lexeme) != Tokens.DEF:
                    lookup_simple(lexeme)

            # EOF
            case CharClass.EOF:
                next_token = CharClass.EOF
                lexeme = "EOF"
        # End of match

        print("Next token is: {next_token}, Next lexeme is {lexeme}".format(next_token=next_token, lexeme=lexeme))
        lexeme = ""


#######################################################
# main driver
if __name__ == '__main__':
    # Open the input data file and process its contents
    if in_fp == "":
        print("ERROR - cannot open front.in \n")
    else:
        get_char()
        lex()
    exit(0)  # successful exit

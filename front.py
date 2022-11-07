# This the (modified) example lexical analyzer code in pages 173 - 177 of the
# textbook,
#
# Sebesta, R. W. (2012). Concepts of Programming Languages.
# Pearson, 10th edition.

# front.py a lexical analyzer system for simple arithmetic expressions

# Global declarations
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
    LEFT_PAREN: int = 40
    RIGHT_PAREN: int = 41
    LEFT_BRACE: int = 42
    RIGHT_BRACE: int = 43
    SEMICOL: int = 44
    COMMA: int = 45


# Function definitions
#######################################################
# lookup - a function to lookup operators and parentheses and return the token
def lookup(ch):
    global next_token

    match ch:
        case '(':
            add_char()
            next_token = Tokens.LEFT_PAREN
        case ')':
            add_char()
            next_token = Tokens.RIGHT_PAREN
        case '{':
            add_char()
            next_token = Tokens.LEFT_BRACE
        case '}':
            add_char()
            next_token = Tokens.RIGHT_BRACE
        case ';':
            add_char()
            next_token = Tokens.SEMICOL
        case ',':
            add_char()
            next_token = Tokens.COMMA
        case '+':
            add_char()
            next_token = Tokens.ADD_OP
        case '-':
            add_char()
            next_token = Tokens.SUB_OP
        case '*':
            add_char()
            next_token = Tokens.MULT_OP
        case '/':
            add_char()
            next_token = Tokens.DIV_OP
        case '%':
            add_char()
            next_token = Tokens.MOD_OP
        case '<':
            add_char()
            next_token = Tokens.LESS_OP
        case '<=':
            add_char()
            next_token = Tokens.LESSEQ_OP
        case '>':
            add_char()
            next_token = Tokens.GREAT_OP
        case '>=':
            add_char()
            next_token = Tokens.GREATEQ_OP
        case '==':
            add_char()
            next_token = Tokens.EQUAL_OP
        case '!=':
            add_char()
            next_token = Tokens.NOTEQ_OP
        case '!':
            add_char()
            next_token = Tokens.NOT_OP
        case '&&':
            add_char()
            next_token = Tokens.AND_OP
        case '||':
            add_char()
            next_token = Tokens.OR_OP
        case '\n':
            pass
        case _:
            add_char()
            next_token = CharClass.EOF
    return next_token


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

    lex_len = 0

    get_non_blank()

    match char_class:
        # Parse identifiers
        case CharClass.LETTER:
            add_char()
            get_char()
            while char_class == CharClass.LETTER or char_class == CharClass.DIGIT:
                add_char()
                get_char()
            next_token = Tokens.IDENT

        # Parse integer literals
        case CharClass.DIGIT:
            add_char()
            get_char()
            while char_class == CharClass.DIGIT:
                add_char()
                get_char()
            next_token = Tokens.INT_LIT

        # Parentheses and operators
        case CharClass.UNKNOWN:
            lookup(next_char)
            get_char()

        # EOF
        case CharClass.EOF:
            next_token = CharClass.EOF
            lexeme = "EOF"
    # End of match

    print("Next token is: {next_token}, Next lexeme is {lexeme}".format(next_token = next_token, lexeme = lexeme))
    lexeme = ""
    return next_token


#######################################################
# main driver
if __name__ == '__main__':
    # Open the input data file and process its contents
    if in_fp == "":
        print("ERROR - cannot open front.in \n")
    else:
        get_char()
        lex()
        while next_token != CharClass.EOF:
            lex()
    exit(0)  # exit code for success

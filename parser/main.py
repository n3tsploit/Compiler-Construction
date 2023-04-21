import ply.lex as lex
import ply.yacc as yacc

# Define the lexer tokens
tokens = [
    'IDENTIFIER',
    'KEYWORD',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LT',
    'GT',
    'EQ',
    'NEQ',
    'LTE',
    'GTE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'COMMA',
    'SEMICOLON',
    'STRING'
]

# Define the regular expressions for the tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LT = r'<'
t_GT = r'>'
t_EQ = r'=='
t_NEQ = r'!='
t_LTE = r'<='
t_GTE = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_STRING = r'\".*?\"'


# Define additional tokens
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    keywords = {
        'if': 'KEYWORD',
        'else': 'KEYWORD',
        'while': 'KEYWORD',
        'for': 'KEYWORD',
        'return': 'KEYWORD',
        'printf': 'KEYWORD',
    }
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t



def t_NUMBER(t):
    r'-?\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

t_ignore = ' \t\n'


def t_error(t):
    print(f"Invalid token: {t.value[0]}")
    t.lexer.skip(1)


# Define the parser rules
def p_program(p):
    '''program : statement
               | statement program
               | function_declaration main_function
               | main_function
               | function_call '''
    p[0] = ['program'] + [p[i] for i in range(1, len(p))]


def p_function_declaration(p):
    '''function_declaration : NUMBER IDENTIFIER LPAREN NUMBER IDENTIFIER COMMA NUMBER IDENTIFIER RPAREN LBRACE function_body RBRACE
                            | NUMBER IDENTIFIER LPAREN NUMBER IDENTIFIER COMMA NUMBER IDENTIFIER RPAREN block'''
    # Save the function name and body
    p[0] = [p[2], p[11]]


def p_function_body(p):
    '''function_body : IDENTIFIER expression SEMICOLON'''
    # Save the expression as the return value
    p[0] = p[2]


def p_function_call(p):
    '''function_call : NUMBER IDENTIFIER EQ IDENTIFIER LPAREN IDENTIFIER COMMA IDENTIFIER RPAREN SEMICOLON
                     | IDENTIFIER LPAREN STRING COMMA IDENTIFIER RPAREN SEMICOLON'''

def p_main_function(p):
    '''main_function : KEYWORD LPAREN RPAREN LBRACE statement RBRACE'''
    # Save the statement as the main block
    p[0] = p[5]



def p_statement(p):
    '''statement : if_statement
                 | expression SEMICOLON
                 | while_loop
                 | assignment
                 | print_statement
                 | block
                 | function_call
                 | expression'''
    p[0] = ['statement'] + [p[1]]


def p_if_statement(p):
    '''if_statement : KEYWORD LPAREN expression RPAREN LBRACE program RBRACE
                     | KEYWORD LPAREN expression RPAREN statement
                     | KEYWORD LPAREN expression RPAREN LBRACE program RBRACE KEYWORD LBRACE program RBRACE'''
    if len(p) == 8:
        p[0] = ['if'] + [p[3]] + [p[6]]
    else:
        p[0] = ['if'] + [p[3]] + [p[6]] + ['else'] + [p[10]]


def p_while_loop(p):
    '''while_loop : KEYWORD LPAREN expression RPAREN block'''
    p[0] = ['while'] + [p[3]] + [p[5]]


def p_assignment(p):
    '''assignment : IDENTIFIER EQ expression SEMICOLON
                  | NUMBER IDENTIFIER EQ NUMBER SEMICOLON
                    '''
    p[0] = ['assignment'] + [p[1]] + [p[3]]


def p_statement_print(p):
    '''print_statement : KEYWORD LPAREN STRING RPAREN SEMICOLON'''
    p[0] = ['print'] + [p[3]]


def p_expression(p):
    '''
    expression : expression PLUS term
               | expression MINUS term
               | expression GT term
               | expression GTE term
               | expression LTE term
               | expression NEQ term
               | expression LT term
               | IDENTIFIER DIVIDE IDENTIFIER TIMES NUMBER
               | term
    '''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]


def p_term(p):
    '''term : term TIMES factor
    | term DIVIDE factor
    | factor'''
    if len(p) == 4:
        p[0] = [p[2]] + [p[1]] + [p[3]]
    else:
        p[0] = p[1]


def p_factor(p):
    '''factor : LPAREN expression RPAREN
    | NUMBER
    | IDENTIFIER'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_block(p):
    '''block : LBRACE program RBRACE
             | LBRACE statement_list RBRACE '''
    p[0] = ['block'] + [p[2]]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''


def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, column {p.lexpos}")
    else:
        print("Syntax error at EOF")



# Build the lexer and parser
lexer = lex.lex()
parser = yacc.yacc()

# Test the parser
if __name__ == '__main__':
    with open('code.c', 'r') as r:
        code = r.read()
    lexer.input(code)

    result = parser.parse(code, lexer=lexer)
    print(result)

#!/usr/local/bin/python3
import pysig as ps

tokens = (
    'NAME','NUMBER','PI',
    'DB','UNIT','SCALE','ABS','NEG','DC','LOG',
	'LINEAR','SINE','BIPOLAR','SAWTOOTH','SQUARE',
	'AM','DIVIDE','HILBERT','GRADIENT','ADD','CAT',
	'MULTIPLEX','WAVE',
    'LPAREN','RPAREN','LSQUARE','RSQUARE'
    )

t_DB      = r'dB'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = ps.signal(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_DB(t):
	'number : number DB'
	t[0] = ps.DB(t[1])


# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()


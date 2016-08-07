# ------------------------------------------------------------
# modelparser.py
#
# (C) Tiago Almeida 2016
# Still in early development stages.
# ------------------------------------------------------------

import ply.lex as lex

reserved = {
   'String' : 'STRING',
   'Date' : 'DATE',
}

# List of token names.   This is always required
tokens = (
   'MODELNAME',
   'NUMBER',
   'COMMA',
   'STAR',
   'LPAREN',
   'RPAREN',
   'COLON',
   'LBRACKET',
   'RBRACKET',
   'SEMICOLON',
   'ID'
) + tuple(reserved.values())

# Regular expression rules for simple tokens
t_COMMA  	  = r'\,'
t_STAR   	  = r'\*'
t_LPAREN  	= r'\('
t_RPAREN    = r'\)'
t_COLON		  = r'\:'
t_LBRACKET	= r'\{'
t_RBRACKET	= r'\}'
t_SEMICOLON = r'\;'


# A regular expression rule with some action code
def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)    
	return t

# Identifier match 
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


# Test it out
data = '''
Post{
	title: String;
	author: Author;
	body: String;
	publishDate: Date;
	tags: Tag;

}

Tag{
	name: String;
}


Author{
	name: String;
	dateOfBirth: Date;
}
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)
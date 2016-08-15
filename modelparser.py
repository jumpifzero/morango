# ============================================================
# modelparser.py
#
# (C) Tiago Almeida 2016
#
# Still in early development stages.
#
# This module uses PLY (http://www.dabeaz.com/ply/ply.html)
# and a set of grammar rules to parse a custom model 
# definition language.
# ============================================================

import functools as ftools
import pprint
import ply.lex as lex
import ply.yacc as yacc
import sys
import exceptions


# ============================================================
# Constants
# ============================================================
MULT_SINGLE = 1
MULT_ANY    = 2


# ============================================================
# Lexer rules
# ============================================================
reserved = {
   'String' : 'STRING',
   'Date'   : 'DATE',
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
   'EXCLAMATION',
   'ID'
) + tuple(reserved.values())

# Regular expression rules for simple tokens
t_COMMA  	    = r'\,'
t_STAR   	    = r'\*'
t_LPAREN  	  = r'\('
t_RPAREN      = r'\)'
t_COLON       = r'\:'
t_LBRACKET    = r'\{'
t_RBRACKET    = r'\}'
t_SEMICOLON   = r'\;'
t_EXCLAMATION = r'\!'



# A regular expression rule with some action code
def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)    
	return t

# Identifier match 
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID') # Check for reserved words
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


# ============================================================
# Parser rules
# ============================================================
# ----------------
# BNF Grammar
# ----------------
# model   : MODELNAME { fields }
# fields  : fields field ;
#         | field ;
models = []
fields = []
def p_file(p):
  """
  rules : models
  """
  p[0] = p[1]


def p_modelsdecl(p):
  """
  models : models model
         | model
  """
  if len(p) >= 3: 
    models.append(p[2])
  else:
    models.append(p[1])


def p_modeldecl(p):
  'model : ID LBRACKET fields RBRACKET'
  global fields
  p[0] = {  'model':  p[1],
            'fields': fields
          }
  fields = []


def p_fields_decl(p):
  """
  fields : fields field
         | field
  """
  if len(p) >= 3: 
    fields.append(p[2])
  else:
    fields.append(p[1])


def p_field_decl(p):
  """
  field : ID COLON multiplicity datatype notnull SEMICOLON
  """
  # return an object with the field data
  # 
  p[0] = {
          'name': p[1],
          'type': p[4],
          'mult': p[3],
          'null': p[5]
          }


def p_datatype(p):
  """
  datatype : STRING
           | DATE
           | ID
  """
  p[0] = p[1]


def p_field_multiplicity(p):
  """
  multiplicity : STAR
               | empty
  """
  if p[1] == '*':
    p[0] = MULT_ANY
  else:
    p[0] = MULT_SINGLE


def p_field_notnull(p):
  """
  notnull : EXCLAMATION
          | empty
  """
  if p[1] == '!':
    p[0] = False
  else:
    p[0] = True


def p_empty(p):
    'empty :'
    pass


def p_modeldecl_print_error(p):
     'model : ID LBRACKET error RBRACKET'
     print("Syntax error in model declaration. Bad body")


# Error rule for syntax errors
def p_error(p):
  pass


def validate_models_unique(models):
  """
  Given a list of models, validates there are no repetitions.
  """
  index = {}
  for m in models:
    print(m['model'])
    if m['model'] in index:
      raise exceptions.ModelNotUnique(m['model'])
    else:
      index[m['model']] = True


def validate_fields_unique(models):
  """
  Given a list of models, for each one validates there are no
  repeated fields.
  """
  pass


def parse(file_path, debug_lexer=False):
  """
  """
  global models
  models = []
  # Build the lexer
  lexer = lex.lex()
  # Read argv(1) file
  with open(file_path) as f:
    data = f.read()

  if debug_lexer: 
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)

  parser = yacc.yacc()
  result = parser.parse(data)
  return models 


def parse_files(files_lst):
  # parse the files and join the sublists of models into one 
  models_fragments = list(map(parse, files_lst))
  models = list(ftools.reduce(lambda l1,l2: l1 + l2, 
                models_fragments))
  validate_models_unique(models)
  return models


def main():
  parse(sys.argv[1])


if __name__ == '__main__':
  main()
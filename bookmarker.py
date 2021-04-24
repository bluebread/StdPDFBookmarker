from PyPDF2 import PdfFileReader, PdfFileWriter

import ply.lex as lex
import ply.yacc as yacc

tokens = (
	'NUMBER',
	'HEAD',
	'TITLE',
	'COLON',
	'INDENT'
)

# Tokens
t_HEAD = r'-'
t_TITLE = r'[a-zA-Z][a-zA-Z]*'
t_COLON = r':'
t_INDENT = r'\t+'

# Ignored symbols
t_ignore  = ' '

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

# Define a rule so we can track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

# Context Free Grammar
def p_empty(p):
	'empty : '
	p[0] = None

def p_bookmark(p):
	'bookmark : HEAD TITLE COLON NUMBER'
	p[0] = (p[2], p[4], [])

def p_indent(p):
	'''indent : INDENT 
			  | empty'''
	p[0] = len(p[1]) if p[1] else 0

def p_line(p):
	'line : indent bookmark'
	p[0] = (p[1], p[2])

def p_lines(p):
	'''lines : line lines 
			 | empty'''
	if len(p) > 2:
		p[2].append(p[1])
		p[0] = p[2]
	else:
		p[0] = []

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build Tree structure
def build_tree(result, ind):
	tree = []
	parent = None
	while len(result) > 0:
		i_n, bookmark = result.pop()
		if parent is None:
			if i_n != ind:
				raise Exception("Bookmark Syntax Error")
			parent = bookmark[2]
		if i_n > ind:
			result.append((i_n, bookmark))
			subtree = build_tree(result, ind + 1)
			parent.extend(subtree)
		elif i_n < ind:
			result.append((i_n, bookmark))
			break
		else:
			parent = bookmark[2]
			tree.append(bookmark)
	return tree

def parse_bookmarks(file_path):
	tree = None

	lexer = lex.lex()
	parser = yacc.yacc(start='lines')

	with open(file_path, 'r') as f:
		data = f.read().replace('\n', '')
		lexer.input(data)
		result = parser.parse(data)
		tree = build_tree(result, 0)
	
	return tree


def AddBookmarksInPDF(pdf_file, bm_file):
	writer = PdfFileWriter()
	bookmarks = parse_bookmarks(bm_file)

	def recursive_add_bookmarks(bookmarks, parent=None):
		for title, page_num, child_bookmarks in bookmarks:
			ref = writer.addBookmark(title, page_num, parent=parent)
			recursive_add_bookmarks(child_bookmarks, parent=ref)

	with open(pdf_file, 'rb') as f:
		reader = PdfFileReader(f, strict=False)
		writer.appendPagesFromReader(reader)
		recursive_add_bookmarks(bookmarks)

	with open(pdf_file, 'wb') as f:
		writer.write(f)

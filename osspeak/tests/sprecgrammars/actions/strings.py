EMPTY = ''
HANGING_PLUS = "foo +"
HANGING_COMMA = "foo ,"
GROUPING_TOKEN_MISMATCH = '{ctrl+1)'

BASIC_KEYPRESS = '{shift+ctrl+e}'
KEYPRESS_WITHOUT_DELIMITER = '{alt 4}'

BASIC_FUNCTION = 'mouse.click()'
NESTED_FUNCTIONS = 'mouse.move(mouse.x(), mouse.y())'
EXTENSIONS_FUNCTION = 'extensions.run(excel)'
EXTENSIONS_FUNCTION_WITH_ARGS = 'extensions.message(excel.main, foo)'

FUNCTION_WITH_ARGS = 'mouse.move(100, 200)'

VARIABLE1 = '"hello" $1 "world"'
# VARIABLE2 = '0 or 3 "hello world" max(len($1), 2*4)'
VARIABLE2 = 'len($1, $-2)'
VARIABLE3 = 'len($1, $-2) "foo $2"'

LAMBDA_EXPRESSION = '(lambda a, b: a + b)(4, 5)'
KWARG_EXPRESSION = 'int(x="45")'
SORTED_EXPR = 'list(sorted([barr, foo, "another string"], key=len))'
TOP_LEVEL_BUILTIN = 'len'
INDEX_EXPR = 'x[0]'
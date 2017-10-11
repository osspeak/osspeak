rules = [      
    ["jsScope", "scope='scope string'"],
    ["jsForRange", "forrange='range string'"],
    ["jsForOf", "forof='for of'"],
    ["jsKeyword", "(<jsScope> | <jsForRange> | <jsForOf>)"]
]

GROUPING1 = '(hello (world|universe))'

SUBSTITUTE1 = '(west = left | (east) = right)'
SUBSTITUTE2 = 'export=mouse.click() export'
SUBSTITUTE3  = "(slash='/' | semicolon=';')"
SUBSTITUTE4  = "((dollar sign)='$' | semicolon)"

NAMED_RULES = {
    'digit': '(0|1|2|3|4|5|6|7|8|9|)'
}
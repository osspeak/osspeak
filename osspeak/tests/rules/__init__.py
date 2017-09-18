["jsScope", "scope=brackets()"],
["jsForRange", "forrange='for ' parentheses() 'let i = 0; i < ; i++' repeat({left}, 5)"],
["jsForOf", "forof='for ' parentheses() 'let  of ' clipboard.get() repeat({left}, len(clipboard.get())) repeat({left}, 4)"],
["jsKeyword", "(<jsScope> | <jsElse> | <jsForRange>)"]
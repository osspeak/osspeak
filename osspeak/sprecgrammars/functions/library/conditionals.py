def osspeak_if(action, variables, arguments, type_result):
    print(action, variables, arguments)
    if_result = action.arguments[0].evaluate(variables, arguments)
    if if_result:
        return action.arguments[1].evaluate(variables, arguments, type_result=type_result)
    elif len(action.arguments) > 2:
        return action.arguments[2].evaluate(variables, arguments, type_result=type_result)
        
def repeat(action, variables, arguments, type_result):
    if len(action.arguments) == 1:
         start, stop = 0, 1
    elif len(action.arguments) == 2:
        start, stop = 0, action.arguments[1].evaluate(variables, arguments)
    else:
        assert len(action.arguments) == 3
        start = action.arguments[1].evaluate(variables, arguments)
        stop = action.arguments[2].evaluate(variables, arguments)
    if start == '':
        start = 1
    if stop == '':
        stop = 1
    total_result = None
    for i in range(int(start), int(stop)):
        result = action.arguments[0].evaluate(variables, arguments,  type_result=type_result)
        if total_result is None:
            total_result = result
        else:
            try:
                total_result += result
            except:
                pass
    return total_result
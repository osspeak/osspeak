def osspeak_if(action, variables, arguments):
    print(action, variables, arguments)
    if_result = action.arguments[0].evaluate(variables, arguments)
    if if_result:
        return action.arguments[1].evaluate(variables, arguments)
    elif len(action.arguments) > 2:
        return action.arguments[2].evaluate(variables, arguments)
        
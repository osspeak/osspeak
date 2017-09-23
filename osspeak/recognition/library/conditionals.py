import threading

def osspeak_if(action, variables, arguments, type_result, result_state):
    print(action, variables, arguments)
    if_result = action.arguments[0].evaluate(variables, arguments, result_state=result_state)
    if if_result:
        return action.arguments[1].evaluate(variables, arguments, type_result=type_result, result_state=result_state)
    elif len(action.arguments) > 2:
        return action.arguments[2].evaluate(variables, arguments, type_result=type_result, result_state=result_state)
        
# def repeat(action, variables, arguments, type_result, result_state):
#     if len(action.arguments) == 1:
#          start, stop = 0, 1
#     elif len(action.arguments) == 2:
#         start, stop = 0, action.arguments[1].evaluate(variables, arguments, result_state=result_state)
#     else:
#         assert len(action.arguments) == 3
#         start = action.arguments[1].evaluate(variables, arguments, result_state=result_state)
#         stop = action.arguments[2].evaluate(variables, arguments, result_state=result_state)
#     if start == '':
#         start = 1
#     if stop == '':
#         stop = 1
#     total_result = None
#     for i in range(int(start), int(stop)):
#         result = action.arguments[0].evaluate(variables, arguments,  type_result=type_result, result_state=result_state)
#         if total_result is None:
#             total_result = result
#         else:
#             try:
#                 total_result += result
#             except:
#                 pass
#     return total_result

def execute_async(action, variables, arguments, type_result, result_state):
    thread = threading.Thread(target=execute_async_thread, args=[action, variables, arguments, type_result, result_state])
    result_state['threads'] = result_state.get('threads', []) + [thread]
    thread.start()

def execute_async_thread(action, variables, arguments, type_result, result_state):
    for action_arg in action.arguments:
        action_arg.evaluate(variables, arguments, type_result=type_result, result_state=result_state)
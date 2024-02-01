import threading

def run_function_with_timeout(func, timeout):

    # Function to return the result as a parameter
    def func_wrapper(result):
        result.append(func())

    # List for the result of the function
    result = []

    # Thread with timeout
    thread = threading.Thread(target=func_wrapper, args=(result,))
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return None
    else:
        return result[0]

from concurrent.futures import ThreadPoolExecutor
import threading

pool = ThreadPoolExecutor(max_workers=10)

def run_in_thread(*actions):
    threading.Thread(target=lambda x: run_actions(*x), daemon=True, args=(actions,)).start()
    # pool.submit(run_actions, *actions)

def run_actions(*lambda_args):
    from recognition.actions import perform
    for lambda_arg in lambda_args:
        perform.perform_io(lambda_arg())
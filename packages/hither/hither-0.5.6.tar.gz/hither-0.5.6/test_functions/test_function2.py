import os
import time

def test_function2(a: str):
    print('test function 2')
    time.sleep(2)
    print('test function 2b')
    time.sleep(2)
    return f'test_function2: a = {a} ; {os.getenv("TESTVAR")}'
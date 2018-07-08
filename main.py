from specific_support_function_for_this_project import *
from multiprocessing import Process
import os

# Implement your main function here


"""
The following is the example to do parallel programming in python. Please be careful that the parallel control shall be
always used in your program later implemented.

Delete the example when you are ready to go.
"""
def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()

import os
import sys

for key in os.environ.keys():
    print(key)

class A:
    def __init__(self):
        self.p = 1
        pass

class B(A):
    pass

class C:
    pass

def foo(a:A, b:A):
    if a == None:
        return ""
    else:
        return A()

sys.exit()
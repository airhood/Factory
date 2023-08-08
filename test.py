
script = 'print(f)\nprint("wow")'

def func(s):
    exec("f = 2")
    exec(script)

a = func(1000)
print(a)

script = 'def say(text):\n  print(text)\nsay("abc")\nprint("wow")'

def func(s):
    exec("f = 2")
    exec(script)

a = func(1000)
print(a)
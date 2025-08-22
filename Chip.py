from collections import deque

class Chip():
    def __init__(self, name):
        self.name = name
        self.ports = {
            'A': deque(),
            'B': deque(),
            'C': deque(),
            'D': deque()
        }
        self.x = None
        self.y = None
        self.compile_code = None
        self.compile_checker = None
        self.activate = True
        self.chip_global_var = {}
        self.tile = None

    def set_script(self, script):
        converted_script = self.convert(script)
        self.compile_code = compile(converted_script, '<string>', 'exec')

    def set_checker(self, checker):
        converted_checker = self.convert_checker(checker)
        self.compile_checker = compile(converted_checker, '<string>', 'exec')

    def convert(self, script):
        lines = script.split('\n')
        converted_script = ""
        for line in lines:
            if line.find('return') != -1:
                line = line.replace('return-A', 'return_val[0] =')
                line = line.replace('return-B', 'return_val[1] =')
                line = line.replace('return-C', 'return_val[2] =')
                line = line.replace('return-D', 'return_val[3] =')
            converted_script += line + "\n"
        return converted_script

    def convert_checker(self, checker):
        lines = checker.split('\n')
        converted_checker = ""
        for line in lines:
            if line.find('return') != -1:
                line = line.replace('return', 'return_checker = ')
            converted_checker += line + "\n"
        return converted_checker

    def add_input(self, port, value):
        if port in self.ports:
            self.ports[port].append(value)

    def can_calculate(self):
        if not self.activate:
            return False
        
        if self.compile_checker:
            a, b, c, d = (self.ports['A'][0] if self.ports['A'] else None,
                          self.ports['B'][0] if self.ports['B'] else None,
                          self.ports['C'][0] if self.ports['C'] else None,
                          self.ports['D'][0] if self.ports['D'] else None)
            local_vars = {
                'a': a,
                'b': b,
                'c': c,
                'd': d,
                'return_checker': False,
                'count': 0,
                'global_var': self.chip_global_var
            }
            exec(self.compile_checker, {}, local_vars)
            # print(f"return_checker: {local_vars['return_checker']}, count: {local_vars['count']}")
            return local_vars['return_checker']
        return False

    def try_calculate(self):
        if not self.can_calculate():
            return [None, None, None, None]
        return self.calculate()

    def calculate(self):
        a, b, c, d = (self.ports['A'][0] if self.ports['A'] else None,
                      self.ports['B'][0] if self.ports['B'] else None,
                      self.ports['C'][0] if self.ports['C'] else None,
                      self.ports['D'][0] if self.ports['D'] else None)
        return_val = [None, None, None, None]

        if self.compile_code:
            local_vars = {
                'a': a,
                'b': b,
                'c': c,
                'd': d,
                'return_val': return_val
            }
            exec(self.compile_code, {}, local_vars)
            return_val = local_vars['return_val']

        # Clear the ports after calculation
        for port in self.ports.values():
            if port:
                port.popleft()

        return return_val

import pygame

class Chip():
    def __init__(self):
        pass

    def set_script(self, script):
        self.script = script
        # 코드 변환
        self.convert()
        # 코드 컴파일
        self.compile_code = compile(self.script, '<string>', 'exec')

    def convert(self):
        lines = self.script.split('\n')
        converted_script = ""
        for line in lines:
            if line.find('return') != -1:
                # python 코드의 'return' 구문을 실행 가능하도록 변경
                line = line.replace('return', 'global return_val\nreturn_val = ')
            converted_script += line + "\n"
        self.script = converted_script
        print(self.script)

    def calculate(self, portA, portB, portC, portD):
        global return_val
        return_val = None
        exec(self.compile_code)
        return return_val

# 테스트 코드
'''
script = 'print("wow")\nreturn 1'
chip = Chip()
chip.set_script(script)
result = chip.calculate(None, None, None, None)
print(result)
'''
import pygame

class Chip():
    def __init__(self, name):
        self.name = name
        self.portA_saved, self.portB_saved, self.portC_saved, self.portD_saved = 0, 0, 0, 0
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
                line = line.replace('return-A', 'global return_val\nreturn_val[0] = ')
                line = line.replace('return-B', 'global return_val\nreturn_val[1] = ')
                line = line.replace('return-C', 'global return_val\nreturn_val[2] = ')
                line = line.replace('return-D', 'global return_val\nreturn_val[3] = ')
            converted_script += line + "\n"
        self.script = converted_script

    def calculate(self):
        a, b, c, d = self.portA_saved, self.portB_saved, self.portC_saved, self.portD_saved
        global return_val
        return_val = (None, None, None, None)
        (return_val_A, return_val_B, return_val_C, return_val_D) = None, None, None, None
        exec(self.compile_code)
        self.portA_saved, self.portB_saved, self.portC_saved, self.portD_saved = None, None, None, None
        return return_val

# 테스트 코드
'''
script = 'print("wow")\nreturn 1'
chip = Chip()
chip.set_script(script)
result = chip.calculate(None, None, None, None)
print(result)
'''
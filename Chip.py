
class Chip():
    def __init__(self, name):
        self.name = name
        self.portA_saved, self.portB_saved, self.portC_saved, self.portD_saved = None, None, None, None
        pass

    def set_script(self, script):
        converted_script = self.convert(script)
        self.compile_code = compile(converted_script, '<string>', 'exec')

    def convert(self, script):
        lines = script.split('\n')
        converted_script = ""
        for line in lines:
            if line.find('return') != -1:
                # python 코드의 'return' 구문을 실행 가능하도록 변경
                line = line.replace('return-A', 'return_val\nreturn_val[0] = ')
                line = line.replace('return-B', 'return_val\nreturn_val[1] = ')
                line = line.replace('return-C', 'return_val\nreturn_val[2] = ')
                line = line.replace('return-D', 'return_val\nreturn_val[3] = ')
            converted_script += line + "\n"
        return converted_script

    def calculate(self):
        a, b, c, d = self.portA_saved, self.portB_saved, self.portC_saved, self.portD_saved
        return_val = [None, None, None, None]
        exec(self.compile_code)
        self.portA_saved, self.portB_saved, self.portC_saved, self.portD_saved = None, None, None, None
        return return_val

# 테스트 코드

# script = 'return-D 1 + a'
# chip = Chip('wow_chip')
# chip.set_script(script)
# result = chip.calculate()
# print(result)

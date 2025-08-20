import json
from Chip import Chip

def load_chip(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chip_list = []
    for chip_data in data:
        chip_obj = Chip(chip_data['name'])
        chip_obj.set_script(chip_data['script'])
        chip_obj.set_checker(chip_data['checker'])
        chip_obj.activate = False
        
        chip_list.append(chip_obj)
    
    return chip_list
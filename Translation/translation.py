from re import search
from os import path

class Translation():
    def __init__(self, pseudocode: str) -> None:
        self.pseudocode = pseudocode
        self._transpiled = ''

    @property
    def pseudocode(self, pseudocode: str) -> None:
        self._pseudocode = pseudocode

    @pseudocode.getter
    def pseudocode(self):
        return self._pseudocode
    
    def compile(self):
        indent = ''
        for line in self.pseudocode:
            if var := search(rf'^{indent}SEND (.)+ TO DISPLAY'):
                self.transpiled += 'print(var)'

    def transpile(self, path):
        try:
            with open(path.join('temp', 'transpiled.py'), 'w') as transpiled_file:
                transpiled_file.write(self._transpiled)
        except FileNotFoundError:
            pass
        

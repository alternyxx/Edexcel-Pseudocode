from re import search, match
from os import path

class Translation():
    def __init__(self, pseudocode: str) -> None:
        self.pseudocode = pseudocode
        self._transpiled = ''

    @property
    def pseudocode(self) -> str:
        return self._pseudocode

    @pseudocode.setter
    def pseudocode(self, pseudocode: str) -> None:
        self._pseudocode = pseudocode
    
    def compile(self):
        indent = ''
        for line in self.pseudocode:
            if var := match(rf"{indent}SEND ([^ ]|'.*') TO DISPLAY", line):
                self._transpiled += f'print({var.group(1)})'

    def transpile(self):
        try:
            with open(path.join('temp', 'transpiled.py'), 'w') as transpiled_file:
                transpiled_file.write(self._transpiled)
        except FileNotFoundError:
            pass
        

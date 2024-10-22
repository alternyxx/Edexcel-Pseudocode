from re import search, match
from os import path

class Translation():
    def __init__(self, pseudocode: str) -> None:
        self.pseudocode = pseudocode
        self._variables = {}
        self._transpiled = ''


    # Getter for the written pseudocode
    @property
    def pseudocode(self) -> str:
        return self._pseudocode


    @pseudocode.setter
    def pseudocode(self, pseudocode: str) -> None:
        self._pseudocode = pseudocode
    

    def compile(self):
        # For indentation
        indent = ''

        for line in self.pseudocode:

            # Check if the line is a declaration and initialization of a variable #(?:, \[.*\])*)
            if var_set := match(rf"{indent}SET ([^ ]+)( \[[0-9+]\])? TO ([^ \[\]]+(?:\[0-9+\])?|'.*'|\[.*\])", line):
                if var_set.group(2):
                    self._transpiled += f'{var_set.group(1)}{var_set.group(2)} = {var_set.group(3)}' 
                else:
                    self._transpiled += f'{var_set.group(1)} = {var_set.group(3)}\n'

            # Check if the line is a print function
            elif print_function := match(rf"{indent}SEND ([^ \[\]]+(?: \[0-9+\])?|'.*'|\[.*\]) TO DISPLAY", line):
                self._transpiled += f'print({print_function.group(1).replace(' ', '')})\n'


    def transpile(self):
        # Try to transpile the file in the place user gives
        try:
            with open(path.join('temp', 'transpiled.py'), 'w') as transpiled_file:
                # Write the transpiled code
                transpiled_file.write(self._transpiled)
        except:
            print('Unable to access output file location.')

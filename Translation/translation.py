from re import search, match, fullmatch, sub
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

        # Common regex patterns
        value = r"[^\[\]]+(?:\[[^'\"]+\])?"
        # If anyone could clarify if a ' can be in a string in pseudocode, thatd be great
        string = r"'.*'"
        array = r"\[.*\]"
        # regex for variable / array index initialisation
        var_index = r"[^ \[\]]+(?:\[[^ '\"]+\])?"
        condition = r".*"
        if_con = r""

        for line in self.pseudocode:

            # Check if the line is a declaration and initialization of a variable
            if var_set := match(rf"{indent}SET ({var_index}) TO ({value}|{string}|{array})", line):
                self._transpiled += f'{indent}{var_set.group(1)} = {var_set.group(2)}\n'

            elif line == '\n':
                self._transpiled += line

            # Check if the line is a print function
            elif print_function := match(rf"{indent}SEND ({value}|{string}|{array}) TO DISPLAY", line):
                self._transpiled += f'{indent}print({print_function.group(1).replace(' ', '')})\n'
            
            # Check if the line is an input function
            elif input_function := match(rf"RECEIVE ({var_index}) FROM (?:\(STRING\)|\(INTEGER\)|\(CHARACTER\)) KEYBOARD"):
                self._transpiled = f'{input_function.group(1)} = input()'

            elif if_condition := match(rf'{indent}IF (.)+ THEN', line):
                self.transpiled += f'if {if_condition}:'
                indent += '    '

            elif while_loop := match(rf"WHILE (.+) DO", line):
                self._transpiled += f'{indent}while {while_loop.group(1)}:\n'
                indent += '    '
            
            #elif indent:
            elif fullmatch(rf'{indent.removesuffix('    ')}END WHILE', line):
                indent.removesuffix('    ')
            
            elif fullmatch(rf'REPEAT', line):
                ...
            
            elif define := match(rf"FUNCTION")


    #def transpile(self):
        #sub(rf"SET ([^ ]+)( \[[^ '\"]+\])? TO ([^\[\]]+(?: \[[^ '\"]+\])?|'.*'|\[.*\])", "")


    def output_file(self):
        # Try to transpile the file in the place user gives
        try:
            with open(path.join('temp', 'transpiled.py'), 'w') as transpiled_file:
                # Write the transpiled code
                transpiled_file.write(self._transpiled)
        except:
            print('Unable to access output file location.')


    def precompile(self):
        ...
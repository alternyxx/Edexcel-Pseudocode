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
        value = r"[^'\"\[\]]+(?:\[[^'\"]+\])*"
        # If anyone could clarify if a ' can be in a string in pseudocode, thatd be great
        string = r"'.*'"
        array = r"\[.*\]"
        # regex for variable / array index initialisation
        var_index = r"[^ \[\]]+(?:\[[^ '\"]+\])*"
        # Also whether or not its fine for the ' ?' to be a ' *' instead
        condition = rf"{value}(?: ?(?:=|!=|>|>=|<|<=) ?{value})?(?: (?:AND|OR|NOT) {value}(?: ?(?:=|!=|>|>=|<|<=) ?{value})?)*"
        arithmetic = r" ?(?:\+|-|\*|\^)"
        comment = r'#.*'
        end_of_line = rf' *(?:{comment})?(?:\n)?'

        for line in self.pseudocode:

            # declaration and initialization of a variable
            if var_set := fullmatch(rf"{indent}SET ({var_index}) TO ({value}|{string}|{array})({end_of_line})", line):
                self._transpiled += f'{indent}{var_set.group(1)} = {var_set.group(2)}{str(var_set.group(3) or '')}'

            elif empty_line := fullmatch(rf'({end_of_line})', line):
                self._transpiled += f'{str(empty_line.group(1) or '')}'

            # print function
            elif print_function := fullmatch(rf"{indent}SEND ({value}|{string}|{array}) TO DISPLAY({end_of_line})", line):
                self._transpiled += f'{indent}print({print_function.group(1).replace(' ', '')}){str(print_function.group(2) or '')}'
            
            # input function
            elif input_function := fullmatch(rf"RECEIVE ({var_index}) FROM (?:\(STRING\)|\(INTEGER\)|\(CHARACTER\)) KEYBOARD({end_of_line})", line):
                self._transpiled = f'{indent}{input_function.group(1)} = input(){str(input_function(2) or '')}'

            # If conditions
            elif if_condition := fullmatch(rf'{indent}IF ({condition}) THEN({end_of_line})', line):
                self._transpiled += f'{indent}if {if_condition.group(1)}:{str(if_condition.group(2) or '')}'
                indent += '    '
            
            elif elif_condition := fullmatch(rf"{indent.removesuffix('    ')}ELSE IF ({condition}) THEN({end_of_line})", line):
                self._transpiled += f'{indent}elif {elif_condition.group(1)}:{str(elif_condition.group(2) or '')}'
            
            elif fullmatch(rf'{indent.removesuffix('    ')}END IF({end_of_line})', line):
                indent.removesuffix('    ')

            elif while_loop := fullmatch(rf"WHILE ({condition}) DO({end_of_line})", line):
                self._transpiled += f'{indent}while {while_loop.group(1)}:{str(while_loop.group(2) or '')}'
                indent += '    '
            
            elif fullmatch(rf'{indent.removesuffix('    ')}END WHILE({end_of_line})', line):
                indent = indent.removesuffix('    ')
            
            elif fullmatch(rf'REPEAT({end_of_line})', line):
                ...
            
            elif define := match(rf"FUNCTION({end_of_line})", line):
                ...
            
            else:
                print(f'Syntax Error at line{self.pseudocode.index (line)}')
                exit()


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
        compilation = ''.join(self.pseudocode)
        print(compilation)
            
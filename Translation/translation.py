from re import *
from os import path

# Class for conditions within ifs, elifs and elses 
class Condition():
    def __init__(self, condition: str) -> None:
        self.condition = condition

    
    @property
    def condition(self):
        return self._condition


    @condition.setter
    def condition(self, condition):
        # Replace valid python syntax
        # I actually dont know how to make sure these are not in a string, so just pray :pray:
        # did look into (?:)
        self._condition = sub(r'<>', '!=', sub(r'=', '==', sub(r'NOT', 'not', sub(r'AND', 'and', sub(r'OR', 'or', condition)))))


    def __str__(self):
        return self._condition


class Translation():
    def __init__(self, PSEUDOCODE: str) -> None:
        self.PSEUDOCODE = PSEUDOCODE
        self._variables = {}
        self._transpiled = ''


    # Getter for the written PSEUDOCODE
    @property
    def PSEUDOCODE(self) -> str:
        return self._PSEUDOCODE


    @PSEUDOCODE.setter
    def PSEUDOCODE(self, PSEUDOCODE: str) -> None:
        self._PSEUDOCODE = PSEUDOCODE
    

    def compile(self):
        # For indentation
        indent: str = ''

        # Common regex patterns
        value: str = r"[^'\"\[\]]+(?:\[[^'\"]+\])*"
        # If anyone could clarify if a ' can be in a string in PSEUDOCODE, thatd be great
        string: str = r"(?:'.*'|\".*\")"
        array: str = r"\[.*\]"
        # regex for variable / array index initialisation
        variable: str = r"[^ '\"\[\]]+"
        var_index: str = rf"{variable}(?:\[[^'\"]+\])*"
        # Also whether or not its fine for the ' ?' to be a ' *' instead
        condition: str = rf"(?:NOT )?{value}(?: ?(?:=|<>|>|>=|<|<=) ?{value})?(?: (?:AND|OR) (?:NOT )?{value}(?: ?(?:=|<>|>|>=|<|<=) ?{value})?)*"
        arithmetic: str = r" ?(?:\+|-|\*|\^)"
        comment: str = r'#.*'
        end_of_line: str = rf' *(?:{comment})?(?:\n)?'

        for line in self.PSEUDOCODE:

            # Variables and arrays
            if var_set := fullmatch(rf"{indent}SET ({var_index}) TO ({value}|{string}|{array})({end_of_line})", line):
                self._transpiled += f'{indent}{var_set.group(1)} = {var_set.group(2)}{str(var_set.group(3) or '')}'

            # Empty lines / Comments
            elif empty_line := fullmatch(rf'({end_of_line})', line):
                self._transpiled += f'{str(empty_line.group(1) or '')}'

            # Input / Output
            elif print_function := fullmatch(rf"{indent}SEND ({value}|{string}|{array}) TO DISPLAY({end_of_line})", line):
                self._transpiled += f'{indent}print({print_function.group(1).replace(' ', '')}){str(print_function.group(2) or '')}'

            elif input_function := fullmatch(rf"{indent}RECEIVE ({var_index}) FROM (\(STRING\)|\(INTEGER\)|\(CHARACTER\)) KEYBOARD({end_of_line})", line):
                if input_function.group(2) == '(INTEGER)':
                    self._transpiled += f'{indent}{input_function.group(1)} = int(input()){str(input_function.group(3) or '')}'
                else:
                    self._transpiled += f'{indent}{input_function.group(1)} = input(){str(input_function.group(3) or '')}'

            # Selection
            elif if_condition := fullmatch(rf'{indent}IF ({condition}) THEN({end_of_line})', line):
                self._transpiled += f'{indent}if {str(Condition(if_condition.group(1)))}: {str(if_condition.group(2) or '')}'
                indent += '    '
            
            elif elif_condition := fullmatch(rf"{indent.removesuffix('    ')}ELSE IF ({condition}) THEN({end_of_line})", line):
                self._transpiled += f'{indent}elif {str(Condition(elif_condition.group(1)))}: {str(elif_condition.group(2) or '')}'
            
            elif else_condition := fullmatch(rf"{indent.removesuffix('    ')}ELSE({end_of_line})", line):
                self._transpiled += f'{indent.removesuffix('    ')}else: {str(else_condition.group(1) or '')}'
            
            elif fullmatch(rf'{indent.removesuffix('    ')}END IF({end_of_line})', line):
                indent = indent.removesuffix('    ')

            # Repitition
            # While loops
            elif while_loop := fullmatch(rf"{indent}WHILE ({condition}) DO({end_of_line})", line):
                self._transpiled += f'{indent}while {str(Condition(while_loop.group(1)))}:{str(while_loop.group(2) or '')}'
                indent += '    '
            
            elif fullmatch(rf'{indent.removesuffix('    ')}END WHILE({end_of_line})', line):
                indent = indent.removesuffix('    ')

            # Repeat loops
            elif repeat := fullmatch(rf'{indent}REPEAT({end_of_line})', line):
                ...

            # For loops
            elif for_loop := fullmatch(rf'{indent}FOR ([^ \[\]]+) FROM ({value}) TO ({value}) (?:(?:STEP )({value}) )?DO({end_of_line})', line):
                if for_loop.group(4):
                    self._transpiled += f'{indent}for {for_loop.group(1)} in range({for_loop.group(2)}, {for_loop.group(3)}, {for_loop.group(4)}): {str(for_loop.group(5) or '')}'
                else:
                    self._transpiled += f'{indent}for {for_loop.group(1)} in range({for_loop.group(2)}, {for_loop.group(3)}): {str(for_loop.group(5) or '')}'
                indent += '    '
            
            elif iteration := fullmatch(rf'{indent}FOR EACH ({var_index}) FROM ({value}|{string}|{array}) DO({end_of_line})', line):
                self._transpiled += f'{indent}for {iteration.group(1)} in {iteration.group(2)}: {str(iteration.group(3) or '')}'
                indent += '    '
            
            elif fullmatch(rf'{indent.removesuffix('    ')}END FOR({end_of_line})', line):
                indent = indent.removesuffix('    ')
            
            # File handling
            elif read := fullmatch(rf"READ({end_of_line})", line):
                ...

            elif write := fullmatch(rf"WRITE({end_of_line})", line):
                ...

            # Subprograms
            elif define := fullmatch(rf"{indent}FUNCTION ({variable}) ?(\((?:{variable}(?:, {variable}?))*\))({end_of_line})", line):
                ...
            
            elif return_val := fullmatch(rf"{indent.removesuffix('    ')}RETURN (.*)", line):
                ...
            
            else:   
                print(indent, 'baa')
                print(line)
                print(f'Syntax Error at line {self.PSEUDOCODE.index(line) + 1}')
                exit()
        
        # Additional functions
        self._transpiled, count = subn(r'RANDOM\(', 'randint(0, ',  ''.join(self._transpiled))
        if count > 0:
            self._transpiled: str = 'from random import randint\n\n' + self._transpiled
        print()


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

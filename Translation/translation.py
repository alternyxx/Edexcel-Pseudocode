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
        self._condition = sub(r'<>', '!=', sub(r'=', '==', sub(r'NOT', 'not', sub(r'AND', 'and', sub(r'OR', 'or', condition)))))


    def __str__(self):
        return self._condition


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
        string = r"(?:'.*'|\".*\")"
        array = r"\[.*\]"
        # regex for variable / array index initialisation
        var_index = r"[^ \[\]]+(?:\[[^ '\"]+\])*"
        # Also whether or not its fine for the ' ?' to be a ' *' instead
        condition = rf"(?:NOT )?{value}(?: ?(?:=|<>|>|>=|<|<=) ?{value})?(?: (?:AND|OR) (?:NOT )?{value}(?: ?(?:=|<>|>|>=|<|<=) ?{value})?)*"
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
            elif input_function := fullmatch(rf"{indent}RECEIVE ({var_index}) FROM (\(STRING\)|\(INTEGER\)|\(CHARACTER\)) KEYBOARD({end_of_line})", line):
                if input_function.group(2) == '(INTEGER)':
                    self._transpiled += f'{indent}{input_function.group(1)} = int(input()){str(input_function.group(3) or '')}'
                else:
                    self._transpiled += f'{indent}{input_function.group(1)} = input(){str(input_function.group(3) or '')}'

            # If conditions
            elif if_condition := fullmatch(rf'{indent}IF ({condition}) THEN({end_of_line})', line):
                self._transpiled += f'{indent}if {str(Condition(if_condition.group(1)))}: {str(if_condition.group(2) or '')}'
                indent += '    '
            
            elif elif_condition := fullmatch(rf"{indent.removesuffix('    ')}ELSE IF ({condition}) THEN({end_of_line})", line):
                self._transpiled += f'{indent}elif {str(Condition(elif_condition.group(1)))}: {str(elif_condition.group(2) or '')}'
            
            elif else_condition := fullmatch(rf"{indent.removesuffix('    ')}ELSE({end_of_line})", line):
                self._transpiled += f'{indent.removesuffix('    ')}else: {str(else_condition.group(1) or '')}'
            
            elif fullmatch(rf'{indent.removesuffix('    ')}END IF({end_of_line})', line):
                indent = indent.removesuffix('    ')

            elif while_loop := fullmatch(rf"{indent}WHILE ({condition}) DO({end_of_line})", line):
                self._transpiled += f'{indent}while {str(Condition(while_loop.group(1)))}:{str(while_loop.group(2) or '')}'
                indent += '    '
            
            elif repeat := fullmatch(rf'{indent}REPEAT({end_of_line})', line):
                ...

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
            
            elif fullmatch(rf'{indent.removesuffix('    ')}END WHILE({end_of_line})', line):
                indent = indent.removesuffix('    ')
            
            elif fullmatch(rf'{indent}REPEAT({end_of_line})', line):
                ...
            
            elif define := match(rf"FUNCTION({end_of_line})", line):
                ...
            
            else:   
                print(indent, 'baa')
                print(line)
                print(f'Syntax Error at line {self.pseudocode.index(line) + 1}')
                exit()
            
        self._transpiled, count = subn(r'RANDOM\(', 'randint(0, ',  ''.join(self._transpiled))
        if count > 0:
            self._transpiled = 'from random import randint\n\n' + self._transpiled
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

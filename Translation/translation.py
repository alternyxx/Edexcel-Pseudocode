from re import *
from os import path

# Class for conditions within ifs, elifs and elses 
class Condition():
    def __init__(self, condition: str) -> None:
        self.condition = condition

    
    @property
    def condition(self) -> str:
        return self._condition


    @condition.setter
    def condition(self, condition: str) -> None:
        # Replace valid python syntax
        # I actually dont know how to make sure these are not in a string, so just pray :pray:
        # did look into (?:)
        self._condition = sub(r'<>', '!=', sub(r'=', '==', sub(r'NOT', 'not', sub(r'AND', 'and', sub(r'OR', 'or', condition)))))


    def __str__(self) -> str:
        return self._condition


class Translation():
    def __init__(self, PSEUDOCODE: str) -> None:
        self.PSEUDOCODE: str = PSEUDOCODE
        self._variables: dict = {}
        self._transpiled: str = ''



    @property
    def PSEUDOCODE(self) -> str:
        return self._PSEUDOCODE


    @PSEUDOCODE.setter
    def PSEUDOCODE(self, PSEUDOCODE: str) -> None:
        self._PSEUDOCODE: str = PSEUDOCODE
    

    def compile(self) -> None:
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

        # Compiling regex patterns
        # Variables and arrays
        var_set: Pattern = compile(rf"{indent}SET ({var_index}) TO ({value}|{string}|{array})({end_of_line})")

        # Empty lines
        empty_line: Pattern = compile(rf'({end_of_line})')

        # Input/Output
        print_function: Pattern = compile(rf"{indent}SEND ({value}|{string}|{array}) TO DISPLAY({end_of_line})")
        input_function: Pattern = compile(rf"{indent}RECEIVE ({var_index}) FROM (\(STRING\)|\(INTEGER\)|\(CHARACTER\)) KEYBOARD({end_of_line})")

        # Selection
        if_condition: Pattern = compile(rf"{indent}IF ({condition}) THEN({end_of_line})")
        elif_condition: Pattern = compile(rf"{indent}IF ({condition}) THEN({end_of_line})")
        else_condition: Pattern = compile(rf"{indent.removesuffix('    ')}ELSE({end_of_line})")
        end_if: Pattern = compile(rf'{indent.removesuffix('    ')}END IF({end_of_line})')

        # Repitition
        # while loops
        while_loop: Pattern = compile(rf"{indent}WHILE ({condition}) DO({end_of_line})")
        end_while: Pattern = compile(rf"{indent.removesuffix('    ')}END WHILE({end_of_line})")

        # repeat loops
        repeat_loop: Pattern = compile(rf'{indent}REPEAT({end_of_line})')

        # for loops
        for_loop: Pattern = compile(rf'{indent}FOR ([^ \[\]]+) FROM ({value}) TO ({value}) (?:(?:STEP )({value}) )?DO({end_of_line})')
        for_each: Pattern = compile(rf"{indent}FOR EACH ({var_index}) FROM ({value}|{string}|{array}) DO({end_of_line})")
        end_for: Pattern = compile(rf'{indent.removesuffix('    ')}END FOR({end_of_line})')

        # File handing
        read: Pattern = compile(rf"READ({end_of_line})")
        write: Pattern = compile(rf"WRITE({end_of_line})")


        # Subprograms
        procedure: Pattern = compile()
        function: Pattern = compile(rf"{indent}FUNCTION ({variable}) ?(\((?:{variable}(?:, {variable}?))*\))({end_of_line})")
        return_val: Pattern = compile(rf"{indent.removesuffix('    ')}RETURN (.*)")

        for line in self.PSEUDOCODE:

            # declaration and initialization of a variable
            if var_set_result := var_set.fullmatch(line):
                self._transpiled += f'{indent}{var_set_result.group(1)} = {var_set_result.group(2)}{str(var_set_result.group(3) or '')}'

            elif empty_line_result := empty_line.fullmatch(line):
                self._transpiled += f'{str(empty_line_result.group(1) or '')}'

            # print function
            elif print_function_result := print_function.fullmatch(line):
                self._transpiled += f'{indent}print({print_function_result.group(1).replace(' ', '')}){str(print_function_result.group(2) or '')}'

            # input function
            elif input_function_result := input_function.fullmatch(line):
                if input_function_result.group(2) == '(INTEGER)':
                    self._transpiled += f'{indent}{input_function_result.group(1)} = int(input()){str(input_function_result.group(3) or '')}'
                else:
                    self._transpiled += f'{indent}{input_function_result.group(1)} = input(){str(input_function_result.group(3) or '')}'

            # If conditions
            elif if_condition_result := if_condition.fullmatch(line):
                self._transpiled += f'{indent}if {str(Condition(if_condition_result.group(1)))}: {str(if_condition_result.group(2) or '')}'
                indent += '    '
            
            elif elif_condition_result := elif_condition.fullmatch(line):
                self._transpiled += f'{indent}elif {str(Condition(elif_condition_result.group(1)))}: {str(elif_condition_result.group(2) or '')}'
            
            elif else_condition_result := else_condition.fullmatch(line):
                self._transpiled += f'{indent.removesuffix('    ')}else: {str(else_condition_result.group(1) or '')}'
            
            elif end_if.fullmatch(line):
                indent = indent.removesuffix('    ')

            elif while_loop_result := while_loop.fullmatch(line):
                self._transpiled += f'{indent}while {str(Condition(while_loop_result.group(1)))}:{str(while_loop_result.group(2) or '')}'
                indent += '    '
            
            elif fullmatch(rf'{indent}REPEAT({end_of_line})', line):
                indent += '    '

            elif for_loop_result := for_loop.fullmatch(line):
                if for_loop_result.group(4):
                    self._transpiled += f'{indent}for {for_loop_result.group(1)} in range({for_loop_result.group(2)}, {for_loop_result.group(3)}, {for_loop_result.group(4)}): {str(for_loop_result.group(5) or '')}'
                else:
                    self._transpiled += f'{indent}for {for_loop_result.group(1)} in range({for_loop_result.group(2)}, {for_loop_result.group(3)}): {str(for_loop_result.group(5) or '')}'
                indent += '    '
            
            elif for_each_result := end_for.fullmatch(line):
                self._transpiled += f'{indent}for {for_each_result.group(1)} in {for_each_result.group(2)}: {str(for_each_result.group(3) or '')}'
                indent += '    '
            
            elif end_for.fullmatch(line):
                indent = indent.removesuffix('    ')
            
            elif end_while.fullmatch(line):
                indent = indent.removesuffix('    ')
            
            elif procedure := match(rf""):
                ...

            elif define := function.fullmatch(line):
                ...
            
            else:   
                print(indent, 'baa')
                print(line)
                print(f'Syntax Error at line {self.PSEUDOCODE.index(line) + 1}')
                exit()

        self._transpiled = sub(r'LENGTH(', 'len(', self._transpiled)    
        self._transpiled, count = subn(r'RANDOM\(', 'randint(0, ',  self._transpiled)
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

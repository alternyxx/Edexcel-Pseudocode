from re import *

# Class for conditions within ifs, elifs and elses 
class Condition():
    def __init__(self, condition: str) -> None:
        self.condition: str = condition

    
    @property
    def condition(self) -> str:
        return self._condition


    @condition.setter
    def condition(self, condition) -> None:
        # Replace with valid python syntax
        # I actually dont know how to make sure these are not in a string, so just pray :pray:
        # future self: i actually do, i just dont wanna delete this class :P
        self._condition: str = sub(r'<>', '!=', sub(r'(?<!\!\>\<)=', '==', sub(r'NOT', 'not', sub(r'AND', 'and', sub(r'OR', 'or', condition)))))


    def __str__(self) -> str:
        return self._condition


class Translation():
    def __init__(self, pseudocode: list) -> None:
        self.pseudocode: list = pseudocode
        self._variables: str = {}
        self._transpiled: str = ''


    # Getter for the written pseudocode
    @property
    def pseudocode(self) -> str:
        return self._pseudocode


    @pseudocode.setter
    def pseudocode(self, pseudocode: list) -> None:
        self._pseudocode: list = pseudocode
    

    def compile(self):
        # For indentation
        indent: str = ''

        # Common regex patterns
        value: str = r"[^'\"\[\]]+(?:\[[^'\"]+\])*"
        # If anyone could clarify if a ' can be in a string in pseudocode, thatd be great
        string: str = r"'[^']*'|\"[^\"]*\""
        array: str = r"\[.*\]"
        # regex for variable / array index initialisation
        variable: str = r"[^ '\"\[\]]+"
        var_index: str = rf"{variable}(?:\[[^'\"]+\])*"
        # Also whether or not its fine for the ' ?' to be a ' *' instead
        condition: str = rf"(?:NOT )?{value}(?: ?(?:=|<>|>|>=|<|<=) ?{value})?(?: (?:AND|OR) (?:NOT )?{value}(?: ?(?:=|<>|>|>=|<|<=) ?{value})?)*"
        
        # no, even though i unescaped spaces, im not going back to normal ' 's because it has traumatised me
        space: str = rf"(?: )"
        newline:str = rf"(?:\n)"
        comment: str = r"#.*"
        end_of_line: str = rf"{space}*(?:{comment})?{newline}?"

        end_vals = {
            "if_statement": [],
            "while_loop": [],
            "for_loop": [],
            "for_each_loop": [],
            }

        for result_line in self.pseudocode:
            #result_line = escape(line)
            #result_line = result_line.replace('\\ ', ' ').replace('\\\n', 's\n')
            # Variables and arrays
            if var_set := fullmatch(rf"{indent}SET{space}({var_index}){space}TO{space}({value}|{string}|{array})({end_of_line})", result_line):
                self._transpiled += f"{indent}{var_set.group(1)} = {var_set.group(2)}{str(var_set.group(3) or '')}"

            # Empty lines / Comments
            elif empty_line := fullmatch(rf"({end_of_line})", result_line):
                self._transpiled += f"{str(empty_line.group(1) or '')}"

            # Input / Output
            elif print_function := fullmatch(rf"{indent}SEND{space}({value}|{string}|{array}){space}TO{space}DISPLAY({end_of_line})", result_line):
                self._transpiled += f"{indent}print({print_function.group(1)}){str(print_function.group(2) or '')}"

            elif input_function := fullmatch(rf"{indent}RECEIVE{space}({var_index}){space}FROM{space}(\(STRING\)|\(INTEGER\)|\(CHARACTER\)){space}KEYBOARD({end_of_line})", result_line):
                if input_function.group(2) == '(INTEGER)':
                    self._transpiled += f"{indent}{input_function.group(1)} = int(input()){str(input_function.group(3) or '')}"
                else:
                    self._transpiled += f"{indent}{input_function.group(1)} = input(){str(input_function.group(3) or '')}"

            # Selection
            elif if_condition := fullmatch(rf"{indent}IF{space}({condition}){space}THEN({end_of_line})", result_line):
                self._transpiled += f"{indent}if {str(Condition(if_condition.group(1)))}: {str(if_condition.group(2) or '')}"
                indent += '    '
            
            elif elif_condition := fullmatch(rf"{indent.removesuffix('    ')}ELSE{space}IF{space}({condition}){space}THEN({end_of_line})", result_line):
                self._transpiled += f"{indent.removesuffix('    ')}elif {str(Condition(elif_condition.group(1)))}: {str(elif_condition.group(2) or '')}"
            
            elif else_condition := fullmatch(rf"{indent.removesuffix('    ')}ELSE({end_of_line})", result_line):
                self._transpiled += f"{indent.removesuffix('    ')}else: {str(else_condition.group(1) or '')}"
            
            elif fullmatch(rf"{indent.removesuffix('    ')}END{space}IF({end_of_line})", result_line):
                indent = indent.removesuffix('    ')

            # Repitition
            # While loops
            elif while_loop := fullmatch(rf"{indent}WHILE{space}({condition}){space}DO({end_of_line})", result_line):
                self._transpiled += f"{indent}while {str(Condition(while_loop.group(1)))}:{str(while_loop.group(2) or '')}"
                indent += '    '
            
            elif fullmatch(rf"{indent.removesuffix('    ')}END{space}WHILE({end_of_line})", result_line):
                indent = indent.removesuffix('    ')

            # Repeat loops
            elif repeat := fullmatch(rf"{indent}REPEAT({end_of_line})", result_line):
                ...

            elif repeat_for := fullmatch(rf"{indent}REPEAT({end_of_line})((?:value|[0-9]+(?:-Number))){space}TIMES({end_of_line})", result_line):
                self.transpiled += f"{indent}for _ in range"

            elif until := fullmatch(rf"UNTIL{space}{condition}({end_of_line})", result_line):
                self.transpiled += ""
            
            elif end_repeat := fullmatch(rf"{indent.removesuffix('    ')}END{space}REPEAT({end_of_line})", result_line):
                ...

            # For loops
            elif for_loop := fullmatch(rf"{indent}FOR{space}([^ \[\]]+){space}FROM{space}({value}){space}TO{space}({value}){space}(?:(?:STEP{space})({value}){space})?DO({end_of_line})", result_line):
                if for_loop.group(4):
                    self._transpiled += f"{indent}for {for_loop.group(1)} in range({for_loop.group(2)}, {for_loop.group(3)} + 1, {for_loop.group(4)}): {str(for_loop.group(5) or '')}"
                else:
                    self._transpiled += f"{indent}for {for_loop.group(1)} in range({for_loop.group(2)}, {for_loop.group(3)}): {str(for_loop.group(5) or '')}"
                indent += '    '
            
            elif iteration := fullmatch(rf'{indent}FOR{space}EACH{space}({var_index}){space}FROM{space}({value}|{string}|{array}){space}DO({end_of_line})', result_line):
                self._transpiled += f"{indent}for {iteration.group(1)} in {iteration.group(2)}: {str(iteration.group(3) or '')}"
                indent += '    '
            
            elif fullmatch(rf"{indent.removesuffix('    ')}END{space}FOR({end_of_line})", result_line):
                indent = indent.removesuffix('    ')
            
            elif fullmatch(rf"{indent.removesuffix('    ')}END{space}FOR{space}?EACH({end_of_line})", result_line):
                indent = indent.removesuffix('    ')
            
            # File handling
            elif read := fullmatch(rf"READ{space}(\w+.\w){space}(?:[a-zA-Z0-9_ '\"]*)({end_of_line})", result_line):
                self._transpiled += f"with open({read.group(1)}) as file:"

            elif write := fullmatch(rf"WRITE(?:[a-zA-Z0-9_ '\"]*)({end_of_line})", result_line):
                ...

            # Subprograms
            elif procedure := fullmatch(rf"{indent}PROCEDURE{space}({variable}){space}?(\((?:{variable}(?:,{space}{variable}?))*\))({end_of_line})", result_line):
                self._transpiled += f"{indent}# This was originally a procedure\n{indent}def {procedure.group(1)}({(define.group(2))}): {(define.group(3))}"

            elif fullmatch(rf"{indent}BEGIN{space}PROCEDURE({end_of_line})", result_line):
                indent += '    '

            elif define := fullmatch(rf"{indent}FUNCTION{space}({variable}){space}?(\((?:{variable}(?:,{space}{variable}?))*\))({end_of_line})", result_line):
                self._transpiled += f"def {define.group(1)}({(define.group(2))}): {(define.group(3))}"
            
            elif fullmatch(rf"{indent}BEGIN{space}FUNCTION({end_of_line})", result_line):
                indent += '    '
            
            elif return_val := fullmatch(rf"{indent.removesuffix('    ')}RETURN{space}(.*)({end_of_line})", result_line):
                self._transpiled += f"{indent}return {return_val.group(1)}"
            
            elif fullmatch(rf"{indent.removesuffix('    ')}END FUNCTION({end_of_line})", result_line):
                indent.removesuffix('    ')
            
            # Unrecognised syntax
            else:   
                print(f'Syntax Error at line {self.pseudocode.index(result_line) + 1}')
                exit()
        
        # Additional functions
        self._transpiled = sub(r'LENGTH\(', r'len\(', self._transpiled)    
        self._transpiled, count = subn(r'RANDOM\(', r'randint\(0, ',  ''.join(self._transpiled))
        if count > 0:
            self._transpiled: str = 'from random import randint\n\n' + self._transpiled


    def output_file(self, output_file):
        # Try to transpile the file in the place user gives
        try:
            with open(output_file, 'w') as transpiled_file:
                # Write the transpiled code
                transpiled_file.write(self._transpiled)
        except:
            print('Unable to access output file location.')
            exit()
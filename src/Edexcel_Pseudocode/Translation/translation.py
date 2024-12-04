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
        self._transpiled: str = ''


    # Getter for the written pseudocode
    @property
    def pseudocode(self) -> str:
        return self._pseudocode


    @pseudocode.setter
    def pseudocode(self, pseudocode: list) -> None:
        self._pseudocode: list = pseudocode
    

    def transpile(self):
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
        newline:str = rf"(?:\n)"
        comment: str = r"#.*"
        end_of_line: str = rf" *(?:{comment})?{newline}?"

        # Compiling regex patterns
        # Variables and arrays
        var_set: Pattern = compile(rf"SET ({var_index}) TO ({value}|{string}|{array})({end_of_line})")

        # Empty lines
        empty_line: Pattern = compile(rf"({end_of_line})")

        # Input/Output
        print_function: Pattern = compile(rf"SEND ({value}|{string}|{array}) TO DISPLAY({end_of_line})")
        input_function: Pattern = compile(rf"RECEIVE ({var_index}) FROM (\(STRING\)|\(INTEGER\)|\(CHARACTER\)) KEYBOARD({end_of_line})")

        # Selection
        if_condition: Pattern = compile(rf"IF ({condition}) THEN({end_of_line})")
        elif_condition: Pattern = compile(rf"IF ({condition}) THEN({end_of_line})")
        else_condition: Pattern = compile(rf"ELSE({end_of_line})")
        end_if: Pattern = compile(rf"END IF({end_of_line})")

        # Repitition
        # while loops
        while_loop: Pattern = compile(rf"WHILE ({condition}) DO({end_of_line})")
        end_while: Pattern = compile(rf"END WHILE({end_of_line})")

        # repeat loops
        repeat_loop: Pattern = compile(rf"REPEAT({end_of_line})")
        until: Pattern = compile(rf"UNTIL {condition}({end_of_line})")
        repeat_for: Pattern = compile(rf"REPEAT ((?:{value}|[0-9]+(?:-Number))) TIMES({end_of_line})")
        end_repeat: Pattern = compile(rf"END REPEAT({end_of_line})")

        # for loops
        for_loop: Pattern = compile(rf"FOR ([^ \[\]]+) FROM ({value}) TO ({value}) (?:(?:STEP )({value}) )?DO({end_of_line})")
        for_each: Pattern = compile(rf"FOR EACH ({var_index}) FROM ({value}|{string}|{array}) DO({end_of_line})")
        end_for: Pattern = compile(rf"END FOR({end_of_line})")
        # the appendix i cited doesnt have the space there LMFAO, the textbook has it tho
        end_for_each: Pattern = compile(rf"END FOR ?EACH({end_of_line})")

        # File handing
        fread: Pattern = compile(rf"READ (\w+.\w) (?:[a-zA-Z0-9_ '\"]*)({end_of_line})")
        fwrite: Pattern = compile(rf"WRITE(?:[a-zA-Z0-9_ '\"]*)({end_of_line})")

        # Subprograms
        procedure: Pattern = compile(rf"PROCEDURE ({variable}) ?(\((?:{variable}(?:, {variable}?))*\))({end_of_line})")
        begin_procedure: Pattern = compile(rf"BEGIN PROCEDURE({end_of_line})")
        function: Pattern = compile(rf"FUNCTION ({variable}) ?(\((?:{variable}(?:, {variable}?))*\))({end_of_line})")
        begin_function: Pattern =compile(rf"BEGIN FUNCTION({end_of_line})")
        return_val: Pattern = compile(rf"RETURN (.*)")
        end_function: Pattern = compile(rf"END FUNCTION({end_of_line})")

        # Dev checks
        variables: list[str] = []
        functions: list[str] = []
        end_vals: dict = {
            "if_statement": {"line": None, "indent": None},
            "while_loop": {"line": None, "indent": None},
            "for_loop": {"line": None, "indent": None},
            "for_each_loop": {"line": None, "indent": None},
            }

        for line in self.pseudocode:
            if line.startswith(indent):
                result_line = line.removeprefix(indent)
                # Variables and arrays
                if var_set_result := var_set.fullmatch(result_line):
                    self._transpiled += f"{indent}{var_set_result.group(1)} = {var_set_result.group(2)}{str(var_set_result.group(3) or '')}"

                # Empty lines / Comments
                elif empty_line_result := empty_line.fullmatch(result_line):
                    self._transpiled += f"{str(empty_line_result.group(1) or '')}"

                # Input / Output
                elif print_function_result := print_function.fullmatch(result_line):
                    self._transpiled += f"{indent}print({print_function_result.group(1)}){str(print_function_result.group(2) or '')}"

                elif input_function_result := input_function.fullmatch(result_line):
                    if input_function_result.group(2) == "(INTEGER)":
                        self._transpiled += f"{indent}{input_function_result.group(1)} = int(input()){str(input_function_result.group(3) or '')}"
                    else:
                        self._transpiled += f"{indent}{input_function_result.group(1)} = input(){str(input_function_result.group(3) or '')}"

                # Selection
                elif if_condition_result := if_condition.fullmatch(result_line):
                    self._transpiled += f"{indent}if {str(Condition(if_condition_result.group(1)))}: {str(if_condition_result.group(2) or '')}"
                    indent += '    '

                # Repitition
                # While loops
                elif while_loop_result := while_loop.fullmatch(result_line):
                    self._transpiled += f"{indent}while {str(Condition(while_loop_result.group(1)))}:{str(while_loop_result.group(2) or '')}"
                    indent += '    '
                
                # Repeat loops
                elif repeat := fullmatch(rf"{indent}REPEAT({end_of_line})", result_line):
                    ...

                elif repeat_for_result := repeat_for.fullmatch(result_line):
                    self.transpiled += f"{indent}for _ in range"

                # For loops
                elif for_loop_result := for_loop.fullmatch(result_line):
                    if for_loop_result.group(4):
                        self._transpiled += f'{indent}for {for_loop_result.group(1)} in range({for_loop_result.group(2)}, {for_loop_result.group(3)} + 1, {for_loop_result.group(4)}): {str(for_loop_result.group(5) or '')}'
                    else:
                        self._transpiled += f'{indent}for {for_loop_result.group(1)} in range({for_loop_result.group(2)}, {for_loop_result.group(3)}): {str(for_loop_result.group(5) or '')}'
                    indent += '    '
                
                elif for_each_result := for_each.fullmatch(result_line):
                    self._transpiled += f'{indent}for {for_each_result.group(1)} in {for_each_result.group(2)}: {str(for_each_result.group(3) or '')}'
                    indent += '    '
                
                # File handling
                elif fread_result := fread.fullmatch(result_line):
                    self._transpiled += f"with open({fread_result.group(1)}) as file:"

                elif fwrite_result := fwrite.fullmatch(result_line):
                    self._transpiled += f"with open({fwrite_result.group(1)}, w) as file:"

                # Subprograms
                elif procedure_result := procedure.fullmatch(result_line):
                    self._transpiled += f'{indent}# This was originally a procedure\n{indent}def {procedure_result.group(1)}({(procedure_result.group(2))}): {(procedure_result.group(3))}'

                elif fullmatch(result_line):
                    indent += '    '

                elif function_result := function.fullmatch(result_line):
                    self._transpiled += f"def {function_result.group(1)}({(function_result.group(2))}): {(function_result.group(3))}"
                
                elif fullmatch(result_line):
                    indent += '    '
                
                elif return_val_result := return_val.fullmatch(result_line):
                    self._transpiled += f"{indent}return {return_val_result.group(1)}{return_val_result.group(2)}"
                
                elif call_result := fullmatch(rf"{indent}({'|'.join(functions)})({end_of_line})", result_line):
                    self.transpiled += f"{call_result.group(1)}"

                # Unrecognised syntax
                else:   
                    print(f'Syntax Error at line {self.pseudocode.index(line) + 1}')
                    exit()

            # Deindent section
            else:
                # Selection
                result_line = line.removeprefix(indent + '    ')
                if elif_condition_result := elif_condition.fullmatch(result_line):
                    self._transpiled += f"{indent.removesuffix('    ')}elif {str(Condition(elif_condition_result.group(1)))}: {str(elif_condition_result.group(2) or '')}"
                
                elif else_condition_result := else_condition.fullmatch(result_line):
                    self._transpiled += f"{indent.removesuffix('    ')}else: {str(else_condition_result.group(1) or '')}"
                
                elif end_if.fullmatch(result_line):
                    indent = indent.removesuffix('    ')

                # Repitition
                # While Loops
                elif end_while.fullmatch(result_line):
                    indent = indent.removesuffix('    ')

                # Repeat Loops
                elif until_result := until.fullmatch(result_line):
                    self.transpiled += ""
                
                elif end_repeat := fullmatch(result_line):
                    ...

                # For Loops
                elif end_for.fullmatch(result_line):
                    indent = indent.removesuffix('    ')
                
                elif end_for_each.fullmatch(result_line):
                    indent = indent.removesuffix('    ')

                # Subprograms
                elif end_function.fullmatch(result_line):
                    indent.removesuffix('    ')
                
                else:   
                    print(f'Syntax Error at line {self.pseudocode.index(line) + 1}')
                    exit()

        # Additional functions
        # Skip over strings
        self._transpiled = sub(r'LENGTH\(', r'len\(', self._transpiled)    
        self._transpiled, count = subn(r'RANDOM\(', r'randint\(0, ',  ''.join(self._transpiled))
        if count > 0:
            self._transpiled = 'from random import randint\n\n' + self._transpiled


    def output_file(self, output_file):
        # Try to transpile the file in the place user gives
        try:
            with open(output_file, 'w') as transpiled_file:
                # Write the transpiled code
                transpiled_file.write(self._transpiled)
        except:
            print('Unable to access output file location.')
            exit()
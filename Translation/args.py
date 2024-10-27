from sys import exit
from argparse import ArgumentParser, Namespace

class Args():
    def __init__(self) -> None:
        self.parser = ArgumentParser(
                    prog = 'EdexcelPseudocode',
                    description = 'Transpile Pearson International GCSE Pseudocode to Python, essentially making them runnable and testable.')
        self.parser.add_arguement(
            'file', help = 'Enter file name in which the pseudocode is written.'
        )
        self.args: Namespace = self.parser.parse_args()


    def action(self):
        if len(self.args):
            print('''pseudo2py: missing operand
                  Try 'pseudo2py --help' for more information
                  ''')
            exit()


    @staticmethod
    def help(self):
        print('''Usage: pseudo2py [OPTION]... [PSEUDOCODE_FILE] [OUTPUT_FILE]
              Transpiles Pearson IGCSEs pseudocode to Python.

                --help          display this help and exit
              ''')

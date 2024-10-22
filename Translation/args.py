from sys import exit

class args():
    def __init__(self, args: list) -> None:
        self.args = args


    @property
    def args(self):
        return self._args
    

    @args.setter
    def args(self, args):
        self._args = args

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

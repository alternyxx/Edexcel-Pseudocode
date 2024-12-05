from argparse import ArgumentParser, Namespace

class Args():
    def __init__(self) -> None:
        self.parser: ArgumentParser = ArgumentParser(
                                            prog = "EdexcelPseudocode",
                                            #usage = '%(prog)s [options] Pseudocode_File'
                                            description = "Transpile Pearson International GCSE Pseudocode to Python, essentially making them runnable and testable."
                                            )
        self.parser.add_argument(
            "Pseudocode_File", help = "Enter file name in which the pseudocode is written.")
        
        self.parser.add_argument(
            "Output_File", help = "[Optional] Enter file name in which the pseudocode will be transpiled to Python.", default = None, nargs = '?')
        self.args: Namespace = self.parser.parse_args()
 
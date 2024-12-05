# from Translation.translation import Translation
# import cli
from edexcel_pseudocode import *


def main() -> None:
    # Class for handling CLI
    args: cli.Args = cli.Args()
    # File interpretation
    try:
        with open(args.args.Pseudocode_File) as file:
            pseudocode: list = file.readlines()
    # Doesnt Exist  
    except FileNotFoundError:
        print("File doesn't exist")
    else:
        # Translate the file
        translate = translation.Translation(pseudocode)
        translate.transpile()
        if args.args.Output_File:
            translate.output_file(args.args.Output_File)

        # Run the transpiled file
        exec(translate._transpiled)

if __name__ == "__main__":
    main()
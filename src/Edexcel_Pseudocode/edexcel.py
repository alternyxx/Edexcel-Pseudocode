# from Translation.translation import Translation
# import cli
from src.Edexcel_Pseudocode import *


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
        translation = translation.Translation(pseudocode)
        translation.transpile()
        translation.output_file('transpiled.py')
        if args.args.Output_File:
            translation.output_file(args.args.Output_File)

        # Run the transpiled file
        __import__('transpiled')

if __name__ == "__main__":
    main()
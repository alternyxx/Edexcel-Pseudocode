from re import search
from Translation.translation import Translation
from sys import argv
from os import path

def main() -> None:
    try:
        with open(path.join('temp', 'pseudocode.txt')) as file:
            pseudocode = file.readlines()
    except FileNotFoundError:
        print("File doesn't exist")
    except IndexError:
        print("pseudo2python -h for help")
    else:
        translation = Translation(pseudocode)
        translation.compile()
        translation.transpile()

if __name__ == "__main__":
    main()    
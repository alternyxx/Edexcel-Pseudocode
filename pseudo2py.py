from Translation.translation import Translation
from os import path

def main() -> None:
    try:
        with open(path.join('temp', 'pseudocode.txt')) as file:
            pseudocode = file.readlines()
    except FileNotFoundError:
        print("File doesn't exist")
    except IndexError:
        print("pseudo2python --h for help")
    else:
        translation = Translation(pseudocode)
        translation.compile()
        translation.output_file()

        # A rare time and never should anyone break the practice of importing at the top
        # This is to run the transpiled file
        import temp.transpiled

def parsing() -> None:
    ...


if __name__ == "__main__":
    main()    
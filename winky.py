#winky compiler code

import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage : python3 winkey.py <filename>")

    filename = sys.argv[1]
    print(filename)

    with open(filename) as file:
        source = file.read()
        print(source)

        #todo: tokenize the source code

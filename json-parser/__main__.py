import argparse, sys
from .src.parser import Parser

arg_parser = argparse.ArgumentParser(prog="json-parser", description="A JSON parser for a coding challenge")

arg_parser.add_argument('file', help="File to parse")

args = arg_parser.parse_args()

try:
    file = None
    with open(args.file) as fd:
        file = fd.read()

    json_parser = Parser(file)
    program_node = json_parser.parseProgram()

except FileNotFoundError:
    print(f'File {args.file} not found')
    sys.exit(1)
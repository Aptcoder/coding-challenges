import argparse, locale
import sys
from typing import IO
from src import wc, utils

parser = argparse.ArgumentParser(prog="ccwc", description="Coding challenge, wc tool copy attempt", add_help=True)

parser.add_argument('filepath', action="store", nargs="?", help="filepath to work with")
parser.add_argument('-c', action="store_true", help="return the number of bytes used in the file")
parser.add_argument('-m', action="store_true", help="return the number of characters in the file")
parser.add_argument('-l', action="store_true", help="return the number of lines in the file")
parser.add_argument('-w', action="store_true", help="return the number of words in the file")
args = parser.parse_args()


if not (args.c or args.l or args.w or args.m): # If none of the flags was used, use default setting
     args.c, args.l, args.w = True, True, True

output: str = ''
fd: IO = None 
try: 
    if args.filepath:
        try:
            fd = open(args.filepath, newline='')
            output = args.filepath + ' ' + output
        except FileNotFoundError:
                print(f'file at {args.filepath} not found')
                sys.exit(1)
    else:
        data = sys.stdin.read()
        '''
        Write to file because the stdin can not be `seeked` and that is being used in the wc package
        '''
        sample_fd = open('sample.txt', 'w')
        sample_fd.write(data)
        sample_fd.close()

        fd = open('sample.txt', 'r', newline="")
    

    if args.c:
        if args.m: # If -c is used, it cancels out -m if used before
            args.m = False
        number_of_bytes = wc.get_number_of_bytes(fd)
        output = utils.append_to_string(str(number_of_bytes), output)

    if args.m:
        number_of_characters = wc.get_number_of_characters(fd)
        output = utils.append_to_string(str(number_of_characters), output)

    if args.l or args.w:
        nl, nw = wc.get_number_of_lines_and_words(fd)
        if args.w:
            output = utils.append_to_string(str(nw), output)

        if args.l:
            output = utils.append_to_string(str(nl), output)

    if fd:
        fd.close()
except KeyboardInterrupt:
    print('\nprogram interrupted')
    sys.exit(1)
except Exception as e:
    print('Error', e)
    sys.exit(1)

print(output)
sys.exit(0)
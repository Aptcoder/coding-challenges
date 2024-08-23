import os, locale
from typing import IO


def get_number_of_bytes(fd: IO):
    fd.seek(0, os.SEEK_END)
    return fd.tell()

def get_number_of_lines_and_words(fd: IO):
    number_of_lines, number_of_words = 0, 0
    fd.seek(0)
    while line := fd.readline():
        number_of_lines += 1
        number_of_words += len(line.split())

    return number_of_lines, number_of_words

def get_number_of_characters(fd: IO):
    chunk_size = 1024 # a byte
    char_count = 0
    fd.seek(0)
    while data := fd.read(chunk_size):
      char_count += len(data)
    return char_count
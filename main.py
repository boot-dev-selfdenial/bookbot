#!/usr/bin/env python3
import argparse
import sys
import errno
from pathlib import Path, PurePath

def book_word_count(book_filename, book_contents):
    # Count words via split()
    word_count = len(book_contents.split())
    print(f"{word_count} words found within {book_filename.name}\n")

def book_character_stats(book_filename, book_contents):
    # Count the number of each character
    book_stats = {}
    book_characters = book_contents.lower()
    for character in book_characters[0::1]:
        if character not in book_stats:
            book_stats[character] = 1
        else:
            book_stats[character] += 1

    print(f"Character statistics for {book_filename.name}:")
    for character in sorted(book_stats, key=book_stats.get, reverse=True):
        print(f"The character {repr(character)} occurred {book_stats[character]} times")
    print(f"\n")

def main():
    # Obtain script_name based on filename
    script = PurePath(__file__)

    # Parse arguments
    arg_parser = argparse.ArgumentParser(prog=script.name,
                                         description='Parse a book',
                                         epilog='Have a look, read a book!')

    arg_parser.add_argument('-b', '--book',
                            help="The book to be parsed.",
                            default="books/frankenstein.txt",
                            type=Path)

    arg_parser.add_argument('-c', '--characterstats',
                            help="Print the book character statistics.",
                            default=False,
                            action=argparse.BooleanOptionalAction)

    arg_parser.add_argument('-p', '--print',
                            help="Print the entire book.",
                            default=False,
                            action=argparse.BooleanOptionalAction)

    arg_parser.add_argument('-w', '--wordcount',
                            help="Print the total count of words within the book.",
                            default=False,
                            action=argparse.BooleanOptionalAction)
    
    script_args = arg_parser.parse_args()

    book_print = script_args.print 
    book_wordcount = script_args.wordcount
    book_characterstats = script_args.characterstats

    if script_args.print == False and script_args.wordcount == False and script_args.characterstats == False:
        book_wordcount = True
        book_characterstats = True

    book_filename = PurePath(script_args.book)

    with open(book_filename) as book:
        book_contents = book.read()

        if book_print == True:
            print(f"{book_filename.name}:\n\n{book_contents}\n")

        if book_wordcount == True:
            book_word_count(book_filename, book_contents)

        if book_characterstats == True:
            book_character_stats(book_filename, book_contents)

try:
    main()
except IOError as e:
    if e.errno == errno.EPIPE:
        # Support pipeline
        pass

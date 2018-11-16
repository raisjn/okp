from __future__ import print_function

import sys
import os

from . import config

def get_parser():
    import argparse

    parser = argparse.ArgumentParser(description='Process .cpy files into C++')
    parser.add_argument('-ni', '--disable-implication', help='disables variable implication', action='store_true')
    parser.add_argument('files', nargs='*', help="list of files to process and compile")
    parser.add_argument('-o', '--output', dest='exename', default="a.out")
    parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")
    parser.add_argument('-p', '--print', dest='print_', action="store_true")
    parser.add_argument('-k', '--keep-dir', dest='keep_dir', action="store_true",
        help="keep compilation directory around")
    parser.add_argument('-c', '-ne', '--no-exe', dest='noexe', action="store_true",
        help='compile .o files only (no main)')
    parser.add_argument('-for', '--enable-for', dest='enable_for', action="store_true",
        help="enable for loop shorthand")
    parser.add_argument('-rof', '--enable-rof', dest='enable_rof', action="store_true",
        help="enable rof loop shorthand")

    return parser

def main():
    parser = get_parser()
    args = parser.parse_args()
    if not args.files:
        parser.print_help()
        return

    if args.disable_implication:
        transforms.variables.DECLARE_VARIABLES = False

    config.VERBOSE = args.verbose

    config.ENABLE_ROF = args.enable_rof
    config.ENABLE_FOR = args.enable_for

    config.KEEP_DIR = args.keep_dir

    from .project import compile_project
    compile_project(args)

if __name__ == "__main__":
    main()
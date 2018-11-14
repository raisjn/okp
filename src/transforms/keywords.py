from util import *

def remove_blocks(lines):
    new_lines = []
    for line in lines:
        indent = get_indent(line)
        cline = line.strip()
        if cline.startswith('block:'):
            line = "%s/* %s */" % (' ' * indent, cline)

        new_lines.append(line)
    return new_lines

def remove_knowns(lines):
    new_lines = []
    for line in lines:
        indent = get_indent(line)
        cline = line.strip()
        if cline.startswith('known '):
            line = "%s// %s" % (' ' * indent, cline)

        new_lines.append(line)
    return new_lines

def replace_tabs(lines):
    return [ line.replace('\t', '    ') for line in lines ]

def replace_pass(lines):
    new_lines = []
    for line in lines:
        if line.strip() == "pass":
            line = line.replace("pass", "(void)0")

        new_lines.append(line)

    return new_lines

def replace_for_shorthand(lines):
    new_lines = []
    for line in lines:
        sline = line.strip()

        if sline.startswith("for ") and sline.find(";") == -1:
            # check if we are in a range loop
            range_loop = False
            if sline.find(':') != -1 and sline.find(':') != len(sline) - 1:
                range_loop = True

            if not range_loop:
                rem = sline[len("for "):].rstrip(':')
                args = rem.split()

                ind = ' ' * get_indent(line)

                if len(args) == 2:
                    line = "%sfor auto %s = 0; %s < %s; %s++" % (ind, args[0], args[0], args[1], args[0])
                if len(args) == 3:
                    line = "%sfor auto %s = %s; %s < %s; %s++" % (ind, args[0], args[1], args[0],
                        args[2], args[0])
                if len(args) == 4:
                    line = "%sfor auto %s = %s; %s < %s; %s += %s" % (ind, args[0], args[1], args[0],
                        args[2], args[0], args[3])


        new_lines.append(line)

    return new_lines

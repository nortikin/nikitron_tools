#!/usr/bin/python

import os
import re
import sys


def file_replace(fname, s_before, s_after):
    out_fname = fname + ".tmp"
    out = open(out_fname, "w")
    for line in open(fname):
        out.write(re.sub(s_before, s_after, line))
    out.close()
    os.rename(out_fname, fname)


def mass_replace(dir_name, s_before, s_after):
    for dirpath, dirnames, filenames in os.walk(dir_name):
        for fname in filenames:
            f = fname.lower()
            # example: limit replace to .txt, .c, and .h files
            if f.endswith('.html'):
                doreplace = input("{0} make this?: ".format(f))
                if doreplace:
                    f = os.path.join(dirpath, fname)
                    file_replace(f, s_before, s_after)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        u = "Usage: replace <dir_name> <string_before> <string_after>\n"
        sys.stderr.write(u)
        sys.exit(1)

    mass_replace(sys.argv[1], sys.argv[2], sys.argv[3])

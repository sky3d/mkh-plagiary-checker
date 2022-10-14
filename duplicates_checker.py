# -*- coding: utf-8 -*-

from optparse import OptionParser
import os.path
import sys
import csv
from time import time
from datetime import datetime

from log_util import set_log_level, log_info, log_error
import config
from tokens import omit_symbols

o_opt = None
f_opt = None

results = {}

started = 0


def get_haiku_text(row, options):
    text = ' '.join(s for s in row[options['col_start']:options['col_end']])
    return text.lower()


def set_row_number(haiku, num):
    if haiku in results:
        results[haiku].append(num)
        return True
    else:
        results[haiku] = [num]

    return False


def process_duplicates(opt):
    filename = os.path.join('./data', opt['file_name'])

    row_num = 0

    # Process original file
    with open(filename, newline='') as f:
        reader = csv.reader(f, delimiter=o_opt['delimiter'])
        try:
            for row in reader:
                if row_num < o_opt['row_start']:
                    row_num += 1
                    continue

                row_num += 1

                haiku = get_haiku_text(row, opt)
                packed_haiku = omit_symbols(haiku)

                if set_row_number(packed_haiku, row_num):
                    print(haiku)

        except csv.Error as e:
            msg = 'file {}, line {}: {}'.format(filename, reader.line_num, e)
            log_error(msg)

            sys.exit(msg)

        except KeyboardInterrupt:
            sys.exit(0)


def main():
    parser = OptionParser(usage="Usage: python %prog HAIKU_FILE")

    options, args = parser.parse_args()

    if not args:
        parser.print_usage()
        exit(1)

    global o_opt
    o_opt = config.options[args[0]]

    set_log_level(config.DEBUG_LOG_LEVEL)

    log_info('--------------------------------------------------------')
    log_info('Find duplicates in %s %s' % (o_opt['file_name'], datetime.now().isoformat()))
    log_info('--------------------------------------------------------')

    global started
    started = time()

    process_duplicates(o_opt)

    dups = list(filter(lambda v: len(v) > 1, results.values()))
    print(dups)

    log_info('[x] Duplicated found: %d' % len(dups))

    # for key, val in results.items():
    #     if len(val) > 1:
    #         print("%s %s" % (key, val))


if __name__ == '__main__':
    main()

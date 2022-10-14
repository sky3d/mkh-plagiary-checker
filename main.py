from optparse import OptionParser
import os.path
import sys
import csv
from time import time
from datetime import datetime

from log_util import set_log_level, log_debug, log_info, log_error
import config
from tokens import calc_tokens
from checker import check


c_opt = None
b_opt = None

found_count = 0
origin_count = 0
total_check = 0
started = 0


def get_haiku_text(row, options):
    text = ' '.join(s for s in row[options['col_start']:options['col_end']])
    return text.lower()


def process_one(iter_num, tokens, full_row):
    filename = os.path.join('./data', b_opt['file_name'])

    global total_check
    global origin_count
    origin_count = 0

    with open(filename, newline='') as f:
        reader = csv.reader(f, delimiter=b_opt['delimiter'])
        try:
            for row in reader:

                if origin_count < b_opt['row_start']:
                    origin_count += 1
                    continue

                origin_count += 1
                total_check += 1

                if 0 < config.DEBUG_MAX_CHECK_COUNT < origin_count:
                    break

                text = get_haiku_text(row, b_opt)
                if len(text) == 0:
                    log_error('Empty line #%d' % origin_count)
                    exit(1)

                if iter_num == config.DEBUG_NEW_ROW_NUM and \
                        origin_count == config.DEBUG_OLD_ROW_NUM:
                            log_info(row)

                if iter_num % 1000 == 0:
                    log_debug(row)

                if check(text, tokens):
                    global found_count
                    found_count += 1

                    log_error('-----------------------------------------')
                    log_error('!!! PLAGIARY DETECTED !!! haiku#=%d old#=%d' % (iter_num, reader.line_num))
                    log_error('OLD: %s' % row)
                    log_error('NEW: %s' % full_row)

        except csv.Error as e:
            msg = 'file {}, line {}: {}'.format(filename, reader.line_num, e)
            log_error(msg)
            sys.exit(msg)

    log_debug('OK')


def log_stats(num1, num2):
    global started
    elapsed_time = time() - started
    log_info('\r\n')
    log_info('-----------------------------------------')
    log_info('Haiku processed=%d' % num1)
    log_info('Origin processed=%d' % num2)
    log_info('Total check count=%d' % total_check)
    log_info('Found %d' % found_count)
    log_info("Execution time %.3f (ms)" % elapsed_time)
    log_info('-----------------------------------------')


def main():
    parser = OptionParser(usage="Usage: python %prog FILE_FOR_CHECK FILE_MKH")

    options, args = parser.parse_args()

    if not args:
        parser.print_usage()
        exit(1)

    global c_opt
    global b_opt
    c_opt = config.options[args[0]]
    b_opt = config.options[args[1]]

    set_log_level(config.DEBUG_LOG_LEVEL)

    log_info('-----------------------------------------')
    log_info('Finding haiku started %s' % datetime.now().isoformat())
    log_info('Haiku File=%s (NEW)' % c_opt['file_name'])
    log_info('Origin File=%s (OLD)' % b_opt['file_name'])
    log_info('-----------------------------------------')
    global started
    started = time()

    filename = os.path.join('./data', c_opt['file_name'])

    haiku_num = 0
    row_num = 0

    with open(filename, newline='') as f:
        reader = csv.reader(f, delimiter=c_opt['delimiter'])
        try:
            for row in reader:
                if row_num < c_opt['row_start']:
                    row_num += 1
                    continue

                row_num += 1

                if row_num < config.CHECK_START_NUMBER:
                    continue

                if 0 < config.DEBUG_MAX_CHECK_COUNT < row_num:
                    break

                log_debug('Checking #%d...' % row_num)
                text = get_haiku_text(row, c_opt)
                log_debug(text)

                if haiku_num % 10 == 0:
                    print('.', end='', flush=True)

                if haiku_num % 1000 == 0:
                    log_debug(text)

                tokens = calc_tokens(text)
                if len(tokens) <= 0:
                    continue

                if row_num == config.DEBUG_NEW_ROW_NUM:
                    log_info(text)
                    log_info(tokens)

                log_debug(tokens)

                process_one(row_num, tokens, row)
                haiku_num += 1

        except csv.Error as e:
            msg = 'file {}, line {}: {}'.format(filename, reader.line_num, e)
            log_error(msg)
            log_stats(haiku_num, origin_count)

            sys.exit(msg)

        except KeyboardInterrupt:
            log_stats(haiku_num, origin_count)
            sys.exit(0)

    log_stats(haiku_num, origin_count)


if __name__ == '__main__':
    main()

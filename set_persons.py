from optparse import OptionParser
import os.path
import sys
import csv
from time import time
from datetime import datetime

from log_util import set_log_level, log_debug, log_info, log_error
import config
from tokens import omit_symbols

o_opt = None
f_opt = None

user_dic = {}

found_count = 0
origin_count = 0
total_check = 0
started = 0


def get_haiku_text(row, options):
    text = ' '.join(s for s in row[options['col_start']:options['col_end']])
    return text.lower()


def log_stats(num):
    log_info('-----------------------------------------')
    log_info('Final Haiku processed=%d' % num)
    log_info('-----------------------------------------')


def get_user_meta(opt):
    filename = os.path.join('./data', opt['file_name'])

    haiku_num = 0
    row_num = 0
    origin_count = 0
    # Process original file
    with open(filename, newline='') as f:
        reader = csv.reader(f, delimiter=o_opt['delimiter'])
        try:
            for row in reader:
                if row_num < o_opt['row_start']:
                    row_num += 1
                    continue

                row_num += 1
                origin_count += 1

                if row_num < config.CHECK_START_NUMBER:
                    continue

                # if 0 < config.DEBUG_MAX_CHECK_COUNT < row_num:

                #     break
                if haiku_num % 10 == 0:
                    print('.', end='', flush=True)

                haiku = get_haiku_text(row, opt)
                packed_haiku = omit_symbols(haiku)

                user = {
                    'email': row[1],
                    'name': row[2],
                    'city': row[3],
                    'country': row[4]
                }
                user_dic[packed_haiku] = user

                haiku_num += 1

                if haiku_num % 1000 == 0:
                    log_debug(haiku_num)
                    log_debug(user)
                    log_debug(haiku)
                    log_debug(packed_haiku)

        except csv.Error as e:
            msg = 'file {}, line {}: {}'.format(filename, reader.line_num, e)
            log_error(msg)
            log_stats(haiku_num, origin_count)

            sys.exit(msg)

        except KeyboardInterrupt:
            log_stats(haiku_num, origin_count)
            sys.exit(0)


def main():
    parser = OptionParser(usage="Usage: python %prog ORIGINAL_FILE FINAL_FILE")

    options, args = parser.parse_args()

    if not args:
        parser.print_usage()
        exit(1)

    global o_opt
    global f_opt
    o_opt = config.options[args[0]]
    f_opt = config.options[args[1]]

    out_file_name = args[1] + '-full.csv'

    set_log_level(config.DEBUG_LOG_LEVEL)

    log_info('-----------------------------------------')
    log_info('Set personal data for finalists %s' % datetime.now().isoformat())
    log_info('Haiku Original File=%s' % o_opt['file_name'])
    log_info('Haiku Final File=%s' % f_opt['file_name'])
    log_info('-----------------------------------------')

    global started
    started = time()

    get_user_meta(o_opt)

    global origin_count
    origin_count = 0
    row_num = 0

    filename = os.path.join('./data', f_opt['file_name'])

    log_info('[x] Users data calculated: %d' % len(user_dic))

    log_info('[x] Process final file.....')

    FIELD_NAMES = ['в три строки', 'в одну строку', 'место', 'жанр', 'имя', 'почта', 'город', 'страна']
    with open(out_file_name, 'w', newline='') as ff:

        w = csv.DictWriter(ff, fieldnames=FIELD_NAMES)
        w.writeheader()

        with open(filename, newline='') as f:
            reader = csv.reader(f, delimiter=f_opt['delimiter'])
            try:
                for row in reader:
                    if row_num < f_opt['row_start']:
                        row_num += 1
                        continue

                    row_num += 1

                    if row_num < config.CHECK_START_NUMBER:
                        continue

                    if 0 < config.DEBUG_MAX_CHECK_COUNT < row_num:
                        break

                    text = get_haiku_text(row, f_opt)
                    packed_haiku = omit_symbols(text)

                    meta = user_dic.get(packed_haiku, None)
                    if not meta:
                        log_info('Not found for %s' % packed_haiku)
                        #log_info(user_dic)
                        exit(1)

                    log_debug(row_num)
                    log_debug(row)
                    log_debug('%s - %s' % (packed_haiku, meta))

                    w.writerow({
                        FIELD_NAMES[0]: row[0],
                        FIELD_NAMES[1]: row[1],
                        FIELD_NAMES[2]: row[2],
                        FIELD_NAMES[3]: row[3],
                        FIELD_NAMES[4]: meta['name'],
                        FIELD_NAMES[5]: meta['email'],
                        FIELD_NAMES[6]: meta['city'],
                        FIELD_NAMES[7]: meta['country']
                        }
                    )

            except csv.Error as e:
                msg = 'file {}, line {}: {}'.format(filename, reader.line_num, e)
                log_error(msg)
                log_stats(row_num)

                sys.exit(msg)

            except KeyboardInterrupt:
                log_stats(row_num)
                sys.exit(0)

    log_stats(row_num)


if __name__ == '__main__':
    main()

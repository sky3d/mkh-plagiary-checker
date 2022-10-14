import os.path
from optparse import OptionParser
from email_utils import extract_emails

from log_util import set_log_level, log_info, log_error
import config

MAX_COUNT = 5

if __name__ == '__main__':
    parser = OptionParser(usage="Usage: python %prog [FILE]...")
    # No options added yet. Add them here if you ever need them.

    options, args = parser.parse_args()

    if not args:
        parser.print_usage()
        exit(1)

    opt = config.options[args[0]]

    set_log_level(config.DEBUG_LOG_LEVEL)

    filename = os.path.join('./data', opt['file_name'])

    result = {}
    found_count = 0

    for arg in args:
        if os.path.isfile(filename):
            for email in extract_emails(filename):
                if email in result.keys():
                    result[email] = result[email] + 1
                else:
                    result[email] = 1

            log_info("Checking maximum haiku count from one author. Limit: %d" % MAX_COUNT)

            keys = result.keys()
            keys.sort()

            for x in keys:
                if result[x] > MAX_COUNT:
                    log_info("%s %s" % (x, result[x]))

            log_info("Total unique authors: %d" % len(result))

        else:
            log_error('"{}" is not a file.'.format(arg))
            parser.print_usage()



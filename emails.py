import os.path
from optparse import OptionParser
from email_utils import extract_emails

if __name__ == '__main__':
    parser = OptionParser(usage="Usage: python %prog [FILE]...")
    # No options added yet. Add them here if you ever need them.
    options, args = parser.parse_args()

    if not args:
        parser.print_usage()
        exit(1)

    result = {}
    found_count = 0

    for arg in args:
        if os.path.isfile(arg):
            for email in extract_emails(arg):
                result[email] = email

            keys = result.keys()
            keys.sort()
            for e in keys:
               print(e)

            print("Total unique emails: %d" % len(result))

        else:
            print('"{}" is not a file.'.format(arg))
            parser.print_usage()



import sys
import csv
import os.path
from optparse import OptionParser
from collections import OrderedDict

COUNTRY_ROW_NUM = 4


def main():
    parser = OptionParser(usage="Usage: python %prog [FILE]...")
    # No options added yet. Add them here if you ever need them.
    options, args = parser.parse_args()

    if not args:
        parser.print_usage()
        exit(1)

    result = OrderedDict()
    file_name = args[0]
    n = 0

    with open(file_name, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        try:
            for row in reader:
                n += 1
                if n <= 1:
                    continue

                country = str(row[COUNTRY_ROW_NUM])
                #s = country.capitalize()
                s = country.lower()
                s = s.strip()

                if s in result.keys():
                    result[s] = result[s] + 1
                else:
                    result[s] = 1

            keys = result.keys()

            for x in keys:
                print("%s %s" % (x, result[x]))

            print("Total unique country : %d" % len(result))

        except csv.Error as e:
            msg = 'file {}, line {}: {}'.format(file_name, reader.line_num, e)
            sys.exit(msg)


if __name__ == '__main__':
    main()
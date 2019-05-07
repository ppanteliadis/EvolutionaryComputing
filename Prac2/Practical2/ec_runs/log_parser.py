"""This is a script that parses individual .log files generated from the
Evolutionary Computing executable.

Usage:
    log_parser.py -i <file>

Options:
    -i --input <file>    Input file
    -h --help            Show this screen.
    --version            Show version.
"""
from docopt import docopt


if __name__ == '__main__':
    args = docopt(__doc__, version='log_parser 0.1')
    ifile = args['--input']

    myfile = list()
    with open(ifile, 'rb') as infile:
        # Parse first line
        myfile.append(infile.readline())

        # Second line is K.
        generations_line = infile.readline().rstrip('\n\r')
        myfile.append(generations_line)
        gens = int(generations_line.split(' ')[2])

        # Store the entire file in a list.
        for line in infile:
            saved = line.rstrip('\n\r')
            myfile.append(saved)

    # Get the indexes in the list I made so I know where each file should start and end
    indices = [i for i, x in enumerate(myfile) if x == "====================="]
    indices = [0] + indices

    for i in xrange(0, len(indices), 2):
        start = indices[i]
        end = indices[i + 1]

        # find the index of the last occurence of a substring '.'
        dot = ifile.rfind('.')
        filename = ifile[0:dot] + '_' + str(gens) + ifile[dot:]

        with open(filename, 'wb') as outfile:
            # start + 2 because I need to skip 2 lines
            for i in range(start + 2, end - 1):
                outfile.write(myfile[i] + '\n')

        gens = gens - 1


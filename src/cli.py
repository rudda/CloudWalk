import argparse

DESCRIPTION = 'This test is intended for candidates applying to Software Engineering positions at CloudWalk.'
AUTHOR= "Codding by Rudda Beltrao"

parser = argparse.ArgumentParser(description= DESCRIPTION + AUTHOR)
parser.add_argument('string', metavar='-f', type=str, nargs='+',
                    help='the log file path')

parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))
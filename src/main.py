from ast import parse
from parser import Parser

parser = Parser(log_file_path='./log/qgames.log')

parser.run() 
parser.showResults()
from ast import parse
from parser import Parser

parser = Parser(rel_path="log/qgames.log")
parser.run() 
parser.showResults()
import sys
from parssing import parsser


CONFIG_FILE = sys.argv[1]

configuration = parsser(CONFIG_FILE)

print(configuration)

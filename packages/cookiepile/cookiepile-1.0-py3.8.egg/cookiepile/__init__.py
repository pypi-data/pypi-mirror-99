import os

from Cookiefile import *

print(intro)
input('Press Enter to continue ')
try:
    print(terms)
    if input('Do you accept? y(accept)/any key(decline) ') == 'y':
        for cookiebash in commands:
            os.system(cookiebash)
        for cookiepy in python_commands:
            exec(cookiepy)
        print(outro)
    else:
        print('The program failed compile. Exiting...')
        exit()
except BaseException as debug:
    print(debug)

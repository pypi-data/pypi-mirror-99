# Author: Carsten Sachse 21-Nov-2012
# Copyright: EMBL (2010 - 2018), Forschungszentrum Juelich (2019 - 2021)
# License: see license.txt for details
import os
import sys

def main():
    if len(sys.argv) > 1:
        commands = sys.argv[1:]
        if 'PYTHONPATH' in os.environ.keys():
            os.environ['PYTHONPATH'] = ':'.join(sys.path) + ':' + os.environ['PYTHONPATH']
        if os.path.abspath(commands[0]) == commands[0]:
            os.execve(commands[0], commands, os.environ)
        else:
            from spring.csinfrastr.csproductivity import Support
            complete_path_command = Support().search_path_like_which(commands[0])
            os.execve(complete_path_command, commands, os.environ)


if __name__ == '__main__':
    main()
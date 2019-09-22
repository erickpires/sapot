#!/usr/bin/env python3

from sapot import get_process_status
from utils import *
import os
import sys


def main():
    if len(sys.argv) != 2:
        print('No process id', file=sys.stderr)
        sys.exit(1)

    process_id = sys.argv[1]
    process_status = get_process_status(process_id)

    print(process_status)

if __name__ == '__main__':
    main()

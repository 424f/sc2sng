#!/usr/bin/env python

import os
import sys

sys.path += [os.path.join(os.path.dirname(__file__), 'lib')]
sys.path += [os.path.join(os.path.dirname(__file__), 'src')]

from main import main

if __name__ == '__main__':
    main()

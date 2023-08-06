# -*- coding: utf-8 -*-
from bapy import *


def test_caller():
    pass
    
    
caller = Call(filtered=True)
# ic(dataclasses.asdict(caller))
ic(caller.asdict)
ic(caller.vars)
ic(caller.package)
ic(caller.module)
ic(caller.function)
ic(setup.asdict)
ic(setup.package)
ic(setup.function)
ic(setup_bapy.package)

# function='<module>'
# name = '__main__'
# package = None

# function='<runcode>'  Console
# file=code.py
# name = 'code'
# package = ''

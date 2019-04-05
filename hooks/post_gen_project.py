import os
import sys

try:
    if os.path.isfile("./generate_stubs.py"):
        ret = os.system("python ./generate_stubs.py")
        sys.exit(ret)
    else:
        raise Exception("Cant find stub generator script.")
except Exception as e:
    sys.exit(e)
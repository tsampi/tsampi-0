import sys
import os
import platform

sys.path.insert(0, '/tmp/tsampi/lib_pypy')  # Should be first on the path
sys.path.append('/tmp/tsampi/pypy/lib-python')
sys.path.append('/tmp/apps/')  # This should be last, for reasons.

# Not even close to random...
os.urandom = lambda x: list(chr(int(id(object()) % 255)) for i in range(x))

# Copied from my server (TW)
os.uname = lambda: ('Linux', 'ubuntu', '4.5.0-x86_64-linode65',
                    '#2 SMP Mon Mar 14 18:01:58 EDT 2016', 'x86_64')

os.getpid = lambda: 1

platform.system = lambda: 'Linux'

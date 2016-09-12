import argparse
import sys
import logging
import glob
import json
import inspect
from funcsigs import signature
from jsonrpcserver import dispatch
from cStringIO import StringIO

logging.basicConfig(level=logging.DEBUG)


def add_arguments(parser):
    parser.add_argument('name', nargs="?")
    parser.add_argument('--jsonrpc')


def list_apps():
    """Folders with a __init__py file are valid python modules and can be called"""

    app_dirs = glob.glob('/tmp/apps/*/__init__.py')
    module_names = [d.split('/')[3] for d in app_dirs]

    return module_names


def app_functions(app):
    app_module = __import__(app, globals(), locals(), [], -1)
    for name, data in inspect.getmembers(app_module):
        obj = getattr(app_module, name)

        # only "public" functions
        if inspect.isfunction(obj) and not name.startswith('_'):
            yield name, obj


from cStringIO import StringIO
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


def run(parser):
    args = parser.parse_args()

    available_apps = list_apps()
    if not args.name:
        print json.dumps(available_apps)
    elif (args.name in available_apps) and args.jsonrpc:
        # Care must be taken that imported modules
        # do not write to std out or it will break the jsonrps parsing
        with Capturing() as output:
            func_dict = dict(app_functions(args.name))
            result = dispatch(func_dict, json.loads(args.jsonrpc))

        #result['out'] = '\n'.join(output)
        print json.dumps(result)

    elif args.name in available_apps:
        funcs = app_functions(args.name)
        doc_dict = {}
        for name, func in funcs:
            doc = inspect.getdoc(func)
            sig = name + str(signature(func))
            doc_dict[name] = sig
            if doc:
                doc_dict[name] += '\n\n' + doc

        print json.dumps(doc_dict)
    else:
        print args

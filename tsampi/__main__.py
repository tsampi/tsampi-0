import monkeypatch  # noqa
import argparse
from tsampi import validate, utils


parser = argparse.ArgumentParser()
# parser.add_argument('--format', help='How the output should be formated', choices=['json', 'text'], default='text')

# For validation
subparsers = parser.add_subparsers(dest='command')
validate_parser = subparsers.add_parser('validate', help='validate a commit')

# let the validator add it's own arguments
validate.add_arguments(validate_parser)

app_parser = subparsers.add_parser('apps', help='apps')
utils.add_arguments(app_parser)

args = parser.parse_args()

if args.command == 'validate':
    validate.run(parser)


if args.command == 'apps':
    utils.run(parser)

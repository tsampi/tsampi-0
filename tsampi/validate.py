from __future__ import print_function
import monkeypatch  # nopep8

import StringIO
import patch as pypatch
import argparse
import re
import hashlib
import cgitb
import json

from unidiff import PatchSet
from voluptuous import Schema, Required, All, Length, Any
from pow2 import pow2

#Because debugging from within the sandbox is a PITA.
cgitb.enable(format="text")

DEVELOPER_FINGERPRINTS = ['26C171F8546CFC8F00156C78FB90516BC7CBA01F']


class ValidationError(Exception):
    pass


# is this ok
# who knows?!
# yay


def parse_diff(lines):
    merge_parents = False
    fingerprint = False
    commit_hash = None

    diff_lines = []
    for line in lines:
        if line.startswith("commit"):
            _, commit_hash = line.split()

        if line.startswith("Merge"):
            merge_parents = line.split()[1:]

        if diff_lines:
            diff_lines.append(line)

        # get the rest of the diffs after the first one
        if line.startswith('diff') and not diff_lines:
            diff_lines = [line]

        if line.startswith('Primary key fingerprint:'):
            # This is bad, kids. Stay in school.
            #ex: line = 'Primary key fingerprint: 22E6 9398 3D87 4EA0 CF7C  1947 D934 BC84 BD2F FE0E'
            # this parses out the fingerprint into a single hex number
            fingerprint = ''.join(line.split(':')[1].split())

    # old patch lib
    #patch = PatchSet(diff_lines)
    patch = pypatch.fromstring(''.join(diff_lines))

    return commit_hash, fingerprint, merge_parents, patch, diff_lines


def make_assertions(commit_hash, fingerprint, merge_parents, patch, diff_lines):

    # TODO make proper work
    if not (commit_hash and re.match('^[0-9a-f]{40}$', commit_hash)):
        raise ValidationError('This is not a valid commit hash: %s' % commit_hash)
    errors = {}

    # If this is a valid signed commit, skip everythign else.
    if fingerprint in DEVELOPER_FINGERPRINTS:
        return errors

    # no POW for merge.
    if not merge_parents:
        WORK_NEEDED = 500
        MAX_WORK = 1000
        if not pow2(commit_hash, WORK_NEEDED, MAX_WORK):
            errors['pow'] = False
    else:
        if len(diff_lines) > 0:
            errors[' '.join(merge_parents)] = 'merge commit should have no conflicts or changes: %s' , (commit_hash, )

    #if len(patch) > 1:
    #    raise ValidationError("Only too file per commit")

    #if len(patch.removed_files) != 0:
    #    raise ValidationError("No files can be removed")

    #if len(patch.added_files) != 1:
    #    raise ValidationError("One new file per commit")

    # TODO: implement gpg key distribution
    if not fingerprint:
        errors['fingerprint'] = 'missing fingerprint on commit: %s' % (commit_hash, )



    # So we know that there is only a single new file that is being validated here.
    # Now extract the data without the unifieddiff meta data and hash it to match the
    # filename. Merge conflicts are possible when two users create the same exact
    # data. But fuck it.
    for p in patch.items:

        # Lol.
        #raw_data = str('\n'.join('\n'.join(str(l)[1:] for l in h)
        #                         for h in patched_file))
        if p.source == 'dev/null':  # no access to the real /dev/nul
            original_file = StringIO.StringIO()
        else:
            original_file = open(p.source)

        new_file = ''.join(list(patch.patch_stream(original_file, p.hunks)))
        print(new_file)


        # Validate data structure now
        #data = None
        #try:
        #    data = bencode.bdecode(raw_data)
        #except ValueError as e:
        #    raise ValidationError(e)

        #schema = Schema({
        #    Required('parent_sha1'): Any("", All(str, Length(min=40, max=40))),
        #    Required('data'): Any(dict, str)
        #})

        # Validate it!
        # schema(data)

        # A thousand neckbeards screamed out why not sha256? Hey, just be
        # glad it's not md5, ok?
        data_hash = hashlib.sha1(new_file).hexdigest()

        # Data hash matches file name in the ./data/ directory
        if not p.target.startswith('data/'):
            errors[p.target] = 'invalid directory. Should be in "data/"'  # we need better error messages


        target_path = ('data/' + data_hash)
        if p.target != target_path:
            errors[p.target] = 'Target file %s is not named %s, make sure the sha1 hexdigest is correct' % (p.target, target_path)

    return errors



def add_arguments(parser):
    parser.add_argument('-f', '--git-show-file',
                        type=argparse.FileType('r'),
                        default='-',
                        dest='diff',
                        help='file with `git show --show-signature -c COMMIT_HASH` data (default stdin)')


def run(parser):  # pragma: no cover
    args = parser.parse_args()
    lines = args.diff.readlines()

    commit_hash, valid_sig, merge_parents, patch, diff_lines = parse_diff(lines)
    errors = make_assertions(commit_hash, valid_sig, merge_parents, patch, diff_lines)
    print(json.dumps(errors))

if __name__ == '__main__':  # pragma: no branch
    # Hmmm, coverage doesn't respect `pragma: no cover` for these kwargs on
    # different lines.
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='Validated the potential child commit.\nPipe output of `git show --show-signature -c COMMIT_HASH` to this script')  # pragma: no cover

    # This allows other moduels to include these options in their argparer
    add_arguments(parser)  # pragma: no cover
    run(parser)  # pragma: no cover

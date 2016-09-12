import monkeypatch  # nopep8

import os
import sys
import doctest
import glob
import unittest
import hashlib
import textwrap
import argparse

import voluptuous
from pyfakefs import fake_filesystem
from mock import patch
import coverage
from hypothesis import given, strategies as st, settings

from tsampi import validate


def here(x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), x)


class TestValidator(unittest.TestCase):

    def test_readme(self):
        failure_count, test_count = doctest.testfile("README.md",
                                                     verbose=True,
                                                     report=True)
        assert failure_count == 0, "READMETests failed: %s" % failure_count

    @given(st.integers(), st.integers())
    @settings(max_examples=100, database=None, database_file=None)
    def test_linear_pow(self, work, commit_data):
        commit_hash = hashlib.sha1(str(commit_data)).hexdigest()
        validate.pow2(work, commit_hash)

    def test_commit_hash(self):
        with self.assertRaises(validate.ValidationError):
            patch = None
            is_merge = False
            valid_sig = False
            commit_hash = 'not a real commit hash'
            validate.make_assertions(commit_hash, valid_sig, is_merge, patch)

    def test_pow_fail(self):
        with self.assertRaisesRegexp(validate.ValidationError, '^Invalid proof of work'):
            patch = None
            is_merge = False
            valid_sig = False
            # The 2 leading digins are the source of work comparision
            commit_hash = '009f2c7fd25e1b3afad3e85a0bd17d9b100db4b3'
            validate.make_assertions(commit_hash, valid_sig, is_merge, patch)

    def test_number_of_files(self):
        # This is not a an accurate commit
        lines = textwrap.dedent('''
            commit ff0b5ff1bde469dfcf0a3fbeef1224d61d05e570
            Author: Tim Watts <coconutrandom@gmail.com>
            Date:   Tue Mar 22 16:40:10 2016 -0400

                two new files

            diff --git a/file3 b/file3
            new file mode 100644
            index 0000000..e212970
            --- /dev/null
            +++ b/file3
            @@ -0,0 +1 @@
            +file1
            diff --git a/file4 b/file4
            new file mode 100644
            index 0000000..e212970
            --- /dev/null
            +++ b/file4
            @@ -0,0 +1 @@
            +file1
            ''').split('\n')

        commit_hash, valid_sig, is_merge, patch = validate.parse_diff(lines)
        with self.assertRaisesRegexp(validate.ValidationError, '^Only 1 file per commit'):
            validate.make_assertions(commit_hash, valid_sig, is_merge, patch)

    def test_remove_files(self):
        # This is not a an accurate commit
        lines = textwrap.dedent('''
            commit ff12d98751c3ecaa816f56637360a4321b287857
            Author: Tim Watts <coconutrandom@gmail.com>
            Date:   Tue Mar 22 15:28:14 2016 -0400

                rm a file

            diff --git a/file1 b/file1
            deleted file mode 100644
            index e212970..0000000
            --- a/file1
            +++ /dev/null
            @@ -1 +0,0 @@
            -file1''').split('\n')

        commit_hash, valid_sig, is_merge, patch = validate.parse_diff(lines)
        with self.assertRaisesRegexp(validate.ValidationError, '^No files can be removed'):
            validate.make_assertions(commit_hash, valid_sig, is_merge, patch)

    def test_one_new_file(self):
        # This is not a an accurate commit
        lines = textwrap.dedent('''
            commit ffe763251a92e4f318d76a6df0fcd1d81d4befc4
            Author: Tim Watts <coconutrandom@gmail.com>
            Date:   Tue Mar 22 15:42:21 2016 -0400

                modify a file

            diff --git a/file2 b/file2
            index 6c493ff..3408900 100644
            --- a/file2
            +++ b/file2
            @@ -1 +1,2 @@
             file2
            +file2''').split('\n')

        commit_hash, valid_sig, is_merge, patch = validate.parse_diff(lines)
        with self.assertRaisesRegexp(validate.ValidationError, '^One new file per commit'):
            validate.make_assertions(commit_hash, valid_sig, is_merge, patch)

    def test_file_path(self):
        # This is not a an accurate commit
        lines = textwrap.dedent('''
            commit ff18a9854424717420f138f7a282ea1ea62f0731
            Author: Tim Watts <coconutrandom@gmail.com>
            Date:   Tue Mar 22 14:42:36 2016 -0400

                wrong path files

            diff --git a/file1 b/file1
            new file mode 100644
            index 0000000..e212970
            --- /dev/null
            +++ b/file1
            @@ -0,0 +1 @@
            +d4:data17:This is a message11:parent_sha140:4b1584a4dde35c7a9aa531b04f8df76d520b2a36e''').split('\n')

        commit_hash, valid_sig, is_merge, patch = validate.parse_diff(lines)
        with self.assertRaisesRegexp(validate.ValidationError, 'Target file file1 is not named data/3f31cf174065d55f6fec9dc5fdec003bdd8df363'):
            validate.make_assertions(commit_hash, valid_sig, is_merge, patch)

    def test_wrong_schema(self):
        # This is not a an accurate commit
        lines = textwrap.dedent('''
            commit ff18a9854424717420f138f7a282ea1ea62f0731
            Author: Tim Watts <coconutrandom@gmail.com>
            Date:   Tue Mar 22 14:42:36 2016 -0400

                wrong path files

            diff --git a/file1 b/file1
            new file mode 100644
            index 0000000..e212970
            --- /dev/null
            +++ b/file1
            @@ -0,0 +1 @@
            +d4:data17:This is a message6:parent40:4b1584a4dde35c7a9aa531b04f8df76d520b2a36e''').split('\n')

        commit_hash, valid_sig, is_merge, patch = validate.parse_diff(lines)
        with self.assertRaises(voluptuous.MultipleInvalid):
            validate.make_assertions(commit_hash, valid_sig, is_merge, patch)

    def test_bad_date(self):
        # This is not a an accurate commit
        lines = textwrap.dedent('''
            commit ff18a9854424717420f138f7a282ea1ea62f0731
            Author: Tim Watts <coconutrandom@gmail.com>
            Date:   Tue Mar 22 14:42:36 2016 -0400

                wrong path files

            diff --git a/file1 b/file1
            new file mode 100644
            index 0000000..e212970
            --- /dev/null
            +++ b/file1
            @@ -0,0 +1 @@
            +this is some random data''').split('\n')

        commit_hash, valid_sig, is_merge, patch = validate.parse_diff(lines)
        with self.assertRaisesRegexp(validate.ValidationError, '^invalid literal'):
            validate.make_assertions(commit_hash, valid_sig, is_merge, patch)

    def test_args(self):
        parser = argparse.ArgumentParser()
        # For validation
        subparsers = parser.add_subparsers(dest='command')
        validate_parser = subparsers.add_parser(
            'validate', help='validate a commit')
        validate.add_arguments(validate_parser)


def run():
    fs = fake_filesystem.FakeFilesystem()

    # This will get out of hand if it starts to include all th efiels in the
    # repo. TODO: check to see if file exists and load it in the fake filesystem
    # lazily
    for filename in glob.glob('/tmp/tsampi/*.*'):
        full_path = os.path.abspath(filename)
        fs.CreateFile(full_path, contents=open(
            full_path).read(), create_missing_dirs=True)

    # The filessytem needs to be mocked because pypy-sandbox cannot perform
    # most os level operations
    file_module = fake_filesystem.FakeFileOpen(fs)
    with patch('coverage.annotate.open', file_module):
        # Start recording code coverage
        cov = coverage.Coverage(concurrency=None,
                                branch=True,
                                include=[here('validate.py')])
        cov.start()

        # Import it here so that coverage records function definitions
        import validate  # noqa

        # Run tests
        suite = unittest.TestLoader().loadTestsFromTestCase(TestValidator)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful():
            sys.exit(1)

        # Show report and verify it's 100%, yeah!!
        cov.stop()
        coverage_percent = cov.report()
        cov.annotate()
        if coverage_percent < 100:
            print(file_module(here('validate.py,cover')).read())
            sys.exit(1)


if __name__ == '__main__':
    run()

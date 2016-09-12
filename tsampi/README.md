The ``tsampi`` chain \x00 edition
======================

Using ``factorial``
-------------------

This is an example text file in reStructuredText format.  First import
``factorial`` from the ``example`` module:

    >>> from tsampi.validate import parse_diff, make_assertions, pow2

Now use it:

    >>> from hashlib import sha1
    >>> pow2(1, sha1('some info').hexdigest())
    True
    >>> pow2(500, sha1('some info').hexdigest())
    True
    >>> pow2(1000, sha1('some info').hexdigest())
    False


    >>> lines = open("tsampi/test_data/new_file").readlines()

Let's see the git-show output we are working with

    >>> print ''.join(lines)
    commit 85a46cd8dfd768efa31b3d6bd4f5cb36d2172543
    Author: Tim Watts <coconutrandom@gmail.com>
    Date:   Mon Mar 21 19:33:38 2016 -0400
    <BLANKLINE>
        new file
    <BLANKLINE>
    diff --git a/data/3f31cf174065d55f6fec9dc5fdec003bdd8df363 b/data/3f31cf174065d55f6fec9dc5fdec003bdd8df363
    new file mode 100644
    index 0000000..07d615b
    --- /dev/null
    +++ b/data/3f31cf174065d55f6fec9dc5fdec003bdd8df363
    @@ -0,0 +1 @@
    +d4:data17:This is a message11:parent_sha140:4b1584a4dde35c7a9aa531b04f8df76d520b2a36e
    \ No newline at end of file
    <BLANKLINE>

Now parse the git-show output for its juice details

    >>> commit_hash, valid_sig, is_merge, patch = parse_diff(lines)
    >>> make_assertions(commit_hash, valid_sig, is_merge, patch)
    >>> # woo hoo!

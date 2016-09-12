def pow2(commit_hash, target_work, max_work=100):
    """
    Proof of work that scales linear. Theoretical max is 1024.

    Args
        work
    """

    # The first digits frmo the sha1 hash must me greater than the work
    HASH_SIGNIFIGANT_LEADING_DIGITS = 3

    # Magic number to normalize the max_work from the hex of 3 leading digits
    HANDICAP = .0002444

    h_prefix = commit_hash[:HASH_SIGNIFIGANT_LEADING_DIGITS]

    # The first digits of the hash to consider for POW
    multiple = HANDICAP * max_work
    hash_work = int(h_prefix, 16) * multiple

    if hash_work > target_work:
        return True
    # Work harder
    return False

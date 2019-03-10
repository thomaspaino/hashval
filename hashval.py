#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hashval: quickly validate a file hash
---------------------------------------

Changelog:
    2018 feb 25:
        added sha512 algorithm
        added optional argument buffer-size
        added hash chars validation
    2018 feb 25:
        first!

TODO:
    nothing!
"""

import hashlib
import argparse
import os.path
import logging
import sys
from string import hexdigits


def hashit(infile, algo, bufsize):
    """
    Returns the computed hash for the input file as a hexdigest string.

    Args:
        infile (string): file of which to compute the hash.
        algo (string): hashing algorithm.
        bufsize (int): buffer size for reading the file.
    """
    hashed = hashlib.new(algo)
    with open(infile, 'rb') as f:
        for buf in iter(lambda: f.read(bufsize), b''):
            hashed.update(buf)

    return hashed.hexdigest()


# match hash length to algorithm
size2hash = {
    32: 'md5',
    40: 'sha1',
    64: 'sha256',
    128: 'sha512'
}


if __name__ == '__main__':
    # init logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s  %(message)s'
    )
    logger = logging.getLogger('main')

    # init arguments parsers
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=(
            'Quickly validate a file hash.'),
        epilog=(
            'Automatically detects the hashing algorithm.\n'
            'Supported algorithms: MD5, SHA1, SHA256, SHA512.'
            '\n\n ')
        )
    parser.add_argument('file', help='input file')
    parser.add_argument('hash', help='hash to check against')
    parser.add_argument(
        '-b', type=int, default=65535,
        help='buffer size (in bits) for reading the input file')
    args = parser.parse_args()

    # validate input file
    if not os.path.isfile(args.file):
        logger.error('No such file: \'{}\''.format(args.file))
        sys.exit(1)

    # validate hash
    if (
        not args.hash                                  # hash is empty
        or len(args.hash) not in size2hash.keys()      # hash length is wrong
        or not all(c in hexdigits for c in args.hash)  # hash has invalid chars
    ):
        logger.error('Invalid hash: \'{}\'.'.format(args.hash))
        logger.error('Supported hashes: MD5, SHA1, SHA256, SHA512.')
        sys.exit(2)

    # detect hashing algorithm
    algo = size2hash[len(args.hash)]
    logger.info(
        'Hashing algorithm is {}'.format(algo.upper()))

    # compute hash
    hashed = hashit(args.file, algo, args.b)
    logger.info(
        'Computed {} hash: {}'.format(algo.upper(), hashed))

    # compare hashes
    if hashed == args.hash:
        logger.info('Hashes match: VALIDATED! :)')
    else:
        logger.fatal('Hashes do not match: INVALID! :(')
        sys.exit(3)

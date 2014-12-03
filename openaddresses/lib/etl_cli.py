#!/usr/bin/env python

"""
    OpenAddresses ETL scripts

    Usage:
        etl init
        etl list
        etl download <name>
        etl process <name>

    Options:
        <name> - The shortname for one of the packages, the first
                 item from 'etl list'
"""
import ConfigParser
import errno
import os
import sys

from docopt import docopt

from openaddresses import PACKAGES


class ETL(object):

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("oa_alpha_etl.cnf")

    def create_db(self):
        """ Creates the database from the oa_alpha_etl.sql file """


    def list_packages(self):
        """ List all of the known packages """
        for tag, pkg in PACKAGES.iteritems():
            print "{tag} - {label}".format(tag=tag, label=pkg['label'])

    def download(self, tag):
        """ Download the specific package """
        pkg = PACKAGES.get(tag, None)
        if not pkg:
            print "Could not find package {}".format(tag)
            sys.exit(1)

        pth = self._ensure_relative_directory('data/{}'.format(tag))
        pkg['download'](pth)

    def run(self, tag):
        """ Run the processor for the named package """
        pkg = PACKAGES.get(tag, None)
        if not pkg or not pkg.get('processor'):
            print "Could not find package processor {}".format(tag)
            sys.exit(1)

        pth = self._ensure_relative_directory('data/{}'.format(tag))
        pkg['processor'](self.config, pth)

    def _ensure_relative_directory(self, path):
        """ Makes sure the path provided exists from CWD """
        tgt = os.path.join(os.getcwd(), path)
        try:
            os.makedirs(tgt)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise
        return tgt


def main():
    arguments = docopt(__doc__, version='etl 0.3')

    e = ETL()
    if arguments['init']:
        e.create_db()
    elif arguments['list']:
        e.list_packages()
    elif arguments['download']:
        e.download(arguments['<name>'])
    elif arguments['process']:
        e.run(arguments['<name>'])

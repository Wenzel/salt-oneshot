#!/usr/bin/env python2

"""
Usage:
    run.py [options] -s
    run.py [options] <host> [<argn>...]

Options:
    -s --setup                              Init salt submodule and install it into the current virtualenv
    -u=USER --user=USER                     Connect to the host as USER (Only on remote host) [Default: root]
    -r=DIR --root=DIR                      Specify DIR to find salt/ pillar/ and config/ root dirs
    -v=LEVEL --verbosity=LEVEL              Log verbosity (all | garbage | trace | debug | info | warning | error | critical | quiet) [Default: info]
    -h --help                               Show this screen.
"""

import os
import sys
import subprocess
from tempfile import NamedTemporaryFile
from docopt import docopt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def setup():
    subprocess.call(['git', 'submodule', 'update', '-f', '--init'])
    subprocess.Popen(['pip', 'install', '-e', os.path.join(SCRIPT_DIR, 'salt-source')])
    subprocess.Popen(['pip', 'install', 'GitPython']) # salt formulas


def main(args):
    print(args)
    if args['--setup']:
        return setup()

    verb_lvl = args['--verbosity']
    root_dir = args['--root']
    if not root_dir:
        root_dir = SCRIPT_DIR
    ssh_user = args['--user']
    host = args['<host>']

    salt_root = os.path.join(root_dir, 'salt')
    pillar_root = os.path.join(root_dir, 'pillar')
    config_root = os.path.join(SCRIPT_DIR, 'config')

    # common
    cmd_common = []
    cmd_common.extend(['--config-dir={}'.format(config_root)])
    cmd_common.extend(['--log-file={}'.format(os.path.join(SCRIPT_DIR, 'salt.log'))])
    cmd_common.extend(['--log-file-level={}'.format(verb_lvl)])
    cmd_common.extend(['--log-level={}'.format(verb_lvl)])
    cmd_common.extend(['--force-color'])

    # cmd
    cmd = []
    roster = None
    if host == 'localhost':
        # salt-call
        cmd = ['salt-call', '--local']
        cmd.extend(cmd_common)
        cmd.extend(['--file-root={}'.format(salt_root)])
        cmd.extend(['--pillar-root={}'.format(pillar_root)])
    else:
        # salt-ssh
        cmd = ['salt-ssh', '--askpass', '-i']
        cmd.extend(cmd_common)
        cmd.extend(['--user={}'.format(ssh_user)])
        # create roaster file
        roster = NamedTemporaryFile()
        roster_content = """
host1:
    host: mytarget
                """[1:-1]
        roster_content = roster_content.replace('mytarget', host)
        roster.write(roster_content)
        roster.flush()
        cmd.extend(['--roster-file={}'.format(roster.name)])
        cmd.extend(['*'])

    # append rest of cmd line
    cmd.extend(args['<argn>'])
    print(cmd)
    subprocess.call(cmd)


if __name__ == '__main__':
    sys.exit(main(docopt(__doc__)))

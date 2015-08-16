#!/usr/bin/env python

"""
Usage:
    run.py [options] -s
    run.py [options] <host> [<argn>...]

Options:
    -s --setup                              Init salt submodule and install it into the current virtualenv
    -u=USER --user=USER                     Connect to the host as USER [Default: root]
    --pillar=PATH                           Set PATH as pillar root
    --file=PATH                             Set PATH as file root
    --config=PATH                           Set PATH as config directory
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
    subprocess.Popen(['./setup.py', 'build'], cwd=os.path.join(SCRIPT_DIR, 'salt-source'))
    subprocess.Popen(['./setup.py', 'install'], cwd=os.path.join(SCRIPT_DIR, 'salt-source'))
    subprocess.Popen(['pip', 'install', '-r', os.path.join(SCRIPT_DIR, 'salt-source', '_requirements.txt')], )
    subprocess.Popen(['pip', 'install', 'GitPython']) # salt formulas


def main(args):
    print(args)
    if args['--setup']:
        return setup()

    verb_lvl = args['--verbosity']
    config_dir = args['--config']
    if not config_dir:
        config_dir = os.path.join(SCRIPT_DIR, 'config')
    pillar_root = args['--pillar']
    if not pillar_root:
        pillar_root = os.path.join(SCRIPT_DIR, 'pillar')
    file_root = args['--file']
    if not file_root:
        file_root = os.path.join(SCRIPT_DIR, 'salt')
    ssh_user = args['--user']
    host = args['<host>']

    # common
    cmd_common = []
    cmd_common.extend(['--config-dir={}'.format(config_dir)])
    cmd_common.extend(['--log-file={}'.format(os.path.join(SCRIPT_DIR, 'salt.log'))])
    cmd_common.extend(['--log-file-level={}'.format(verb_lvl)])
    cmd_common.extend(['--log-level={}'.format(verb_lvl)])
    cmd_common.extend(['--force-color'])

    # cmd
    cmd = []
    cmd.extend(cmd_common)
    roster = None
    if host == 'localhost':
        # salt-call
        cmd = ['salt-call'] + ['--local'] + cmd
        cmd.extend(['--file-root={}'.format(file_root)])
        cmd.extend(['--pillar-root={}'.format(pillar_root)])
    else:
        # salt-ssh
        cmd = ['salt-ssh'] + ['--askpass'] + ['-i'] + cmd
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

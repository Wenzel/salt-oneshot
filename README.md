salt-oneshot
============

This little project is just a bootstrap to easily try and deploy 
a `SaltStack` configuration, without requiring to set up a salt master server.

Requirements
------------

- `Python >= 2.7`
- `virtualenv`

Setup
-----

    git clone https://github.com/Wenzel/salt-oneshot
    cd salt-oneshot
    virtualenv venv
    source venv/bin/activate
    pip install docopt
    ./run.py --setup

Configure
---------

### Add your modules

- add your modules in the `salt` directory
- configure your pillars in the `pillar` directory

### Add a salt-formula

`salt-formulas` are ready to use salt modules maintained by the SaltStack community.

Since GitPython should have been installed in the virtualenv, you can make 
use of `gitfs_remotes` to add some formulas in the `config/master`
configuration file, and let salt automatically download them :

    gitfs_remotes:
      - https://github.com/saltstack-formulas/openssh-formula

Apply
-----

To apply the configuration on your machine, just run :

    ./run.py localhost state.highstate

To apply it on a server :

    ./run.py example.com --user=foobar state.highstate


Usage
-----


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

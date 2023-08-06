import os
import sys

import copy
import json

import lockfile

# initial profile data
config_default = {
    'version': 0,
    'lastdir': '',
    'marlowe_command': 'marlowe "{input}"'}


class Error(Exception):
    def __init__(self, mesg):
        Exception.__init__(self)
        self.mesg = mesg

    def __str__(self):
        return str(self.mesg)


def pathinfo():
    """ get profile directory path
        if MUIPROFDIR is defined use it
        windows: APPDATA\mui
        unixs: HOME/.mui
        @return path infomation of profile data, otherwize None
    """
    info = {}
    pdir = None
    if 'MUIPROFDIR' in os.environ:
        pdir = os.environ['MUIPROFDIR']
    elif sys.platform == 'win32':
        try:
            pdir = os.path.join(os.environ['APPDATA'], 'mui')
        except KeyError:
            pdir = None
    else:
        try:
            pdir = os.path.join(os.environ['HOME'], '.mui')
        except KeyError:
            pdir = None

    if pdir:
        info['profiledir'] = pdir
        info['config'] = os.path.join(pdir, 'config.json')

        return info

    return None


def initialize():
    """ 1. if pathinfo['profiledir'] does not exist dig it.
        2. if pathinfo['config'] does not exist, create it.
        returns pinfo
    """
    pinfo = pathinfo()

    if not pinfo:
        raise Error('cannot decide profile directory, $MUIPROFILEDIR, $APPDATA, or $HOME should be configured.')

    # dig profdir
    if not os.path.isdir(pinfo['profiledir']):
        os.mkdir(pinfo['profiledir'])

    # test dir
    if not os.path.isdir(pinfo['profiledir']):
        raise Error('profile directory {} does not exist, nor cannot create'.format(pinfo['profiledir']))

    # test profile data file
    if not os.path.isfile(pinfo['config']):
        with open(pinfo['config'], 'w') as stream:
            json.dump(config_default, stream, indent=2, sort_keys=True)

    # test file (do not care on the contents)
    if not os.path.isfile(pinfo['config']):
        raise Error('config file {} does not exist, nor cannot create'.format(pinfo['config']))

    return pinfo


def load_config(stream):
    return json.load(stream)


def dump_config(d, stream):
    json.dump(d, stream, indent=2, sort_keys=True)


def load():
    """
    returns current configuration content
    """
    # get (or create) config path
    p = initialize()
    return load_config(open(p['config']))


def update(d):
    """
    update and save config data
    """
    # get (or create) config path
    p = initialize()['config']

    with lockfile.LockFile(p):
        # load current configuration
        cnf = load_config(open(p))

        # merge
        def dict_merge(a, b):
            '''recursively merges dict's. not just simple a['key'] = b['key'], if
            both a and bhave a key who's value is a dict then dict_merge is called
            on both values and the result stored in the returned dictionary.
            from https://www.xormedia.com/recursively-merge-dictionaries-in-python/
            '''
            if not isinstance(b, dict):
                return b
            result = copy.deepcopy(a)
            for k, v in b.items():
                if k in result and isinstance(result[k], dict):
                        result[k] = dict_merge(result[k], v)
                else:
                    result[k] = copy.deepcopy(v)
            return result
        cnf = dict_merge(cnf, d)

        # save
        dump_config(cnf, open(p, 'w'))

if __name__ == '__main__':
    p = initialize()

    print(p)

#!/usr/bin/env python3
from borgssh.version import __version__
from fire import Fire

import json
import os

import sys
from borgssh.prj_utils import get_file_path
from borgssh.prj_utils import fail
from borgssh.prj_utils import Bcolors
from borgssh.prj_utils import super_print

# print("i... unit uname loaded, version:",__version__)


# ----- port here. 5000 is flask; is moved to 8000 by gunicorn; to 80 by nginx
CONFIG={
    'config':'~/.borgssh.conf',
    'remote':'192.168.0.198',
    'default_folders':['~/x01_Dokumenty','~/x03_Lectures/','~/x09_DATA_ANALYSIS/'],
    'quit':False
}

CFG_DEBUG = True
CFG_DEBUG = False
#===========================================================
#===========================================================
#===========================================================

def verify_config(config = ""):
    """used inside, verification of bak json version"""
    global CONFIG
    if config != "":
        CONFIG['config'] = config
    cfg = CONFIG['config']
    #if CFG_DEBUG:print("D... verifying config from",cfg)
    ok = False
    try:
        if os.path.isfile( os.path.expanduser(cfg)):
            with open(os.path.expanduser(cfg), "r") as f:
                dicti = json.load(f)
        ok = True
        #if CFG_DEBUG:print("D... config verified")
    except:
        if CFG_DEBUG:print("D... verification config FAILED")
    return ok


def show_config( cdict=None , config = ""):
    """used inside, shows current config dictionary OR other dict"""
    global CONFIG
    if config != "":
        CONFIG['config'] = config
    if cdict==None:
        print( json.dumps(CONFIG, indent=1) )
    else:
        print( json.dumps(cdict, indent=1) )


def cfg_to_bak(filename="", config = ""):
    """used inside, rename config (before save)"""
    global CONFIG
    if config != "":
        CONFIG['config'] = config

    if filename=="":
        cfg = CONFIG['config']
    else:
        cfg = filename

    cfgbak = cfg + ".bak"
    if CFG_DEBUG:print("D... creating a backup config:", cfgbak )
    if os.path.isfile( os.path.expanduser(cfg)):
        #if CFG_DEBUG:print("D... config exists:",cfg, "... renaming to:", cfgbak)
        os.rename(os.path.expanduser(cfg),
                  os.path.expanduser(cfgbak))
        #if CFG_DEBUG:print("D... config is backedup:", cfgbak)
    else:
        if CFG_DEBUG:print("D... config did not exist:", cfg,"no bak file created")


def bak_to_cfg(filename="", config = ""):
    """used inside, rename back the bak version"""
    global CONFIG
    if config != "":
        CONFIG['config'] = config

    if filename=="":
        cfg = CONFIG['config']
    else:
        cfg = filename

    cfgbak = cfg + ".bak"
    if CFG_DEBUG:print("D... testing if backup config exists:", cfgbak)
    if os.path.isfile( os.path.expanduser(cfgbak)):
        if CFG_DEBUG:print("D... BACUP config exists:",cfgbak, "... renaming to:", cfg)
        os.rename(os.path.expanduser(cfgbak),
                  os.path.expanduser(cfg))
        #if CFG_DEBUG:print("D... config is recovered from:", cfgbak)
    else:
        if CFG_DEBUG:print("D... bak config did not exist:", cfgbak,"no bak file recovery")


def save_config(filename="", config = ""): # duplicit... filename overrides
    """FRONT function, save config to filename"""
    global CONFIG
    if config != "":
        CONFIG['config'] = config

    if filename=="":
        cfg = CONFIG['config']
    else:
        cfg = filename

    if CFG_DEBUG: print("DD... calling cfg_to_bak:", cfg)
    cfg_to_bak(cfg)
    if CFG_DEBUG:print("D... writing config:", cfg)
    with open(os.path.expanduser(cfg), "w+") as f:
        f.write(json.dumps(CONFIG, indent=1))
        #if CFG_DEBUG:print("D... config was written:", cfg)

    if verify_config(config):
        if CFG_DEBUG:print("D... verified by verify_config ... ok ... ending here")
        return
    #====ELSE RECOVER BAK
    return bak_to_cfg()



def load_config(config=""):
    """FRONT function, load config file"""
    global CONFIG
    if config != "":
        CONFIG['config'] = config
    cfg = CONFIG['config']
    cfg = cfg+".from_memory"
    if CFG_DEBUG: print("DD... calling save_config:")
    save_config( cfg )

    cfg = CONFIG['config']
    #if CFG_DEBUG:print("D... loading config from",cfg)

    if not verify_config(config):
        print("X... FAILED on verifications")
        print(" ... maybe there is a wrong comma in the json or something...")
        sys.exit(1)
        return False

    if CFG_DEBUG: print("D... passed verification of:",cfg)
    dicti = CONFIG

    if CFG_DEBUG: print("D... directly loading json:",cfg)
    if os.path.isfile( os.path.expanduser(cfg)):
        with open(os.path.expanduser(cfg), "r") as f:
            dicti = json.load(f)

    # rewriting in memory
    if sorted(dicti.keys()) == sorted(CONFIG.keys()):
        if CFG_DEBUG: print("D... memory and disk identical:")
    else:
        if CFG_DEBUG: print("X... memory and disk differ:")
        # show_config(CONFIG)
        # there may be more lines in the CODE after upgrade.
        for k in CONFIG.keys(): # search CODE version
            if not (k in dicti.keys()):
                print("D... key not on DISK:", k )
                dicti[k] = CONFIG[k]


    CONFIG = dicti
    if CFG_DEBUG: print("DD... final CONFIG:")
    show_config(CONFIG)
    if CFG_DEBUG: print("DD... end load")


def loadsave(config = ""):
    """FRONT function, if DISK is earlier version than CODE, this may update DISK"""
    if config != "":
        CONFIG['config'] = config

    load_config(config)
    save_config() #?


if __name__=="__main__":
    print("i... _________________ in ZCONFIG ______________________" )
    Fire()

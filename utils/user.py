import configparser
import os
import sys

from . import config
from . import logger

log = logger.get_logger(__name__)


############################################################
# USER SETTINGS
############################################################

def get_setting(user, type, name):
    try:
        config_path = os.path.join(config.USER_PATH.replace('$USER$', user), 'updater.ini')
        log.debug("Fetching %r setting %r from %r", type, name, config_path)

        cfg = configparser.ConfigParser()
        cfg.read(config_path)
        return cfg[type][name]

    except:
        log.exception("Exception retrieving %r setting %r for %r: ", type, name, user)
        sys.exit("Unexpected exception....")

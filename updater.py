#!/usr/bin/env python3.5
import argparse
import time

try:
    from shlex import quote as cmd_quote
except ImportError:
    from pipes import quote as cmd_quote

from utils import logger
from utils import process
from utils import user
from utils.plex import Plex

############################################################
# INIT
############################################################
# Logging
log = logger.get_root_logger()

############################################################
# ARG PARSE
############################################################

parser = argparse.ArgumentParser(description='The Source Docker Updater')
parser.add_argument('-t', '--type', metavar='type', type=str, help='Type of container to update (plex etc...)')
parser.add_argument('-u', '--user', metavar='user', type=str, help='User who owns the container')
parser.add_argument('-c', '--container', metavar='container', type=str, help='Name of the container')


############################################################
# UPDATERS
############################################################

def update_plex(username, container):
    # read required settings
    plex_url = user.get_setting(username, 'plex', 'url')
    plex_token = user.get_setting(username, 'plex', 'token')
    log.info("Loaded plex settings, url=%r token=%r", plex_url, plex_token)

    # validate server
    plex_server = Plex("%s server" % username, plex_url, plex_token)
    if not plex_server.validate():
        log.error("Unable to validate %s's server url/token...", username)
        exit(1)

    while True:
        # check active scanners
        log.info("Checking active scanners for %s's plex container", username)
        plex_scanners = process.find('Plex Media Scanner', username)
        if plex_scanners is None:
            log.error("There was an unexpected error while checking available scanners for %s's container", username)
        elif len(plex_scanners):
            log.info("Checking %s's scanners again in 1 minute because there were %d active scanners...",
                     username, len(plex_scanners))
            time.sleep(60)
            continue

        # check active streams
        log.info("Checking active streams for %s's plex container", username)
        plex_streams = plex_server.get_streams()
        if plex_streams is None:
            log.error("There was an unexpected error while checking available streams for %s's server", username)
            exit(1)
        elif len(plex_streams):
            log.info("Checking %s's scanners and server again in 1 minute because there were %d active streams...",
                     username,
                     len(plex_streams))
            time.sleep(60)
            continue

        log.info("Ready to update %s's container, there were no active streams or scanners!", username)
        break

    # restart users plex container
    #process.run_command("docker restart %s" % cmd_quote(container))
    # uncomment this line to do reboot instead
    process.run_command("sleep 5 && shutdown -r now &")

    log.info("Finished updating plex for %r!", username)
    exit(0)


############################################################
# MAIN
############################################################

if __name__ == "__main__":
    # parse arguments
    args = parser.parse_args()
    if not args.type or not args.user or not args.container:
        log.error("You must specify a type, user and container!")
        exit(1)

    # process arguments
    log.info("Updating %r container: %r for %r", args.type, args.container, args.user)
    if args.type == 'plex':
        update_plex(args.user, args.container)
